import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import sys
import pygame
import threading
from Buttons import ToggleButton as TB

def main():
    pygame.init()

    screen = pygame.display.set_mode((900,1000))
    pygame.display.set_caption('Nishant\'s Tic Tac Toe Game')
    background = pygame.Surface((900, 900))

    clock = pygame.time.Clock()

    main_screen(screen, background, clock)
    

def main_screen(screen, background, clock):
    script_dir = os.path.dirname(__file__)
    font = pygame.font.Font(os.path.join(script_dir, './assets/font/Roboto-Bold.ttf'), 40)
    title_font = pygame.font.Font(os.path.join(script_dir, './assets/font/Roboto-Bold.ttf'), 80)

    play_button = TB(background, (210,210,210), (200,200,200), (270, 420, 360, 60), font)
    play_button.change_value('Play')
    button_rect = pygame.Rect(270, 420, 360, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit(0)
        
        if pygame.mouse.get_pressed()[0]:
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                game(screen, background, clock)
                
        screen.fill((255, 255, 255))
        background.fill((255,255,255))
        play_button.update(update_button)
        play_button.draw(draw_button, [])
        title_surface_1 = title_font.render('Nishant\'s', True, (0,0,0)); title_rect_1 = title_surface_1.get_rect(center = (450, 100))
        title_surface_2 = title_font.render('Tic Tac Toe', True, (0,0,0)); title_rect_2 = title_surface_2.get_rect(center = (450, 180))
        title_surface_3 = title_font.render('Game', True, (0,0,0)); title_rect_3 = title_surface_3.get_rect(center = (450, 260))
        background.blit(title_surface_1, title_rect_1)
        background.blit(title_surface_2, title_rect_2)
        background.blit(title_surface_3, title_rect_3)
        
        screen.blit(background, (0,0))
        pygame.display.update()
        clock.tick(120)

def game(screen, background, clock):
    # Fonts
    script_dir = os.path.dirname(__file__)
    font = pygame.font.Font(os.path.join(script_dir, './assets/font/Roboto-Bold.ttf'), 250)
    win_font = pygame.font.Font(os.path.join(script_dir, './assets/font/Roboto-Bold.ttf'), 40)

    # Buttons
    buttons = []
    for x in range(0, 601, 300):
        for y in range(0, 601, 300):
            temp = TB(background, (255, 255, 255), (200, 200, 200), (x, y, 300, 300), font)
            temp.coords = (x // 300, y // 300)
            buttons.append(temp)

    board = TTT_Board()

    winner = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_r:
                    board = TTT_Board()

        background.fill((255,255,255))
        screen.fill((0,0,0))
    
        for button in buttons: button.update(update_button)

        if winner == '':
            for button in buttons:
                if button.double_clicked:
                    board.move(button.coords[0], button.coords[1])
                    button.double_clicked = False
                    button.clicked = False
                button.change_value(board.board[button.coords[0]][button.coords[1]])
        else:
            font_surface = win_font.render(f'{winner} won!', True, (255,255,255))
            font_rect = font_surface.get_rect(center = (450, 950))
            screen.blit(font_surface, font_rect)

        winner, points = board.check_win()

        for button in buttons: button.draw(draw_button, points)

        for x in [295, 595]:
            pygame.draw.rect(background, (0,0,0), (x, 0, 10, 900))
            pygame.draw.rect(background, (0,0,0), (0, x, 900, 10))

        screen.blit(background, (0,0))
        pygame.display.update()
        clock.tick(120)

class TTT_Board():
    def __init__(self):
        self.board = [[' ' for i in range(3)] for j in range(3)]
        self.player_1 = True
        self.winner = ''
    
    def __str__(self):
        result = ''
        for row in self.board:
            for col in row:
                result += col + '\t'
            result += '\n'
        return result

    def move(self, row, col):
        if self.board[row][col] == ' ':
            if self.player_1:
                self.board[row][col] = 'X'
            else:
                self.board[row][col] = 'O'

            self.player_1 = not(self.player_1)

    def check_win(self):
        for row in range(3):
            count = {'X': 0, 'O': 0, ' ' : 0}
            points = []
            for col in range(3):
                count[self.board[row][col]] += 1
                points.append((row, col))
            if count['X'] == 3:
                return 'Player 1', points
            elif count['O'] == 3:
                return 'Player 2', points

        for col in range(3):
            points = []
            count = {'X': 0, 'O': 0, ' ' : 0}
            for row in range(3):
                count[self.board[row][col]] += 1
                points.append((row, col))
            if count['X'] == 3:
                return 'Player 1', points
            elif count['O'] == 3:
                return 'Player 2', points

        count_back = {'X': 0, 'O': 0, ' ' : 0}
        points_back = []
        count_for = {'X': 0, 'O': 0, ' ' : 0}
        points_front = []
        for row in range(3):
            for col in range(3):
                if row == col:
                    count_back[self.board[row][col]] += 1
                    points_back.append((row, col))
                if row + col == 2:
                    count_for[self.board[row][col]] += 1
                    points_front.append((row, col))

        if count_back['X'] == 3:
            return 'Player 1', points_back
        elif count_back['O'] == 3:
            return 'Player 2', points_back

        if count_for['X'] == 3:
            return 'Player 1', points_front
        elif count_for['O'] == 3:
            return 'Player 2', points_front

        return '', []

def draw_button(self, *args):
    if self.is_hovering:
            pygame.draw.rect(self.surface, self.hover_color, self.rect)
    else:
        pygame.draw.rect(self.surface, self.colors, self.rect)
    if self.clicked:
        pygame.draw.rect(self.surface, (255, 255, 0), self.rect)
    for point in args[0]:
        if point == self.coords:
            pygame.draw.rect(self.surface, (0, 255, 0), self.rect)
    font_surface = self.font.render(self.value if self.value != '' else ' ', True, (0,0,0))
    font_rect = font_surface.get_rect(center = (self.rect[0] + self.rect[2]//2, self.rect[1] + self.rect[3]//2))
    self.surface.blit(font_surface, font_rect)

def update_button(self):
    val = pygame.mouse.get_pos()
    x,y = val
    if pygame.mouse.get_pressed()[0]:
        if self.rect[0] < x < self.rect[0] + self.rect[2]:
            if self.rect[1] < y < self.rect[1] + self.rect[3]:
                if self.clicked and self.unclicked:
                    self.double_clicked = True
                    self.unclicked = False
                else:
                    self.clicked = True
            else:
                self.clicked = False
                self.double_clicked = False
        else:
            self.clicked = False
            self.double_clicked = False
    else:
        self.unclicked = False
        if self.clicked:
            self.unclicked = True
    self.hover(val)

if __name__=='__main__':
    main()