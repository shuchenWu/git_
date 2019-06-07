from random import choice

defeated_by = dict(paper='scissors',
                   rock='paper',
                   scissors='rock')
lose = '{} beats {}, you lose!'
win = '{} beats {}, you win!'
tie = 'tie!'


def _get_computer_move():
    """Randomly select a move"""
    return choice(['rock', 'paper', 'scissors'])


def _get_winner(computer_choice, player_choice):
    """Return above lose/win/tie strings populated with the
       appropriate values (computer vs player)"""
    if defeated_by[player_choice] == computer_choice:
        return lose.format(computer_choice, player_choice)
    elif player_choice == computer_choice:
        return tie
    else:
        return win.format(player_choice, computer_choice)

def game():
    """Game loop, receive player's choice via the generator's
       send method and get a random move from computer (_get_computer_move).
       Raise a StopIteration exception if user value received = 'q'.
       Check who wins with _get_winner and print its return output."""
    ch = 'Welcome to Rock Paper Scissors'
    ch = yield ch
    while True:
        if ch == 'q':
            raise StopIteration
        com_ch = _get_computer_move()
        ch = yield _get_winner(com_ch, ch)
