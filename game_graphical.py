from connect_4 import Board
from Algorithms.minimax import minimax
import pygame

pygame.init()

# Board Sizes
SQUARE = 100
CIRCLE_R = 40
COLS, ROWS = 7, 6
WIDTH = SQUARE * COLS
HEIGHT = SQUARE * (ROWS + 2)

# Colours
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,165,0)
GREEN = (0,255,0)        

def game_over_check(board):
    return board.is_full() or board.winner() != 0

def draw_header(surface, font):
    pygame.draw.rect(surface, BLACK, (0, 0, SQUARE * COLS, SQUARE))
    for c in range(COLS):
        create_textbox(surface, f"Col. {c + 1}", font, c * SQUARE, 0, BLACK, WHITE, SQUARE, SQUARE, 2)

def create_textbox(surface, text, font, x_corner, y_corner, text_colour, bg_colour, width, height, border):
    new_rect = pygame.Rect(x_corner + border, y_corner + border, (width - border * 2), (height - border * 2))
    pygame.draw.rect(surface, bg_colour, new_rect)
    line_height = font.get_linesize()
    lines = text.split('\n')
    num_lines = text.count('\n')
    y = y_corner + (height - num_lines * line_height) / 2
    for line in lines:
        text_surface = font.render(line, True, text_colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x_corner + width / 2, y)
        surface.blit(text_surface, text_rect)
        y += line_height

    return new_rect

def board_init(surface, font):
    surface.fill(BLACK)
    draw_header(surface, font)
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(surface, BLUE, (c * SQUARE, (r + 1) * SQUARE, SQUARE, SQUARE))
            pygame.draw.circle(surface, WHITE, ((c + 0.5) * SQUARE, (r + 1.5) * SQUARE), CIRCLE_R)
    
    # Build AI, Undo, Quit buttons
    undo_button = create_textbox(surface, "UNDO", font, SQUARE, (ROWS + 1) * SQUARE, BLACK, ORANGE, SQUARE, SQUARE, 2)
    ai_button = create_textbox(surface, "Minimax\nAI", font, SQUARE * 2, (ROWS + 1) * SQUARE, BLACK, GREEN, SQUARE, SQUARE, 2)
    quit_button = create_textbox(surface, "QUIT", font, (COLS - 1) * SQUARE, (ROWS + 1) * SQUARE, BLACK, RED, SQUARE, SQUARE, 2)

    # Player Turn Indicator
    create_textbox(surface, "Player\nTurn", font, 0, (ROWS + 1) * SQUARE, BLACK, RED, SQUARE, SQUARE, 2)

    pygame.display.update()
    
    return undo_button, ai_button, quit_button

def draw_board(surface, board, font, game_active):
    for c in range(COLS):
        for r in range(ROWS):
            if board.grid[r][c] == 1:
                cur_colour = RED
            elif board.grid[r][c] == 2:
                cur_colour = YELLOW
            else:
                cur_colour = WHITE
            pygame.draw.circle(surface, cur_colour, ((c + 0.5) * SQUARE, (r + 1.5) * SQUARE), CIRCLE_R)
    # Player Turn Indicator
    if game_active:
        if board.player_turn() == 1:
            create_textbox(surface, "Player\nTurn", font, 0, (ROWS + 1) * SQUARE, BLACK, RED, SQUARE, SQUARE, 2)
        else:
            create_textbox(surface, "Player\nTurn", font, 0, (ROWS + 1) * SQUARE, BLACK, YELLOW, SQUARE, SQUARE, 2)
    pygame.display.update()

def main():
    print("Game Start!")
    clock = pygame.time.Clock()
    
    board = Board()
    
    font = pygame.font.SysFont("Arial", 24)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")
    undo_button, ai_button, quit_button = board_init(screen, font)

    game_active = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    return
                elif undo_button.collidepoint(event.pos) and board.history:
                    board.undo()
                    if not game_active:
                        draw_header(screen, font)
                    game_active = True
                elif ai_button.collidepoint(event.pos) and game_active and not game_over_check(board):
                    create_textbox(screen, "AI is thinking...", font, 3 * SQUARE, (ROWS + 1) * SQUARE, WHITE, BLACK, SQUARE * 2, SQUARE, 2)
                    pygame.display.update()
                    print("AI is thinking...")
                    ai_player = board.player_turn()
                    
                    # The algorithm now returns the stats dictionary directly on the root call
                    col, minimax_score, stats = minimax(board, 5, True, ai_player) 
                    
                    print(f"AI plays column {col + 1} (Score: {minimax_score})")
                    print(f"Runtime: {stats['time_seconds']:.4f}s | Nodes: {stats['nodes_evaluated']:,} | Speed: {stats['nodes_per_second']:,.0f} n/s")
                    board.place_piece(col)
                    create_textbox(screen, "", font, 3 * SQUARE, (ROWS + 1) * SQUARE, WHITE, BLACK, SQUARE * 2, SQUARE, 2)
                    pygame.display.update()
                    pygame.event.clear()
                elif event.pos[1] < SQUARE and game_active and not game_over_check(board):
                    place_col = event.pos[0] // SQUARE
                    if place_col in board.legal_moves():
                        board.place_piece(place_col)
                        
        draw_board(screen, board, font, game_active)
        
        if game_over_check(board) and game_active:
            winner = board.winner()
            if winner != 0: 
                ending_colour = (RED if winner == 1 else YELLOW)
                ending_text = f"Player {winner} wins!"
            else:
                ending_colour = ORANGE
                ending_text = "Game tied!"
            print(ending_text)
            create_textbox(screen, ending_text, font, 0, 0, BLACK, ending_colour, SQUARE * COLS, SQUARE, 2)
            create_textbox(screen, "Game\nOver", font, 0, (ROWS + 1) * SQUARE, BLACK, WHITE, SQUARE, SQUARE, 2)
            pygame.display.update()
            game_active = False
        clock.tick(30)
    
if __name__ == "__main__":
    main()