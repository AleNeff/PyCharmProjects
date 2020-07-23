import pygame
import random
from pygame import mixer

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
pygame.init()
pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
game_font = 'arial' # font for text in-game

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# BACKGROUND MUSIC
mixer.music.load('background.wav')
mixer.music.play(-1)

# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        # shapes.index(shape) returns index of shape in "shapes[]" then that index is used to index into shape_colors
        self.rotation = 0

def update_score(nscore):
    score = max_score() # score is first line of score.txt

    with open('scores.txt', 'w') as f:  # if possible, open scores.txt, open for reading, make f the object for it
        if int(nscore) > int(score):
            f.write(str(nscore))    # write new score over old if higher
        else:
            f.write(str(score))     # put back old score

def max_score():
    with open('scores.txt', 'r') as f:  # if possible, open scores.txt, open for reading, make f the object for it
        lines = f.readlines()   # lines = list of all lines in file
        score = lines[0].strip()    # score = first line with \n stripped away

    return score

# def play_score_sound():
    # score_sound = mixer.Sound('score.wav')
    # score_sound.play()


def create_grid(locked_pos={}): # locked_pos is a {(x, y): (r,g,b)} dictionary
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]
    # grid is a 10 across 20 down 2D array of (r,g,b)'s,
    # (0, 0, 0) is black & empty, a color means occupied

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:    # if corresponding (x, y) is an index in locked_pos dictionary,
                c = locked_pos[(j, i)]  # value at (j, i) index is the corresponding color,
                grid[i][j] = c          # set that "block" of grid to that (r,g,b) value
    return grid


def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)] # len(piece.shape) returns # of arrays in shapes[] array AKA # of rotations
                                                            # format = desired orientation of letter
    for i, line in enumerate(format):  # i is index, line value at index
        row = list(line)               # row = set of chars at index ; list(line) turns line (set of chars) into a list
        for j, column in enumerate(row):    # j is index within row, column is char at that row & column (or x & y)
            if column == '0':               # '0' = block taken by shape
                positions.append((piece.x + j, piece.y + i))
                # positions[] <++ (x,y) position for actual location of occupied blocks

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) # account for offset of "." values inside letter orientation lists

    return positions    # positions is an array with (x, y) positions of blocks taken by piece


def valid_space(piece, grid):   # passed a piece & a 10x20 grid of locked & unlocked positions to check
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # 2D array of tuples, each element is a (j, i) index to an (r,g,b) value in grid IF IT IS (0,0,0) AKA black
    # (j, i) indexes to rgb value due to locked_pos dictionary
    accepted_pos = [j for sub in accepted_pos for j in sub]
    # this line turns the 2D array of accepted positions into a 1D list of (j, i) coordinates
    # [[(1,3)], [(4,2)]] --> [ (1,3), (4,2) ]
    formatted = convert_shape_format(piece) # c_s_f(piece) returns an array with (x, y) pos's of occupied blocks
                                            # based on rotation
    for pos in formatted:   # pos iterates through each occupied (x,y)
        if pos not in accepted_pos: # accepted_pos hold each (x,y) that is open
            if pos[1] > -1:     # only blocks with a y-value of 0 or greater in an "invalid spot" should be invalid
                return False    # because blocks coming from top of screen will be "invalid" but aren't actually
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:   # pos=each (x, y) of locked positions, if "locked" off top of screen, game is lost
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))   #middle & top of screen, randomly select shape


def draw_text_middle(surface, text, size, color):
    pygame.font.init()  # init font
    font = pygame.font.SysFont(game_font, size, bold=True)  # init font as desired
    label = font.render(text, 1, color) # label = desired text & font

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))
    # label is desired text with desired size # color, blitted to display at center of playing screen


def draw_grid(surface, grid):   # draws grey gridlines onto screen
    sx = top_left_x # easier to work with names
    sy = top_left_y # easier to work with names

    for i in range(len(grid)):   # len(grid) is 20, vertical lines iterated through first
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
    for j in range(len(grid[0])):    # len(grid[i]) is 10, x-values iterated through here
        pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy), (sx + j * block_size, sy+play_height))
        # I un-nested these loops, different from video

def clear_rows(grid, locked):
    # locked is locked_pos dictionary
    inc = 0     # counter for rows filled
    ind = 0    # index of lowest row to be deleted
    for i in range(len(grid) - 1, - 1, -1): # loop through grid - start at 19, go backwards
        row = grid[i]   # row = each row of grid (there are 20 rows)
        if (0,0,0) not in row:  # if black isn't present at all in the row it is filled
            inc += 1    # row filled (could be > 1 row filled)
            if i > ind:  # if this row is LOWEST row to be deleted, this fixes the error of
                ind = i  # two non-adjacent rows deleting but leaving a space between
            for j in range(len(row)):   # for each j in the filled row
                try:
                    del locked[(j, i)]  # remove that block from the dictionary of locked_pos{} (unlock position)
                except:
                    continue
    if inc > 0:
        # lambdanote : r = lambda op1, op2: op1 operand op2 --> creates function r that operates on op1 & op2
        for initialx_y in sorted(list(locked), key=lambda x: x[1])[::-1]:  # [::-1] reverses list, key is a tuple--> (x, y)
            # key=lambda x: x[1] turns x into the y-val for each tuple-this causes list(locked) to be sorted by y value
            # it is now in descending y-value (from bottom to top) order
            # each initialx_y is the (x, y) tuple of the newly-sorted list
            x, y = initialx_y  # initialx_y is an (x, y) tuple
            if y < ind: # if y of locked_pos{(x, y):(r,g,b)} is "above" row being deleted,
                newx_y = (x, y + inc)   # (x, y) but shifted down by # of rows deleted
                locked[newx_y] = locked.pop(initialx_y)
    # new (x,y) added to locked_pos dictionary, .pop(initialx_y) gets color for new position (using initialx_y as index)
    return inc



def draw_next_shape(piece, surface):
    sx = top_left_x + play_width + 50   # top left + play area w/ offset to look better
    sy = top_left_y + play_height/2 - 100   # top left + halfway down play area w/ offset to look better

    font = pygame.font.SysFont(game_font, 30)         # create font look
    label = font.render('Next Shape', 1, (255,255,255)) # label = rendered words to be blitted
    surface.blit(label, (sx + 10, sy - 30))   # blit label to screen, constants offset for better look

    format = piece.shape[piece.rotation % len(piece.shape)] # format = currently desired orientation for piece

    for i, line in enumerate(format):   # i is index of row, line is each row of chars from format
        row = list(line)    # row = line of chars turned into list
        for j, column in enumerate(row):    # j is index of column, column is each char in the row
            if column == "0":   # if block is desired at this coordinate
                pygame.draw.rect(surface, piece.color, (sx + j*block_size, sy + i*block_size, block_size, block_size),0)
                # draw next piece using x & y corresponding to blocks of the shape & its color


def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0)) # black-out screen

    pygame.font.init()
    font = pygame.font.SysFont(game_font, 60)   #create game font for Tetris title
    label = font.render('Tetris', 1, (255, 255, 255))   # label = title

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))    # blit title to screen
# CURRENT SCORE
    sx = top_left_x + play_width + 50   # top left + play area w/ offset to look better
    sy = top_left_y + play_height/2 - 100   # top left + halfway down play area w/ offset to look better

    font = pygame.font.SysFont(game_font, 30)         # create font look
    label = font.render('Score: ' + str(score), 1, (255,255,255)) # label = score to be shown
    surface.blit(label, (sx + 25, sy + 160))    # draw score onto screen
# HIGH SCORE
    sx = top_left_x - 250  # further left than play area
    sy = top_left_y + 100  # move it down the screen

    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))  # label = high_score to be shown
    surface.blit(label, (sx + 25, sy + 160))  # draw score onto screen

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, (grid[i][j]), (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)
            # draw each block of color to grid, grid[i][j] returns color
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)
            # draw red box around play area
    draw_grid(surface, grid)    # draw in lines of grid


def main(win):
    last_score = max_score()    # last_score = highscore from .txt file
    locked_positions = {}   # blank "dictionary", (x, y) is key name(index), color is value -> (x, y) : (r,g,b)
    grid = create_grid(locked_positions)    # assign grid the colored blocks from locked positions

    change_piece = False    # flag for piece reaching bottom / other block
    run = True
    current_piece = get_shape() # assign random shape
    next_piece = get_shape()    # assign random shape
    clock = pygame.time.Clock() # create game clock object for ticks
    fall_time = 0       # incremented with clock
    fall_speed = 0.27   # delay before piece moves down (in seconds)
    level_time = 0      # timer/counter for if speed should increase
    max_fall_speed = .12    # shortest delay per piece drop (max speed) allowed
    fall_speed_increase = .005  # drop delay decrease per level_time reset (speed increase)
    score = 0 # score variable

    while run:
        grid = create_grid(locked_positions)    # make grid w/ current locked blocks
        fall_time += clock.get_rawtime()    # increment timer (units of ms)
        level_time += clock.get_rawtime()   # level_time incremented by ms passed

        if level_time/1000 > 5: # 5 seconds per speed increase
            level_time = 0      # reset speed increase ticker
            if fall_speed > max_fall_speed: # if not at max speed
                fall_speed -= fall_speed_increase   # increase speed (by decreasing delay)
        clock.tick()    # increment clock by ms passed

        if fall_time / 1000 > fall_speed:   # /1000 makes fall_time be in seconds
            fall_time = 0   # reset fall timer
            current_piece.y += 1    # move one spot down screen
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:  # if invalid NOT bc above top of screen
                current_piece.y -= 1    # undo movement
                change_piece = True     # piece has reached bottom or other block, next piece needed

        for event in pygame.event.get():     # increment through inputs to game
            if event.type == pygame.QUIT:   # X'd out of game
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # move left
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1    # undo (invalid)

                if event.key == pygame.K_RIGHT: # move right
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                            current_piece.x -= 1    # undo (invalid)

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1        # move up
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1    # undo (invalid)

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1 # increment rotational (index for orientation of shape)
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1 # undo (invalid)

        shape_pos = convert_shape_format(current_piece) # shape_pos is array of (x, y) values for occupied blocks

        for i in range(len(shape_pos)):     # this loop indexes through set of (x, y) values for blocks
            x, y = shape_pos[i]             # shape_pos[i] is an (x, y) object, so this works
            if y > -1:          # if shape isn't fully on-screen, we don't want to try & set that block's color
                grid[y][x] = current_piece.color    # assign color to blocks of grid

        if change_piece:    # change_piece is set if block has locked in, code below "locks" the piece into place
            for pos in shape_pos:       # pos indexes through each (x, y) of shape_pos
                p = (pos[0], pos[1])    # p = (x, y) of occupied blocks
                locked_positions[p] = current_piece.color   # [(x,y):(r,g,b)] < format for locked_pos = "dictionary",
                # (x, y) acts as an index into locked positions, set corresponding value in dictionary to piece's color
            current_piece = next_piece  # current takes next
            next_piece = get_shape()    # next gets new random shape
            change_piece = False        # piece changed -- flag cleared
            score += clear_rows(grid,locked_positions) * 10
            # clear filled rows, # rows cleared is returned, 10*that=score

        draw_window(win, grid, score, last_score)  # draws window with "win" as game surface & "grid" with new locked positions
        draw_next_shape(next_piece, win) # draw next shape on-screen using win as surface
        pygame.display.update()

        if check_lost(locked_positions):    #check if piece has "locked" past top of screen
            win.fill((0,0,0))   # black out game screen
            draw_text_middle(win, "Game Over!", 80, (255, 255, 255))    # draw game over message

            font = pygame.font.SysFont(game_font, 60, bold=True)        # create end-game font
            label = font.render('Your Score: ' + str(score), 1, (255,255,255))  # label = score msg
            win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + 100 + play_height / 2 - (label.get_height() / 2)))
            # blit score msg to appropriate place on-screen
            pygame.display.update() # update display
            pygame.time.delay(2000) # delay for 2000 ms
            run = False # game over
            update_score(score) # send nscore to check if it should overwrite old score


def main_menu(win): # win = surface = whole game window
    run_main = True # mainmenu run flag
    while run_main:
        win.fill((0,0,0))   # black out main screen
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))    # show this at middle
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # check if game exit
                run_main = False
            if event.type == pygame.KEYDOWN:    # check if key pressed
                main(win)   # run main game

    pygame.display.quit()   # game quit

win = pygame.display.set_mode((s_width, s_height))  # creates surface with (screen width, screen height) dimensions
                                                    # to be "drawn on" by game -- total game window
pygame.display.set_caption("Tetris")    # caption on game window
icon = pygame.image.load('tetrislogo.png')  # logo for game window
pygame.display.set_icon(icon)   # set logo as desired logo image
main_menu(win)  # start game
