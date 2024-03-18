""""""

import pygame
import random
import sys
import pygame_menu

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 233, 0)
GREEN = (0, 128, 0)
GRAY = (128, 128, 128)

SCREEN_SIZE = 800
SCREEN = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

game = {
    'circle_size': 50,
    'move_size': 50,
    'previous_x': 0,
    'previous_y': 0,
    'user_x': SCREEN_SIZE / 2,
    'user_y': SCREEN_SIZE / 2,
    'hidden_x': 0,
    'hidden_y': 0,
    'user_color': WHITE,
    'hidden_color': BLACK,
    'num_moves': 0,
    'x': 0,
    'y': 0
}


# Global variable


def set_center_location():
    global game
    game['user_x'] = (SCREEN_SIZE - game['circle_size']) // 2
    game['user_y'] = (SCREEN_SIZE - game['circle_size']) // 2


def set_circle_color():
    global game

    overlap = game['circle_size'] * 2 - 10

    if abs(game['user_x'] - game['hidden_x']) < overlap and abs(game['user_y'] - game['hidden_y']) < overlap:
        game['hidden_color'] = YELLOW
        game['user_color'] = GREEN

    else:
        if game['previous_x'] != game['user_x']:
            if abs(game['previous_x'] - game['hidden_x']) > abs(game['user_x'] - game['hidden_x']):
                game['user_color'] = RED
            else:
                game['user_color'] = BLUE

        if game['previous_y'] != game['user_y']:
            if abs(game['previous_y'] - game['hidden_y']) > abs(game['user_y'] - game['hidden_y']):
                game['user_color'] = RED
            else:
                game['user_color'] = BLUE

    game['previous_x'] = game['user_x']
    game['previous_y'] = game['user_y']


def display_instructions():
    global game

    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Total moves = {game['num_moves']}", True, WHITE)
    SCREEN.blit(text, (10, 10))
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

    """game['hidden_x'] = random.randint(game['circle_size'] * 2, SCREEN_SIZE - game['circle_size'] * 2)
    game['hidden_y'] = random.randint(game['circle_size'] * 2, SCREEN_SIZE - game['circle_size'] * 2)
"""
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
        game['circle_size'], game['move_size'] = (4, 4)
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


def main():
    pygame.init()
    pygame.display.set_caption('Hot Cold Game')

    menu_obj = menu(SCREEN)
    menu_obj.mainloop(SCREEN)

    pygame.quit()


if __name__ == '__main__':
    main()
