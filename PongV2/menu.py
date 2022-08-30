import pygame as pg
import webbrowser
pg.init()

HEADER_FONT = pg.font.SysFont("Freshman", 250)
BUTTON_FONT = pg.font.SysFont("Freshman", 100)


def draw_menu(win, width, height, color, event=pg.event.Event(pg.KEYUP)):

    win.fill(color["BLACK"])

    game_header_font = HEADER_FONT.render("PONG v2", True, color["WHITE"])
    sp_button_font = BUTTON_FONT.render("1 PLAYER", True, color["WHITE"])
    mp_button_font = BUTTON_FONT.render("2 PLAYER", True, color["WHITE"])
    help_button_font = BUTTON_FONT.render("HELP", True, color["WHITE"])
    quit_button_font = BUTTON_FONT.render("QUIT", True, color["WHITE"])

    padding = 10

    game_header_rect = pg.Rect(width//2 - game_header_font.get_width()//2,
                               height//4 - game_header_font.get_height()//2,
                               game_header_font.get_width() + 2*padding,
                               game_header_font.get_height() + padding)
    sp_button_rect = pg.Rect(width//2 - sp_button_font.get_width()//2 - padding,
                             game_header_rect.y + game_header_rect.height + padding,
                             sp_button_font.get_width() + 2*padding,
                             sp_button_font.get_height() + padding)
    mp_button_rect = pg.Rect(width//2 - mp_button_font.get_width()//2 - padding,
                             sp_button_rect.y + sp_button_rect.height + padding,
                             mp_button_font.get_width() + 2*padding,
                             mp_button_font.get_height() + padding)
    help_button_rect = pg.Rect(width//2 - help_button_font.get_width()//2 - padding,
                               mp_button_rect.y + mp_button_rect.height + padding,
                               help_button_font.get_width() + 2*padding,
                               help_button_font.get_height() + padding)
    quit_button_rect = pg.Rect(width//2 - quit_button_font.get_width()//2 - padding,
                               help_button_rect.y + help_button_rect.height + padding,
                               quit_button_font.get_width() + 2*padding,
                               quit_button_font.get_height() + padding)

    if game_header_rect.collidepoint(pg.mouse.get_pos()):
        game_header_font = HEADER_FONT.render("PONG v2", True, color["GREEN"])
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            webbrowser.open(r"https://github.com/itsDV7/PyGame_Projects")
    if sp_button_rect.collidepoint(pg.mouse.get_pos()):
        sp_button_font = BUTTON_FONT.render("1 PLAYER", True, color["RED"])
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            return "1"
    if mp_button_rect.collidepoint(pg.mouse.get_pos()):
        mp_button_font = BUTTON_FONT.render("2 PLAYER", True, color["RED"])
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            return "2"
    if help_button_rect.collidepoint(pg.mouse.get_pos()):
        help_button_font = BUTTON_FONT.render("HELP", True, color["RED"])
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            return "h"
    if quit_button_rect.collidepoint(pg.mouse.get_pos()):
        quit_button_font = BUTTON_FONT.render("QUIT", True, color["RED"])
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            return "q"
    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        return "q"

    win.blit(game_header_font, ((game_header_rect.x + padding), (game_header_rect.y + padding)))
    win.blit(sp_button_font, ((sp_button_rect.x + padding), (sp_button_rect.y + padding)))
    win.blit(mp_button_font, ((mp_button_rect.x + padding), (mp_button_rect.y + padding)))
    win.blit(help_button_font, ((help_button_rect.x + padding), (help_button_rect.y + padding)))
    win.blit(quit_button_font, ((quit_button_rect.x + padding), (quit_button_rect.y + padding)))

    pg.draw.circle(win, color["AQUA"], pg.mouse.get_pos(), 5)
