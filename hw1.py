import time
import numpy as np
from gridgame import *

##############################################################################################################################

# You can visualize what your code is doing by setting the GUI argument in the following line to true.
# The render_delay_sec argument allows you to slow down the animation, to be able to see each step more clearly.

# For your final submission, please set the GUI option to False.

# The gs argument controls the grid size. You should experiment with various sizes to ensure your code generalizes.
# Please do not modify or remove lines 18 and 19.

##############################################################################################################################

game = ShapePlacementGrid(GUI=True, render_delay_sec=0.5, gs=6, num_colored_boxes=5)
shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')
np.savetxt('initial_grid.txt', grid, fmt="%d")

##############################################################################################################################

# Initialization

# shapePos is the current position of the brush.

# currentShapeIndex is the index of the current brush type being placed (order specified in gridgame.py, and assignment instructions).

# currentColorIndex is the index of the current color being placed (order specified in gridgame.py, and assignment instructions).

# grid represents the current state of the board. 
    
    # -1 indicates an empty cell
    # 0 indicates a cell colored in the first color (indigo by default)
    # 1 indicates a cell colored in the second color (taupe by default)
    # 2 indicates a cell colored in the third color (veridian by default)
    # 3 indicates a cell colored in the fourth color (peach by default)

# placedShapes is a list of shapes that have currently been placed on the board.
    
    # Each shape is represented as a list containing three elements: a) the brush type (number between 0-8), 
    # b) the location of the shape (coordinates of top-left cell of the shape) and c) color of the shape (number between 0-3)

    # For instance [0, (0,0), 2] represents a shape spanning a single cell in the color 2=veridian, placed at the top left cell in the grid.

# done is a Boolean that represents whether coloring constraints are satisfied. Updated by the gridgames.py file.

##############################################################################################################################

shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')

print(shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done)


####################################################
# Timing your code's execution for the leaderboard.
####################################################

start = time.time()  # <- do not modify this.



##########################################
# Write all your code in the area below. 
##########################################



'''

YOUR CODE HERE


'''
class HC_Agent: 
    def __init__(self, game):
        #initializing with game instance
        self.game = game

    def evaluate_grid(self, grid, placedshapes):
        """
        Objective function to evaluate the current state of grid.
        Return a score based on:
        - Number of colored boxes (higher is better)
        - Number of violations (lower is better)
        - Number of shapes used (lower is better)
        """
        # Count filled cells
        filled_cells = np.sum(grid != -1)
        
        # Count adjacency violations
        violations = 0
        grid_size = len(grid)
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i, j] != -1:
                    color = grid[i, j]
                    # Check right neighbor
                    if j < grid_size - 1 and grid[i, j + 1] == color:
                        violations += 1
                    # Check down neighbor
                    if i < grid_size - 1 and grid[i + 1, j] == color:
                        violations += 1
        
        # Calculate score
        # Higher filled cells is better, fewer violations is better, fewer shapes is better
        num_shapes = len(placedshapes)
        
        # Score components (weighted)
        score = filled_cells * 100 - violations * 500 - num_shapes * 10
        
        return score

    def get_valid_placements(self, grid):
        """
        Get all valid placements for current state.
        Returns list of (shape_idx, x, y, color_idx) tuples.
        """
        valid_placements = []
        grid_size = len(grid)
        
        # Try all shapes
        for shape_idx in range(len(self.game.shapes)):
            shape = self.game.shapes[shape_idx]
            shape_height, shape_width = shape.shape
            
            # Try all positions
            for y in range(grid_size):
                for x in range(grid_size):
                    # Check if shape fits in bounds
                    if x + shape_width > grid_size or y + shape_height > grid_size:
                        continue
                    
                    # Check if we can place at this position
                    if self.game.canPlace(grid, shape, [x, y]):
                        # Try all colors
                        for color_idx in range(len(self.game.colors)):
                            valid_placements.append((shape_idx, x, y, color_idx))
        
        return valid_placements

    def simulate_placement(self, grid, shape_idx, x, y, color_idx):
        """
        Simulate placing a shape and return the new grid state.
        """
        new_grid = grid.copy()
        shape = self.game.shapes[shape_idx]
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    new_grid[y + i, x + j] = color_idx
        
        return new_grid

    def solve(self):
        """
        Hill climbing algorithm to solve the puzzle.
        """
        max_iterations = 1000
        
        for iteration in range(max_iterations):
            # Get current state
            shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = self.game.execute('export')
            
            # Check if done
            if done:
                print(f"Solution found in {iteration} iterations!")
                break
            
            # Get all valid placements
            valid_placements = self.get_valid_placements(grid)
            
            if not valid_placements:
                print("No valid placements available!")
                break
            
            # Evaluate all valid placements
            best_score = self.evaluate_grid(grid, placedShapes)
            best_placement = None
            
            for shape_idx, x, y, color_idx in valid_placements:
                # Simulate placement
                new_grid = self.simulate_placement(grid, shape_idx, x, y, color_idx)
                new_placed = placedShapes + [(shape_idx, [x, y], color_idx)]
                
                # Evaluate
                score = self.evaluate_grid(new_grid, new_placed)
                
                if score > best_score:
                    best_score = score
                    best_placement = (shape_idx, x, y, color_idx)
            
            # If we found an improvement, make the move
            if best_placement:
                shape_idx, x, y, color_idx = best_placement
                
                # Switch to the right shape
                while self.game.currentShapeIndex != shape_idx:
                    self.game.execute('switchshape')
                
                # Move to the right position
                current_pos = self.game.shapePos
                while current_pos[0] != x:
                    if current_pos[0] < x:
                        self.game.execute('right')
                    else:
                        self.game.execute('left')
                    current_pos = self.game.shapePos
                
                while current_pos[1] != y:
                    if current_pos[1] < y:
                        self.game.execute('down')
                    else:
                        self.game.execute('up')
                    current_pos = self.game.shapePos
                
                # Switch to the right color
                while self.game.currentColorIndex != color_idx:
                    self.game.execute('switchcolor')
                
                # Place the shape
                self.game.execute('place')
            else:
                print("No improvement found (local maximum reached)")
                break


# Create and run the agent
agent = HC_Agent(game)
agent.solve()

# Update final state
shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')




########################################

# Do not modify any of the code below. 

########################################

end=time.time()

np.savetxt('grid.txt', grid, fmt="%d")
with open("shapes.txt", "w") as outfile:
    outfile.write(str(placedShapes))
with open("time.txt", "w") as outfile:
    outfile.write(str(end-start))
