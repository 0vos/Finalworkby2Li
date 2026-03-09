# 2025 Algorithm Course Design
## Task Description
### 1. Generating a Maze using Divide and Conquer
Initially empty, using the cross wall-building method to divide areas, and digging doors on the walls.
![sample_maze.png](readme_images%2Fsample_maze.png)
### 2. Resource Collection Path Planning using Dynamic Programming (As the Gold Standard for Real-time Strategy)
Uses a queue to record the position and the current resource collection at that position. Each time, taking the head of the queue to move in four directions. If more resources can be obtained, it updates, and adds the positions affected by the update to the tail of the queue.
### 3. Designing Real-time Resource Pick-up Strategy using Greedy Algorithm
In a 3x3 field of view, calculates a "value score" for each position, score = val_score - penalty: final score. Selects the position with the highest score in the current field of view, prioritizing unvisited G positions, avoiding repeated visits to the same position (penalty mechanism) and negative value areas like traps. When the exit E appears in the field of view, it immediately interrupts resource collection and uses the BFS algorithm to find the shortest path to the exit.

![greedy.gif](readme_images%2Fgreedy.gif)
### 4. Solving the Puzzle Level using Backtracking
Initializes the password as an empty list, iterates through each digit, and adds it to the empty list. When the list length reaches 3, it determines whether it completely meets the conditions of the clues. If so, it checks if the hash value of this password string is the same as the given hash value.
![lock.gif](readme_images%2Flock.gif)
### 5. Boss Battle Strategy Optimization using Branch and Bound
With the help of the A* algorithm, using a priority queue to explore different states, finding the minimum number of rounds required to defeat all BOSSes. During the exploration process, using the average damage value to estimate the remaining rounds, while recording the visited states to avoid repeated calculations, and pruning the states that do not meet the requirements.

![boss.gif](readme_images%2Fboss.gif)

## Quick Start
```sh
pip install -r requirements.txt
python show.py
```
## File Description
- test_and_manual/: Stores the test files distributed by the school and the course design task requirements
- img/: Textures used in the game
- music/: Music used in the game
