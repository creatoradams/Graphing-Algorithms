from pathlib import Path
import subprocess, sys, runpy, io, contextlib
""" Chapter 3 Programming Assignment """
class GraphExercises:
    # Simple recursive DFS used by components
    def dfs(self, graph, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        for key in graph[start] - visited:
            self.dfs(graph, key, visited)
        return visited

    """  #1) Connected components """
    def connected_components(self, graph):
        seen = set()
        comps = []
        for v in sorted(graph.keys()):
            if v not in seen:
                comp = self.dfs(graph, v, set())
                comps.append(comp)
                seen |= comp
        return comps

    """ #2) DFS path (backtracking) between two nodes on an undirected graph """
    def dfs_path(self, graph, start, goal):
        path = []
        visited = set()

        def backtrack(u):
            visited.add(u)
            path.append(u)
            if u == goal:
                return True
            for nxt in graph[u] - visited:
                if backtrack(nxt):
                    return True
            path.pop()
            return False

        if start not in graph or goal not in graph:
            return None
        return path if backtrack(start) else None

    """ #3) Topological order """
    #    Prints the countdown (n, node) lines and returns the order printed.
    def topo_from(self, digraph, seed):
        rec = []
        n = len(digraph)

        def dfs_tpl(u, path):
            nonlocal n
            path = path + [u]
            for v in digraph[u]:
                if v not in path:
                    path = dfs_tpl(v, path)
            print(n, u)
            rec.append(u)
            n -= 1
            return path

        dfs_tpl(seed, [])
        return rec

def main():
    gx = GraphExercises()

    # Undirected graph from s
    g = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}

    print('--- Connected Components (undirected) ---')
    for comp in gx.connected_components(g):
        print(comp)

    print('\\n--- DFS Paths (undirected) ---')
    for s, t in [('D','F'), ('A','E'), ('A','F')]:
        print(f'{s} -> {t}:', gx.dfs_path(g, s, t))

    # Directed graph from your topo script
    h = {'A': set(['C', 'D']),
         'B': set(['D', 'E']),
         'C': set(['D', 'F', 'H']),
         'D': set(['E']),
         'E': set(['G', 'I']),
         'F': set(['G']),
         'G': set(['I']),
         'H': set(['I']),
         'I': set()}

    print('\\n--- Topological order style (directed) ---')
    for seed in ['A', 'B', 'C']:
        print(f"Start at {seed!r}")
        order = gx.topo_from(h, seed)
        print('Order:', order)
        print()

if __name__ == '__main__':
    main()

# Run it to show outputs
print(subprocess.run([sys.executable, "/mnt/data/graph_exercises_class.py"], capture_output=True, text=True).stdout)
