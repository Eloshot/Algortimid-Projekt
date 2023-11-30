import pygame
import networkx as nx
import time
import random


max_int = 2**31


board_x_size = 20
board_y_size = 20
board_spacing = 20


def add_node_with_edges(board, x, y, max_x, max_y):
    board.add_node((x, y))
    left = x - 1
    right = x + 1
    top = y - 1
    bottom = y + 1
    if (left > -1 and left < max_x):
        board.add_edge((x, y), (left, y))
    if (right > -1 and right < max_x):
        board.add_edge((x, y), (right, y))
    if (top > -1 and top < max_y):
        board.add_edge((x, y), (x, top))
    if (bottom > -1 and bottom < max_y):
        board.add_edge((x, y), (x, bottom))


def make_board_graph(x_size, y_size):
    board = nx.Graph()

    for i in range(0, x_size):
        for j in range(0, y_size):
            add_node_with_edges(board, i, j, x_size, y_size)

    return board


board_graph = make_board_graph(board_x_size, board_y_size)

# Pygame initialization
pygame.init()

# Set the dimensions of the window
width, height = board_x_size * board_spacing + \
    board_spacing, board_y_size * board_spacing + board_spacing
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Graph Visualization")


def convert_coordinates(pos):
    # Function to convert graph coordinates to screen coordinates
    # Adjusted scaling factor
    return pos[0] * board_spacing + board_spacing, pos[1] * board_spacing + board_spacing


def draw_possible_points():
    # Draw the nodes
    for node in board_graph.nodes:
        pygame.draw.circle(screen, (255, 255, 255), convert_coordinates(
            node), 2)  # Adjusted circle radius


def draw_path(path):
    # Draw the path
    for i in range(len(path) - 1):
        point_a = path[i]
        point_b = path[i + 1]
        pygame.draw.line(screen, (0, 255, 0), convert_coordinates(
            point_a), convert_coordinates(point_b), 3)


def draw_snake(path):
    # Draw the head
    pygame.draw.circle(screen, (0, 0, 255),
                       convert_coordinates(snake.head()), 8)
    # Draw the path
    for i in range(len(path) - 1):
        point_a = path[i]
        point_b = path[i + 1]
        pygame.draw.line(screen, (255, 255, 0), convert_coordinates(
            point_a), convert_coordinates(point_b), 5)


class Snake:
    def __init__(self, initial_parts):
        self.parts = initial_parts
        self.ate_positions = []

    def move(self, position):
        """
        Moves all parts of the snake down one position, and adds the new part (the new position) to the front
        Extends the snake if the last position, the tip of the snake tail, was previously at the position of the
        food eaten
        """
        died = False

        # skip the same position updates
        if (position[0] == self.parts[0][0] and position[1] == self.parts[0][1]):
            return died

        new_parts = []
        last = self.parts.pop()
        for i in range(0, len(self.parts)):
            new_parts.append(self.parts[i])

        # Check the position is not occupied after the snake tail has move
        # If we check the position before the snake tail has moved, the snake not be able to
        # Move to its current tail position
        if position in self.parts:
            died = True

        new_parts.insert(0, position)

        self.parts = new_parts
        ate_at = self.ate_positions[0] if len(self.ate_positions) > 0 else None
        if ate_at is not None and ate_at[0] == last[0] and ate_at[1] == last[1]:
            self.parts.append(ate_at)
            self.ate_positions.remove(ate_at)

        return died

    def eat(self, position):
        self.ate_positions.append(position)

    def head(self):
        return self.parts[0]


# Main loop
running = True
direction = (1, 0)
snake = Snake([(5, 5), (4, 5), (3, 5), (2, 5)])


def get_random_food_position():
    maybe = random.choice(list(board_graph.nodes))
    if maybe in snake.parts:
        return get_random_food_position()
    else:
        return maybe


food_position = get_random_food_position()


def snake_parts_weights_to_avoid_collision(point_a, point_b, direction):
    if point_b in snake.parts:
        return max_int
    else:
        return 1


def get_shortest_path(point_a, point_b):
    path = nx.shortest_path(
        board_graph, source=point_a, target=point_b, weight=snake_parts_weights_to_avoid_collision)
    path.remove(path[0])

    return path


# Define path before the loop starts
path_to_food = get_shortest_path(snake.head(), food_position)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw nodes and edges
    draw_possible_points()

    # Draw the path
    draw_path(path_to_food)

    draw_snake(snake.parts)

    # Draw the red ball at the endpoint
    pygame.draw.circle(screen, (255, 0, 0),
                       convert_coordinates(food_position), 8)

    # Update the display
    pygame.display.flip()

    # Add a delay for smooth animation
    time.sleep(0.0001)

    # Check if the blue ball has reached the endpoint
    if snake.head() == food_position:
        snake.eat(food_position)
        food_position = get_random_food_position()

        # Compute the new path
        path_to_food = get_shortest_path(snake.head(), food_position)

    # Move the blue ball along the path
    if path_to_food:
        died = snake.move(path_to_food[0])
        if died:
            running = False
            draw_snake(snake.parts)
            font = pygame.font.SysFont('chalkduster.ttf', 72)
            img = font.render('Game over!', True, "#FF0000")
            screen.blit(img, (20, 20))
            pygame.display.flip()
            print("Game over")

            time.sleep(4)

        path_to_food.remove(path_to_food[0])

# Quit pygame
pygame.quit()
