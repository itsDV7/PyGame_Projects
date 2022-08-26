from main import Powerups
import pygame as pg
pg.init()

HELP_FONT = pg.font.SysFont("Freshman", 50)
BUTTON_FONT = pg.font.SysFont("Freshman", 100)


def draw_help(win, width, height, color, event=pg.event.Event(pg.KEYUP)):

    win.fill(color["BLACK"])

    padding = 10

    expand_block = Powerups(width // 32, height//32, win)
    expand_block.expand()
    expand_block.draw_powerup()

    shrink_block = Powerups(width // 32, expand_block.y + expand_block.height + padding, win)
    shrink_block.shrink()
    shrink_block.draw_powerup()

    slow_board_block = Powerups(width // 32, shrink_block.y + shrink_block.height + padding, win)
    slow_board_block.slow_board()
    slow_board_block.draw_powerup()

    slow_ball_block = Powerups(width // 32, slow_board_block.y + slow_board_block.height + padding, win)
    slow_ball_block.slow_ball()
    slow_ball_block.draw_powerup()

    extreme_ball_block = Powerups(width // 32, slow_ball_block.y + slow_ball_block.height + padding, win)
    extreme_ball_block.extreme_ball()
    extreme_ball_block.draw_powerup()

    double_ball_block = Powerups(width // 32, extreme_ball_block.y + extreme_ball_block.height + padding, win)
    double_ball_block.double_ball()
    double_ball_block.draw_powerup()

    golden_block = Powerups(width // 32, double_ball_block.y + double_ball_block.height + padding, win)
    golden_block.golden()
    golden_block.draw_powerup()

    shield_block = Powerups(width // 32, golden_block.y + golden_block.height + padding, win)
    shield_block.shield()
    shield_block.draw_powerup()

    expand_text = "Expand - Increase paddle length by few pixels"
    shrink_text = "Shrink - Reduce paddle length by few pixels"
    slow_board_text = "Slow Board - Reduce opponent paddle movement speed"
    slow_ball_text = "Slow Ball - Reduce ball speed to default"
    extreme_ball_text = "Extreme Ball - Increase ball speed above maximum"
    double_ball_text = "Double Ball - Doubles the number of ball on screen (Max: 4)"
    golden_text = "Golden Ability - Reduce opponent score by 1"
    shield_text = "Shield - Activate shield that saves 1 fall"

    expand_block_font = HELP_FONT.render(expand_text, True, color["WHITE"])
    shrink_block_font = HELP_FONT.render(shrink_text, True, color["WHITE"])
    slow_board_block_font = HELP_FONT.render(slow_board_text, True, color["WHITE"])
    slow_ball_block_font = HELP_FONT.render(slow_ball_text, True, color["WHITE"])
    extreme_ball_block_font = HELP_FONT.render(extreme_ball_text, True, color["WHITE"])
    double_ball_block_font = HELP_FONT.render(double_ball_text, True, color["WHITE"])
    golden_block_font = HELP_FONT.render(golden_text, True, color["WHITE"])
    shield_block_font = HELP_FONT.render(shield_text, True, color["WHITE"])

    win.blit(expand_block_font, ((expand_block.x + expand_block.width + padding),
                                 (expand_block.y + expand_block.height//2 - expand_block_font.get_height()//2)))
    win.blit(shrink_block_font, ((shrink_block.x + shrink_block.width + padding),
                                 (shrink_block.y + shrink_block.height // 2 - shrink_block_font.get_height() // 2)))
    win.blit(slow_board_block_font,
             ((slow_board_block.x + slow_board_block.width + padding),
              (slow_board_block.y + slow_board_block.height // 2 - slow_board_block_font.get_height() // 2)))
    win.blit(slow_ball_block_font,
             ((slow_ball_block.x + slow_ball_block.width + padding),
              (slow_ball_block.y + slow_ball_block.height // 2 - slow_ball_block_font.get_height() // 2)))
    win.blit(extreme_ball_block_font,
             ((extreme_ball_block.x + extreme_ball_block.width + padding),
              (extreme_ball_block.y + extreme_ball_block.height // 2 - extreme_ball_block_font.get_height() // 2)))
    win.blit(double_ball_block_font,
             ((double_ball_block.x + double_ball_block.width + padding),
              (double_ball_block.y + double_ball_block.height // 2 - double_ball_block_font.get_height() // 2)))
    win.blit(golden_block_font, ((golden_block.x + golden_block.width + padding),
                                 (golden_block.y + golden_block.height // 2 - golden_block_font.get_height() // 2)))
    win.blit(shield_block_font, ((shield_block.x + shield_block.width + padding),
                                 (shield_block.y + shield_block.height // 2 - shield_block_font.get_height() // 2)))

    back_button_font = BUTTON_FONT.render("BACK", True, color["WHITE"])
    back_button_rect = pg.Rect(width - back_button_font.get_width() - 4*padding,
                               height - back_button_font.get_height() - 4*padding,
                               back_button_font.get_width() + 2*padding,
                               back_button_font.get_height() + padding)
    if back_button_rect.collidepoint(pg.mouse.get_pos()):
        back_button_font = BUTTON_FONT.render("BACK", True, color["RED"])
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            return True

    win.blit(back_button_font, ((back_button_rect.x + padding), (back_button_rect.y + padding)))

    pg.draw.circle(win, color["AQUA"], pg.mouse.get_pos(), 5)
