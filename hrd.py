import argparse
import heapq

char_single = '2'

class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_2_by_2, is_single, coord_x, coord_y, orientation):
        """
        :param is_2_by_2: True if the piece is a 2x2 piece and False otherwise.
        :type is_2_by_2: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v')
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_2_by_2 = is_2_by_2
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def set_coords(self, coord_x, coord_y):
        """
        Move the piece to the new coordinates.

        :param coord: The new coordinates after moving.
        :type coord: int
        """

        self.coord_x = coord_x
        self.coord_y = coord_y

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_2_by_2, self.is_single, \
                                       self.coord_x, self.coord_y, self.orientation)


class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, height, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = height
        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()

    # customized eq for object comparison.
    def __eq__(self, other):
        if isinstance(other, Board):
            return self.grid == other.grid
        return False

    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.
        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_2_by_2:
                self.grid[piece.coord_y][piece.coord_x] = '1'
                self.grid[piece.coord_y][piece.coord_x + 1] = '1'
                self.grid[piece.coord_y + 1][piece.coord_x] = '1'
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = '1'
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def display(self):
        """
        Print out the current board.
        """
        for line in self.grid:
            for ch in line:
                print(ch, end='')
            print()


class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces.
    State has a Board and some extra information that is relevant to the search:
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, hfn, f, depth, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param hfn: The heuristic function.
        :type hfn: Optional[Heuristic]
        :param f: The f value of current state.
        :type f: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.hfn = hfn
        self.f = f
        self.depth = depth
        self.parent = parent

    def __lt__(self, other):
        """
        Comparison function to allow sorting by f-value (used for A* priority queue).
        """
        return self.f < other.f


def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    final_pieces = []
    final = False
    found_2by2 = False
    finalfound_2by2 = False
    height_ = 0

    for line in puzzle_file:
        height_ += 1
        if line == '\n':
            if not final:
                height_ = 0
                final = True
                line_index = 0
            continue
        if not final:  # initial board
            for x, ch in enumerate(line):
                if ch == '^':  # found vertical piece
                    pieces.append(Piece(False, False, x, line_index, 'v'))
                elif ch == '<':  # found horizontal piece
                    pieces.append(Piece(False, False, x, line_index, 'h'))
                elif ch == char_single:
                    pieces.append(Piece(False, True, x, line_index, None))
                elif ch == '1':
                    if found_2by2 == False:
                        pieces.append(Piece(True, False, x, line_index, None))
                        found_2by2 = True
        else:  # goal board
            for x, ch in enumerate(line):
                if ch == '^':  # found vertical piece
                    final_pieces.append(Piece(False, False, x, line_index, 'v'))
                elif ch == '<':  # found horizontal piece
                    final_pieces.append(Piece(False, False, x, line_index, 'h'))
                elif ch == char_single:
                    final_pieces.append(Piece(False, True, x, line_index, None))
                elif ch == '1':
                    if finalfound_2by2 == False:
                        final_pieces.append(Piece(True, False, x, line_index, None))
                        finalfound_2by2 = True
        line_index += 1

    puzzle_file.close()
    board = Board(height_, pieces)
    goal_board = Board(height_, final_pieces)
    return board, goal_board


def grid_to_string(grid):
    string = ""
    for i, line in enumerate(grid):
        for ch in line:
            string += ch
        string += "\n"
    return string


def is_goal_state(board, goalbd):
    """
    Check if the current board matches the goal state, equivalence function
    """
    return board == goalbd

def successor(state):
    """
    Return the possible moves for a given board state by generating new board
    states.This is essentially my successor function that will return all possible moves
    from a state. Main function for both searches
    """
    board = state.board
    all_mov = []
    emptys = find_empty(board)

    for piece in board.pieces:
        if piece.is_2_by_2:
            moves = check_2x2(piece, emptys, board)
        elif piece.is_single:
            moves = check_single(piece, emptys, board)
        else:
            moves = check_rectangular(piece, emptys, board)
        for nboard in moves:
            new_state = State(nboard, None, 0, state.depth + 1, state)
            all_mov.append(new_state)
    return all_mov

def mv_piece(board, piece, new_x, new_y):
    """
    Move a piece to a new position and return the new board with that piece moved.
    """
    npcs = [Piece(p.is_2_by_2, p.is_single, p.coord_x, p.coord_y, p.orientation) for p in board.pieces]
    nboard = Board(board.height, npcs)

    for p in nboard.pieces:
        if p.coord_x == piece.coord_x and p.coord_y == piece.coord_y:
            if p.is_2_by_2:
                # Idk it doesnt work without making the old piece to empty using "."
                nboard.grid[p.coord_y][p.coord_x] = '.'
                nboard.grid[p.coord_y][p.coord_x + 1] = '.'
                nboard.grid[p.coord_y + 1][p.coord_x] = '.'
                nboard.grid[p.coord_y + 1][p.coord_x + 1] = '.'
            else:
                nboard.grid[p.coord_y][p.coord_x] = '.'
            p.set_coords(new_x, new_y)
            break # Not sure but it doesnt work without this
    nboard = Board(nboard.height, nboard.pieces)
    return nboard
def find_empty(board):
    """
    Find all empty spaces on the board,  and get the coordinates for each "." pieces
    on the board, and return it as a set.
    """
    emptys = set()
    for y in range(board.height):
        for x in range(board.width):
            if board.grid[y][x] == '.':
                emptys.add((x, y))
    return emptys

def check_single(piece, emptys, board):
    """
    Check the possible moves for a 1x1 piece.
    """
    new_brds = []
    x, y = piece.coord_x, piece.coord_y
    if (x - 1, y) in emptys:
        nboard = mv_piece(board, piece, x - 1, y)
        new_brds.append(nboard)
    if (x + 1, y) in emptys:
        nboard = mv_piece(board, piece, x + 1, y)
        new_brds.append(nboard)
    if (x, y + 1) in emptys:
        nboard = mv_piece(board, piece, x, y + 1)
        new_brds.append(nboard)
    if (x, y - 1) in emptys:
        nboard = mv_piece(board, piece, x, y - 1)
        new_brds.append(nboard)

    return new_brds

def check_rectangular(piece, emptys, board):
    """
    Check the possible moves for a 1x2 (horizontal) or 2x1 (vertical) piece.
    """
    new_brds = []
    x, y = piece.coord_x, piece.coord_y

    # Horizontal Piece cheker
    if piece.orientation == 'h':
        if (x - 1, y) in emptys:
            nboard = mv_piece(board, piece, x - 1, y)
            new_brds.append(nboard)
        if (x + 2, y) in emptys:
            nboard = mv_piece(board, piece, x + 1, y)
            new_brds.append(nboard)
        if (x, y - 1) in emptys and (x + 1, y - 1) in emptys:
            nboard = mv_piece(board, piece, x, y - 1)
            new_brds.append(nboard)
        if (x, y + 1) in emptys and (x + 1, y + 1) in emptys:
            nboard = mv_piece(board, piece, x, y + 1)
            new_brds.append(nboard)

    # Vertical Piece checker
    elif piece.orientation == 'v':
        if (x - 1, y) in emptys and (x - 1, y + 1) in emptys:
            nboard = mv_piece(board, piece, x - 1, y)
            new_brds.append(nboard)
        if (x + 1, y) in emptys and (x + 1, y + 1) in emptys:
            nboard = mv_piece(board, piece, x + 1, y)
            new_brds.append(nboard)
        if (x, y - 1) in emptys:
            nboard = mv_piece(board, piece, x, y - 1)
            new_brds.append(nboard)
        if (x, y + 2) in emptys:
            nboard = mv_piece(board, piece, x, y + 1)
            new_brds.append(nboard)

    return new_brds

def check_2x2(piece, emptys, board):
    """
    Check the possible moves for a 1x1 piece. single piece can move any side:
    upwards, right, downwards, leftside.
    """
    new_brds = []
    x, y = piece.coord_x, piece.coord_y
    if (x - 1, y) in emptys and (x - 1, y + 1) in emptys:
        nboard = mv_piece(board, piece, x - 1, y)
        new_brds.append(nboard)
    if (x + 2, y) in emptys and (x + 2, y + 1) in emptys:
        nboard = mv_piece(board, piece, x + 1, y)
        new_brds.append(nboard)
    if (x, y + 2) in emptys and (x + 1, y + 2) in emptys:
        nboard = mv_piece(board, piece, x, y + 1)
        new_brds.append(nboard)
    if (x, y - 1) in emptys and (x + 1, y - 1) in emptys:
        nboard = mv_piece(board, piece, x, y - 1)
        new_brds.append(nboard)
    return new_brds

def dfs_search(initbd, goalbd):
    """
    Depth-first search algorithm to find the goal state using FIFO manner
    """
    instate = State(initbd, hfn=None, f=0, depth=0)
    fr = [instate]
    exp = set() # All previously explored board states, use this for pruning

    while fr: #Loopin thru frontier
        currs = fr.pop()
        currbd = grid_to_string(currs.board.grid)
        if currbd == grid_to_string(goalbd.grid):
            return currs
        if currbd not in exp:
            exp.add(currbd)
            for nexts in successor(currs):
                nextbd = grid_to_string(nexts.board.grid)
                if nextbd not in exp:
                    nexts.parent = currs
                    fr.append(nexts)
    return None

def heuristic(bd):
    """
    The heuristic function calculates manhattan distance of only the 2x2 piece

    * Did use ChatGPT to help come up with ideas for a heuristic
    """
    for pc in bd.pieces:
        if pc.is_2_by_2:
            finpc = next(p for p in goal_board.pieces if p.is_2_by_2)
            return abs(pc.coord_x - finpc.coord_x) + abs(pc.coord_y - finpc.coord_y)
    return 0

def astar_search(initbd, goalbd):
    """
    A* search algorithm to find the goal state that uses mangattan distance as heuristic
    and reconstruct only the path to the goal.
    """
    instate = State(initbd, hfn=None, f=0, depth=0)
    fr = [] # Frontier to beused
    # The heapq is used to allow minnimum states to be present at the top
    heapq.heappush(fr, (instate.f, instate))
    exp = {}  # Dict to store the lowest f value for each board state, to be used while pruning
    while fr: #While it is nnot empty, and it goes through all req. states
        s, currs = heapq.heappop(fr)
        currbd = grid_to_string(currs.board.grid)
        if currbd == grid_to_string(goalbd.grid):
            return currs
        if currbd not in exp or currs.f < exp[currbd]:
            exp[currbd] = currs.f
            for nexts in successor(currs):
                nextbd = grid_to_string(nexts.board.grid)
                nexts.parent = currs
                nexts.depth = currs.depth + 1
                nexts.f = nexts.depth + heuristic(nexts.board)
                if nextbd not in exp or nexts.f < exp.get(nextbd, float('inf')):
                    heapq.heappush(fr, (nexts.f, nexts))
    return None


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()

    # read the board from the file
    board, goal_board = read_from_file(args.inputfile)

    if args.algo == 'astar':
        solution = astar_search(board, goal_board)
    elif args.algo == 'dfs':
        solution = dfs_search(board, goal_board)

    solution_path = []
    if solution:
        while solution:
            solution_path.append(solution.board)
            solution = solution.parent
        solution_path.reverse()

    # write the solution to the output file
    with open(args.outputfile, 'w') as output_file:
        if solution_path:
            for step in solution_path:
                output_file.write(grid_to_string(step.grid))
                output_file.write("\n")
        else:
            output_file.write("No solution")
            output_file.write("\n")
