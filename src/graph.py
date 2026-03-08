


from dataclasses import dataclass
# from typing import TypeVar

import json
from typing import Optional

import pygame

# from path_finding import Location, NodeIndex

# Location = TypeVar('Location')

@dataclass 
class GraphNode:
    id: int
    label: str 
    x: int 
    y: int 



class Graph:
    def __init__(self):
        self.nodes: dict[int, GraphNode] = {}
        self.edges: dict[int, list[int]] = {}

    def load(self, graph_data) -> None:
        if graph_data:
            # Load nodes
            nodes_data = graph_data.get('nodes')
            if nodes_data:
                for node_data in nodes_data:
                    node = GraphNode(
                        id=node_data.get('id'),
                        label=node_data.get('label'),
                        x=node_data.get('x'),
                        y=node_data.get('y')
                    )
                    self.nodes[node.id] = node
            
            # Load edges
            edges_data = graph_data.get('edges')
            if edges_data:
                # Extract "edges" and convert keys from str to int
                self.edges: dict[int, list[int]] = {
                    int(k): v for k, v in edges_data.items()
                }

    def neighbors(self, node_id: int) -> list[int]:
        """Return the list of Neighbors or Children of a GraphNode."""
        return self.edges[node_id]
    
    def get_nodes(self) -> dict[int, GraphNode]:
        return self.nodes
    
    def get_edges(self) -> dict[int, list[int]]:
        return self.edges

    def show_grid(self, screen) -> None:
        """Overlay grid lines and graph edges on the screen.

        The graph is expected to follow the same structure loaded from the
        JSON file (a dictionary with "nodes" list and "edges" mapping).
        Lines are drawn between each node and its children.
        """
        # draw regular grid
        # grid_size = 32  # size of each grid cell in pixels
        # w, h = self.screen.get_size()
        # for x in range(0, w, grid_size):
        #     pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, h), 3)
        # for y in range(0, h, grid_size):
        #     pygame.draw.line(self.screen, (255, 255, 255), (0, y), (w, y), 3)

        # print(f"Graph data: {self.graph}")

        font = pygame.font.Font(None, 24)

        # create a mapping from node id -> (x, y) coordinates
        node_positions = {
            node_id: (node.x, node.y)
            for node_id, node in self.nodes.items()
        }
        
        edges = self.edges
        # iterate through edges: src -> [child_ids]
        for src_key, children in edges.items():
            try:
                # JSON keys might be strings
                src_id = int(src_key)
            except (ValueError, TypeError):
                src_id = src_key

            src_pos = node_positions.get(src_id)
            if not src_pos:
                continue

            # Draw node id 
            text_surface = font.render(str(src_id), True, (255, 0, 0))
            screen.blit(text_surface, (src_pos[0] + 5, src_pos[1] - 15))

            for child_id in children:
                child_pos = node_positions.get(child_id)
                if child_pos:
                    # draw line from source to child
                    pygame.draw.line(screen, (0, 255, 0), src_pos, child_pos, 3)

    def _calculate_distance(self, a: tuple[int, int], b: tuple[int, int]) -> float:
        (x1, y1) = a
        (x2, y2) = b

        return abs(x1 - x2) + abs(y1 - y2)
    
    def get_closest_node(self, position_x : int, position_y: int) -> GraphNode | None:
        """Return the closest GraphNode to a position (x,y)."""
        min_node = None
        
        min_distance = 9999999
        current_distance = 0

        for current_node in self.nodes.values():
            current_distance = self._calculate_distance((position_x, position_y), 
                                                        (current_node.x, current_node.y))
            if current_distance < min_distance:
                min_distance = current_distance
                min_node = current_node

        return min_node
    
    
    def convert_to_pair_points(self, start_node: int, target_node: int, list_node_index: dict[int, Optional[int]]) -> list[tuple[int,int]]:
        """Convert a list of Node indexes to a list of positions(x,y)."""
        output_list = []

        tmp_index = target_node
        current_node_index = target_node

        print("   Path: ", end="")
        while current_node_index != start_node:
            print(f"{current_node_index} -> ", end="")
            # Store the position of the current node 
            node = self.nodes[current_node_index]
            output_list.append((node.x, node.y))

            # Move to the parent node
            tmp_index = list_node_index[current_node_index]
            current_node_index = tmp_index

        # Add the start point 
        print(f"{current_node_index}")
        node = self.nodes[current_node_index]
        output_list.append((node.x, node.y))

        return output_list