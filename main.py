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
__copyright__ = "Copyright 2024.03.27, Hot/Cold Game Assignment"
__github_ = "https://github.com/lindllgrn/hotColdGame"

import pygame
import random
import pygame_menu
import sys

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

# Used for displaying the prompts at the top of the screen for each level
prompt = {
    'prompt1': 'Try to find the hidden circle in 10 moves, you will move on to the next level if you do so.',
    'prompt2': 'Try to find the hidden circle in 20 moves, you will move on to the next level if you do so.',
    'prompt3': 'Try to find the hidden circle in 50 moves, you will move on to the next level if you do so.',
    'prompt4': 'Try to find the hidden circle in 70 moves, you will move on to the next level if you do so.',
    'prompt5': 'Otherwise, you will play the level over until you do.'
}

# Game data that can change  values
game = {
    'circle_size': 50,  # 50=level1, 25=level2, 10=level3, 7=level4
    'move_size': 50,  # 50=level1, 25=level2, 10=level3, 7=level4
    'previous_x': 0,  # Used to determine if getting hotter or colder
    'previous_y': 0,  # Used to determine if getting hotter or colder
    'user_x': SCREEN_SIZE / 2,  # Centered based on half of the screen size
    'user_y': SCREEN_SIZE / 2,  # Centered based on half of the screen size
    'hidden_x': 0,  # Will be randomly generated based on the screen size
    'hidden_y': 0,  # Will be randomly generated based on the screen size
    'user_color': WHITE,  # White at the start of the game but will change to red, blue, or green
    'hidden_color': BLACK,  # Make the hidden circle the same color as the background
    'num_moves': 0  # Keep track of the current number of moves
}


def set_center_location():
    """
    user's circle will be moved to the center of the screen based on circle size and screen size.
    :return: None
    """
    global game

    # Calculate the user_x to center it horizontally
    game['user_x'] = (SCREEN_SIZE - game['circle_size']) // 2
    # Calculate the user_y to center it vertically
    game['user_y'] = (SCREEN_SIZE - game['circle_size']) // 2


def set_circle_color():
    """
    Sets the color of both circles. If the user circle gets closer to the hidden circle, the user circle will turn red.
    If the user circle gets farther away from the hidden circle, the user circle will turn blue. If the circles overlap,
    the user circle turns green and the hidden circle yellow.
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


def random_xy():
    """
    Creates random places for the hidden circle to go
    :return: None
    """
    global game

    user_pos = SCREEN_SIZE / 2  # Center of the screen

    inside_dist = game['circle_size']  # Make sure the hidden circle is not touching the user's circle in the middle
    outside_dist = SCREEN_SIZE - game['circle_size']  # Don't let the hidden circle touch the edge of the screen

    right_user_dist = user_pos - game['circle_size']  # At least one circle away on the right
    left_user_dist = user_pos + game['circle_size']  # At least one circle away on the left

    # Keep looping until a valid location is generated within the screen size and not touching the user's circle
    while True:
        # Hidden location not in center where the user's circle is and yet still inside the screen
        game['user_x'] = random.randint(inside_dist, outside_dist)
        game['user_y'] = random.randint(inside_dist, outside_dist)

        # Make sure the hidden circle is not near the user's circle
        if (game['user_x'] < right_user_dist or game['user_x'] > left_user_dist) and (
                game['user_y'] < right_user_dist or game['user_y'] > left_user_dist):
            game['hidden_x'] = game['user_x']
            game['hidden_y'] = game['user_y']
            return


def setup_game():
    """
    Resets the game if the user decides to restart the game by pressing ' r'
    :return: None
    """
    global game

    game['num_moves'] = 0  # Sets the number of moves back to 0
    game['hidden_color'] = BLACK  # Sets the hidden circle back to black
    random_xy()  # Sets the hidden circle to a random spot on the screen
    set_center_location()  # Sets the user's circle to the center of the screen


def debug():
    """
    Allows the user to debug the game, allowing the hidden circle to become visible for testing the game
    :return: None
    """
    global game

    game['hidden_color'] = GRAY  # Changes hidden circle to gray


def set_difficulty(level, difficulty):
    """
    Adjusts the circle size based on difficulty
    :param level: Gets the level the player chose
    :param difficulty: Chosen by the player. Determines the size of circles and movement increment
    :return: None
    """
    global game

    if difficulty == 1:
        game['circle_size'], game['move_size'] = (50, 50)
    elif difficulty == 2:
        game['circle_size'], game['move_size'] = (25, 25)
    elif difficulty == 3:
        game['circle_size'], game['move_size'] = (10, 10)
    elif difficulty == 4:
        game['circle_size'], game['move_size'] = (7, 7)
    elif difficulty == 5: # Not an actual difficulty to play, used for the ending when the game is completed
        game['circle_size'], game['move_size'] = (0, 0)


# noinspection PyTypeChecker
def completed_game():
    """
    This is also used to create the ending scene of the game. Also has a little surprise to it :)
    :return: None
    """
    font = pygame.font.SysFont(None, 85)  # Change the font
    text = font.render(f" YAY YOU WON THE GAME!", True, YELLOW)  # Displays number of moves
    SCREEN.blit(text, (0, 400))
    pygame.mixer.init()  # Initialize pygame.mixer
    pygame.mixer.music.load('yay.mp3')  # Loads this file as the music
    pygame.mixer.music.set_volume(0.5)  # Sets the volume level to 50%
    pygame.mixer.music.play(loops=1)  # Play the music once


# I did this by using this source https://stackoverflow.com/questions/31942122/rendering-unicode-in-pygame
def funsies():
    """
    Created for the ending scene for when the game is completed. It's a surprise :)
    :return: None
    """
    unistr = "☺"
    font = pygame.font.Font("Arial-Unicode-MS-Regular.ttf", 100) # Changes the font and size
    SCREEN.blit(font.render(unistr, True, YELLOW), (400, 500)) # Sets text location and color
    pygame.display.flip() # Updates the display

    while True:
        SCREEN.blit(font.render(unistr, True, YELLOW), (400, 500))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# noinspection PyTypeChecker
def display_instructions():
    """
    Display the current total number of user's moves
    and game's instruction on the screen in the upper left-hand corner
    :return: None
    """
    global game

    # List of instructions to display
    instructions = [
        " ",
        "Use arrow keys to move",
        "q = Debug mode",
        "h = Move home",
        "r = Reset game",
        " "
    ]

    # Used for displaying things on the first difficulty
    if game['circle_size'] == 50 and game['move_size'] == 50:
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"{prompt['prompt1']}", True, YELLOW) # Display the first prompt
        SCREEN.blit(text, (10, 10)) # Sets text location
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"{prompt['prompt5']}", True, YELLOW) # Used as a constant throughout the game
        SCREEN.blit(text, (10, 30)) # Sets text location
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"Total moves = {game['num_moves']}", True, WHITE)  # Displays number of moves
        SCREEN.blit(text, (10, 130)) # Sets text location
        # Iterates through the instructions to display throughout the game
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, WHITE)
            SCREEN.blit(text, (10, 30 + i * 20))

    # Used to display instructions on the second difficulty
    if game['circle_size'] == 25 and game['move_size'] == 25:
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"{prompt['prompt2']}", True, YELLOW) # Displays the prompt
        SCREEN.blit(text, (10, 10)) # Sets the location of the text
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"{prompt['prompt5']}", True, YELLOW) # Used as a constant throughout the game
        SCREEN.blit(text, (10, 30)) # Sets the location of the text
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"Total moves = {game['num_moves']}", True, WHITE)  # Displays number of moves
        SCREEN.blit(text, (10, 130)) # Sets the location of the text

        # Iterates to display the instructions at the top of the screen
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, WHITE)
            SCREEN.blit(text, (10, 30 + i * 20))

    # Used for displaying things on the third difficulty
    if game['circle_size'] == 10 and game['move_size'] == 10:
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"{prompt['prompt3']}", True, YELLOW) # Display the third prompt
        SCREEN.blit(text, (10, 10)) # Sets the text location
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"{prompt['prompt5']}", True, YELLOW) # Used as a constant throughout the game
        SCREEN.blit(text, (10, 30)) # Sets the location of the text
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"Total moves = {game['num_moves']}", True, WHITE)  # Displays number of moves
        SCREEN.blit(text, (10, 130)) # Sets the location of the text

        # Iterates to display the instructions at the top of the screen
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, WHITE)
            SCREEN.blit(text, (10, 30 + i * 20))

    # Used for displaying things on the fourth difficulty
    if game['circle_size'] == 7 and game['move_size'] == 7:
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"{prompt['prompt4']}", True, YELLOW) # Displays the prompt
        SCREEN.blit(text, (10, 10)) # Sets the text location
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"{prompt['prompt5']}", True, YELLOW) # Used as a constant throughout the game
        SCREEN.blit(text, (10, 30)) # Sets the text location
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"Total moves = {game['num_moves']}", True, WHITE)  # Displays number of moves
        SCREEN.blit(text, (10, 130)) # Sets the text location

        # Iterates to display the instructions at the top of the screen
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, WHITE)
            SCREEN.blit(text, (10, 30 + i * 20))

    # Used for displaying things on the fifth difficulty
    if game['circle_size'] == 0 and game['move_size'] == 0:
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"Total moves = {game['num_moves']}", True, BLACK)  # Displays number of moves
        SCREEN.blit(text, (10, 110)) # Sets text location
        font = pygame.font.SysFont(None, 24)  # Change the font
        text = font.render(f"{prompt['prompt5']}", True, BLACK) # Used as a constant throughout the game
        SCREEN.blit(text, (10, 30)) # Set the text location

        # Iterates to display the instructions at the top of the screen
        for i, instruction in enumerate(instructions):
            text = font.render(f"{prompt['prompt4']}", True, BLACK)
            SCREEN.blit(text, (10, 30 + i * 20))

        completed_game()
        funsies()


def play_game():
    """
    Plays the game. Creates the circles and accounts for which key the user presses.
    Displays instructions in the top left corner
    :return: None
    """
    global game

    clock = pygame.time.Clock()  # Initialize pygame clock

    run_me = True

    while run_me:
        clock.tick(15)  # Controls frame rate of the user circle
        SCREEN.fill(BLACK)  # Fill the screen with black color
        set_circle_color()  # Sets color of circles

        # Draws the hidden circle
        pygame.draw.circle(SCREEN, game['hidden_color'], (game['hidden_x'], game['hidden_y']), game['circle_size'])
        # Draws the user circle
        pygame.draw.circle(SCREEN, game['user_color'], (game['user_x'], game['user_y']), game['circle_size'])

        display_instructions()  # Displays game instructions
        pygame.display.flip()  # Update the display

        keys = pygame.key.get_pressed()  # Checks for keyboard inputs

        if keys[pygame.K_q]:
            debug()
        if keys[pygame.K_r]:
            setup_game()
        if keys[pygame.K_h]:
            set_center_location()
        if keys[pygame.K_LEFT]:
            game['user_x'] -= game['move_size']
            game['num_moves'] += 1
        if keys[pygame.K_a]:
            game['user_x'] -= game['move_size']
            game['num_moves'] += 1
        if keys[pygame.K_d]:
            game['user_x'] += game['move_size']
            game['num_moves'] += 1
        if keys[pygame.K_RIGHT]:
            game['user_x'] += game['move_size']
            game['num_moves'] += 1
        if keys[pygame.K_w]:
            game['user_y'] -= game['move_size']
            game['num_moves'] += 1
        if keys[pygame.K_UP]:
            game['user_y'] -= game['move_size']
            game['num_moves'] += 1
        if keys[pygame.K_s]:
            game['user_y'] += game['move_size']
            game['num_moves'] += 1
        if keys[pygame.K_DOWN]:
            game['user_y'] += game['move_size']
            game['num_moves'] += 1

        # Allows the user to move from level to level if they get a certain amount of moves
        if game['num_moves'] > 10 and game['user_color'] == GREEN and game['circle_size'] == 50 and game['move_size'] == 50:
            setup_game()
        elif game['num_moves'] and game['user_color'] == GREEN and game['circle_size'] == 50 and game['move_size'] == 50:
            set_difficulty(None, 2)
            setup_game()

        if game['num_moves'] > 21 and game['user_color'] == GREEN and game['circle_size'] == 25 and game['move_size'] == 25:
            setup_game()
        elif game['num_moves'] and game['user_color'] == GREEN and game['circle_size'] == 25 and game['move_size'] == 25:
            set_difficulty(None, 3)
            setup_game()

        if game['num_moves'] > 50 and game['user_color'] == GREEN and game['circle_size'] == 10 and game['move_size'] == 10:
            setup_game()
        elif game['num_moves'] and game['user_color'] == GREEN and game['circle_size'] == 10 and game['move_size'] == 10:
            set_difficulty(None, 4)
            setup_game()

        if game['num_moves'] and game['user_color'] == GREEN and game['circle_size'] == 7 and game['move_size'] == 7:
            set_difficulty(None, 5)

        # Checks for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_me = False


def menu(screen):
    """
    Displays the game menu
    :param screen: Surface object representing the game screen where the menu will be displayed
    :return: Menu
    """

    # Creates a menu object with the title 'Hot/Cold Game' and specified dimensions
    menu = pygame_menu.Menu('Hot/Cold Game', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    # Add a selector widget for selecting the game difficulty
    menu.add.selector('Difficulty :', [('Level 1', 1), ('Level 2', 2), ('Level 3', 3), ('Level 4', 4)],
                      onchange=set_difficulty)
    # Add a button to start playing the game
    menu.add.button('Play', play_game)
    # Add a button to quit the game
    menu.add.button('Quit', pygame_menu.events.EXIT)
    # Set the window caption
    pygame.display.set_caption('Hot Cold Game')

    return menu


def play_music():
    """
    Plays the background music
    :return: None
    """
    pygame.mixer.init()  # Initialize pygame.mixer
    pygame.mixer.music.load('Fluffing-a-Duck.mp3')  # Loads this file as the music
    pygame.mixer.music.set_volume(0.5)  # Sets the volume level to 50%
    pygame.mixer.music.play(loops=-1)  # Play the music on an infinite loop


def main():
    """
    Used for running the game as a whole
    :return: None
    """
    pygame.init()  # Initializes pygame
    play_music()  # Plays the music on infinite loop

    # Display the game menu and handle events

    menu_obj = menu(SCREEN)
    menu_obj.mainloop(SCREEN)

    pygame.quit()  # Quit pygame


if __name__ == '__main__':
    main()
