import game_graphical
import game_terminal

def main():
    game_selection = None
    while game_selection != 't' and game_selection != 'g':
        game_selection = input((f"Choose to play Connect 4 on the Terminal (t) or with Graphics (g): "))
    if game_selection == 't':
        game_terminal.main()
    else:
        game_graphical.main()

if __name__ == "__main__":
    main()