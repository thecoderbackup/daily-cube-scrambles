#!/usr/bin/env python3
import sys
import argparse
import random
import os
import pycuber as pc
from pycuber.solver import CFOPSolver

def generate_scramble_sequence(length=20):
    """Generate a random scramble sequence of the specified length."""
    moves = ["U", "U'", "U2", "D", "D'", "D2",
             "L", "L'", "L2", "R", "R'", "R2",
             "F", "F'", "F2", "B", "B'", "B2"]
    scramble = []
    for _ in range(length):
        mv = random.choice(moves)
        scramble.append(mv)
    return ' '.join(scramble)

def save_to_file(filename, scramble):
    """Save scramble sequence to a file."""
    with open(filename, 'w') as f:
        f.write(scramble)

def read_from_file(filename):
    """Read scramble sequence from a file."""
    with open(filename, 'r') as f:
        return f.read().strip()

def generate_batch_files(output_dir, num_files=25):
    """Generate multiple scramble files with solutions and visualizations."""
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_files):
        scramble_length = random.randint(0, 40)
        scramble = generate_scramble_sequence(scramble_length)
        filename = os.path.join(output_dir, f'scramble_{i+1}.txt')
        
        cube = pc.Cube()
        cube(scramble)
        scrambled_state = str(cube)
        
        solver = CFOPSolver(cube)
        solution = solver.solve(suppress_progress_messages=True)
        solution_str = str(solution)
        solution_moves = solution_str.split()
        
        step_by_step = []
        for j in range(len(solution_moves)):
            step_cube = pc.Cube()
            step_cube(scramble)
            step_cube(" ".join(solution_moves[:j+1]))
            step_by_step.append(str(step_cube))
        
        with open(filename, 'w') as f:
            f.write(f"Scramble ({scramble_length} moves): {scramble}\n\n")
            f.write("Scrambled Cube:\n")
            f.write(f"{scrambled_state}\n\n")
            f.write(f"Solution ({len(solution_moves)} moves): {solution_str}\n\n")
            f.write("Step-by-Step Solution:\n")
            for idx, state in enumerate(step_by_step, 1):
                f.write(f"Step {idx}:\n{state}\n\n")
        
        print(f"Generated: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Advanced Rubik's Cube Solver")
    parser.add_argument('--generate', action='store_true', help='Generate a single scramble')
    parser.add_argument('--generate-batch', action='store_true', help='Generate 25 scramble files')
    parser.add_argument('--solve', action='store_true', help='Solve a cube from file')
    parser.add_argument('--scramble-length', type=int, default=20, help='Length of scramble sequence')
    parser.add_argument('--file', '-f', type=str, help='Input/output file')
    parser.add_argument('--output-dir', type=str, default='scrambles', help='Directory for batch files')
    parser.add_argument('--visualize', '-v', action='store_true', help='Show step-by-step solution')

    args = parser.parse_args()

    if args.generate:
        scramble = generate_scramble_sequence(args.scramble_length)
        print(f"Scramble: {scramble}")
        cube = pc.Cube()
        cube(scramble)
        print("\nScrambled Cube:")
        print(cube)
        if args.file:
            save_to_file(args.file, scramble)
            print(f"Saved to {args.file}")

    elif args.generate_batch:
        generate_batch_files(args.output_dir)
        print(f"Generated 25 scrambles in '{args.output_dir}'")

    elif args.solve:
        if not args.file:
            print("Error: Specify input file with --file")
            sys.exit(1)
        try:
            scramble = read_from_file(args.file)
            cube = pc.Cube()
            cube(scramble)
            print(f"Loaded scramble from {args.file}")
            print("\nScrambled Cube:")
            print(cube)
            
            solver = CFOPSolver(cube)
            solution = solver.solve(suppress_progress_messages=True)
            print(f"\nSolution: {solution}")
            
            if args.visualize:
                print("\nVisualizing Steps:")
                steps = []
                for move in solution:
                    steps.append(str(move))
                    viz_cube = pc.Cube()
                    viz_cube(scramble + " " + " ".join(steps))
                    print(f"\nAfter {move}:")
                    print(viz_cube)

        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()