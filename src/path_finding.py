


# from queue import Queue
from collections import deque

from typing import Optional, Protocol, TypeVar

from graph import Graph
# from collections import deque



NodeIndex = int

def get_path(graph: Graph, start_x: int, start_y: int, target_x: int, target_y: int) -> dict[NodeIndex, Optional[NodeIndex]]:
    # Get the closest point to the Start Location
    start_node = graph.get_closest_node(start_x, start_y)

    # Get the closest point to the Target Location
    end_node = graph.get_closest_node(target_x, target_y)

    list_points : dict[NodeIndex, Optional[NodeIndex]] = {}
    if start_node is None or end_node is None:
        return list_points

    # Apply BFS
    list_points = breadth_first_search(graph, start_node.id, end_node.id)

    return list_points


def breadth_first_search(graph: Graph, start: NodeIndex, target: NodeIndex) -> dict[NodeIndex, Optional[NodeIndex]]:
    # frontier = Queue()
    # frontier.put(start)
    frontier = deque()
    frontier.append(start)
    came_from: dict[NodeIndex, Optional[NodeIndex]] = {}
    came_from[start] = None
    
    # while not frontier.empty():
    while not frontier:
        # current: Location = frontier.get()
        current: NodeIndex = frontier.popleft()
        
        # Early exit
        if current == target: 
            break
        
        for next in graph.neighbors(current):
            if next not in came_from:
                # frontier.put(next)
                frontier.append(next)
                came_from[next] = current
    
    return came_from


# parents = breadth_first_search(g, start, goal)

