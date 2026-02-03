# Hill Climbing Agent

Brief implementation and usage notes for the Hill Climbing agent provided in this repository.

## Overview

This project contains an implementation of a Hill Climbing (HC) agent that places shapes and colors on a grid to satisfy local constraints and maximize an objective. The agent is implemented in `hw1.py` and uses the grid environment defined in `gridgame.py`.

## Files

- `hw1.py`: Main script containing a `HC_Agent` class implementing the hill climbing algorithm and a runnable script that interacts with the `ShapePlacementGrid` environment.
- `gridgame.py`: Grid environment and helper functions used by the agent (provided with the assignment).
- `.gitignore`: Excludes generated files such as `hw1_submission.zip`, `hw1.pdf`, Jupyter checkpoints, and `.DS_Store`.

## Implementation details

- State: represented by a 2D `grid` array where `-1` means empty and non-negative integers represent color indices.
- Moves: placements of available shapes at valid grid positions and colors. The agent enumerates valid placements for the current state and simulates each placement.
- Objective: a weighted score combining number of filled cells, adjacency violations (penalized), and number of shapes used. The agent evaluates simulated states and accepts placements that improve the score.
- Search: greedy hill climbing — at each iteration the agent selects the single placement that yields the best score improvement. If no improving placement exists, the algorithm stops (local maximum).

## Parameters and tuning

- `max_iterations`: a limit on iterations to avoid infinite loops (set in `hw1.py`).
- Score weights: adjust weights in `evaluate_grid()` inside `HC_Agent` to favor different objectives (filling vs. violations vs. shape count).
- Restarts / randomization: the current implementation is deterministic; adding random restarts or simulated annealing can help escape local maxima.

## Running

To run the agent (visual GUI or headless):

```bash
cd /Users/anand/Desktop/NEU/FAI/hw1
python hw1.py
```

Edit the `ShapePlacementGrid(GUI=..., render_delay_sec=..., gs=...)` call in `hw1.py` to change visualization, speed, and grid size. For final submissions, set `GUI=False`.

## Dependencies

- Python 3.8+ recommended
- `numpy`

Install requirements:

```bash
pip install numpy
```

## Notes

- `.DS_Store` has been added to `.gitignore`. If it was previously pushed, it is removed from tracking in a later commit.
- For further experiments, consider adding command-line flags to `hw1.py` to control parameters such as grid size, GUI mode, and search options.

---

If you'd like, I can add a short example run script or convert parameters to command-line flags next.

