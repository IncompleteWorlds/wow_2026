


# from queue import Queue
from collections import deque

from typing import Optional, Protocol, TypeVar

from graph import Graph
# from collections import deque


# Location = tuple[int, int]
# NodeIndex = int

def get_path(graph: Graph, start_x: int, start_y: int, target_x: int, target_y: int) -> list[tuple[int, int]]:
    """Find the path from the start point (x,y) to the target point (x,y)."""
    # Get the closest point to the Start Location
    start_node = graph.get_closest_node(start_x, start_y)
    # print(f"Start Node: {start_node.id}.  Pos: {start_x},{start_y}")

    # Get the closest point to the Target Location
    end_node = graph.get_closest_node(target_x, target_y)
    # print(f"End Node: {end_node.id}.  Pos: {target_x},{target_y}")

    if start_node is None or end_node is None:
        return []

    # Apply BFS
    map_parents : dict[int, Optional[int]] = {}
    map_parents = breadth_first_search(graph, start_node.id, end_node.id)

    # Convert to pair of positions (x,y)
    list_pair_points : list[tuple[int, int]] = []
    list_pair_points = graph.convert_to_pair_points(start_node.id, end_node.id, map_parents)

    # Add the target position 
    list_pair_points.append((target_x, target_y))

    print("*** List pairs: ", list_pair_points)
    return list_pair_points


def breadth_first_search(graph: Graph, start: int, target: int) -> dict[int, Optional[int]]:
    # Way forward
    frontier = deque()
    frontier.append(start)

    # Way back to the starting point
    came_from: dict[int, Optional[int]] = {}
    came_from[start] = None
    
    # while not frontier.empty():
    while frontier:
        current: int = frontier.popleft()
        
        # Early exit
        if current == target: 
            break
        
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.append(next)
                came_from[next] = current
    
    return came_from

