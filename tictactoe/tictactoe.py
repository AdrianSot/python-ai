"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    moves = 0
    for row in board:
        for cell in row:
            if cell is not None:
                moves += 1
    return X if moves % 2 == 0 else O    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_actions = set()
    for i,row in enumerate(board):
        for j,cell in enumerate(row):
            if cell is None:
                set_actions.add((i,j))
    return set_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if(action in actions(board)):
        newBoard = copy.deepcopy(board)
        newBoard[action[0]][action[1]] = player(board)
        return newBoard
    raise ValueError()


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None
    if board[0][0] == board[0][1] == board[0][2] is not None:
        winner = board[0][0]
    elif board[1][0] == board[1][1] == board[1][2] is not None:
        winner = board[1][0]
    elif board[2][0] == board[2][1] == board[2][2] is not None:
        winner = board[2][0]
    elif board[0][0] == board[1][0] == board[2][0] is not None:
        winner = board[0][0]
    elif board[0][1] == board[1][1] == board[2][1] is not None:
        winner = board[0][1]
    elif board[0][2] == board[1][2] == board[2][2] is not None:
        winner = board[0][2]
    elif board[0][0] == board[1][1] == board[2][2] is not None:
        winner = board[0][0]
    elif board[2][0] == board[1][1] == board[0][2] is not None:
        winner = board[2][0]
    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """ 
    isTerminal = False
    if len(actions(board)) == 0 or winner(board) is not None:
         isTerminal = True
    return isTerminal

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    the_winner = winner(board)
    utility = 0
    if the_winner == X:
        utility = 1
    elif the_winner == O:
        utility = -1
    return utility 


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if board == initial_state():
        return (random.randint(0,2),random.randint(0,2))
    if player(board) == X:
        _, move = maximize(board)
    else:
        _, move = minimize(board)
    return move    

def maximize(board):
    if terminal(board):
        return utility(board), None
    move = {}
    v = -2
    for action in actions(board):
        u, _ = minimize(result(board,action)) 
        if u > v:
            v = u
            move = action
    return v, move

def minimize(board):
    if terminal(board):
        return utility(board), None
    move = {}
    v = 2
    for action in actions(board):
        u, _ = maximize(result(board,action)) 
        if u < v:
            v = u
            move = action
    return v, move
