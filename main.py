import pygame, sys
from pygame.locals import QUIT
from pygame import MOUSEBUTTONDOWN
from pygame import USEREVENT
from datetime import datetime

pygame.init()
size = 1
FPS = 100
width = 640*size
height = 480*size
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("test")
screen.fill(black)
move = True
clock = pygame.time.Clock()
mouse_x = 0
mouse_y = 0
start = False
score_value = 0
hit_point_value = 3
end = False

class Paddle(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
    def move(self):
        self.rect.bottom = height * 3 / 4
        self.rect.left = mouse_x  - self.width / 2

paddle = Paddle(80*size,5*size)

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, speed):
        self.radius = radius
        self.rect = pygame.Rect(0, 0 ,self.radius, self.radius)
        self.speed = speed
        
    def move(self):
        self.rect.top += self.speed[0]
        self.rect.left += self.speed[1]
        if self.rect.left < 0 or self.rect.right > width :
            self.speed[1] = self.speed[1] * -1
        if self.rect.top < 0 or self.rect.bottom > height :
            self.speed[0] = self.speed[0] * -1
        
ball = Ball(8.5*size, [4*size, 4*size])

class Brick(pygame.sprite.Sprite):
    def __init__(self):
        self.rect_array = []
        for i in range(10):
            for j in range(10):
                self.rect_array.append([i*60*size+20*size, j*20*size,53*size,16*size])

    def draw(self):
        global score_value

        for i in brick.rect_array:
            pygame.draw.rect(screen, white, i, 0)
        for i in brick.rect_array :
            if ball.rect.colliderect(i) == 1 :
                ball.speed[0] = ball.speed[0] * -1
                score_value += 1
                brick.rect_array.remove(i)

brick = Brick()

class Score():
    def __init__(self):
        self.FontSet = pygame.font.SysFont(None , 40*size)
        self.text = self.FontSet.render("score:"+ str(score_value), True, white)
        self.rect = self.text.get_rect()
        self.rect.center = (100*size,400*size)

class HitPoint():
    def __init__(self, value, width, height, position_x):
        self.width = width
        self.height = height
        self.value = value
        self.raw_image = pygame.image.load("heart.png").convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (position_x, 440*size)

    def update(self):
        if hit_point_value == 1:
            screen.blit(hit_point1.image, hit_point1.rect)
        if hit_point_value == 2:
            screen.blit(hit_point2.image, hit_point2.rect)
            screen.blit(hit_point1.image, hit_point1.rect)
        if hit_point_value == 3:
            screen.blit(hit_point3.image, hit_point3.rect)
            screen.blit(hit_point2.image, hit_point2.rect)
            screen.blit(hit_point1.image, hit_point1.rect)

hit_point1 = HitPoint(hit_point_value, 20*size, 20*size, 560*size)
hit_point2 = HitPoint(hit_point_value, 20*size, 20*size, 590*size)
hit_point3 = HitPoint(hit_point_value, 20*size, 20*size, 620*size)

def score_record(score):
    with open("score.txt", "r") as file:
        content = []
        for line in file.readlines():
            content.append(line)
    with open("score.txt", "w") as file:
        score_list = []
        time = str(datetime.now())[0:-7]
        content.append(time +", score = " + str(score_value)+ "\n")
        file.writelines(content)

    highest = 0

    for score in content:
        score = score[28:-1]
        score = int(score)
        score_list.append(score)

    highest = max(score_list)

    return highest

while not end:
    screen.fill(black)
    clock.tick(FPS)
    RESET_EVENT = USEREVENT + 1
    END_EVENT = USEREVENT + 2
    mouse_x = pygame.mouse.get_pos()[0]
    paddle.move()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN :
            start = True
        elif event.type == RESET_EVENT:
            ball.rect.bottomleft = (mouse_x - ball.radius, paddle.rect.top)
            start = False
        elif event.type == END_EVENT:
            end = True
            print(score_record(score_value))

    if start == True:
        ball.move()

    else:
        ball.rect.bottomleft = (mouse_x - ball.radius, paddle.rect.top - ball.radius/2)

    brick.draw()

    if ball.rect.colliderect(paddle.rect) == True:
        ball.speed[0] = ball.speed[0] * -1

    if ball.rect.bottom >= height:
        hit_point_value -= 1
        reset_event = pygame.event.Event(RESET_EVENT)
        pygame.event.post(reset_event)
        
    hit_point1.update()

    if hit_point_value == 0:
        end_event = pygame.event.Event(END_EVENT)
        pygame.event.post(end_event)

    pygame.draw.circle(screen, red, ball.rect.center, ball.radius, 0)
    pygame.draw.rect(screen, white, paddle.rect, 0)
    score = Score()
    screen.blit(score.text,score.rect)
    pygame.display.flip()