from connect_4 import COLS, ROWS

WIN_SCORE = 1_000_000


def evaluate_window(window, piece):
    """Scores a slice of 4 slots to help the AI gauge if a move is good."""
    score = 0
    opp_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # Block opponent's 3-in-a-row
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


def evaluate_board(board, piece):
    """Scans the whole board and tallies up the score for a specific player."""
    score = 0

    # Priority 1: Control the center column
    center_array = [int(board.grid[r][COLS // 2]) for r in range(ROWS)]
    score += center_array.count(piece) * 3

    # Score Horizontal
    for r in range(ROWS):
        row_array = board.grid[r]
        for c in range(COLS - 3):
            score += evaluate_window(row_array[c:c + 4], piece)

    # Score Vertical
    for c in range(COLS):
        col_array = [board.grid[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            score += evaluate_window(col_array[r:r + 4], piece)

    # Score Positive Diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board.grid[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score Negative Diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board.grid[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def evaluate_position(board, piece):
    winner = board.winner()
    if winner == piece:
        return WIN_SCORE
    if winner != 0:
        return -WIN_SCORE
    if board.is_full():
        return 0
    return evaluate_board(board, piece)
