from graphingAlgo import GraphExercises

class Task3:
    # make weighted graph
    def __init__(self, w_edges=None, graph=None):
        if graph is not None:
            self.w = graph
        else:
            self.w = {}
            # add both directions since it's undirected
            for u, v, w in (w_edges or []):
                self.w.setdefault(u, {})[v] = w
                self.w.setdefault(v, {})[u] = w

    # --- dijkstra shortest path ---
    def dijkstra(self, s):
        W = self.w
        dist = {u: float('inf') for u in W}  # store best known distances
        par = {u: None for u in W}  # track parents
        vis = set()

        if s not in W:
            return dist, par
        dist[s] = 0

        # loop until all nodes are visited
        while len(vis) < len(W):
            u = None
            best = float('inf')
            for x in W:
                if x not in vis and dist[x] < best:
                    best = dist[x]
                    u = x
            if u is None:
                break
            vis.add(u)

            # update distances to neighbors
            for v, w in W[u].items():
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    par[v] = u
        return dist, par

    # get list of edges from the shortest path tree
    def spt_edges(self, par):
        e = set()
        for v, p in par.items():
            if p is not None:
                a, b = (p, v) if p < v else (v, p)
                e.add((a, b))
        return sorted(e)

    # --- kruskal mst ---
    class DSU:
        def __init__(self, xs):
            self.p = {x: x for x in xs}
            self.r = {x: 0 for x in xs}
        def find(self, x):
            while self.p[x] != x: # follow parents until root
                self.p[x] = self.p[self.p[x]]  # path compression
                x = self.p[x]
            return x
        def union(self, a, b):
            ra, rb = self.find(a), self.find(b)
            if ra == rb:
                return False
            # union by rank
            if self.r[ra] < self.r[rb]:
                self.p[ra] = rb
            elif self.r[ra] > self.r[rb]:
                self.p[rb] = ra
            else:
                self.p[rb] = ra
                self.r[ra] += 1
            return True

    def mst_kruskal(self):
        W = self.w
        E, seen = [], set()

        # collect all unique edges
        for u in W:
            for v, w in W[u].items():
                a, b = (u, v) if u < v else (v, u)
                if (a, b) not in seen:
                    seen.add((a, b))
                    E.append((w, a, b))

        E.sort()  # sort by weight
        dsu = self.DSU(W.keys())
        T, total = [], 0

        # build MST
        for w, a, b in E:
            if dsu.union(a, b):
                T.append((a, b))
                total += w
        return sorted(T), total


# --- main ---
if __name__ == "__main__":
    # weighted edges (A–G)
    w_edges = [
        ('A', 'B', 22), ('A', 'E', 12), ('A', 'F', 36),
        ('B', 'C', 35), ('B', 'F', 34), ('B', 'E', 26),
        ('C', 'D', 42), ('C', 'G', 12),
        ('D', 'G', 21), ('E', 'F', 12), ('F', 'G', 18)
    ]

    t3 = Task3(w_edges=w_edges)

    # shortest paths
    print("Dijkstra start A:")
    dist, par = t3.dijkstra('A')
    for k in sorted(dist):
        d = dist[k]
        print(f"A -> {k} =", "∞" if d == float('inf') else d)
    print("SPT edges:", t3.spt_edges(par))

    # minimum spanning tree
    print("\nMST:")
    mst_edges, total = t3.mst_kruskal()
    print("Edges:", mst_edges)
    print("Total weight:", total)

    # compare SPT and MST
    print("\nSPT same as MST?")
    same = set(t3.spt_edges(par)) == set(mst_edges)
    print("Same?", same)
    print("Note: SPT = shortest paths from one node, MST = smallest total weight.")

    # explain about negatives
    print("\nNegative weights?")
    print("No. Dijkstra can’t handle negatives — use Bellman-Ford for that.")
