from connect_4 import Board, get_input, print_board
from Algorithms.minimax import minimax

# Main game loop
def main():
    board = Board()
    while True:
        print_board(board)
        
        player_input = get_input(board)
        
        if player_input == 'q':
            print(f"Exiting game")
            return

        if player_input == 'u':
            board.undo()
            continue
        
        if player_input == 'm':
            print("AI is thinking...")
            ai_player = board.player_turn()
            
            # Call the imported function
            col, minimax_score = minimax(board, 4, True, ai_player) 
            
            print(f"AI plays column {col + 1} (Score: {minimax_score})")
            board.place_piece(col)
        else:
            # Original manual piece placement
            board.place_piece(player_input)
            
        if board.is_full() or board.winner() != 0:
            print_board(board)
            winner = board.winner()
            if winner != 0: 
                print(f"Player {winner} wins!")
            else:
                print("Game tied!")
            return

if __name__ == "__main__":
    main()