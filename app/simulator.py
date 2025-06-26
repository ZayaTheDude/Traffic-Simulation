# Simulator class for managing the traffic simulation.
#
# This class is responsible for:
#   - Initializing the grid, cars, and intersections
#   - Advancing the simulation in discrete time steps
#   - Enforcing traffic rules (e.g., stopping at red lights, avoiding collisions)
#   - Providing a method to run the simulation for a set number of steps
#
# The design keeps the simulation logic separate from the data models (Car, Intersection),
# making the code modular and easier to test or extend.

import random
import os
import time
from app.models import Car, Intersection, RoadNetwork
from app.config import GRID_SIZE, NUM_CARS

class Simulator:
    def __init__(self, grid_size=GRID_SIZE, num_cars=NUM_CARS, intersection_cycle=5):
        """
        Initialize the simulation environment.
        Args:
            grid_size (int): Size of the grid (grid is grid_size x grid_size)
            num_cars (int): Number of cars to simulate
            intersection_cycle (int): Steps before traffic lights switch
        """
        self.grid_size = grid_size
        self.time_step = 0  # Tracks the current simulation step
        self.cars = []  # List of Car objects
        self.intersections = {}  # Dict mapping (x, y) to Intersection objects
        self.road_network = RoadNetwork(grid_size)

        # Place intersections at every 3x3 grid cell for simplicity
        for x in range(0, grid_size, 3):
            for y in range(0, grid_size, 3):
                self.intersections[(x, y)] = Intersection((x, y), cycle_length=intersection_cycle)

        # Randomly place cars on the grid, avoiding intersections
        for i in range(num_cars):
            while True:
                pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
                if pos not in self.intersections and all(car.position != pos for car in self.cars):
                    break
            direction = random.choice(['N', 'S', 'E', 'W'])
            self.cars.append(Car(i, pos, direction))

    def update(self):
        """
        Advance the simulation by one time step:
          - Update all intersection lights
          - Attempt to move each car (obeying lights and avoiding collisions)
        """
        self.time_step += 1
        # Update all intersections' lights
        for intersection in self.intersections.values():
            intersection.update_light()

        # Track new positions to prevent collisions
        new_positions = set()
        for car in self.cars:
            next_pos = self._get_next_position(car)
            # Check for grid bounds
            if not self._in_bounds(next_pos):
                continue  # Car stays in place if it would leave the grid
            # Check for intersection and red light
            intersection = self.intersections.get(next_pos)
            if intersection and not intersection.is_green(car.direction):
                continue  # Car stops at red light
            # Check for collision with another car
            if next_pos in new_positions or any(other.position == next_pos for other in self.cars):
                continue  # Car stops to avoid collision
            # Move the car
            car.move()
            new_positions.add(car.position)

    def _get_next_position(self, car):
        """
        Calculate the next position for a car based on its direction.
        Args:
            car (Car): The car to move
        Returns:
            tuple: The (x, y) position the car would move to
        """
        x, y = car.position
        if car.direction == 'N':
            return (x, y - 1)
        elif car.direction == 'S':
            return (x, y + 1)
        elif car.direction == 'E':
            return (x + 1, y)
        elif car.direction == 'W':
            return (x - 1, y)
        return (x, y)

    def _in_bounds(self, pos):
        """
        Check if a position is within the grid bounds.
        Args:
            pos (tuple): (x, y) position
        Returns:
            bool: True if within bounds, False otherwise
        """
        x, y = pos
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def get_state(self):
        """
        Return the current state of the simulation for inspection or API use.
        Returns:
            dict: Contains time_step, cars, and intersections
        """
        return {
            'time_step': self.time_step,
            'cars': [
                {'id': car.id, 'position': car.position, 'direction': car.direction}
                for car in self.cars
            ],
            'intersections': [
                {'position': intersection.position, 'NS': intersection.light_state['NS'], 'EW': intersection.light_state['EW']}
                for intersection in self.intersections.values()
            ]
        }

    def render(self):
        """
        Print a simple ASCII-art visualization of the grid, cars, and intersections.
        C: Car, +: Intersection, .: Empty space
        Cars will overwrite intersections if they occupy the same cell.
        """
        grid = [['.' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        # Draw intersections
        for pos, intersection in self.intersections.items():
            x, y = pos
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                # Show green/red for NS/EW: G/R or g/r
                if intersection.light_state['NS'] == 'green':
                    grid[y][x] = '+'  # Could use 'G' or 'g' for more detail
                else:
                    grid[y][x] = 'x'  # Could use 'R' or 'r' for more detail
        # Draw cars (overwrites intersection if on same cell)
        for car in self.cars:
            x, y = car.position
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                grid[y][x] = 'C'
        # Print the grid
        print("\nGrid:")
        for row in grid:
            print(' '.join(row))
        print()  # Blank line after grid

    def run(self, steps=20, visual=True, delay=0.2):
        """
        Run the simulation for a given number of steps, animating the grid if visual=True.
        Args:
            steps (int): Number of time steps to simulate
            visual (bool): Whether to print the grid visually
            delay (float): Seconds to pause between frames (for animation)
        """
        for _ in range(steps):
            self.update()
            if visual:
                # Clear the terminal for animation effect
                os.system('clear')  # Use 'cls' on Windows
                print(f"Step {self.time_step}:")
                self.render()
                time.sleep(delay)
            else:
                print(f"Step {self.time_step}: {self.get_state()}")

    # TODO: Add a pathfinding method (e.g., bfs or a_star) to compute paths for cars
    def find_path(self, start, goal):
        """
        Find a path from start to goal using the road network.
        Returns a list of positions (path) or [] if no path found.
        """
        # TODO: Implement BFS or A* pathfinding here
        return []