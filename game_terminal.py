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
            
            # The algorithm now returns the stats dictionary directly on the root call
            col, minimax_score, stats = minimax(board, 5, True, ai_player) 
            
            print(f"AI plays column {col + 1} (Score: {minimax_score})")
            print(f"Runtime: {stats['time_seconds']:.4f}s | Nodes: {stats['nodes_evaluated']:,} | Speed: {stats['nodes_per_second']:,.0f} n/s")
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