#🧩 State Space Search: Hua Rong Dao Sliding Puzzle Solver
University project that solves Hua-Rong-Dao Puzzle using State Space Searching.

## 📖 Introduction
This project involves implementing a solver for a variant of the Hua Rong Dao (or Klotski) tile sliding puzzle. Learn more about the traditional puzzle [here](http://chinesepuzzles.org/huarong-pass-sliding-block-puzzle/).

### 🔍 Key Differences in Our Variant:
- Board dimensions: 4 spaces wide, unlimited height.
- Piece types:
  - 🟥 2x2 pieces
  - 🟧 1x2 pieces (horizontal/vertical)
  - 🟨 1x1 pieces
- Fully specified goal state, unlike traditional Hua Rong Dao puzzles.

The objective is to reach the specified goal configuration by sliding pieces while adhering to movement rules.

---

## 💼 Features

### 🎯 Your Tasks:
1. Implement **DFS (Depth-First Search)** and **A* Search** to solve the puzzle.
2. Validate solutions for both algorithms, ensuring:
   - DFS solutions are valid.
   - A* solutions are optimal.

### 📋 Input & Output:
- **Input:** Plain text files describing initial and goal states.
- **Output:** Sequence of moves to transform the initial state into the goal state.

### Input:
Two states (initial and goal) separated by a blank line.
Characters:
.: Empty space
1: 2x2 piece
2: 1x1 piece
<, >: Left/right of a horizontal 1x2 piece
^, v: Top/bottom of a vertical 1x2 piece
Example Input File:
^^^^
vvvv
22..
11<>
1122

....
....
....
^^^^
....
### Output:
If no solution exists, output:
No solution
If a solution exists, output the sequence of states, each separated by a blank line.

### 🛠️ Heuristic Function:
- **Manhattan Distance**: Calculate the sum of horizontal and vertical distances between pieces' current and goal positions.


## 🚀 How to Run

### Prerequisites
- **Python 3**: Ensure your system has Python 3 installed.

### Commands
To solve a puzzle:
```bash
python3 hrd.py --algo astar --inputfile input.txt --outputfile output_astar.txt
python3 hrd.py --algo dfs --inputfile input.txt --outputfile output_dfs.txt


