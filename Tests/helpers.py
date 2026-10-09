def play_moves(board, moves):
    '''Set up a test board using legal moves without continuing after a win.'''
    for col in moves:
        assert not board.check_win(), "Test setup continues after a win."
        assert col in board.legal_moves(), "Test setup uses an illegal move."
        board.place_piece(col)


def search(algorithm, board, depth, is_maximizing, ai_player):
    '''Run a search algorithm and check that it leaves the board unchanged.'''
    grid = [row[:] for row in board.grid]
    heights = board.heights[:]
    history = board.history[:]

    result = algorithm(board, depth, is_maximizing, ai_player)

    assert board.grid == grid, "Search changed the board grid."
    assert board.heights == heights, "Search changed the column heights."
    assert board.history == history, "Search changed the move history."
    return result
