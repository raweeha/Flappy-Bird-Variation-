import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 720
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_width))

pygame.display.set_caption("Flappy Pika")

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colour
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 200
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

#load images
bg = pygame.image.load('gamebg.jpg')
ground_img = pygame.image.load('gamegroundsprite.png')

def draw_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    screen.blit(img, (x,y))

class Kurp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        kurpsprite = pygame.image.load('kurapika-face.png')
        self.image = pygame.transform.scale(kurpsprite, (85,85))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 610:
                self.rect.y += int(self.vel)

        if game_over == False:
            #jumping
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

class Eyes(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Kurtapipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        #delete pipe once it goes off screen
        if self.rect.right < 0:
            self.kill()

kurp_group = pygame.sprite.Group()

eyes_group = pygame.sprite.Group()

kurapika = Kurp(100, int(screen_height / 2))

kurp_group.add(kurapika)

run = True
while run:

    clock.tick(fps)
    #draw background
    screen.blit(bg, (0,0))
    #bird
    kurp_group.draw(screen)
    kurp_group.update()
    eyes_group.draw(screen)

    #draw ground
    screen.blit(ground_img, (ground_scroll, 600))

    # check the score
    if len(eyes_group) > 0:
        if kurp_group.sprites()[0].rect.left > eyes_group.sprites()[0].rect.left \
                and kurp_group.sprites()[0].rect.right < eyes_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if kurp_group.sprites()[0].rect.left > eyes_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    print(score)
    draw_text(str(score), font, white, int(screen_width / 2), 20)

    #look for collision
    if pygame.sprite.groupcollide(kurp_group, eyes_group, False, False) or kurapika.rect.top < 0:
        game_over = True
    #check if kurapika has hit the ground
    if kurapika.rect.bottom >= 610:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-50,50)
            btm_pipe = Eyes(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Eyes(screen_width, int(screen_height / 2) + pipe_height, 1)
            eyes_group.add(btm_pipe)
            eyes_group.add(top_pipe)
            last_pipe = time_now

        #draw and scroll ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 375:
            ground_scroll=0

        eyes_group.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True
    pygame.display.update()
pygame.quit()
