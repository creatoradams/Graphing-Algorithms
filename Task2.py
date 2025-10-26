from graphingAlgo import GraphExercises


class Task2:
    def __init__(self, edges=None, graph=None):
        if graph is not None:
            self.g = graph
        else:
            self.g = {}
            for u, v in (edges or []):
                self.g.setdefault(u, set()).add(v)
                self.g.setdefault(v, set())  # ensure node exists

#--- Kosaraju helpers ---
    def _rev(self, g):
        r = {u: set() for u in g}
        for u in g:
            for v in g[u]:
                r.setdefault(v, set()).add(u)
        return r

    def _finish_order(self, g):
        vis, order = set(), []

        def go(u):
            vis.add(u)
            for v in g[u]:
                if v not in vis:
                    go(v)
            order.append(u)           # push after exploring

        for u in g:
            if u not in vis:
                go(u)
        return order

# --- strongly connected components (a) ---
    def scc(self):
        g = self.g
        order = self._finish_order(g)  # fix name
        rg = self._rev(g)
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

# --- meta-graph over scc ids (b) ---
    def meta_graph(self, comp_id, k):
        m = {i: set() for i in range(k)}
        for u in self.g:
            cu = comp_id[u]
            for v in self.g[u]:
                cv = comp_id[v]
                if cu != cv:
                    m[cu].add(cv)
        return m

# --- topological order of the metta-graph (c) ---
    def topo(self, dag):
        indeg = {u: 0 for u in dag}  # Kahn's Algorithm
        for u in dag:
            for v in dag[u]:
                indeg[v] += 1
        q = [u for u in dag if indeg[u] == 0]
        out = []
        while q:
            u = q.pop(0)
            out.append(u)
            for v in list(dag[u]):
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return out

# ---
if __name__ == "__main__":
    edges = [
        ('1','2'), ('2','3'), ('3','1'),        # SCC (1,2,3)
        ('3','4'),                              # 3→4 bridge
        ('4','5'), ('5','4'),                   # SCC (4,5)
        ('5','6'),                              # bridge
        ('6','7'), ('7','8'), ('8','9'),
        ('9','6'),                              # SCC (6,7,8,9)
        ('9','10'), ('10','11'), ('11','12'),
        ('12','10')                             # SCC (10,11,12)
    ]

    t2 = Task2(edges=edges)

    print("Strongly Connected Components:")
    comps, cid = t2.scc()
    for i, S in enumerate(comps):
        print(f"SCC {i} ->", sorted(S))

    print("\nMeta Graph (SCC connections):")
    M = t2.meta_graph(cid, len(comps))
    for i in sorted(M):
        for j in sorted(M[i]):
            print(f"{i} -> {j}")

    print("\nTopological Order:")
    print(t2.topo(M))

