import heapq
import math
import os
import sys

from flask import Flask, jsonify, request, send_from_directory

# ------------------------------------------------------------------
# Find the folder that contains graph_city.py (works in Pydroid too)
# ------------------------------------------------------------------
CANDIDATES = [
    os.getcwd(),
    "/storage/emulated/0/Download",
    "/storage/emulated/0/Downloads",
    "/storage/emulated/0",
]
BASE = next((f for f in CANDIDATES
             if os.path.exists(os.path.join(f, "graph_city.py"))), None)
if BASE is None:
    raise SystemExit("graph_city.py not found in Download folder")

sys.path.insert(0, BASE)

from graph_city import build_city_graph, find_image

app = Flask(__name__)
graph = build_city_graph()


# ------------------------------------------------------------------
# STEP 1: distance  ->  used for BOTH edge cost g and heuristic h
#   d(a, b) = sqrt((xa - xb)^2 + (ya - yb)^2)
# ------------------------------------------------------------------
def dist(a, b):
    return math.hypot(a.X - b.X, a.Y - b.Y)


# ------------------------------------------------------------------
# STEP 2: one search function, 3 algorithms.
# Only the PRIORITY changes:
#   UCS    -> f(n) = g(n)
#   Greedy -> f(n) = h(n)
#   A*     -> f(n) = g(n) + h(n)
# ------------------------------------------------------------------
def search(start, goal, algo):
    s, t = graph.vertices[start], graph.vertices[goal]

    def priority(g, v):
        h = dist(v, t)
        if algo == "ucs":
            return g
        if algo == "greedy":
            return h
        return g + h  # astar

    counter = 0                              # tie-breaker for the heap
    frontier = [(priority(0, s), counter, 0, start)]
    best_g = {start: 0}                      # cheapest known cost to each node
    parent = {start: None}                   # to rebuild the path
    closed = set()
    explored = []                            # order of expansion (for animation)

    while frontier:
        _, _, g, name = heapq.heappop(frontier)
        if name in closed:
            continue
        closed.add(name)
        explored.append(name)
        if name == goal:
            break

        for nb in graph.vertices[name].neighbors:
            if nb.value in closed:
                continue
            new_g = g + dist(graph.vertices[name], nb)

            if algo == "greedy":
                if nb.value in parent:       # greedy never revisits/improves
                    continue
            elif new_g >= best_g.get(nb.value, math.inf):
                continue                     # not a cheaper route, skip

            best_g[nb.value] = new_g
            parent[nb.value] = name
            counter += 1
            heapq.heappush(frontier, (priority(new_g, nb), counter, new_g, nb.value))

    if goal not in closed:
        return {"found": False, "explored": explored}

    # STEP 3: walk backwards goal -> start using parent
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    return {
        "found": True,
        "path": path,
        "explored": explored,
        "cost": round(best_g[goal], 1),
        "expanded": len(explored),
    }


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(BASE, "index.html")


# ---- PWA files (service worker must be served from "/" to control the whole app) ----
PWA_FILES = {
    "manifest.webmanifest": "application/manifest+json",
    "sw.js": "application/javascript",
    "icon-192.png": "image/png",
    "icon-512.png": "image/png",
    "icon-maskable-512.png": "image/png",
    "apple-touch-icon.png": "image/png",
}


@app.route("/<name>")
def pwa_file(name):
    if name not in PWA_FILES:
        return ("Not found", 404)
    resp = send_from_directory(BASE, name, mimetype=PWA_FILES[name])
    if name == "sw.js":
        resp.headers["Service-Worker-Allowed"] = "/"
        resp.headers["Cache-Control"] = "no-cache"
    return resp


@app.route("/map")
def city_map():
    path, folder = find_image()
    return send_from_directory(folder, "city_map.jpg")


@app.route("/api/graph")
def api_graph():
    return jsonify({
        "vertices": [{"id": v.value, "x": v.X, "y": v.Y} for v in graph.vertices.values()],
        "edges": [[a.value, b.value] for a, b in graph.edges],
    })


@app.route("/api/route")
def api_route():
    start = request.args.get("start")
    goal = request.args.get("goal")
    algo = request.args.get("algo", "astar")
    if start not in graph.vertices or goal not in graph.vertices:
        return jsonify({"error": "Unknown start or goal"}), 400
    if algo not in ("ucs", "greedy", "astar"):
        return jsonify({"error": "Unknown algorithm"}), 400
    return jsonify(search(start, goal, algo))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)