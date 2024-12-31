import string
import time
import os

node_count = 0

# Function to check if the grid is valid after placing a value at a position
def is_valid(grid, x, y, value):

    width = len(grid[0])
    height = len(grid)

    # Check for three consecutive same values horizontally
    if x >= 2 and grid[y][x-1] == value and grid[y][x-2] == value:
        return False
    if x < width - 2 and grid[y][x+1] == value and grid[y][x+2] == value:
        return False
    if x >= 1 and x < width - 1 and grid[y][x-1] == value and grid[y][x+1] == value:
        return False

    # Check for three consecutive same values vertically
    if y >= 2 and grid[y-1][x] == value and grid[y-2][x] == value:
        return False
    if y < height - 2 and grid[y+1][x] == value and grid[y+2][x] == value:
        return False
    if y >= 1 and y < height - 1 and grid[y-1][x] == value and grid[y+1][x] == value:
        return False

    # Check if the number of 'B' or 'W' exceeds half the width in the row
    row_values = [grid[y][i] for i in range(width) if grid[y][i] is not None]
    col_values = [grid[i][x] for i in range(height) if grid[i][x] is not None]
    
    if row_values.count('B') + (value == 'B') > width // 2:
        return False
    if row_values.count('W') + (value == 'W') > width // 2:
        return False

    # Check if the number of 'B' or 'W' exceeds half the height in the column
    if col_values.count('B') + (value == 'B') > height // 2:
        return False
    if col_values.count('W') + (value == 'W') > height // 2:
        return False

    return True

# Recursive function to solve the grid
def solve_grid(grid, max_nodes):
    global node_count
    width = len(grid[0])
    height = len(grid)

    for y in range(height):
        for x in range(width):
            if grid[y][x] is None:
                for value in ['B', 'W']:
                    if is_valid(grid, x, y, value):
                        grid[y][x] = value
                        node_count += 1
                        if node_count > max_nodes:
                            raise RuntimeError("Maximum number of nodes expanded reached.")
                        if solve_grid(grid, max_nodes):
                            return True
                        grid[y][x] = None
                return False
    return True

# Function to decode the string format into a grid
def decode_grid(input_file):
    with open(input_file, 'r') as file:
        input_str = file.read().strip()
    dimensions, positions = input_str.split(':')
    n, m = map(int, dimensions.split('x'))

    board = [[None for _ in range(m)] for _ in range(n)]

    position_index = -1
    row, col = 0, 0
    for char in positions:
        if char.islower():
            step = string.ascii_lowercase.index(char) + 1
            color = "W"
        elif char.isupper():
            step = string.ascii_uppercase.index(char) + 1
            color = "B"
        else:
            continue

        position_index += step
        row, col = divmod(position_index, m)
        if row < n:
            board[row][col] = color

    return board

# Function to encode the grid into a string format
def encode(grid):
    n = len(grid)
    m = len(grid[0])
    positions = []
    position_index = -1

    for row in range(n):
        for col in range(m):
            if grid[row][col] is not None:
                step = (row * m + col) - position_index
                position_index = row * m + col
                if grid[row][col] == 'W':
                    positions.append(string.ascii_lowercase[step - 1])
                elif grid[row][col] == 'B':
                    positions.append(string.ascii_uppercase[step - 1])
    positions.append(string.ascii_lowercase[step - 1])
    dimensions = f"{n}x{m}"
    encoded_str = f"{dimensions}:{''.join(positions)}"
    return encoded_str

# Function to print the grid like a table
def print_grid(grid):
    for row in grid:
        print(' '.join(str(cell) if cell is not None else '.' for cell in row))

# Main function
def main():
    global node_count
    
    node_count = 0

    input_file = input("Enter the input file name: ")
    if not os.path.isfile(input_file):
        print(f"File {input_file} does not exist.")
        return

    try:
        max_nodes = int(input("Enter the maximum number of nodes to expand: "))
    except ValueError:
        print("Invalid input for maximum number of nodes. Please enter an integer.")
        return

    grid = decode_grid(input_file)
    
    print("Starting Board:")
    print_grid(grid)

    print("\nSolving Puzzle...")

    start_time = time.time()
    try:
        if solve_grid(grid, max_nodes):
            end_time = time.time()
            print("\nSolved Puzzle:")
            print_grid(grid)
            with open('output.txt', 'w') as file:
                file.write(encode(grid))
        else:
            end_time = time.time()
            print("No solution found.")
    except RuntimeError as e:
        end_time = time.time()
        print(e)

    execution_time = end_time - start_time
    print(f"\nExecution Time: {execution_time:.5f} seconds")
    print(f"Nodes Expanded: {node_count}")

if __name__ == "__main__":
    main()
