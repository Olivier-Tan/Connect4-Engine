import game_graphical
import game_terminal

def main():
    game_selection = None
    while game_selection != 't' and game_selection != 'g' and game_selection != 'q':
        game_selection = input((f"Choose to play Connect 4 on the Terminal (t) or with Graphics (g) or quit (q): "))
    if game_selection == 't':
        game_terminal.main()
    elif game_selection == 'g':
        game_graphical.main()
    else:
        return

if __name__ == "__main__":
    main()