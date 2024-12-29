from collections import defaultdict, deque

def bfs_farthest_node(graph, start):
    visited = set()
    queue = deque([(start, 0)])
    farthest_node = start
    max_distance = 0
    
    while queue:
        node, distance = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        if distance > max_distance:
            max_distance = distance
            farthest_node = node
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))
    
    return farthest_node, max_distance

def tree_diameter(edges, n):
    if n == 0:
        return 0
    
    # Create the graph
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Perform the first BFS from an arbitrary node (node 1)
    start_node = edges[0][0]
    farthest_node, _ = bfs_farthest_node(graph, start_node)
    
    # Perform the second BFS from the farthest node found
    _, diameter = bfs_farthest_node(graph, farthest_node)
    
    return diameter

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    index = 0
    results = []
    
    while index < len(data):
        if data[index].strip() == '':
            index += 1
            continue
        
        n = int(data[index].strip())
        index += 1
        
        edges = []
        for _ in range(n):
            u, v = map(int, data[index].strip().split())
            edges.append((u, v))
            index += 1
        
        results.append(tree_diameter(edges, n))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
