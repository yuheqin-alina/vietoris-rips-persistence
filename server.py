#!/usr/bin/env python3
"""Vietoris–Rips persistence via GUDHI; serves the web UI and /api/persistence."""

from __future__ import annotations

import math
from pathlib import Path

import gudhi
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

ROOT = Path(__file__).resolve().parent
EPS = 1e-9

app = Flask(__name__, static_folder=str(ROOT), static_url_path="")
CORS(app)


def max_pairwise_distance(points: list[list[float]]) -> float:
    n = len(points)
    best = 0.0
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            best = max(best, math.hypot(xi - xj, yi - yj))
    return best


def distance_to_radius(value: float) -> float:
    """GUDHI Rips filtrations use edge length; the UI uses disk radius ε = dist / 2."""
    return value / 2.0


def compute_persistence(points: list[list[float]]) -> dict:
    n = len(points)
    if n == 0:
        return {"intervals": [], "maxFilt": 0.0, "source": "gudhi"}

    max_edge = max_pairwise_distance(points)
    max_filt = distance_to_radius(max_edge)

    if n == 1:
        return {
            "intervals": [
                {
                    "dim": 0,
                    "birth": 0.0,
                    "death": None,
                    "persistence": None,
                }
            ],
            "maxFilt": max_filt,
            "source": "gudhi",
        }

    rips = gudhi.RipsComplex(points=points, max_edge_length=max_edge)
    simplex_tree = rips.create_simplex_tree(max_dimension=3)
    simplex_tree.compute_persistence(homology_coeff_field=2)

    intervals: list[dict] = []
    for birth_sk, death_sk in simplex_tree.persistence_pairs():
        dim = len(birth_sk) - 1
        birth_eps = distance_to_radius(simplex_tree.filtration(birth_sk))

        if not death_sk:
            death_eps = None
            persistence = None
        else:
            death_eps = distance_to_radius(simplex_tree.filtration(death_sk))
            persistence = death_eps - birth_eps
            if persistence <= EPS:
                continue

        intervals.append(
            {
                "dim": int(dim),
                "birth": birth_eps,
                "death": death_eps,
                "persistence": persistence,
                "birthVerts": list(birth_sk),
                "deathVerts": list(death_sk) if death_sk else None,
            }
        )

    return {"intervals": intervals, "maxFilt": max_filt, "source": "gudhi"}


@app.get("/")
def index() -> object:
    return send_from_directory(ROOT, "index.html")


@app.post("/api/persistence")
def persistence_api() -> object:
    payload = request.get_json(silent=True) or {}
    raw_points = payload.get("points", [])
    points = [[float(p["x"]), float(p["y"])] for p in raw_points]
    return jsonify(compute_persistence(points))


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
