import pygame as pg
from random import randint
import numpy as np

pg.init()

WIDTH, HEIGHT = (1000, 700)
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("2 Player Pong!")

FPS = 60
CLOCK = pg.time.Clock()
START_TIME = pg.time.get_ticks()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (8, 255, 8)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BOARD_SPEED = 10
BALL_SPEED = 8
LEFT_BOARD = pg.Rect(0, HEIGHT//2 - 75//2, 10, 75)
RIGHT_BOARD = pg.Rect(WIDTH - 10, HEIGHT//2 - 75//2, 10, 75)
BALL = pg.Rect(WIDTH//2 - 20//2, HEIGHT//2 - 20//2, 15, 15)
POWER_RECT = pg.Rect(-15, -15, 50, 50)
BALL_DIRECTION = [randint(0, 1), randint(0, 1)]
SCORE_LEFT = pg.USEREVENT + 1
SCORE_RIGHT = pg.USEREVENT + 2
POWER = pg.USEREVENT + 3
HIT_RIGHT = pg.USEREVENT + 4
HIT_LEFT = pg.USEREVENT + 5
HIT_POWER = pg.USEREVENT + 6
SCORE_FONT = pg.font.SysFont("Freshman", 400)
WINNER_FONT = pg.font.SysFont("Freshman", 100)


def handle_left_board_movement(key_pressed, left_board):
    if key_pressed[pg.K_w] and left_board.y - BOARD_SPEED > 0:
        left_board.y -= BOARD_SPEED
    if key_pressed[pg.K_s] and left_board.y + left_board.height + BOARD_SPEED < HEIGHT:
        left_board.y += BOARD_SPEED


def handle_right_board_movement(key_pressed, right_board):
    if key_pressed[pg.K_UP] and right_board.y - BOARD_SPEED > 0:
        right_board.y -= BOARD_SPEED
    if key_pressed[pg.K_DOWN] and right_board.y + right_board.height + BOARD_SPEED < HEIGHT:
        right_board.y += BOARD_SPEED


def handle_ball_logic():
    if BALL_DIRECTION[0] == 0:
        BALL.x -= BALL_SPEED
    if BALL_DIRECTION[0] == 1:
        BALL.x += BALL_SPEED
    if BALL_DIRECTION[1] == 0:
        BALL.y -= BALL_SPEED
    if BALL_DIRECTION[1] == 1:
        BALL.y += BALL_SPEED
    if BALL.y <= 0:
        BALL_DIRECTION[1] = 1
    if BALL.y + BALL.height >= HEIGHT:
        BALL_DIRECTION[1] = 0
    if BALL.x <= 0:
        pg.event.post(pg.event.Event(SCORE_RIGHT))
        BALL.x, BALL.y = WIDTH//2 - 20//2, HEIGHT//2 - 20//2
        LEFT_BOARD.x, LEFT_BOARD.y = 0, HEIGHT // 2 - 75 // 2
        RIGHT_BOARD.x, RIGHT_BOARD.y = WIDTH - 10, HEIGHT // 2 - 75 // 2
        LEFT_BOARD.height = 75
        RIGHT_BOARD.height = 75
    if BALL.x + BALL.width >= WIDTH:
        pg.event.post(pg.event.Event(SCORE_LEFT))
        BALL.x, BALL.y = WIDTH // 2 - 20 // 2, HEIGHT // 2 - 20 // 2
        LEFT_BOARD.x, LEFT_BOARD.y = 0, HEIGHT // 2 - 75 // 2
        RIGHT_BOARD.x, RIGHT_BOARD.y = WIDTH - 10, HEIGHT // 2 - 75 // 2
        LEFT_BOARD.height = 75
        RIGHT_BOARD.height = 75
    if LEFT_BOARD.colliderect(BALL):
        BALL_DIRECTION[0] = 1
        pg.event.post(pg.event.Event(HIT_LEFT))
    if RIGHT_BOARD.colliderect(BALL):
        BALL_DIRECTION[0] = 0
        pg.event.post(pg.event.Event(HIT_RIGHT))


def draw_assets(score_left, score_right, spawn_power, power_x, power_y):
    SCREEN.fill(BLACK)
    left_score_text = SCORE_FONT.render(str(score_left), True, WHITE)
    right_score_text = SCORE_FONT.render(str(score_right), True, WHITE)
    SCREEN.blit(left_score_text,
                (WIDTH//2 + WIDTH//4 - left_score_text.get_width()//2,
                 HEIGHT//2 - left_score_text.get_height()//2))
    SCREEN.blit(right_score_text,
                (WIDTH // 4 - right_score_text.get_width() // 2,
                 HEIGHT // 2 - right_score_text.get_height() // 2))
    pg.draw.rect(SCREEN, WHITE, LEFT_BOARD)
    pg.draw.rect(SCREEN, WHITE, RIGHT_BOARD)
    pg.draw.rect(SCREEN, GREEN, BALL)
    draw_line_dashed(SCREEN, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    if spawn_power:
        POWER_RECT.x = power_x
        POWER_RECT.y = power_y
        pg.draw.rect(SCREEN, YELLOW, POWER_RECT)
        if BALL.colliderect(POWER_RECT):
            pg.event.post(pg.event.Event(HIT_POWER))


def declare_winner(winner_text):
    text = WINNER_FONT.render(winner_text, True, RED)
    SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pg.display.flip()
    pg.time.delay(5000)


def draw_line_dashed(surface, color, start_pos, end_pos, width=1, dash_length=10, exclude_corners=True):
    start_pos = np.array(start_pos)
    end_pos = np.array(end_pos)
    length = np.linalg.norm(end_pos - start_pos)
    dash_amount = int(length / dash_length)
    dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()
    return [pg.draw.line(surface, color, tuple(dash_knots[n]), tuple(dash_knots[n+1]), width)
            for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]


def main():
    score_right = 0
    score_left = 0
    score_change = False
    run = True
    pg.time.set_timer(POWER, 5000)
    spawn_power = False
    power_x = 0
    power_y = 0
    hit_left = False
    hit_right = False
    while run:
        CLOCK.tick(FPS)
        pg.display.update()
        if score_change:
            pg.time.delay(1000)
            score_change = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == SCORE_RIGHT:
                score_left += 1
                score_change = True
            if event.type == SCORE_LEFT:
                score_right += 1
                score_change = True
            if event.type == POWER:
                if spawn_power:
                    spawn_power = False
                else:
                    spawn_power = True
                    power_x = randint(WIDTH // 4, WIDTH // 2 + WIDTH // 4)
                    power_y = randint(0, HEIGHT - 50)
            if event.type == HIT_LEFT:
                hit_left = True
                hit_right = False
            if event.type == HIT_RIGHT:
                hit_left = False
                hit_right = True
            if event.type == HIT_POWER and hit_left:
                if LEFT_BOARD.height + 50 < WIDTH//4:
                    LEFT_BOARD.height += 50
                spawn_power = False
            if event.type == HIT_POWER and hit_right:
                if RIGHT_BOARD.height + 50 < WIDTH//4:
                    RIGHT_BOARD.height += 50
                spawn_power = False
        winner = ""
        if score_right >= 5:
            winner = "PLAYER 1 WINS!"
        if score_left >= 5:
            winner = "PLAYER 2 WINS!"
        key_pressed = pg.key.get_pressed()
        handle_left_board_movement(key_pressed, LEFT_BOARD)
        handle_right_board_movement(key_pressed, RIGHT_BOARD)
        handle_ball_logic()
        draw_assets(score_left, score_right, spawn_power, power_x, power_y)
        if winner:
            declare_winner(winner)
            break
    if run:
        main()
    else:
        pg.quit()


if __name__ == "__main__":
    main()
