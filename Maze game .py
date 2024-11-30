import random

def generate_maze(size):
    """Generates a simple maze with walls and open paths."""
    maze = [['#' for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            maze[i][j] = '.' if random.choice([True, False]) else '#'
    maze[0][0] = 'S'  # Start point
    maze[size - 1][size - 1] = 'E'  # End point
    return maze

def print_maze(maze, player_pos):
    """Print the maze with the player's current position."""
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if (i, j) == player_pos:
                print('P', end=' ')  # Player
            else:
                print(cell, end=' ')
        print()

def move_player(player_pos, direction, maze):
    """Move the player in the maze."""
    x, y = player_pos
    size = len(maze)
    if direction == 'w' and x > 0 and maze[x - 1][y] != '#':  # Up
        x -= 1
    elif direction == 's' and x < size - 1 and maze[x + 1][y] != '#':  # Down
        x += 1
    elif direction == 'a' and y > 0 and maze[x][y - 1] != '#':  # Left
        y -= 1
    elif direction == 'd' and y < size - 1 and maze[x][y + 1] != '#':  # Right
        y += 1
    return x, y

def play_game(size):
    """Main game logic."""
    maze = generate_maze(size)
    player_pos = (0, 0)
    print("Welcome to the Maze Game!")
    print("Use 'w' (up), 's' (down), 'a' (left), 'd' (right) to move. Reach 'E' to win!")

    while True:
        print_maze(maze, player_pos)
        if player_pos == (size - 1, size - 1):
            print("Congratulations! You've reached the end of the maze!")
            break
        direction = input("Move (w/a/s/d): ").strip().lower()
        if direction in ['w', 'a', 's', 'd']:
            player_pos = move_player(player_pos, direction, maze)
        else:
            print("Invalid input! Use 'w', 'a', 's', or 'd'.")

# Run the game
