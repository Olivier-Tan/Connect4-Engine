
import os
import pygame

from connect_4 import Board
import game_graphical as gui

# Allow Pygame to run without opening a real window
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.init()
pygame.display.set_mode((gui.WIDTH, gui.HEIGHT))

surface = pygame.Surface((gui.WIDTH, gui.HEIGHT))
font = pygame.font.SysFont("Arial", 24)

def test_initial_board_rendering(board):
    """Initialises a board and verifies it all spaces are white."""
    gui.board_init(surface, font)
    gui.draw_board(surface, board, font, True)

    # Check that all board positions are initially empty (white)
    for col in range(gui.COLS):
        for row in range(gui.ROWS):
            centre = (
                int((col + 0.5) * gui.SQUARE),
                int((row + 1.5) * gui.SQUARE)
            )

            assert surface.get_at(centre)[:3] == gui.WHITE, f"Expected colour of {centre} to be WHITE, got {surface.get_at(centre)[:3]}"

def test_player_one_piece_rendering(board):
    """Places the first piece and verifies the location it is placed is RED"""
    board.place_piece(0)

    gui.board_init(surface, font)
    gui.draw_board(surface, board, font, True)

    # Check that Player 1's piece is rendered red
    centre = (gui.SQUARE // 2, gui.SQUARE * 6 + gui.SQUARE // 2)

    assert surface.get_at(centre)[:3] == gui.RED, f"Expected colour of {centre} to be RED, got {surface.get_at(centre)[:3]}"

def test_player_two_piece_rendering(board):
    """Places the second piece and verifies the location it is placed is YELLOW"""
    board.place_piece(0)
    board.place_piece(1)

    gui.board_init(surface, font)
    gui.draw_board(surface, board, font, True)

    # Check that Player 2's piece is rendered yellow
    centre = (gui.SQUARE + gui.SQUARE // 2, gui.SQUARE * 6 + gui.SQUARE // 2)

    assert surface.get_at(centre)[:3] == gui.YELLOW, f"Expected colour of {centre} to be YELLOW, got {surface.get_at(centre)[:3]}"

def test_button_positions(board):
    """Initialises the board and verifies the size and location of the undo, ai and quit buttons"""
    undo, ai, quit_button = gui.board_init(surface, font)

    # Check button dimensions
    assert undo.width == gui.SQUARE - gui.BORDER * 2, f"Expected width of UNDO to be 96, got {undo.width}"
    assert undo.height == gui.SQUARE - gui.BORDER * 2, f"Expected height of UNDO to be 96, got {undo.height}"

    assert ai.width == gui.SQUARE - gui.BORDER * 2, f"Expected width of AI to be 96, got {ai.width}"
    assert ai.height == gui.SQUARE - gui.BORDER * 2, f"Expected height of AI to be 96, got {ai.height}"

    assert quit_button.width == gui.SQUARE - gui.BORDER * 2, f"Expected width of QUIT to be 96, got {quit.width}"
    assert quit_button.height == gui.SQUARE - gui.BORDER * 2, f"Expected height of QUIT to be 96, got {quit.height}"

    # Check button positions
    assert undo.topleft == (gui.SQUARE + 2, (gui.ROWS + 1) * gui.SQUARE + 2), "UNDO not found in expected location"
    assert ai.topleft == (gui.SQUARE * 2 + 2, (gui.ROWS + 1) * gui.SQUARE + 2), "AI not found in expected location"
    assert quit_button.topleft == ((gui.COLS - 1) * gui.SQUARE + 2, (gui.ROWS + 1) * gui.SQUARE + 2), "QUIT not found in expected location"

def test_button_click_detection(board):
    """Initialises the board and verifies the hitbox of the buttons are correct"""
    undo, ai, quit_button = gui.board_init(surface, font)

    # Check that the button rectangles align their own positions
    assert undo.collidepoint(undo.center), "UNDO button not aligned with its centre"
    assert ai.collidepoint(ai.center), "AI button not aligned with its centre"
    assert quit_button.collidepoint(quit_button.center), "QUIT button not aligned with its centre"

    # Check that buttons do not overlap the outside its rectangle
    assert not undo.collidepoint((50, 50)), "UNDO button detected outside its rectangle"
    assert not ai.collidepoint((50, 50)), "AI button detected outside its rectangle"
    assert not quit_button.collidepoint((50, 50)), "QUIT button detected outside its rectangle"

def test_game_not_over_initially(board):
    """Initialises the board and verifies the game is not immediately over"""
    assert gui.game_over_check(board) is False, "Game incorrectly flagged as over on initialisation"

def test_game_not_over_after_valid_move(board):
    """Plays a non-winning move and verifies the game is still continuing"""
    board.place_piece(0)

    assert gui.game_over_check(board) is False, "Game incorrectly flagged as over on initialisation"

def test_draw_board_reflects_undo(board):
    """Plays a move and verifies the undo button correctly removes that piece"""
    board.place_piece(0)

    gui.board_init(surface, font)
    gui.draw_board(surface, board, font, True)

    # Confirm piece is initially displayed
    assert surface.get_at((gui.SQUARE // 2, gui.SQUARE * 6 + gui.SQUARE // 2))[:3] == gui.RED, f"Expected colour of placed piece to be RED, got {surface.get_at((50, 150))[:3]}"

    board.undo()

    gui.draw_board(surface, board, font, True)

    # Confirm piece disappears after undo
    assert surface.get_at((gui.SQUARE // 2, gui.SQUARE * 6 + gui.SQUARE // 2))[:3] == gui.WHITE, f"Expected colour of placed piece to be WHITE, got {surface.get_at((50, 150))[:3]}"
    
def test_winner_correctly_identified(board):
    """Plays a winning move and verifies the correct winner is announced"""
    moves = [4, 5, 4, 5, 4, 5, 4]
    for move in moves:
        board.place_piece(move)

    gui.board_init(surface, font)
    gui.draw_board(surface, board, font, True)

    # Confirm top banner is RED
    assert surface.get_at((gui.SQUARE // 2, gui.SQUARE // 2))[:3] == gui.RED, f"Expected colour of placed piece to be RED, got {surface.get_at((50, 150))[:3]}"

    board.undo()
    board.place_piece(6)
    board.place_piece(5)
    
    gui.draw_board(surface, board, font, True)
    
    # Confirm top banner is YELLOW
    assert surface.get_at((gui.SQUARE // 2, gui.SQUARE // 2))[:3] == gui.YELLOW, f"Expected colour of placed piece to be YELLOW, got {surface.get_at((50, 150))[:3]}"

    pygame.quit()