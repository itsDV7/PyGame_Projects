import pygame as pg
from random import randint, choices, choice
import sys

# Pygame Settings
pg.init()
pg.event.set_blocked(pg.MOUSEMOTION)
pg.event.set_blocked(pg.MOUSEWHEEL)
pg.event.set_blocked(pg.MOUSEBUTTONUP)
pg.event.set_blocked(pg.MOUSEBUTTONDOWN)
pg.event.set_blocked(pg.ACTIVEEVENT)

# Defaults
WIDTH, HEIGHT = (1280, 720)
BOARD_WIDTH, BOARD_HEIGHT = (20, 100)
POWER_WIDTH, POWER_HEIGHT = (75, 75)
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("2 Player Pong! v2")
CLOCK = pg.time.Clock()
FPS = 60
COLOR = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREEN": (8, 255, 8),
    "GREEN2": (0, 255, 0),
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "PINK": (255, 105, 180),
    "GOLD": (255, 215, 0),
    "AQUA": (127, 255, 212)
}

# Userevents
SCORE_LEFT = pg.USEREVENT + 1
SCORE_RIGHT = pg.USEREVENT + 2
POWER_HIT = pg.USEREVENT + 3
DOUBLE_BALL = pg.USEREVENT + 4
REDUCE_SCORE_RIGHT = pg.USEREVENT + 5
REDUCE_SCORE_LEFT = pg.USEREVENT + 6
RIGHT_SHIELD = pg.USEREVENT + 7
LEFT_SHIELD = pg.USEREVENT + 8

# Fonts
SCORE_FONT = pg.font.SysFont("Freshman", 400)
SYMBOL_FONT = pg.font.SysFont("Freshman", 40)
PROMPT_FONT = pg.font.SysFont("Freshman", 100)
PROMPT_FONT2 = pg.font.SysFont("Freshman", 40)


class Board:
    # Class for Left and Right Boards
    VEL = 10

    def __init__(self, x, y, width, height):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.width = width
        self.height = self.initial_height = height
        self.vel = self.VEL

    # Draw Board
    def draw(self, win):
        board_pos = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(win, COLOR["WHITE"], board_pos)

    # Board Movement
    def move(self, up=False, down=False):
        if up and self.y - self.vel >= 0:
            self.y -= self.vel
        if down and self.y + self.height + self.vel <= HEIGHT:
            self.y += self.vel

    # Board Reset
    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.height = self.initial_height


class Ball:
    # Class for pong balls
    VEL = 5
    MAX_VEL = 10
    EX_VEL = 15

    def __init__(self, x, y, radius):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.radius = radius
        self.x_vel = choice([-1 * self.VEL, self.VEL])
        self.y_vel = randint(-5, 5)
        self.color = COLOR["GREEN"]

    # Draw pong balls
    def draw(self, win):
        ball_pos = (self.x, self.y)
        pg.draw.circle(win, self.color, ball_pos, self.radius)

    # Pong balls movement
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    # Reset pong balls
    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.x_vel = choice([-1 * self.VEL, self.VEL])
        self.y_vel = randint(-5, 5)
        self.color = COLOR["GREEN"]


class Powerups:
    # Class for powerups
    def __init__(self, x, y, win):
        self.x = x
        self.y = y
        self.win = win
        self.symbol = ""
        self.power_color = ""
        self.symbol_color = ""
        self.width = POWER_WIDTH
        self.height = POWER_HEIGHT

    # Expand -> + Board Length -> +
    def expand(self):
        self.symbol = "+"
        self.power_color = COLOR["GREEN2"]
        self.symbol_color = COLOR["PINK"]

    # Shrink -> - Board Length -> -
    def shrink(self):
        self.symbol = "-"
        self.power_color = COLOR["RED"]
        self.symbol_color = COLOR["RED"]

    # Slow Board -> Slow Opponent -> S
    def slow_board(self):
        self.symbol = "S"
        self.power_color = COLOR["GREEN2"]
        self.symbol_color = COLOR["PINK"]

    # Slow Ball -> Ball to Minimum speed -> 0
    def slow_ball(self):
        self.symbol = "0"
        self.power_color = COLOR["GREEN2"]
        self.symbol_color = COLOR["PINK"]

    # Extreme Ball -> Sudden Max Velocity -> Make ball Red -> F
    def extreme_ball(self):
        self.symbol = "F"
        self.power_color = COLOR["RED"]
        self.symbol_color = COLOR["RED"]

    # Double Ball -> Double the number of balls -> Switch y_vel -> D
    def double_ball(self):
        self.symbol = "D"
        self.power_color = COLOR["RED"]
        self.symbol_color = COLOR["RED"]

    # Golden Ability -> -1 Point -> G
    def golden(self):
        self.symbol = "G"
        self.power_color = COLOR["GOLD"]
        self.symbol_color = COLOR["GOLD"]

    # Shield -> Ball cant pass -> P
    def shield(self):
        self.symbol = "P"
        self.power_color = COLOR["GOLD"]
        self.symbol_color = COLOR["GOLD"]

    # Draw powerups
    def draw_powerup(self):
        outer_rect = pg.Rect(self.x, self.y, self.width, self.height)
        inner_rect = pg.Rect(self.x + 5, self.y + 5, self.width - 10, self.height - 10)
        inner_rect_x_middle = (self.x + 5 + inner_rect.width // 2)
        inner_rect_y_middle = (self.y + 5 + inner_rect.height // 2)
        symbol = SYMBOL_FONT.render(str(self.symbol), True, self.symbol_color)
        pg.draw.rect(self.win, self.power_color, outer_rect)
        pg.draw.rect(self.win, COLOR["WHITE"], inner_rect)
        self.win.blit(symbol, (inner_rect_x_middle - symbol.get_width()//2,
                               inner_rect_y_middle - symbol.get_height()//2))


class ApplyPowers:
    # Class to apply powerup effects
    def __init__(self, powerup_choice, ball, left_board, right_board):
        self.powerup_name = powerup_choice.__name__
        self.left_board = left_board
        self.right_board = right_board
        self.ball = ball

    # Apply the effect according to name
    def give(self):
        # Expand -> + Board Length -> +
        if self.powerup_name == "expand":
            if self.ball.x_vel >= 0:
                if self.left_board.height + 50 <= HEIGHT//2:
                    self.left_board.height += 50
            else:
                if self.right_board.height + 50 <= HEIGHT//2:
                    self.right_board.height += 50
        # Shrink -> - Board Length -> -
        if self.powerup_name == "shrink":
            if self.ball.x_vel >= 0:
                if self.left_board.height - 50 >= BOARD_HEIGHT:
                    self.left_board.height -= 50
                else:
                    if self.right_board.height - 50 >= BOARD_HEIGHT:
                        self.right_board.height -= 50
        # Slow Board -> Slow Opponent -> S
        if self.powerup_name == "slow_board":
            if self.ball.x_vel >= 0:
                self.left_board.vel -= 2
            else:
                self.right_board.vel -= 2
        # Slow Ball -> Ball to Minimum speed -> 0
        if self.powerup_name == "slow_ball":
            self.ball.x_vel = (self.ball.x_vel * self.ball.VEL) // abs(self.ball.x_vel)
            self.ball.y_vel = (self.ball.y_vel * self.ball.VEL) // abs(self.ball.y_vel)
        # Extreme Ball -> Sudden Max Velocity -> Make ball Red -> F
        if self.powerup_name == "extreme_ball":
            self.ball.x_vel = (self.ball.x_vel * self.ball.EX_VEL) // abs(self.ball.x_vel)
            self.ball.y_vel = (self.ball.y_vel * self.ball.EX_VEL) // abs(self.ball.y_vel)
            self.ball.color = COLOR["RED"]
        # Double Ball -> Double the number of balls -> Switch y_vel -> D
        if self.powerup_name == "double_ball":
            pg.event.post(pg.event.Event(DOUBLE_BALL))
        # Golden Ability -> -1 Point -> G
        if self.powerup_name == "golden":
            if self.ball.x_vel >= 0:
                pg.event.post(pg.event.Event(REDUCE_SCORE_LEFT))
            else:
                pg.event.post(pg.event.Event(REDUCE_SCORE_RIGHT))
        # Shield -> Ball cant pass -> P
        if self.powerup_name == "shield":
            if self.ball.x_vel >= 0:
                pg.event.post(pg.event.Event(LEFT_SHIELD))
            else:
                pg.event.post(pg.event.Event(RIGHT_SHIELD))


def handle_board_movement(keys, left_board, right_board):
    # Handles board movements
    if keys[pg.K_w]:
        left_board.move(up=True)
    if keys[pg.K_s]:
        left_board.move(down=True)
    if keys[pg.K_UP]:
        right_board.move(up=True)
    if keys[pg.K_DOWN]:
        right_board.move(down=True)


def reset_game(balls, boards):
    # Resets game to default
    for ball in balls:
        ball.reset()
    for board in boards:
        board.reset()


def handle_ball_collision(balls, left_board, right_board, right_shield, left_shield, keys):
    # Handles ball collision and speed
    for ball in balls:
        # Collision with Ceil and Floor
        if (ball.y - ball.radius <= 0) or (ball.y + ball.radius >= HEIGHT):
            ball.y_vel *= -1
        # Right board collision and speed
        if (ball.y + ball.radius >= right_board.y) and (ball.y - ball.radius <= right_board.y + right_board.height):
            if ball.x + ball.radius >= right_board.x:
                ball.x_vel = -1 * min(ball.MAX_VEL, abs(ball.x_vel) + 1)
                if keys[pg.K_UP]:
                    ball.y_vel = max(-1 * ball.MAX_VEL, -1 * (abs(ball.y_vel) + 1))
                elif keys[pg.K_DOWN]:
                    ball.y_vel = min(ball.MAX_VEL, abs(ball.y_vel) + 1)
                else:
                    if ball.y_vel >= 0:
                        ball.y_vel = min(ball.MAX_VEL, abs(ball.y_vel) + 1)
                    elif ball.y_vel < 0:
                        ball.y_vel = max(-1 * ball.MAX_VEL, -1 * (abs(ball.y_vel) + 1))
        # Left board collision and speed
        if (ball.y + ball.radius >= left_board.y) and (ball.y - ball.radius <= left_board.y + left_board.height):
            if ball.x - ball.radius <= left_board.x + left_board.width:
                ball.x_vel = min(ball.MAX_VEL, abs(ball.x_vel) + 1)
                if keys[pg.K_w]:
                    ball.y_vel = max(-1 * ball.MAX_VEL, -1 * (abs(ball.y_vel) + 1))
                elif keys[pg.K_s]:
                    ball.y_vel = min(ball.MAX_VEL, abs(ball.y_vel) + 1)
                else:
                    if ball.y_vel >= 0:
                        ball.y_vel = min(ball.MAX_VEL, abs(ball.y_vel) + 1)
                    elif ball.y_vel < 0:
                        ball.y_vel = max(-1 * ball.MAX_VEL, -1 * (abs(ball.y_vel) + 1))
        # Right shield collision
        if right_shield:
            if ball.x - ball.radius >= WIDTH:
                ball.x_vel = -1 * ball.x_vel
                pg.event.post(pg.event.Event(RIGHT_SHIELD))
        else:
            if ball.x - ball.radius >= WIDTH:
                left_board.reset()
                right_board.reset()
                pg.event.post(pg.event.Event(SCORE_LEFT))
        # Left shield collision
        if left_shield:
            if ball.x + ball.radius <= 0:
                ball.x_vel = -1 * ball.x_vel
                pg.event.post(pg.event.Event(LEFT_SHIELD))
        else:
            if ball.x + ball.radius <= 0:
                left_board.reset()
                right_board.reset()
                pg.event.post(pg.event.Event(SCORE_RIGHT))


def handle_powerup_collision(powerup, spawn_power, balls):
    # Handles collision of ball and powerups
    x = powerup.x
    y = powerup.y
    width = powerup.width
    height = powerup.height
    powerup_pos = [
        (x, y),
        (x+width, y),
        (x, y+height),
        (x+width, y+height),
        (x+(width//2), y),
        (x, y+(height//2)),
        (x+width, y+(height//2)),
        (x+(width//2), y+height)
    ]

    if spawn_power:
        for ball in balls:
            collide = False
            for pos in powerup_pos:
                if (((ball.x - pos[0])**2) + ((ball.y - pos[1])**2)) <= (ball.radius**2):
                    pg.event.post(pg.event.Event(POWER_HIT))
                    collide = True
                    break
                elif (x <= ball.x <= (x + width)) and (y <= ball.y <= (y + height)):
                    pg.event.post(pg.event.Event(POWER_HIT))
                    collide = True
                    break
            if collide:
                return ball


def powerup_randomizer():
    # Generates a random position for powerup to spawn
    powerup_x = randint(WIDTH // 4 - POWER_WIDTH, (WIDTH // 2 + WIDTH // 4) - POWER_WIDTH)
    powerup_y = randint(0, HEIGHT - POWER_HEIGHT)
    powerup = Powerups(powerup_x, powerup_y, WIN)
    powerup_list = [
        powerup.expand,
        powerup.shrink,
        powerup.slow_board,
        powerup.slow_ball,
        powerup.extreme_ball,
        powerup.double_ball,
        powerup.golden,
        powerup.shield
    ]
    powerup_weights = [
        50,
        50,
        20,
        30,
        15,
        20,
        1,
        10
    ]
    powerup_choice = choices(powerup_list, powerup_weights)
    return powerup, powerup_x, powerup_y, powerup_choice


def draw_dashed_line(win, color, start_pos, end_pos, width):
    # Draw dashed line in the middle of screen
    for i in range(start_pos, end_pos-5, 5):
        if i % 2 == 0:
            continue
        dash = pg.Rect(WIDTH//2 - width//2, i, width, 5)
        pg.draw.rect(win, color, dash)


def draw_assets(win, boards, balls, score_left, score_right, spawn_power,
                powerup_choice, powerup, right_shield, left_shield, winner, countdown, game_start):
    # Draw all assets of the game
    win.fill(COLOR["BLACK"])
    draw_dashed_line(win, COLOR["WHITE"], 0, HEIGHT, 5)

    # Renders
    left_score_text = SCORE_FONT.render(str(score_left), True, COLOR["WHITE"])
    right_score_text = SCORE_FONT.render(str(score_right), True, COLOR["WHITE"])
    winner_text = PROMPT_FONT.render(str(winner), True, COLOR["GOLD"])
    countdown_text = PROMPT_FONT.render(f"Starts in... {str(countdown)}", True, COLOR["GOLD"])
    help_text = PROMPT_FONT2.render("Press R to Restart Game.", True, COLOR["GOLD"])
    help_text2 = PROMPT_FONT2.render("Press any key / Move mouse to start!", True, COLOR["GOLD"])
    right_shield_rect = pg.Rect(WIDTH - 2, 0, 2, HEIGHT)
    left_shield_rect = pg.Rect(0, 0, 2, HEIGHT)
    # Draw scores
    win.blit(left_score_text,
             (WIDTH // 4 - left_score_text.get_width() // 2,
              HEIGHT // 2 - left_score_text.get_height() // 2))
    win.blit(right_score_text,
             (WIDTH//2 + WIDTH // 4 - right_score_text.get_width() // 2,
              HEIGHT // 2 - right_score_text.get_height() // 2))
    # Draw right shields
    if right_shield:
        pg.draw.rect(win, COLOR["AQUA"], right_shield_rect)
    # Draw left shields
    if left_shield:
        pg.draw.rect(win, COLOR["AQUA"], left_shield_rect)
    # Draw boards
    for board in boards:
        board.draw(win)
    # Draw balls
    for ball in balls:
        ball.draw(win)
    # Draw powerups
    if spawn_power:
        if powerup_choice:
            powerup_choice[0]()
            powerup.draw_powerup()
    # Show countdown
    if countdown != 0 and not game_start:
        win.blit(countdown_text, ((WIDTH//2 - countdown_text.get_width()//2),
                                  (HEIGHT//2 - countdown_text.get_height()//2)))
    # Show winner
    if winner:
        win.blit(winner_text, ((WIDTH//2 - winner_text.get_width()//2),
                               (HEIGHT//2 - winner_text.get_height()//2)))
        win.blit(help_text, ((WIDTH//2 - help_text.get_width()//2),
                             (HEIGHT//2 + winner_text.get_height() - help_text.get_height()//2)))
        reset_game(balls, boards)
    # Show start game countdown
    if game_start:
        win.blit(help_text2, ((WIDTH//2 - help_text2.get_width()//2), (HEIGHT//2 - help_text2.get_height()//2)))
    pg.display.update()


def main():
    # Main
    run = True
    # Boards
    left_board = Board(0, HEIGHT // 2 - BOARD_HEIGHT // 2, BOARD_WIDTH, BOARD_HEIGHT)
    right_board = Board(WIDTH - BOARD_WIDTH, HEIGHT // 2 - BOARD_HEIGHT // 2, BOARD_WIDTH, BOARD_HEIGHT)
    boards = [left_board, right_board]
    # Pong balls
    ball = Ball(WIDTH//2, HEIGHT//2, 10)
    balls = [ball]
    num_balls = len(balls)
    # Scores
    score_left = 0
    score_right = 0
    # Timers and conditions
    countdown_time = powerup_time = current_time = pg.time.get_ticks()
    spawn_power = False
    powerup_choice = None
    powerup = None
    hit_ball = None
    right_shield = False
    left_shield = False
    winner = ""
    win_score = 1
    countdown = 3
    game_start = True
    # Start with any key
    draw_assets(WIN, boards, balls, score_left, score_right, spawn_power,
                powerup_choice, powerup, right_shield, left_shield, winner, countdown, game_start)
    pg.time.delay(500)
    pg.event.get()
    pg.event.wait()
    game_start = False
    # Main game loop
    while run:
        CLOCK.tick(FPS)
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                run = False
                continue
            # Score increase left side
            if event.type == SCORE_LEFT:
                score_left += 1
                powerup_time = current_time
                spawn_power = False
                if score_left < win_score:
                    countdown_time = current_time
                    countdown = 3
                while len(balls) > 1:
                    balls.pop()
                for ball in balls:
                    ball.reset()
            # Score increase right side
            if event.type == SCORE_RIGHT:
                score_right += 1
                powerup_time = current_time
                spawn_power = False
                if score_right < win_score:
                    countdown_time = current_time
                    countdown = 3
                while len(balls) > 1:
                    balls.pop()
                for ball in balls:
                    ball.reset()
            # If ball hits powerup
            if event.type == POWER_HIT:
                powerup_time = current_time
                spawn_power = False
                num_balls = len(balls)
                apply_powers = ApplyPowers(powerup_choice[0], hit_ball, left_board, right_board)
                apply_powers.give()
            # If ball hits Double Ball powerup
            if event.type == DOUBLE_BALL:
                if num_balls <= 2:
                    for i in range(num_balls):
                        new_ball = Ball(balls[i].x, balls[i].y, balls[i].radius)
                        new_ball.x_vel = -1 * balls[i].x_vel
                        new_ball.y_vel = balls[i].y_vel
                        balls.append(new_ball)
            # If ball hits golden powerup from right
            if event.type == REDUCE_SCORE_RIGHT:
                if score_right:
                    score_right -= 1
                powerup_time = current_time
                spawn_power = False
            # If ball hits golden powerup from left
            if event.type == REDUCE_SCORE_LEFT:
                if score_left:
                    score_left -= 1
                powerup_time = current_time
                spawn_power = False
            # If ball hits right shield
            if event.type == RIGHT_SHIELD:
                right_shield = True ^ right_shield
            # If ball hits left shield
            if event.type == LEFT_SHIELD:
                left_shield = True ^ left_shield
        # Powerups spawn timer
        current_time = pg.time.get_ticks()
        time_elapsed = current_time - powerup_time
        if time_elapsed >= 10000:
            spawn_power = True ^ spawn_power
            powerup_time = current_time
        if not spawn_power:
            powerup, powerup_x, powerup_y, powerup_choice = powerup_randomizer()

        draw_assets(WIN, boards, balls, score_left, score_right, spawn_power,
                    powerup_choice, powerup, right_shield, left_shield, winner, countdown, game_start)
        # Countdown
        if countdown > 0:
            if current_time - countdown_time >= 1000:
                countdown -= 1
                countdown_time = current_time
            powerup_time = current_time
            continue

        handle_board_movement(keys, left_board, right_board)
        # Winner prompts
        if winner:
            pg.time.delay(3000)
            while winner:
                win_event = pg.event.wait()
                if win_event.type == pg.KEYDOWN and (win_event.key == pg.K_r or win_event.key == pg.K_ESCAPE):
                    if win_event.key == pg.K_ESCAPE:
                        run = False
                        break
                    main()
        # Score prompts
        if score_right >= win_score:
            winner = "RIGHT WINS!"
            spawn_power = False
            powerup_time = current_time
        elif score_left >= win_score:
            winner = "LEFT WINS!"
            spawn_power = False
            powerup_time = current_time

        for ball in balls:
            ball.move()

        handle_ball_collision(balls, left_board, right_board, right_shield, left_shield, keys)

        hit_ball = handle_powerup_collision(powerup, spawn_power, balls)

    pg.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
