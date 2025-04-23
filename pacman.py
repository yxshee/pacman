import pygame
import random
import math

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
CELL_SIZE = 20
MAZE_WIDTH = 15
MAZE_HEIGHT = 15
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE
SPEED = 2  # Pixels per frame

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Directions
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

# Maze layout (1 = wall, 0 = path)
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Pellets (1 = pellet, 0 = no pellet)
pellets = [[1 if maze[i][j] == 0 else 0 for j in range(MAZE_WIDTH)] for i in range(MAZE_HEIGHT)]
pellets_left = sum(sum(row) for row in pellets)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Add score & lives
score = 0
lives = 3
font = pygame.font.SysFont('arial', 18)

# Pac-Man starting position and direction (placed in cell (1,1))
pacman_x = 1 * CELL_SIZE + CELL_SIZE // 2
pacman_y = 1 * CELL_SIZE + CELL_SIZE // 2
direction = RIGHT
requested_direction = RIGHT

# Ghost starting position and direction (placed in cell (7,3))
ghost_x = 7 * CELL_SIZE + CELL_SIZE // 2
ghost_y = 3 * CELL_SIZE + CELL_SIZE // 2
ghost_direction = DOWN

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                requested_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                requested_direction = RIGHT
            elif event.key == pygame.K_UP:
                requested_direction = UP
            elif event.key == pygame.K_DOWN:
                requested_direction = DOWN

    # Move Pac-Man
    dx, dy = direction
    new_x = pacman_x + dx * SPEED
    new_y = pacman_y + dy * SPEED

    # Determine current grid cell (from previous position)
    grid_x = int(pacman_x // CELL_SIZE)
    grid_y = int(pacman_y // CELL_SIZE)

    # Check for wall collision for Pac-Man
    if dx > 0 and new_x > (grid_x + 1) * CELL_SIZE \
       and grid_x + 1 < MAZE_WIDTH and maze[grid_y][grid_x + 1] == 1:
        new_x = (grid_x + 1) * CELL_SIZE - 1
    elif dx < 0 and new_x < grid_x * CELL_SIZE \
       and grid_x - 1 >= 0 and maze[grid_y][grid_x - 1] == 1:
        new_x = grid_x * CELL_SIZE
    if dy > 0 and new_y > (grid_y + 1) * CELL_SIZE \
       and grid_y + 1 < MAZE_HEIGHT and maze[grid_y + 1][grid_x] == 1:
        new_y = (grid_y + 1) * CELL_SIZE - 1
    elif dy < 0 and new_y < grid_y * CELL_SIZE \
       and grid_y - 1 >= 0 and maze[grid_y - 1][grid_x] == 1:
        new_y = grid_y * CELL_SIZE

    pacman_x, pacman_y = new_x, new_y

    # Allow turning and pellet consumption when near the center of a cell
    center_x = grid_x * CELL_SIZE + CELL_SIZE // 2
    center_y = grid_y * CELL_SIZE + CELL_SIZE // 2
    if abs(pacman_x - center_x) < SPEED and abs(pacman_y - center_y) < SPEED:
        req_dx, req_dy = requested_direction
        next_grid_x = grid_x + req_dx
        next_grid_y = grid_y + req_dy
        if (0 <= next_grid_x < MAZE_WIDTH and 0 <= next_grid_y < MAZE_HEIGHT and 
            maze[next_grid_y][next_grid_x] == 0):
            direction = requested_direction
            pacman_x, pacman_y = center_x, center_y

        # Eat pellet if available (bounds‑checked)
        if 0 <= grid_y < MAZE_HEIGHT and 0 <= grid_x < MAZE_WIDTH \
           and pellets[grid_y][grid_x] == 1:
            pellets[grid_y][grid_x] = 0
            score += 10
            pellets_left -= 1

    # Move Ghost
    ghost_dx, ghost_dy = ghost_direction
    ghost_new_x = ghost_x + ghost_dx * SPEED
    ghost_new_y = ghost_y + ghost_dy * SPEED

    # Calculate ghost grid position after movement for collision checking
    ghost_grid_x = int(ghost_new_x // CELL_SIZE)
    ghost_grid_y = int(ghost_new_y // CELL_SIZE)

    # Check for wall collisions for Ghost
    if ghost_dx > 0 and ghost_new_x > (ghost_grid_x + 1) * CELL_SIZE \
       and ghost_grid_x + 1 < MAZE_WIDTH and maze[ghost_grid_y][ghost_grid_x + 1] == 1:
        ghost_new_x = (ghost_grid_x + 1) * CELL_SIZE - 1
    elif ghost_dx < 0 and ghost_new_x < ghost_grid_x * CELL_SIZE \
       and ghost_grid_x - 1 >= 0 and maze[ghost_grid_y][ghost_grid_x - 1] == 1:
        ghost_new_x = ghost_grid_x * CELL_SIZE
    if ghost_dy > 0 and ghost_new_y > (ghost_grid_y + 1) * CELL_SIZE \
       and ghost_grid_y + 1 < MAZE_HEIGHT and maze[ghost_grid_y + 1][ghost_grid_x] == 1:
        ghost_new_y = (ghost_grid_y + 1) * CELL_SIZE - 1
    elif ghost_dy < 0 and ghost_new_y < ghost_grid_y * CELL_SIZE \
       and ghost_grid_y - 1 >= 0 and maze[ghost_grid_y - 1][ghost_grid_x] == 1:
        ghost_new_y = ghost_grid_y * CELL_SIZE

    ghost_x, ghost_y = ghost_new_x, ghost_new_y

    # Change ghost direction at cell center
    ghost_center_x = ghost_grid_x * CELL_SIZE + CELL_SIZE // 2
    ghost_center_y = ghost_grid_y * CELL_SIZE + CELL_SIZE // 2
    if abs(ghost_x - ghost_center_x) < SPEED and abs(ghost_y - ghost_center_y) < SPEED:
        possible_directions = [
            d for d in [RIGHT, LEFT, UP, DOWN]
            if (0 <= ghost_grid_x + d[0] < MAZE_WIDTH and 0 <= ghost_grid_y + d[1] < MAZE_HEIGHT and
                maze[ghost_grid_y + d[1]][ghost_grid_x + d[0]] == 0)
        ]
        if possible_directions:
            ghost_direction = random.choice(possible_directions)
        ghost_x, ghost_y = ghost_center_x, ghost_center_y

    # Check for collision between Pac-Man and Ghost
    if (int(pacman_x // CELL_SIZE) == int(ghost_x // CELL_SIZE) and
        int(pacman_y // CELL_SIZE) == int(ghost_y // CELL_SIZE)):
        lives -= 1
        if lives > 0:
            # Reset positions
            pacman_x = 1 * CELL_SIZE + CELL_SIZE // 2
            pacman_y = 1 * CELL_SIZE + CELL_SIZE // 2
            direction = RIGHT
            requested_direction = RIGHT
            ghost_x = 7 * CELL_SIZE + CELL_SIZE // 2
            ghost_y = 3 * CELL_SIZE + CELL_SIZE // 2
            ghost_direction = DOWN
        else:
            # Final Game Over screen
            game_over = font.render("GAME OVER", True, YELLOW)
            screen.blit(game_over, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 10))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

    # Drawing
    screen.fill(BLACK)

    # UI overlay with translucent background
    ui_text = f"Score: {score}   Lives: {lives}   Pellets: {pellets_left}"
    ui_surf = font.render(ui_text, True, WHITE)
    bg_surf = pygame.Surface((ui_surf.get_width()+6, ui_surf.get_height()+4), pygame.SRCALPHA)
    bg_surf.fill((0, 0, 0, 150))  # semi‑transparent black
    screen.blit(bg_surf, (8, 8))
    screen.blit(ui_surf, (10, 10))

    # Draw maze walls
    for i in range(MAZE_HEIGHT):
        for j in range(MAZE_WIDTH):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, BLUE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw pellets
    for i in range(MAZE_HEIGHT):
        for j in range(MAZE_WIDTH):
            if pellets[i][j] == 1:
                pygame.draw.circle(screen, WHITE, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), 2)

    # Draw Pac-Man with mouth animation
    radius = CELL_SIZE//2 - 2
    mouth_open = (pygame.time.get_ticks() // 200) % 2 == 0
    rect = (int(pacman_x)-radius, int(pacman_y)-radius, radius*2, radius*2)
    if mouth_open:
        pygame.draw.arc(screen, YELLOW, rect, math.radians(30), math.radians(330), radius)
    else:
        pygame.draw.circle(screen, YELLOW, (int(pacman_x), int(pacman_y)), radius)

    # Draw Ghost with circle body + eyes
    radius = CELL_SIZE//2 - 2
    gx, gy = int(ghost_x), int(ghost_y)
    # head & body
    pygame.draw.circle(screen, RED, (gx, gy), radius)
    pygame.draw.rect(screen, RED, (gx - radius, gy, radius*2, radius))
    # eyes
    ex = radius // 2
    ey = radius // 2
    pygame.draw.circle(screen, WHITE, (gx - ex, gy - ey), radius//3)
    pygame.draw.circle(screen, WHITE, (gx + ex, gy - ey), radius//3)
    pygame.draw.circle(screen, BLUE,  (gx - ex, gy - ey), radius//6)
    pygame.draw.circle(screen, BLUE,  (gx + ex, gy - ey), radius//6)

    pygame.display.flip()

    # Frame rate control
    clock.tick(30)

pygame.quit()
