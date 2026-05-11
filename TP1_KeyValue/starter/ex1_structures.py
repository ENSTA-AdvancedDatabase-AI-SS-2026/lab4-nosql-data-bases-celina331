
Ex1 — Structures de données Redis (4 pts)
ShopFast : Modélisation des entités e-commerce

Structures utilisées :
  - Hash        → produit        (product:{id})
  - Hash        → panier         (cart:{user_id})
  - List        → historique nav (history:{user_id})
  - Set         → produits/cat   (category:{category})


import redis


# ──────────────────────────────────────────────────────────────────────────────
# Connexion
# ──────────────────────────────────────────────────────────────────────────────

def get_redis_client() -> redis.Redis:
    """Retourne une connexion Redis locale (db=0)."""
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


# ══════════════════════════════════════════════════════════════════════════════
# 1.1 — PRODUIT  (Hash)
# ══════════════════════════════════════════════════════════════════════════════
# Clé : "product:{product_id}"
# Pourquoi Hash ?  Un produit est un objet structuré avec plusieurs champs.
# HSET permet de stocker/modifier un champ sans réécrire tout l'objet,
# et HGET permet de récupérer un seul champ sans tout charger.

def store_product(r: redis.Redis, product: dict) -> None:
    """
    Stocke un produit dans un Hash Redis.

    Clé    : product:{id}
    Champs : id, name, price, stock, category, description

    On utilise HSET avec **mapping pour envoyer tous les champs
    en une seule commande réseau (O(N) champs).
    """
    key = f"product:{product['id']}"
    r.hset(key, mapping=product)


def get_product(r: redis.Redis, product_id: str) -> dict | None:
    """
    Récupère tous les champs d'un produit (HGETALL).

    Retourne None si la clé n'existe pas (dict vide = produit absent).
    """
    key = f"product:{product_id}"
    data = r.hgetall(key)
    return data if data else None


def update_product_stock(r: redis.Redis, product_id: str, quantity_sold: int) -> int:
    """
    Décrémente atomiquement le stock via HINCRBY.

    HINCRBY est atomique côté Redis : pas de race condition entre
    un HGET + HSET séparés.

    Lève ValueError si le produit n'existe pas ou si le stock
    deviendrait négatif (rollback avec un second HINCRBY).
    """
    key = f"product:{product_id}"

    if not r.exists(key):
        raise ValueError(f"Produit '{product_id}' introuvable dans Redis.")

    new_stock = r.hincrby(key, "stock", -quantity_sold)

    if new_stock < 0:
        r.hincrby(key, "stock", quantity_sold)   # rollback
        raise ValueError(
            f"Stock insuffisant pour '{product_id}'. "
            f"Demandé : {quantity_sold}, disponible : {new_stock + quantity_sold}."
        )

    return new_stock


def get_product_field(r: redis.Redis, product_id: str, field: str) -> str | None:
    """
    Récupère un seul champ d'un produit (HGET).

    Utile quand on n'a besoin que du prix ou du stock — évite de
    transférer tous les champs inutilement.
    """
    return r.hget(f"product:{product_id}", field)


# ══════════════════════════════════════════════════════════════════════════════
# 1.2 — PANIER  (Hash)
# ══════════════════════════════════════════════════════════════════════════════
# Clé : "cart:{user_id}"
# Pourquoi Hash ?  product_id → quantité est exactement un mapping clé/valeur.
# HINCRBY gère l'ajout/retrait de quantité de façon atomique.

def add_to_cart(r: redis.Redis, user_id: str, product_id: str, quantity: int) -> None:
    """
    Ajoute `quantity` unités de `product_id` au panier.

    HINCRBY cumule la quantité si le produit est déjà dans le panier.
    Si la quantité résultante <= 0, on supprime le champ (retrait complet).
    """
    key = f"cart:{user_id}"
    new_qty = r.hincrby(key, product_id, quantity)
    if new_qty <= 0:
        r.hdel(key, product_id)


def get_cart(r: redis.Redis, user_id: str) -> dict:
    """
    Retourne le panier complet : {product_id: quantité (int)}.

    Redis stockant tout en string, on convertit en int.
    Retourne un dict vide si le panier n'existe pas.
    """
    raw = r.hgetall(f"cart:{user_id}")
    return {pid: int(qty) for pid, qty in raw.items()}


def remove_from_cart(r: redis.Redis, user_id: str, product_id: str) -> bool:
    """
    Supprime un produit du panier (HDEL).
    Retourne True si le produit existait, False sinon.
    """
    return bool(r.hdel(f"cart:{user_id}", product_id))


def clear_cart(r: redis.Redis, user_id: str) -> None:
    """
    Vide entièrement le panier (DEL sur la clé du Hash).
    Appelé après validation d'une commande.
    """
    r.delete(f"cart:{user_id}")


def get_cart_total(r: redis.Redis, user_id: str) -> float:
    """
    Calcule le montant total du panier en DZD.

    Utilise un pipeline pour récupérer tous les prix en un seul
    aller-retour réseau plutôt qu'un HGET par produit.
    """
    cart = get_cart(r, user_id)
    if not cart:
        return 0.0

    product_ids = list(cart.keys())
    pipe = r.pipeline()
    for pid in product_ids:
        pipe.hget(f"product:{pid}", "price")
    prices = pipe.execute()

    total = 0.0
    for pid, price_str in zip(product_ids, prices):
        if price_str is not None:
            total += float(price_str) * cart[pid]
    return total


# ══════════════════════════════════════════════════════════════════════════════
# 1.3 — HISTORIQUE DE NAVIGATION  (List)
# ══════════════════════════════════════════════════════════════════════════════
# Clé : "history:{user_id}"
# Pourquoi List ?  Maintient l'ordre d'insertion.
# LPUSH insère en tête → le plus récent est toujours à l'index 0.
# LTRIM borne la taille pour éviter une consommation mémoire infinie.

HISTORY_MAX_SIZE = 10


def add_to_history(r: redis.Redis, user_id: str, product_id: str) -> None:
    """
    Enregistre la consultation d'un produit en tête de l'historique.

    Stratégie LPUSH + LTRIM dans un pipeline :
      1. LPUSH  → insère en position 0 (le plus récent).
      2. LTRIM  → conserve seulement les HISTORY_MAX_SIZE premiers éléments.
    Les deux commandes sont envoyées en un seul round-trip réseau.
    """
    key = f"history:{user_id}"
    pipe = r.pipeline()
    pipe.lpush(key, product_id)
    pipe.ltrim(key, 0, HISTORY_MAX_SIZE - 1)
    pipe.execute()


def get_history(r: redis.Redis, user_id: str, limit: int = HISTORY_MAX_SIZE) -> list[str]:
    """
    Retourne les `limit` derniers produits consultés (du plus récent au plus ancien).
    """
    return r.lrange(f"history:{user_id}", 0, limit - 1)


def clear_history(r: redis.Redis, user_id: str) -> None:
    """Supprime l'historique complet d'un utilisateur."""
    r.delete(f"history:{user_id}")


# ══════════════════════════════════════════════════════════════════════════════
# 1.4 — PRODUITS PAR CATÉGORIE  (Set)
# ══════════════════════════════════════════════════════════════════════════════
# Clé : "category:{category_name}"
# Pourquoi Set ?  Pas de doublons, appartenance en O(1) avec SISMEMBER,
# et SINTER permet des filtres multi-catégories très efficacement.

def add_product_to_category(r: redis.Redis, product_id: str, category: str) -> None:
    """
    Ajoute product_id dans le Set de la catégorie.
    SADD ignore les doublons → opération idempotente.
    """
    r.sadd(f"category:{category}", product_id)


def get_products_by_category(r: redis.Redis, category: str) -> set[str]:
    """
    Retourne tous les product_id d'une catégorie (SMEMBERS).
    O(N) où N = taille du Set.
    """
    return r.smembers(f"category:{category}")


def get_products_in_categories(r: redis.Redis, *categories: str) -> set[str]:
    """
    Retourne les produits présents dans TOUTES les catégories (SINTER).

    Exemple : get_products_in_categories(r, "smartphones", "en_promo")
    → produits qui sont à la fois smartphones ET en promotion.
    """
    if not categories:
        return set()
    keys = [f"category:{cat}" for cat in categories]
    return r.sinter(keys)


def is_product_in_category(r: redis.Redis, product_id: str, category: str) -> bool:
    """
    Vérifie l'appartenance d'un produit à une catégorie (SISMEMBER, O(1)).
    """
    return r.sismember(f"category:{category}", product_id)


def remove_product_from_category(r: redis.Redis, product_id: str, category: str) -> bool:
    """Retire un produit d'une catégorie (SREM). Retourne True s'il y était."""
    return bool(r.srem(f"category:{category}", product_id))


# ══════════════════════════════════════════════════════════════════════════════
# Démonstration  (python ex1_structures.py)
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    r = get_redis_client()

    print("=" * 60)
    print("ShopFast — Ex1 : Structures de données Redis")
    print("=" * 60)

    # — Produits ---------------------------------------------------------------
    products = [
        {"id": "P001", "name": "iPhone 15 Pro",     "price": "189000",
         "stock": "30",  "category": "smartphones",  "description": "Apple iPhone 15 Pro 256 Go"},
        {"id": "P002", "name": "Samsung Galaxy S24", "price": "149000",
         "stock": "45",  "category": "smartphones",  "description": "Samsung Galaxy S24 128 Go"},
        {"id": "P003", "name": "MacBook Air M3",     "price": "289000",
         "stock": "15",  "category": "laptops",      "description": "Apple MacBook Air M3 8 Go"},
        {"id": "P004", "name": "AirPods Pro 2",      "price": "39000",
         "stock": "100", "category": "accessories",  "description": "Apple AirPods Pro 2ème gen"},
    ]

    print("\n📦 Stockage des produits (HSET)...")
    for p in products:
        store_product(r, p)
        add_product_to_category(r, p["id"], p["category"])
    print("  ✓ 4 produits stockés")

    print("\n🔍 Lecture d'un produit (HGETALL)...")
    p = get_product(r, "P001")
    print(f"  → {p['name']} | Prix : {p['price']} DZD | Stock : {p['stock']}")

    print("\n  Lecture d'un seul champ (HGET)...")
    price = get_product_field(r, "P001", "price")
    print(f"  → Prix P001 : {price} DZD")

    print("\n📉 Mise à jour du stock (HINCRBY)...")
    new_stock = update_product_stock(r, "P001", 5)
    print(f"  → Stock P001 après vente de 5 unités : {new_stock}")

    try:
        update_product_stock(r, "P001", 9999)
    except ValueError as e:
        print(f"  ✓ ValueError attendue : {e}")

    print("\n🛒 Gestion du panier (Hash)...")
    add_to_cart(r, "U001", "P001", 2)
    add_to_cart(r, "U001", "P004", 1)
    add_to_cart(r, "U001", "P001", 1)   # cumul → P001 : 3
    cart  = get_cart(r, "U001")
    total = get_cart_total(r, "U001")
    print(f"  → Panier U001 : {cart}")
    print(f"  → Total       : {total:,.0f} DZD")

    remove_from_cart(r, "U001", "P004")
    print(f"  → Après retrait P004 : {get_cart(r, 'U001')}")

    print("\n📜 Historique de navigation (List)...")
    for pid in ["P002", "P001", "P003", "P001", "P004"]:
        add_to_history(r, "U001", pid)
    history = get_history(r, "U001")
    print(f"  → Dernières pages vues (récent → ancien) : {history}")

    print("\n🏷️  Produits par catégorie (Set)...")
    smartphones = get_products_by_category(r, "smartphones")
    print(f"  → Smartphones : {smartphones}")
    print(f"  → P001 est un smartphone : {is_product_in_category(r, 'P001', 'smartphones')}")

    # Tags promo
    add_product_to_category(r, "P001", "en_promo")
    add_product_to_category(r, "P002", "en_promo")
    promos_smartphones = get_products_in_categories(r, "smartphones", "en_promo")
    print(f"  → Smartphones EN PROMO (SINTER) : {promos_smartphones}")

    print("\n✅ Ex1 terminé avec succès !")
