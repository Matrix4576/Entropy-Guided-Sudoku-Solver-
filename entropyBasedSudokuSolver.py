import math
import random

BOARD = [
    [4, 7, 1, 0, 0, 3, 6, 2, 0],
    [5, 0, 0, 4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 1, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 9, 3],
    [0, 0, 3, 0, 0, 0, 5, 0, 0],
    [6, 5, 0, 0, 0, 0, 0, 7, 0],
    [0, 0, 0, 3, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 6, 0, 0, 7],
    [0, 4, 9, 8, 0, 0, 1, 6, 5]
]

BOARD_ROWS = 9
BOARD_COLOUMS = 9
DIGITS = {1, 2, 3, 4, 5, 6, 7, 8, 9}
def candidates(board, rows, col):
    candidates = {}
    for i in range(rows):
        for j in range(col):
            if board[i][j] == 0:
                candidates[(i, j)] = DIGITS.copy()
            else:
                candidates[(i, j)] = {board[i][j]}
    return candidates
def constraints(board, rows, col, candidates):
    for i in range(rows):
        for j in range(col):
            if board[i][j] != 0:
                val = board[i][j]
                for x in range(rows):
                    if (i, x) in candidates and (i, x) != (i, j):
                        candidates[(i, x)].discard(val)
                for y in range(col):
                    if (y, j) in candidates and (y, j) != (i, j):
                        candidates[(y, j)].discard(val)
                brow = (i // 3) * 3
                bcol = (j // 3) * 3
                for r in range(brow, brow + 3):
                    for c in range(bcol, bcol + 3):
                        if (r, c) in candidates and (r, c) != (i, j):
                            candidates[(r, c)].discard(val)    
    return candidates
def unsolved(candidates):
    d = {}
    for pos, cand in candidates.items():
        if len(cand) > 1:
            d[pos] = cand
    return d
def minEntropy(candidates):
    freq = {}
    for k, v in candidates.items():
        for x in v:
            if x not in freq:
                freq[x] = 1
            else:
                freq[x] += 1
    weights = {}
    for k, v in candidates.items():
        entropy = 0
        for x in v:
            p = 1 / freq[x]
            entropy += -p * math.log2(p)
        weights[k] = entropy
    return weights
def update(board, cell, value):
    r, c = cell
    board[r][c] = value
def backtrack(board, cand):
    changed = True
    while changed:
        changed = False
        for cell, opts in list(cand.items()):
            r, c = cell
            if board[r][c] == 0 and len(opts) == 1:
                val = list(opts)[0]
                update(board, cell, val)
                cand = constraints(board, BOARD_ROWS, BOARD_COLOUMS, candidates(board, BOARD_ROWS, BOARD_COLOUMS))
                changed = True
    unsolve = unsolved(cand)
    if not unsolve:
        return board
    candidate = []
    for v in unsolve.values():
        for x in v:
            candidate.append(x)
    freq = {}
    for i in range(len(candidate)):
        if candidate[i] not in freq:
            freq[candidate[i]] = 1
        else:
            freq[candidate[i]] += 1
    entropy = minEntropy(unsolve)
    minEnt = float('inf')
    for k, v in entropy.items():
        if v < minEnt:
            minEnt = v
            bestCell = k
    r, c = bestCell
    choice = list(cand[bestCell])
    random.shuffle(choice)
    for x in choice:
        nb = []
        for i in board:
            nb.append(i)
        nb[r][c] = x
        nc = candidates(nb, BOARD_ROWS, BOARD_COLOUMS)
        nconst = constraints(nb, BOARD_ROWS, BOARD_COLOUMS, nc)
        if not all(len(opts) > 0 for opts in nconst.values()):
            continue
        result = backtrack(nb, nconst)
        if result:
            return result
    return None
def solve(board):
    initial = constraints(board, BOARD_ROWS, BOARD_COLOUMS, candidates(board, BOARD_ROWS, BOARD_COLOUMS))
    return backtrack(board, initial)
print("Input Board (NOTE THE 0 ARE EMPTY CELLS): \n")
for i in range(len(BOARD)):
    print(*BOARD[i])
solution = solve(BOARD)
if solution == None:
    print("No Solutions exist for this board")
else:
    print("\nSolution: \n")
    for i in range(len(solution)):
        print(*solution[i])