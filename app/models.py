# Define core classes like Car, Intersection, etc.
#
# This file contains the main data models for the traffic simulation.
# The goal is to keep each class focused on a single responsibility, making the code easy to maintain and extend.
#
# We start with two core entities: Car and Intersection.
#
# Car: Represents a vehicle in the simulation. It knows its own position and direction, and can move forward.
# Intersection: Represents a traffic light at a grid intersection, with logic for cycling the light state.

class Car:
    def __init__(self, car_id, position, direction, destination=None, path=None):
        """
        Initialize a Car object.
        
        Args:
            car_id (int): Unique identifier for the car. Useful for tracking and debugging.
            position (tuple): (x, y) coordinates on the grid. This allows us to easily update and check positions.
            direction (str): One of 'N', 'S', 'E', 'W'. This keeps direction logic simple and readable.
            destination (tuple, optional): Target position (x, y) for the car to reach.
            path (list, optional): List of (x, y) tuples representing the path to the destination.
        """
        self.id = car_id  # Unique ID for each car, helps with debugging and tracking
        self.position = position  # (x, y) tuple for grid position
        self.direction = direction  # Cardinal direction as a string
        self.destination = destination  # (x, y) tuple for destination
        self.path = path or []  # List of (x, y) tuples for the path

    def move(self):
        """
        Move the car one step forward in its current direction.
        
        This method updates the car's position based on its direction.
        The grid is assumed to have (0,0) at the top-left, with y increasing downward.
        """
        x, y = self.position
        if self.direction == 'N':
            self.position = (x, y - 1)  # Move up
        elif self.direction == 'S':
            self.position = (x, y + 1)  # Move down
        elif self.direction == 'E':
            self.position = (x + 1, y)  # Move right
        elif self.direction == 'W':
            self.position = (x - 1, y)  # Move left
        # This simple approach makes it easy to add more directions or rules later.

    def next_move(self):
        """
        Decide the next move based on the path.
        Update direction if a turn is needed at an intersection.
        
        This method will be responsible for following the computed path and navigating the car
        towards its destination, including turning at intersections.
        """
        pass  # TODO: Implement logic to follow path, turn at intersections, and update direction

    def __repr__(self):
        """
        String representation for debugging and logging.
        Shows the car's ID, position, and direction.
        """
        return f"Car(id={self.id}, pos={self.position}, dir={self.direction})"

class Intersection:
    def __init__(self, position, initial_state=None, cycle_length=5):
        """
        Initialize an Intersection object with two-directional lights.
        
        Args:
            position (tuple): (x, y) coordinates on the grid.
            initial_state (dict, optional): Dict like {'NS': 'green', 'EW': 'red'}.
                If None, defaults to NS green, EW red.
            cycle_length (int): Number of simulation steps before the light changes.
        """
        self.position = position  # (x, y) tuple for grid position
        # Track both North-South and East-West lights. Only one can be green at a time.
        if initial_state is None:
            self.light_state = {'NS': 'green', 'EW': 'red'}
        else:
            self.light_state = initial_state.copy()
        self.cycle_length = cycle_length
        self.timer = 0

    def update_light(self):
        """
        Advance the timer and switch both light directions if needed.
        When timer reaches cycle_length, swap NS and EW lights.
        """
        self.timer += 1
        if self.timer >= self.cycle_length:
            # Swap the light states
            if self.light_state['NS'] == 'green':
                self.light_state['NS'] = 'red'
                self.light_state['EW'] = 'green'
            else:
                self.light_state['NS'] = 'green'
                self.light_state['EW'] = 'red'
            self.timer = 0

    def is_green(self, direction):
        """
        Check if the light is green for a given direction.
        Args:
            direction (str): 'N', 'S', 'E', or 'W'.
        Returns:
            bool: True if green for that direction, False otherwise.
        """
        if direction in ('N', 'S'):
            return self.light_state['NS'] == 'green'
        elif direction in ('E', 'W'):
            return self.light_state['EW'] == 'green'
        return False

    def __repr__(self):
        """
        String representation for debugging and logging.
        Shows the intersection's position and both light states.
        """
        return (f"Intersection(pos={self.position}, "
                f"NS={self.light_state['NS']}, EW={self.light_state['EW']})")

# --- Road network and pathfinding scaffolding ---

class RoadNetwork:
    """
    Represents the road layout as a set of allowed positions (cells).
    Provides methods to check if a cell is a road and to get neighbors for pathfinding.
    """
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.road_cells = set()  # Set of (x, y) tuples
        # TODO: Initialize road_cells with your road layout (e.g., grid, plus, custom)

    def is_road(self, pos):
        """Return True if pos is a road cell."""
        return pos in self.road_cells

    def get_neighbors(self, pos):
        """Return list of adjacent road cells (for pathfinding)."""
        # TODO: Implement neighbor logic (N, S, E, W if those are roads)
        return []