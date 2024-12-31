import os
import random
import math
import string
import time
import matplotlib.pyplot as plt

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
            color = "W"  # White
        elif char.isupper():
            step = string.ascii_uppercase.index(char) + 1
            color = "B"  # Black
        else:
            continue

        position_index += step
        row, col = divmod(position_index, m)
        if row < n:
            board[row][col] = color

    return board

# Function to print the grid like a table
def print_grid(grid):
    for row in grid:
        print(' '.join(str(cell) if cell is not None else '.' for cell in row))

# Objective function
def objective_function(state):
    def count_triples(line):
        return sum(1 for i in range(len(line) - 2) if line[i].lower() == line[i+1].lower() == line[i+2].lower())

    row_violations = sum(abs((row.count('B') + row.count('b')) - (row.count('W') + row.count('w'))) for row in state)
    col_violations = sum(abs(([row[i] for row in state].count('B') + [row[i] for row in state].count('b')) - ([row[i] for row in state].count('W') + [row[i] for row in state].count('w'))) for i in range(len(state[0])))
    triple_row_violations = sum(count_triples(row) for row in state)
    triple_col_violations = sum(count_triples([row[i] for row in state]) for i in range(len(state[0])))
    return row_violations + col_violations + triple_row_violations + triple_col_violations

# Random fill for the initial state
def random_fill(state):
    new_state = [row[:] for row in state]
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] is None:
                new_state[i][j] = random.choice(['b', 'w'])
    return new_state

# Random neighbor
def random_neighbor(state):
    new_state = [row[:] for row in state]
    while True:
        i = random.randint(0, len(state) - 1)
        j = random.randint(0, len(state[0]) - 1)
        if new_state[i][j] in ['b', 'w']:
            new_state[i][j] = 'w' if new_state[i][j] == 'b' else 'b'
            break
    return new_state

# Temperature schedule
def schedule(t, initial_temp):
    return initial_temp / (1 + t)

# Simulated Annealing Algorithm
def simulated_annealing(current_state, initial_temp, max_steps):
    best = current_state
    T = initial_temp

    # For plotting
    steps = []
    values = []
    temperature = []

    for t in range(max_steps):
        T = schedule(t, initial_temp)

        if T == 0:
            break

        next_state = random_neighbor(current_state)

        DE = objective_function(next_state) - objective_function(current_state)
        
        if DE < 0 or random.random() < math.exp(-DE/T):
            current_state = next_state

        if objective_function(current_state) < objective_function(best):
            best = current_state

        f = objective_function(best)
        print(f"Step: {t+1}, Temp: {T:.4f}, Best f: {f}")

        steps.append(t)
        values.append(f)
        temperature.append(T)

    return best, steps, values, temperature

def plot_objective_function_over_steps(steps, values):
    plt.plot(steps, values, label='Objective Function')
    plt.axhline(0, color='r', linestyle='--', label='Zero Violations')
    plt.xlabel('Steps')
    plt.ylabel('Objective Function Value')
    plt.title('Objective Function Value over Steps')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_temperature_over_steps(steps, temperature):
    plt.plot(steps, temperature, label='Temperature')
    plt.xlabel('Steps')
    plt.ylabel('Temperature')
    plt.title('Temperature over Steps')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function
def main():
    input_file = input("Enter the input file name: ")
    if not os.path.isfile(input_file):
        print(f"File {input_file} does not exist.")
        return
    max_steps = int(input("Enter the maximum number of steps: "))

    grid = decode_grid(input_file)
    print("Starting Board:")
    print_grid(grid)

    initial_temp = max_steps
    
    initial_state = random_fill(grid)
    print("\nInitial State:")
    print_grid(initial_state)
    print("\n")

    start_time = time.time()
    result, steps, values, temperature = simulated_annealing(initial_state, initial_temp, max_steps)
    end_time = time.time()

    print("\nBest State:")
    for row in result:
        print(' '.join(row).replace('b', 'B').replace('w', 'W'))
    print(f"Execution Time: {end_time - start_time:.2f} seconds")

    plot_objective_function_over_steps(steps, values)
    #plot_temperature_over_steps(steps, temperature)

if __name__ == "__main__":
    main()
    
