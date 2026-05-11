"""
TP5 - Benchmark Comparatif NoSQL
Redis vs MongoDB vs Cassandra vs Neo4j
"""

import time
import statistics
import json
import threading
from typing import Callable

import redis
from pymongo import MongoClient
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, BatchType
from neo4j import GraphDatabase


# =========================================================
# 🔧 UTILITAIRE LATENCE
# =========================================================

def measure_latency(fn: Callable, iterations: int = 1000) -> dict:
    latencies = []

    for _ in range(iterations):
        start = time.perf_counter()
        fn()
        latencies.append((time.perf_counter() - start) * 1000)

    latencies.sort()

    return {
        "mean_ms": statistics.mean(latencies),
        "p50_ms": latencies[int(0.5 * len(latencies))],
        "p95_ms": latencies[int(0.95 * len(latencies))],
        "p99_ms": latencies[int(0.99 * len(latencies))],
        "max_ms": max(latencies),
        "throughput_rps": 1000 / statistics.mean(latencies)
    }


def print_results(name, res):
    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)
    for k, v in res.items():
        print(f"{k:20s}: {v:.2f}")


# =========================================================
# 🟥 REDIS BENCHMARK
# =========================================================

def benchmark_write_redis(n=10000):
    r = redis.Redis(host="localhost", port=6379)
    pipe = r.pipeline()

    start = time.time()

    for i in range(n):
        pipe.set(f"key:{i}", json.dumps({"id": i, "value": i}))

        if i % 1000 == 0:
            pipe.execute()

    pipe.execute()

    print(f"Redis WRITE: {n / (time.time() - start):.0f} ops/sec")


def benchmark_read_redis():
    r = redis.Redis(host="localhost", port=6379)

    def fn():
        r.get("key:500")

    print("Redis READ:", measure_latency(fn))


# =========================================================
# 🟩 MONGODB BENCHMARK
# =========================================================

def benchmark_write_mongodb(n=10000):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["benchmark"]
    col = db["data"]

    col.drop()

    batch = []
    start = time.time()

    for i in range(n):
        batch.append({"_id": i, "value": i})

        if len(batch) == 1000:
            col.insert_many(batch, ordered=False)
            batch = []

    if batch:
        col.insert_many(batch)

    print(f"MongoDB WRITE: {n / (time.time() - start):.0f} ops/sec")


def benchmark_read_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    col = client["benchmark"]["data"]

    def fn():
        col.find_one({"_id": 500})

    print("MongoDB READ:", measure_latency(fn))


# =========================================================
# 🟦 CASSANDRA BENCHMARK
# =========================================================

def benchmark_write_cassandra(n=10000):
    cluster = Cluster(["localhost"])
    session = cluster.connect("benchmark")

    query = session.prepare("""
        INSERT INTO data (id, value)
        VALUES (?, ?)
    """)

    start = time.time()

    batch = BatchStatement(batch_type=BatchType.UNLOGGED)
    count = 0

    for i in range(n):
        batch.add(query, (i, i))
        count += 1

        if count == 50:
            session.execute(batch)
            batch = BatchStatement(batch_type=BatchType.UNLOGGED)
            count = 0

    if count:
        session.execute(batch)

    print(f"Cassandra WRITE: {n / (time.time() - start):.0f} ops/sec")


# =========================================================
# ⚡ CONCURRENCY BENCHMARK
# =========================================================

def benchmark_concurrent(db_fn, n_clients=50, requests_per_client=200):
    latencies = []

    def worker():
        for _ in range(requests_per_client):
            start = time.perf_counter()
            db_fn()
            latencies.append(time.perf_counter() - start)

    threads = []
    start = time.time()

    for _ in range(n_clients):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start

    print("\n⚡ CONCURRENCY TEST")
    print(f"Total requests: {n_clients * requests_per_client}")
    print(f"Time: {elapsed:.2f}s")
    print(f"Throughput: {(n_clients * requests_per_client)/elapsed:.0f} req/sec")
    print(f"Avg latency: {statistics.mean(latencies)*1000:.2f} ms")


# =========================================================
# 🚀 MAIN
# =========================================================

if __name__ == "__main__":
    print("🚀 TP5 - NoSQL Benchmark")

    N = 10000

    print("\n🟥 REDIS")
    benchmark_write_redis(N)
    benchmark_read_redis()

    print("\n🟩 MONGODB")
    benchmark_write_mongodb(N)
    benchmark_read_mongodb()

    print("\n🟦 CASSANDRA")
    benchmark_write_cassandra(N)

    print("\n⚡ CONCURRENCY (Redis example)")
    benchmark_concurrent(lambda: redis.Redis().get("key:500"))
