def test_column_overflow_handling(board):
    """Fills a single column completely and verifies it is removed from legal moves."""
    col = 0
    for _ in range(6):
        board.place_piece(col)
        
    assert col not in board.legal_moves(), "Full column is still listed in legal_moves()."
    assert board.grid[0][col] == 2, f"Expected top slot to be Player 2, got {board.grid[0][col]}"

def test_undo_mechanic(board):
    """Places a piece, undoes it, and verifies board state reverts completely."""
    board.place_piece(3) # Player 1
    board.place_piece(4) # Player 2
    
    board.undo() # Undo Player 2
    
    assert board.player_turn() == 2, f"Expected it to be Player 2's turn, got Player {board.player_turn()}"
    assert board.heights[4] == 0, f"Expected column 4 height to be 0, got {board.heights[4]}"
    assert board.grid[5][4] == 0, f"Expected grid slot to be empty (0), got {board.grid[5][4]}"

def test_horizontal_win_bottom_edge(board):
    """Checks a win condition right on the bottom boundary of the board."""
    moves = [0, 6, 1, 6, 2, 6, 3] # P1 plays 0,1,2,3. P2 plays 6.
    for move in moves:
        board.place_piece(move)
        
    assert board.check_win() == True, "Board failed to detect horizontal win."
    assert board.winner() == 1, f"Expected winner to be 1, got {board.winner()}"

def test_vertical_win_top_edge(board):
    """Checks a win condition that reaches the very top row."""
    moves = [0, 1, 0, 1, 0, 1, 0] # P1 plays col 0. P2 plays col 1.
    for move in moves:
        board.place_piece(move)
        
    assert board.check_win() == True, "Board failed to detect vertical win."
    assert board.winner() == 1, f"Expected winner to be 1, got {board.winner()}"

def test_positive_diagonal_win(board):
    """Checks a diagonal win (bottom-left to top-right)."""
    moves = [0, 1, 1, 2, 2, 3, 2, 3, 3, 4, 3]
    for move in moves:
        board.place_piece(move)
        
    assert board.check_win() == True, "Board failed to detect positive diagonal win."
    assert board.winner() == 1, f"Expected winner to be 1, got {board.winner()}"

def test_negative_diagonal_win(board):
    """Checks a diagonal win (top-left to bottom-right)."""
    moves = [3, 2, 2, 1, 1, 0, 1, 0, 0, 6, 0]
    for move in moves:
        board.place_piece(move)
        
    assert board.check_win() == True, "Board failed to detect negative diagonal win."
    assert board.winner() == 1, f"Expected winner to be 1, got {board.winner()}"

def test_full_board_tie(board):
    """Simulates a completely full board with no winner (Tie)."""
    tie_moves = [
        0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0,
        2, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2,
        4, 5, 4, 5, 4, 5, 5, 4, 5, 4, 5, 4,
        6, 6, 6, 6, 6, 6
    ]
    for move in tie_moves:
        board.place_piece(move)
        
    assert board.is_full() == True, "Board is completely full but is_full() returned False."
    assert board.check_win() == False, "Board detected a win on a tied board."
    assert board.winner() == 0, f"Expected winner to be 0 (tie), got {board.winner()}"
