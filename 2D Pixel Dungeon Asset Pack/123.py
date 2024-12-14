from heapq import *

graph = {'A': [(2, 'M'), (3, "P")],
         'M': [(2, 'A'), (2, "N")],
         'N': [(2, 'M'), (2, "B")],
         'P': [(3, 'A'), (4, "B")],
         'B': [(4, 'P'), (2, "N")],
         }


def dijkstrs(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neight_cost, neight_node = next_node
            new_cost = cost_visited[cur_node] + neight_cost
            if neight_node not in cost_visited or new_cost < cost_visited[neight_node]:
                heappush(queue, (new_cost, neight_node))
                cost_visited[neight_node] = new_cost
                visited[neight_node] = cur_node
    return visited


visited = dijkstrs("A", "B", graph)

cur_node = "B"
print(f"\npath from B to A: \n B", end="")
while cur_node != "A":
    cur_node = visited[cur_node]
    print(f' ----> {cur_node}', end="")