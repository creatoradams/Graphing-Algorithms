
"""
Task 3: applying Dijkstras algorithm to find the SPT and Kruskal to find the MST
This class builds the weighted graph and then runs Dijkstras algo starting at A to get the SPT,
then runs Kruskals algo to get a MST and compares the edge of SPT and MST.
Adds the weight of the total edges to get the weight of the graph
"""

class Task3:
    # make weighted graph (undirected)
    def __init__(self, w_edges=None, graph=None):
        if graph is not None:
            self.w = graph
        else:
            self.w = {}
            for u, v, w in (w_edges or []):
                self.w.setdefault(u, {})[v] = w
                self.w.setdefault(v, {})[u] = w

    """ dijkstra shortest path """
    def dijkstra(self, s):
        W = self.w
        dist = {u: float('inf') for u in W}
        par  = {u: None for u in W} # parent pointers for SPT
        vis = set() # visited vertices

        # if source is not in graph return
        if s not in W:
            return dist, par
        dist[s] = 0

        # repeat until every reachable vertex is finalized
        while len(vis) < len(W):
            u, best = None, float('inf')
            for x in W:
                if x not in vis and dist[x] < best:
                    best = dist[x]; u = x
            if u is None:
                break
            vis.add(u)


            for v, w in W[u].items():
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    par[v]  = u
        return dist, par

    # get list of edges from the shortest path tree
    def spt_edges(self, par):
        """
        Convert parent pointers into an undirected set of edges.
        Returns a sorted list of tuples
        """
        e = set()
        for v, p in par.items():
            if p is not None:
                # avoid dupes
                a, b = (p, v) if p < v else (v, p)
                e.add((a, b))
        return sorted(e)

    """ 
    kruskal minimum spanning tree
    Gather all unique edges, sort by weight ascending
    returns edges and total weight
    """
    def kruskalMst(self):
        W = self.w
        E, seen = [], set()

        # collect unique undirected edges as (w,a,b)
        for u in W:
            for v, w in W[u].items():
                a, b = (u, v) if u < v else (v, u)
                if (a, b) not in seen:
                    seen.add((a, b))
                    E.append((w, a, b))

        E.sort()  # by weight

        # ---- Inline DSU (parent/rank + find/union) ----
        parent = {x: x for x in W}
        rank   = {x: 0 for x in W}

        def find(x):
            # path compression
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        # union by rank, return true if merged false if already the same set
        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            # union by rank
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            elif rank[ra] > rank[rb]:
                parent[rb] = ra
            else:
                parent[rb] = ra
                rank[ra] += 1
            return True

        T, total = [], 0
        for w, a, b in E:
            if union(a, b): # only add if it connects 2 components
                T.append((a, b)) # store as undirected pair
                total += w
        return sorted(T), total


def run():
    edges = [
        # Left side
        ('A', 'B', 22), ('A', 'C', 9), ('A', 'D', 12),
        ('B', 'C', 35),

        # Center / cross edges
        ('C', 'D', 4), ('C', 'F', 42), ('C', 'E', 65),
        ('D', 'E', 33), ('D', 'I', 30),

        ('E', 'F', 18), ('E', 'G', 23),
        ('F', 'G', 39),

        # Right side
        ('B', 'H', 34), ('F', 'H', 24),
        ('G', 'H', 25), ('G', 'I', 21),
        ('H', 'I', 19),
    ]

    t3 = Task3(edges) # build graph from edge list

    print("Dijkstra start A:")
    dist, par = t3.dijkstra('A')
    for k in sorted(dist):
        d = dist[k]
        print(f"A -> {k} =", "∞" if d == float('inf') else d)
    print("SPT edges:", t3.spt_edges(par))

    print("\nMST:")
    mst_edges, total = t3.kruskalMst()
    print("Edges:", mst_edges)
    print("Total weight:", total)

    print("\nSPT same as MST?")
    print("Same?", set(t3.spt_edges(par)) == set(mst_edges))


if __name__ == "__main__":
    run()
