

class Task2:
    # build a directed graph by passing either graph as a ready made dict
    # or edges which is a list of directed edges
    def __init__(self, edges=None, graph=None):
        if graph is not None:
            self.g = graph
        else:
            self.g = {}
            for u, v in (edges or []):
                self.g.setdefault(u, set()).add(v)
                self.g.setdefault(v, set())  # ensure node exists

    # returns the reversed graph, for every u -> v, create v -> u
    def _rev(self, g):
        r = {u: set() for u in g}
        for u in g:
            for v in g[u]:
                r.setdefault(v, set()).add(u)
        return r

    # implement Kosaraju, do DFS and push each node onto order after exploring its neighbors
    def _finish_order(self, g):
        vis, order = set(), []

        def go(u):
            vis.add(u)
            for v in g[u]:
                if v not in vis:
                    go(v)
            order.append(u) # push after exploring

        for u in g:
            if u not in vis:
                go(u)
        return order

    """ A) strongly connected components """
    def scc(self):
        # use Kosaraju, get nodes in decreasing finish time from graph
        # DFS on the reversed graph in that order to collect SCC's
        # returns comps - list[set] of SCC's and comp_id - dict node -> SCC indexx
        g = self.g
        order = self._finish_order(g)  # finish order on graph
        rg = self._rev(g) # reversed graph
        vis = set()
        comp_id = {}
        comps = []
        cur = -1

        # processes nodes in reverse finished order
        for u in reversed(order):
            if u in vis:
                continue
            cur += 1
            comps.append(set())
            st = [u]
            vis.add(u)
            comp_id[u] = cur
            while st:
                x = st.pop()
                comps[cur].add(x)
                for y in rg[x]:
                    if y not in vis:
                        vis.add(y)
                        comp_id[y] = cur
                        st.append(y)
        return comps, comp_id

    """ B) meta-graph over strongly connected components """
    def meta_graph(self, comp_id, k):
        m = {i: set() for i in range(k)}
        for u in self.g:
            cu = comp_id[u]
            for v in self.g[u]:
                cv = comp_id[v]
                if cu != cv:
                    m[cu].add(cv)
        return m

        """ c) topological order via DFS """
    def topo(self, dag):

        vis = set()
        out = []

        def go(u):
            vis.add(u)
            # Optional: use sorted(dag[u]) for deterministic output
            for v in dag[u]:
                if v not in vis:
                    go(v)
            out.append(u)  # post-order push

        # Optional: iterate in sorted(dag) for deterministic order
        for u in dag:
            if u not in vis:
                go(u)

        out.reverse()
        return out

def run():
    edges = [
        # Left cluster
        (4, 1), (4, 12), (4, 2), (1, 3), (2, 1), (3, 2),
        # Middle & top connections
        (3, 5),
        # Middle-right cluster
        (9, 5), (5, 8), (5, 6), (6, 8), (8, 9), (8, 10), (6, 7),
        (10, 9), (10, 11),
        # Lower-left to middle
        (9, 11), (11, 12),
    ]
    t2 = Task2(edges=edges)
    """ A) SCC's """
    print("Strongly Connected Components:")
    comps, cid = t2.scc()
    for i, S in enumerate(comps):
        print(f"SCC {i} ->", sorted(S))

    """ B) show Meta Graph """
    print("\nMeta Graph:")
    M = t2.meta_graph(cid, len(comps))
    for i in sorted(M):
        for j in sorted(M[i]):
            print(f"{i} -> {j}")

    """ C) Topological Order """
    print("\nTopological Order:")
    print(t2.topo(M))

    if __name__ == "__main__":
        run()


