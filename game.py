import numpy as np
import random
import math
import copy

playing = 1 #First player
RL_player = 1 #Person player
IA_player = 2 #IA player

# Main Board call
def create_board():
	''' Create a flipped ARRAY board'''
	board = np.zeros((6,7))
	return board
board = create_board()

# --- Basic functions ---
def next_player(player): #Prochain joueur =>
	''' Returns the next player'''
	return RL_player if player == IA_player else IA_player

def print_board(board): #Affiche le tableau
	''' Prints the board UNFLIPPED'''
	print(np.flip(board, 0))

def co(board, x,y): #Essayes ces coordonnées !
	''' Tries coordinates and return if existing'''
	try: return board[y][x]
	except: pass


# --- Advanced functions ---
def check_winner(board, player): #Y-a-t'il (déjà) un gagant ? 
	''' Check if there is a winner [+MINIMAX]'''
	for row in range(0,6):
		for column in range(0,7):
			if (co(board, column, row) == co(board, column+1, row) == co(board, column+2, row) == co(board, column+3, row) == player) or (co(board, column, row) == co(board, column, row+1) == co(board, column, row+2) == co(board, column, row+3) == player) or (co(board, column, row) == co(board, column+1, row+1) == co(board, column+2, row+2) == co(board, column+3, row+3) == player) or (co(board, column, row) == co(board, column+1, row-1) == co(board, column+2, row-2) == co(board, column+3, row-3) == player):
				return True
	return False

def drop_piece(board, x, player): #Envoyez une pièce svp!
	''' Drop a piece in a correct place'''
	if x in get_valid_locations(board):
		board[get_next_open_row(board, x)][x] = player
	else: raise Exception("Colonne pleine ou incorrecte")



# --- IA : MINIMAX & Alpha-Beta ---
def board_is_full(board): #Le tableau est-il plein ?
	''' Returns a bool saying if the board is full or not [MINIMAX]'''
	return True if len(get_valid_locations(board)) == 0 else False

def get_valid_locations(board): #Quelles colonnes sont-elles jouables ? [MINIMAX ONLY]
	''' Returns a list of playable columns (x) [MINIMAX]'''
	valid_locations = []
	for col in range(7):
		if board[5][col] == 0:
			valid_locations.append(col)
	return valid_locations

def get_next_open_row(board, col): #Quelle ligne vide est la plus basse sur une certaine colonne ? [MINIMAX ONLY]
	''' Return open row for (x) column [+MINIMAX]'''
	for r in range(7):
		if board[r][col] == 0:
			return r

def is_terminal_node(board): #Est-ce une feuille d'une branche du minimax ?
	''' Return the winning_move of player 1 || winning_move of player 2 || IS no playable columns True ? [MINIMAX]'''
	return winning_move(board, RL_player) or winning_move(board, IA_player) or len(get_valid_locations(board)) == 0

def winning_move(board, piece):
	# Check horizontal locations for win
	for col in range(7-3):
		for row in range(6):
			if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
				return True

	# Check vertical locations for win
	for col in range(7):
		for row in range(6-3):
			if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
				return True

	# Check positively sloped diaganols
	for col in range(7-3):
		for row in range(6-3):
			if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
				return True

	# Check negatively sloped diaganols
	for col in range(7-3):
		for row in range(3, 6):
			if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
				return True

def evaluate_window(window, player): #Combien de points vaux une fenetre (4x4) ?
	''' Gives a score to a 4 sized window from the board [MINIMAX]'''
	score = 0
	if player == IA_player:
		opponent_player = RL_player
	else: opponent_player = IA_player

	if window.count(player) == 4: score += 100
	elif window.count(player) == 3 and window.count(0) == 1: score += 5
	elif window.count(player) == 2 and window.count(0) == 2: score += 2

	if window.count(opponent_player) == 3 and window.count(0) == 1: score -= 4

	return score

def score_position(board, player): #Combien de points vaux le JEU entier (7*6) ?
	''' Gives a score to the CURRENT board [MINIMAX]'''
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, 7//2])] #PB
	center_count = center_array.count(player)
	score += center_count * 3

	## Score Horizontal
	for row in range(0,6):
		row_array = [int(i) for i in list(board[row,:])] #PB
		for col in range(0,7-3):
			window = row_array[col:col+4]
			score += evaluate_window(window, player)

	## Score Vertical
	for col in range(0,7):
		col_array = [int(i) for i in list(board[:,col])] #PB
		for row in range(0,6-3):
			window = col_array[row:row+4]
			score += evaluate_window(window, player)

	## Score posiive sloped diagonal
	for row in range(0,6-3):
		for col in range(0,7-3):
			window = [board[row+i][col+i] for i in range(4)]
			score += evaluate_window(window, player)

	for row in range(0,6-3):
		for col in range(0,7-3):
			window = [board[row+3-i][col+i] for i in range(4)]
			score += evaluate_window(window, player)

	return score

def minimax(board, depth, alpha, beta, maximizingPlayer): #Quel est le meilleur coup et combien de points vaut-il ?
	''' Minimax algorithm pruned with alpha-beta // returns the best move (column) for a certain depth and the score corresponding'''
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, 2):
				return (None, 100000000000000)
			elif winning_move(board, 1):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, 2))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			b_copy[row][col] = IA_player
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			b_copy[row][col] = RL_player
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value



def initialising():
	import Puissance4

# --- Playing functions ---
def player_play(board, x):
	import Puissance4
	global playing
	drop_piece(board, x, RL_player)
	if check_winner(board, RL_player):
		#print('Bravo ! Tu as gagné !')
		Puissance4.end_game('Won', 'Win')
		del Puissance4.liste_jettons[:]
		board = create_board()
		Puissance4.title_screen()
		running = False
	playing = IA_player

	#print_board(board)
	#print("Tour de l'IA.")

def ia_play(board, difficulty, alpha = -math.inf, beta = math.inf, maximizingPlayer = True):
	import Puissance4
	global playing
	col, minimax_score = minimax(board, difficulty, alpha, beta, maximizingPlayer)
	if col in get_valid_locations(board):
		Puissance4.afficher_jetton(Puissance4.IA[2], 580+(col*109), col)
		drop_piece(board, col, IA_player)
		if check_winner(board, IA_player):
			#print('Domage ! Tu as perdu.')
			Puissance4.end_game('Lost', 'Lost')
			del Puissance4.liste_jettons[:]
			board = create_board()
			Puissance4.title_screen()
			running = False
	  #print_board(board)
	  #print("Tour du Joueur 1.")
	playing = RL_player
