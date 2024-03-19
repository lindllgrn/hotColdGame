"""
The Hot/Cold Game
The user has to try to find a hidden circle using his circle to move around the screen.
The game's objective is to see how many moves it takes you to find a hidden circle
on the screen using another circle to navigate.

The hidden circle (same color as the screen background) will be randomly placed on the screen

The user’s circle will always start in the center of the screen

Allow the user to select the difficulty of the game by controlling the size of the circle
and the distance it moves on each attempt

The user’s circle will be red (hot) when getting closer or blue (cold) when getting further away from the hidden circle

The game has the following key options:
Up, Down, Left, and Right arrows
D = Toggle debug mode (displays the display the hidden circle)
H = Move the user’s circle home position user_x=0, user_y=0
R = Reset the game

The game will always display a running total of the number of moves
"""

__author__ = "Lindsay Green"
__version__ = '1.0'
__copyright__ = "Copyright 2024.03.18, Hot/Cold Game Assignment"
__github_ = "https://github.com/lindllgrn/hotColdGame"

import pygame
import random
import pygame_menu

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 233, 0)
GREEN = (0, 128, 0)
GRAY = (128, 128, 128)

# Global variables
SCREEN_SIZE = 800
SCREEN = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
#
game = {
    'circle_size': 50,
    'move_size': 50,
    'previous_x': 0,
    'previous_y': 0,
    'user_x': SCREEN_SIZE / 2,
    'user_y': SCREEN_SIZE / 2,
    'hidden_x': 0,
    'hidden_y': 0,
    'user_color': GREEN,
    'hidden_color': BLACK,
    'num_moves': 0
}


def set_center_location():
    """
    user's circle will be moved to the center of the screen based on circle size and screen size.
    :return: None
    """
    global game

    game['user_x'] = (SCREEN_SIZE - game['circle_size']) // 2
    game['user_y'] = (SCREEN_SIZE - game['circle_size']) // 2


def set_circle_color():
    """
    set the amount the user's circle must overlap by the dimension of both circles added together minus 10
    if the circle overlap
        then set both circles to different green colors
    else
        if the user's circle x location has changed then determine if they are closer or further away from previous x
            if previous x distance is less than current x distance
            then set red else blue
        if the user's circle y location has changed then determine if they are closer or further away from previous y
            if previous y distance is less than current y distance
            then set red else blue
    store the current x, y to previous x, y to get ready for the new user's move
    :return: None
    """
    global game

    # Set the amount the user's circle must overlap by the dimension of both circle added together minus 10
    overlap = game['circle_size'] * 2 - 10

    # If the circle overlap then set both circles to different colors
    if abs(game['user_x'] - game['hidden_x']) < overlap and abs(game['user_y'] - game['hidden_y']) < overlap:
        game['hidden_color'] = YELLOW
        game['user_color'] = GREEN

    else:
        # If the user's circle user_x location has changed then determine if they are closer or farther away from
        # previous_x
        if game['previous_x'] != game['user_x']:
            # If previous_x distance is less than current x distance then set red otherwise blue
            if abs(game['previous_x'] - game['hidden_x']) > abs(game['user_x'] - game['hidden_x']):
                game['user_color'] = RED
            else:
                game['user_color'] = BLUE

        # If the user's circle y location has changed then determine if they are closer or further away from previous y
        if game['previous_y'] != game['user_y']:
            # If previous y distance is less than current y distance then set red otherwise blue
            if abs(game['previous_y'] - game['hidden_y']) > abs(game['user_y'] - game['hidden_y']):
                game['user_color'] = RED
            else:
                game['user_color'] = BLUE

    # Store the current x, y to previous x, y to get ready for the new user's move
    game['previous_x'] = game['user_x']
    game['previous_y'] = game['user_y']


def display_instructions():
    """
    Display the current total number of user's moves
    and game's instruction on the screen in the upper left-hand corner
    :return: None
    """
    global game

    font = pygame.font.SysFont(None, 24)  # Change the font
    text = font.render(f"Total moves = {game['num_moves']}", True, WHITE)  # Displays number of moves
    SCREEN.blit(text, (10, 10))

    # List of instructions to display
    instructions = [
        "Use arrow keys to move",
        "d = Debug mode",
        "h = Move home",
        "r = Reset game"
    ]

    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, WHITE)
        SCREEN.blit(text, (10, 30 + i * 20))


def random_xy():
    global game

    user_pos = SCREEN_SIZE / 2

    inside_dist = game['circle_size']
    outside_dist = SCREEN_SIZE - game['circle_size']

    right_user_dist = user_pos - game['circle_size']
    left_user_dist = user_pos + game['circle_size']

    while True:
        game['user_x'] = random.randint(inside_dist, outside_dist)
        game['user_y'] = random.randint(inside_dist, outside_dist)

        if (game['user_x'] < right_user_dist or game['user_x'] > left_user_dist) and (
                game['user_y'] < right_user_dist or game['user_y'] > left_user_dist):
            game['hidden_x'] = game['user_x']
            game['hidden_y'] = game['user_y']
            return


def setup_game():
    global game

    game['num_moves'] = 0
    game['hidden_color'] = BLACK
    random_xy()
    set_center_location()


def debug():
    global game

    game['hidden_color'] = GRAY


def play_game():
    global game

    clock = pygame.time.Clock()

    run_me = True

    while run_me:
        clock.tick(15)
        SCREEN.fill(BLACK)
        set_circle_color()

        pygame.draw.circle(SCREEN, game['hidden_color'], (game['hidden_x'], game['hidden_y']), game['circle_size'])
        pygame.draw.circle(SCREEN, game['user_color'], (game['user_x'], game['user_y']), game['circle_size'])

        display_instructions()
        pygame.display.flip()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            debug()
        if keys[pygame.K_r]:
            setup_game()
        if keys[pygame.K_h]:
            set_center_location()
        if keys[pygame.K_LEFT]:
            game['user_x'] -= game['move_size']
            game['num_moves'] += 1
        if keys[pygame.K_RIGHT]:
            game['user_x'] += game['move_size']
            game['num_moves'] += 1
        if keys[pygame.K_UP]:
            game['user_y'] -= game['move_size']
            game['num_moves'] += 1
        if keys[pygame.K_DOWN]:
            game['user_y'] += game['move_size']
            game['num_moves'] += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_me = False


def set_difficulty(level, difficulty):
    global game

    if difficulty == 4:
        game['circle_size'], game['move_size'] = (7, 7)
    elif difficulty == 3:
        game['circle_size'], game['move_size'] = (10, 10)
    elif difficulty == 2:
        game['circle_size'], game['move_size'] = (25, 25)
    else:
        game['circle_size'], game['move_size'] = (50, 50)


def menu(screen):
    menu = pygame_menu.Menu('Hot/Cold Game', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.selector('Difficulty :', [('Level 1', 1), ('Level 2', 2), ('Level 3', 3), ('Level 4', 4)],
                      onchange=set_difficulty)
    menu.add.button('Play', play_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    pygame.display.set_caption('Hot Cold Game')
    font = pygame.font.SysFont(None, 24)
    line = font.render('#' + str(game['num_moves']) + " moves", True, YELLOW)
    screen.blit(line, (20, 20))

    return menu


def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load('Fluffing-a-Duck.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)


def main():
    pygame.init()
    play_music()
    pygame.display.set_caption('Hot Cold Game')

    menu_obj = menu(SCREEN)
    menu_obj.mainloop(SCREEN)

    pygame.quit()


if __name__ == '__main__':
    main()
