import pygame
import networkx as nx
import json
import time
import random

# Load the graph from the JSON file
with open("graph.json", "r") as json_file:
    loaded_graph_dict = json.load(json_file)

# Create a graph from the loaded dictionary
loaded_G = nx.node_link_graph(loaded_graph_dict)

# Pygame initialization
pygame.init()

# Set the dimensions of the window
width, height = 420, 420
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Graph Visualization")

# Function to convert graph coordinates to screen coordinates
def convert_coordinates(pos):
    return pos[0] * 20 + 20, pos[1] * 20 + 20  # Adjusted scaling factor

# Draw the nodes
def draw_nodes():
    for node in loaded_G.nodes:
        pygame.draw.circle(screen, (255, 255, 255), convert_coordinates(node), 2)  # Adjusted circle radius

# Draw the path
def draw_path(path):
    for i in range(len(path) - 1):
        pygame.draw.line(screen, (0, 255, 0), convert_coordinates(path[i]), convert_coordinates(path[i + 1]), 3)

# Main loop
running = True
start = (5, 5)
end = (10, 10)
current_position = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw nodes and edges
    draw_nodes()

    # Define path before the loop starts
    path = nx.shortest_path(loaded_G, source=start, target=end)

    # Draw the path
    draw_path(path)

    # Draw the moving blue ball
    pygame.draw.circle(screen, (0, 0, 255), convert_coordinates(start), 8)

    # Draw the red ball at the endpoint
    pygame.draw.circle(screen, (255, 0, 0), convert_coordinates(end), 8)

    # Update the display
    pygame.display.flip()

    # Add a delay for smooth animation
    time.sleep(0.15)

    # Check if the blue ball has reached the endpoint
    if start == end:
        # Choose a new random endpoint
        new_end = random.choice(list(loaded_G.nodes))
        
        # Set the new endpoint as the endpoint
        end = new_end
        
        # Compute the new path
        path = nx.shortest_path(loaded_G, source=start, target=end)
        
        current_position = 0
        
    # Move the blue ball along the path
    if path:
        start = path[current_position]
        current_position = 1

        # Reset the current_position if the end of the path is reached
        if current_position >= len(path):
            current_position = 0

# Quit pygame
pygame.quit()
