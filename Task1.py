
""" Completes task 1 of Project 3 """
class Task1:
    """ class that can build an undirected graph from an edge list """
    def __init__(self, edges=None, graph=None):
        # Build dict-of-sets undirected graph
        if graph is not None:
            self.g = graph
        else:
            self.g = {}
            for u, v in (edges or []):
                self.g.setdefault(u, set()).add(v)
                self.g.setdefault(v, set()).add(u)

""" Core DFS & BFS utilities """
def dfs(graph, start, visited=None):
    # recursive DFS, returns the set of vertices from start
    if visited is None:
        visited = set()
    visited.add(start)
    # iterate over the parts that havent been to yet
    for i in graph[start] - visited:
        dfs(graph, i, visited)
    return visited

""" Enumerate ALL connected components using DFS
    Run DFS from every vertex that hasnt been seen yet
    and collect each set as one component
"""
def components_dfs(graph):
    seen, comps = set(), []
    for v in graph:
        if v not in seen:
            comp = dfs(graph, v, set())
            comps.append(comp)
            seen |= comp # merge the discovered component into the global "seen"
    return comps

""" BFS - returns the set of vertices in the connected components 
    that contains 'start'.
"""
def bfs_component(graph, start):
    visited, queue = set(), [start]
    while queue:
        i = queue.pop(0) # pop from the front
        if i not in visited:
            visited.add(i)
            queue.extend(graph[i] - visited)
    return visited

""" Enumerate all connected components using BFS
    Mirrors components_dfs but uses the BFS traversal
"""
def components_bfs(graph):
    seen, comps = set(), []
    for v in graph:
        if v not in seen:
            comp = bfs_component(graph, v)
            comps.append(comp)
            seen |= comp
    return comps

"""
Find a path from start to the goal using DFS backtracking
Returns a list of vertices if a path is found or none if not.
"""
def dfs_path(graph, start, goal):
    path, visited = [], set()
    def backtrack(u):
        visited.add(u)
        path.append(u)

        # found target
        if u == goal:
            return True

        # try each of the unvisited, if any recursive call reaches the goal,
        # return true or backtrack by pop()
        for nxt in graph[u] - visited:
            if backtrack(nxt):
                return True

        # dead end: remove u and return failure
        path.pop()
        return False

    if start not in graph or goal not in graph:
        return None
    return path if backtrack(start) else None

"""
Find the shortest path from start to goal using BFS.
Returns the path as a list of vertices or none if unreachable.
"""
def bfs_path(graph, start, goal):
    if start == goal:
        return [start]
    visited = {start}
    queue = [(start, [])] # each entry: (current vertex, path to current)

    while queue:
        current, path = queue.pop(0)
        visited.add(current) # mark visited
        for n in graph[current]:
            if n == goal:
                return path + [current, n]
            if n in visited:
                continue
            queue.append((n, path + [current])) # enqueue next with an updated path
            visited.add(n)
    return None # return when the queue is exhausted

""" """
edges = [
    # Top row
    ('A','B'), ('B','C'), ('C','D'),

    # Second/third/fourth rows
    ('E','F'), ('I','J'), ('K','L'),
    ('M','N'),  ('N', 'O'),

    # Columns
    ('A','E'), ('E','I'), ('I','M'),
    ('B','F'),
    ('C','G'), ('K','O'),
    ('H','L'), ('L','P'),

    # Diagonals drawn in the figure (top-left square + center)
    ('A','F'),  # diagonal across A–F
    ('D', 'G'), # down-left from D to G
]
# ----------------------------------------------------------------
g = Task1(edges=edges).g


# ... (all your Task1 code unchanged above) ...
g = Task1(edges=edges).g

def run():
    # (a)
    print("DFS components:", components_dfs(g))
    print("BFS components:", components_bfs(g))
    # (b) + (c)
    pairs = [('A', 'F'), ('D', 'F')]
    for (u, v) in pairs:
        p_dfs = dfs_path(g, u, v)
        p_bfs = bfs_path(g, u, v)
        print(f"DFS path {u}->{v}:", p_dfs)
        print(f"BFS path {u}->{v}:", p_bfs)
        same = (p_dfs is not None and p_bfs is not None and p_dfs == p_bfs)
        print(f"Same path? {same}")

if __name__ == "__main__":
    run()
