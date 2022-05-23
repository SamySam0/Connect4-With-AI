import pygame, sys
from pygame.locals import *
from pygame import mixer
import soundfile as sf
mixer.init()
pygame.mixer.set_num_channels(5)
pygame.init()

# --- Window Settings ---
pygame.display.set_caption("Puissance 4 : Remastered") #Set app's name (left corner) to 'Project : Sonic'
WIN_SIZE = (1920, 1080)
win = pygame.display.set_mode(WIN_SIZE, pygame.FULLSCREEN) #Set display mode (resolution : 1280 x 720)
display = pygame.Surface((1920, 1080))

# --- FPS Settings ---
clock = pygame.time.Clock() #Variable Img Freq (FPS)
SPEED = 70 #FPS Variable

# --- Frames updating ---
def update(frame_speed):
	win.blit(display, (0, 0))
	pygame.display.update() # update display # maintain 'SPEED' (value) fps
	clock.tick(frame_speed)

# --- Volumes Settings ---
music_volume, sound_volume, effect_volume = True, True, False


# --- Intro player ---
sprite_intro = 1
def intro_player(max):
	''' Animated intro player (call) '''
	global sprite_intro
	if sprite_intro > max+0.5:
		sprite_intro = 1
	display_image_menu('video//Open_0' + str(int(sprite_intro)).zfill(2), 1, (-2,-4), '.jpg')
	sprite_intro += 0.2

def intro():
	global sprite_intro
	play_sound('Open')
	run = True
	while run:
		intro_player(77)
		if sprite_intro >= 76: run = False
		update(64)




# --- Menus functions ---

def play_music(music_sound, volume = 1, playtime = -1, extension = '.mp3'):
	''' Play a music ::: volume : 0 - 1, playtime: 1(one time), -1(loop) '''
	mixer.music.load("Musics - Sounds/" + music_sound + extension)
	if music_volume == False:
		mixer.music.set_volume(0)
	else : mixer.music.set_volume(volume)
	mixer.music.play(playtime)

def stop_music():
	''' Stop the current music '''
	mixer.music.stop()

def play_sound(sounds):
	''' Play a sound (sounds) '''
	pygame.mixer.init()
	freq = sf.SoundFile("Musics - Sounds\\" + sounds + '.wav')
	#lenght_int = float(format(len(freq) / freq.samplerate))
	sound_vfx = mixer.Sound("Musics - Sounds\\" + sounds + '.wav')
	if sound_volume == True:
		mixer.find_channel(True).play(sound_vfx) #CRASHES WHEN SPAMMING 
	#time.sleep(lenght_int)

def display_image_menu(image, rescale, position, extension = '.png', inside = 'Others'):
	''' Display an image on a choosen scale, choosen coordinates and custom extension from the main image file repertory '''
	image_to_display = pygame.image.load("Sprites//" + image + extension)
	return display.blit(image_to_display,position)

sprite_count = 1
def animated_background_title_screen(max):
	''' Animated background (call) '''
	global sprite_count
	if sprite_count > max+0.5:
		sprite_count = 1
	display_image_menu('animated_background_title_screen//' + str(int(sprite_count)), 1, (-2,-4), '.jpg')
	sprite_count += 0.5



# --- TITLE SCREENS ---

play_b, options_b, quit_b = 'Play_Off', 'Options_Off', 'Quit_Off'
def title_screen():
	''' MENU : Title screen menu '''
	global play_b, options_b, quit_b, replay
	running = True
	play_music('Title_screen', 0.85, -1)
	click, clicked = False, False
	while running == True:
		mouse_x, mouse_y = pygame.mouse.get_pos()
		animated_background_title_screen(8)
		display_image_menu('Background', 1, (0,0))

		play_button_image = pygame.image.load("Sprites/Play_Off.png")
		play_button = pygame.Rect(int(WIN_SIZE[0]/2 - play_button_image.get_width()/2+12),580+12, play_button_image.get_width()-24, play_button_image.get_height()-24)
		options_button_image = pygame.image.load("Sprites/Options_Off.png")
		options_button = pygame.Rect(int(WIN_SIZE[0]/2 - options_button_image.get_width()/2 +12),727, options_button_image.get_width()-24, options_button_image.get_height()-24)
		quit_button_image = pygame.image.load("Sprites/Quit_Off.png")
		quit_button = pygame.Rect(int(WIN_SIZE[0]/2 - quit_button_image.get_width()/2+12),855+12, quit_button_image.get_width()-24, quit_button_image.get_height()-24)

		if play_button.collidepoint((mouse_x, mouse_y)):
			play_b = 'Play_On'
			if click:
				play_sound('Accept')
				#play()
				difficulty_level()
				running = False

		if options_button.collidepoint((mouse_x, mouse_y)):
			options_b = 'Options_On'
			if click:
				play_sound('Navigation')
				options()

		if quit_button.collidepoint((mouse_x, mouse_y)):
			quit_b = 'Quit_On'
			if click:
				play_sound('Return')
				pygame.quit()
				sys.exit()
				running = False

		if not clicked:
			display_image_menu(play_b, 1, (int(WIN_SIZE[0]/2 - play_button_image.get_width()/2),580), '.png')
			#pygame.draw.rect(display, (0,0,0), play_button)
			display_image_menu(options_b, 1, (int(WIN_SIZE[0]/2 - options_button_image.get_width()/2),715), '.png')
			#pygame.draw.rect(display, (0,0,0), options_button)
			display_image_menu(quit_b, 1, (int(WIN_SIZE[0]/2 - quit_button_image.get_width()/2),855), '.png')
			#pygame.draw.rect(display, (0,0,0), quit_button)

		play_b, options_b, quit_b = 'Play_Off', 'Options_Off', "Quit_Off"
		click = False
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if keys[K_LALT] and keys[K_F4]:
				pygame.quit()
				sys.exit()
			
		update(70)

# Options menu
musics_On_b, musics_Off_b, sounds_On_b, sounds_Off_b = 'Musics_On_On', 'Musics_Off_Off', 'Sounds_On_On', "Sounds_Off_Off"
def options():
	''' MENU : Options screen menu '''
	global musics_On_b, musics_Off_b, sounds_On_b, sounds_Off_b, sound_volume, music_volume
	running = True
	click, clicked = False, False
	while running == True:
		mouse_x, mouse_y = pygame.mouse.get_pos()
		animated_background_title_screen(8)
		display_image_menu('Options', 1, (0,0))

		return_button_image = pygame.image.load("Sprites/Return.png")
		return_button = pygame.Rect(25, 25, return_button_image.get_width(), return_button_image.get_height())
		musics_on_button_image = pygame.image.load("Sprites/Musics_On_On.png")
		musics_on_button = pygame.Rect(int(WIN_SIZE[0]/4 - musics_on_button_image.get_width()/2 - 65),586, musics_on_button_image.get_width(), musics_on_button_image.get_height())
		musics_off_button_image = pygame.image.load("Sprites/Musics_Off_Off.png")
		musics_off_button = pygame.Rect(int(WIN_SIZE[0]/4 - musics_off_button_image.get_width()/2 - 55),685, musics_off_button_image.get_width(), musics_off_button_image.get_height())
		sounds_on_button_image = pygame.image.load("Sprites/Sounds_On_On.png")
		sounds_on_button = pygame.Rect(int(WIN_SIZE[0]/1.255 - musics_on_button_image.get_width()/2 - 65),586, sounds_on_button_image.get_width(), sounds_on_button_image.get_height())
		sounds_off_button_image = pygame.image.load("Sprites/Sounds_Off_Off.png")
		sounds_off_button = pygame.Rect(int(WIN_SIZE[0]/1.255 - musics_off_button_image.get_width()/2 - 55),685, sounds_off_button_image.get_width(), sounds_off_button_image.get_height())

		if return_button.collidepoint((mouse_x, mouse_y)):
			if click:
				play_sound('Navigation')
				running = False
		if musics_on_button.collidepoint((mouse_x, mouse_y)):
			display_image_menu('On_arrows', 1, (int(WIN_SIZE[0]/4 - musics_on_button_image.get_width()/2 - 120),586), '.png')
			if click:
				if musics_On_b == "Musics_On_Off":
					musics_On_b, musics_Off_b, music_volume = "Musics_On_On", "Musics_Off_Off", True
					mixer.music.set_volume(1)
					play_sound('Navigation')

		if musics_off_button.collidepoint((mouse_x, mouse_y)):
			display_image_menu('Off_arrows', 1, (int(WIN_SIZE[0]/4 - musics_off_button_image.get_width()/2 - 109),681), '.png')
			if click:
				if musics_Off_b == "Musics_Off_Off":
					musics_On_b, musics_Off_b, music_volume = "Musics_On_Off", "Musics_Off_On", False
					mixer.music.set_volume(0)
					play_sound('Navigation')

		if sounds_on_button.collidepoint((mouse_x, mouse_y)):
			display_image_menu('On_arrows', 1, (int(WIN_SIZE[0]/1.255 - sounds_on_button_image.get_width()/2 - 120),586), '.png')
			if click:
				if sounds_On_b == "Sounds_On_Off":
					sounds_On_b, sounds_Off_b, sound_volume = "Sounds_On_On", "Sounds_Off_Off", True
					play_sound('Navigation')

		if sounds_off_button.collidepoint((mouse_x, mouse_y)):
			display_image_menu('Off_arrows', 1, (int(WIN_SIZE[0]/1.255 - musics_off_button_image.get_width()/2 - 109),681), '.png')
			if click:
				if sounds_Off_b == "Sounds_Off_Off":
					sounds_On_b, sounds_Off_b, sound_volume = "Sounds_On_Off", "Sounds_Off_On", False
					play_sound('Navigation')

		if not clicked:
			display_image_menu('Return', 1, (25,25), '.png')
			#pygame.draw.rect(display, (0,0,0), return_button)
			display_image_menu(musics_On_b, 1, (int(WIN_SIZE[0]/4 - musics_on_button_image.get_width()/2 - 65),586), '.png')
			#pygame.draw.rect(display, (0,0,0), musics_on_button)
			display_image_menu(musics_Off_b, 1, (int(WIN_SIZE[0]/4 - musics_off_button_image.get_width()/2 - 55),685), '.png')
			#pygame.draw.rect(display, (0,0,0), musics_off_button)
			display_image_menu(sounds_On_b, 1, (int(WIN_SIZE[0]/1.255 - musics_on_button_image.get_width()/2 - 65),586), '.png')
			#pygame.draw.rect(display, (0,0,0), sounds_on_button)
			display_image_menu(sounds_Off_b, 1, (int(WIN_SIZE[0]/1.255 - musics_off_button_image.get_width()/2 - 55),685), '.png')
			#pygame.draw.rect(display, (0,0,0), sounds_off_button)

		click = False
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if keys[K_LALT] and keys[K_F4]:
				pygame.quit()
				sys.exit()
		 
		update(70)




## --- GAME CODE ---

import game # Importing game code and algorithms [+ MINIMAX]
game.initialising() # Initialise game.py

def inverse_row(i):
	''' Reverse the row from the playable_columns (.game) '''
	if i == 0: return 5
	if i == 1: return 4
	if i == 2: return 3
	if i == 3: return 2
	if i == 4: return 1
	if i == 5: return 0

def afficher_jetton(nom, x, column):
	''' Ajoute les jettons à une liste pour tous les afficher à chaque FRAME de la game '''
	liste_jettons.append([nom, (x+8, (94)+109*(inverse_row(game.get_next_open_row(game.board, column))+1))])

difficulty = 5 # Default difficulty
IA = ['Tabletop_red_turn', 'Red_to_play', 'Red_jetton'] # IA parameters
player = ['Tabletop_blue_turn', 'Blue_to_play', 'Blue_jetton'] # Player parameters


# --- Game Menus ---
def difficulty_level():
	''' Set difficulty level MENU '''
	game.board = game.create_board()
	click = False
	running = True
	while running:
		mouse_x, mouse_y = pygame.mouse.get_pos()
		animated_background_title_screen(8)

		display_image_menu('Full_level', 1, (0,0))
 
		easy_button = pygame.Rect(185, 625, 450, 125)
		medium_button = pygame.Rect(735, 625, 450, 125)
		hard_button = pygame.Rect(1285, 625, 450, 125)

		if easy_button.collidepoint((mouse_x, mouse_y)):
			display_image_menu('Easy', 1, (178, 614))
			if click:
				difficulty = 3
				color_selection()
				running = False

		if medium_button.collidepoint((mouse_x, mouse_y)):
			display_image_menu('Medium', 1, (730, 614))
			if click:
				difficulty = 5
				color_selection()
				running = False

		if hard_button.collidepoint((mouse_x, mouse_y)):
			display_image_menu('Hard', 1, (1281, 614))
			if click:
				difficulty = 7
				color_selection()
				running = False

		click = False
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if keys[K_LALT] and keys[K_F4]:
				pygame.quit()
				sys.exit()
		update(70)



def color_selection():
	''' Select your side/color MENU '''
	global IA, player
	level_selection = True
	click = False
	running = True
	while running:
		mouse_x, mouse_y = pygame.mouse.get_pos()
		animated_background_title_screen(8)

		display_image_menu('Full_color', 1, (0,0))
 
		red_button = pygame.Rect(185+231, 605, 450, 125)
		blue_button = pygame.Rect(735+318, 605, 450, 125)

		if red_button.collidepoint((mouse_x, mouse_y)):
			display_image_menu('Red', 1, (413, 595))
			if click:
				player = ['Tabletop_red_turn', 'Red_to_play', 'Red_jetton']
				IA = ['Tabletop_blue_turn', 'Blue_to_play', 'Blue_jetton']
				stop_music()
				play_sound('Navigation')
				play_music('Title_screen_2', 0.85, -1)
				running = False

		if blue_button.collidepoint((mouse_x, mouse_y)):
			display_image_menu('Blue', 1, (1048, 595))
			if click:
				IA = ['Tabletop_red_turn', 'Red_to_play', 'Red_jetton']
				player = ['Tabletop_blue_turn', 'Blue_to_play', 'Blue_jetton']
				stop_music()
				play_sound('Navigation')
				play_music('Title_screen_2', 0.85, -1)
				running = False

		click = False
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if keys[K_LALT] and keys[K_F4]:
				pygame.quit()
				sys.exit()
		update(70)



def timer(t):
	''' Function that is used as a timer '''
	run = True
	start_ticks=pygame.time.get_ticks()
	while run:
		seconds=(pygame.time.get_ticks()-start_ticks)/1000
		if seconds >= t: run = False
		update(70)


liste_jettons = []
def play():
	''' MAIN GAME FUNCTION : Play() '''
	global liste_jettons, IA, player
	game.board = game.create_board()
	game.playing = game.RL_player
	click = False
	run = True
	while run: # game loop
		mouse_x, mouse_y = pygame.mouse.get_pos()

		if game.playing == game.RL_player: display_image_menu(player[0], 1, (0,0), '.jpg')
		elif game.playing == game.IA_player : display_image_menu(IA[0], 1, (0,0), '.jpg')
		else: display_image_menu('Tabletop', 1, (0,0), '.jpg')

		row1_button = pygame.Rect(580, 180 , 109, 675)
		row2_button = pygame.Rect(689, 180 , 109, 675)
		row3_button = pygame.Rect(798, 180 , 109, 675)
		row4_button = pygame.Rect(907, 180 , 109, 675)
		row5_button = pygame.Rect(1016, 180 , 109, 675)
		row6_button = pygame.Rect(1125, 180 , 109, 675)
		row7_button = pygame.Rect(1234, 180 , 109, 675)

		for i in liste_jettons:
			display_image_menu(i[0], 1, i[1])


		if row1_button.collidepoint((mouse_x, mouse_y)) and 0 in game.get_valid_locations(game.board) and game.playing == game.RL_player:
			display_image_menu(player[1], 1, (580-1, 180-130))
			if click:
				afficher_jetton(player[2], 580, 0)
				game.player_play(game.board, 0)
		if row2_button.collidepoint((mouse_x, mouse_y)) and 1 in game.get_valid_locations(game.board) and game.playing == game.RL_player:
			display_image_menu(player[1], 1, (689-1, 180-130))
			if click:
				afficher_jetton(player[2], 689, 1)
				game.player_play(game.board, 1)
		if row3_button.collidepoint((mouse_x, mouse_y)) and 2 in game.get_valid_locations(game.board) and game.playing == game.RL_player:
			display_image_menu(player[1], 1, (798-1, 180-130))
			if click:
				afficher_jetton(player[2], 798, 2)
				game.player_play(game.board, 2)
		if row4_button.collidepoint((mouse_x, mouse_y)) and 3 in game.get_valid_locations(game.board) and game.playing == game.RL_player:
			display_image_menu(player[1], 1, (907-1, 180-130))
			if click:
				afficher_jetton(player[2], 907, 3)
				game.player_play(game.board, 3)
		if row5_button.collidepoint((mouse_x, mouse_y)) and 4 in game.get_valid_locations(game.board) and game.playing == game.RL_player:
			display_image_menu(player[1], 1, (1016-1, 180-130))
			if click:
				afficher_jetton(player[2], 1016, 4)
				game.player_play(game.board, 4)
		if row6_button.collidepoint((mouse_x, mouse_y)) and 5 in game.get_valid_locations(game.board) and game.playing == game.RL_player:
			display_image_menu(player[1], 1, (1125-1, 180-130))
			if click:
				afficher_jetton(player[2], 1125, 5)
				game.player_play(game.board, 5)
		if row7_button.collidepoint((mouse_x, mouse_y)) and 6 in game.get_valid_locations(game.board) and game.playing == game.RL_player:
			display_image_menu(player[1], 1, (1234-1, 180-130))
			if click:
				afficher_jetton(player[2], 1234, 6)
				game.player_play(game.board, 6)

		if game.board_is_full(game.board): 
			end_game('Tie', 'Tie')
			del liste_jettons[:]
			game.board = game.create_board()
			title_screen()
			run = False

		if game.playing == game.IA_player:
			game.ia_play(game.board, difficulty)

		click = False
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if keys[K_LALT] and keys[K_F4]:
				pygame.quit()
				sys.exit()

		update(70) #Uses the update() function to update the screen frame



# --- Results Functions ---

def end_game(sound, image):
	''' Function du declare an END GAME '''
	run = True
	stop_music()
	start_ticks=pygame.time.get_ticks()
	play_sound(sound)
	while run:
		seconds=(pygame.time.get_ticks()-start_ticks)/1000
		display_image_menu('Tabletop', 1, (0,0), '.jpg')
		for i in liste_jettons:
			display_image_menu(i[0], 1, i[1])
		
		display_image_menu(image, 1, (0, 0), '.png')
		if seconds >= 5: run = False

		update(70)
#end_game('Won', 'Win')
#end_game('Lost', 'Lost')
#end_game('Tie', 'Tie')


# --- GAME CALLED FUNCTIONS ---
intro()
title_screen()
play()

# --- Game Launch and Scenes ---
#play_video('Openning-Credits')
#title_screen()
#play_video('Intro-video')


pygame.quit()
sys.exit()