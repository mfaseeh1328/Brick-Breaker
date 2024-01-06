# creating a background class
class Background:
    def __init__(self, img):
        self.img = img
        self.x, self.y = 0, 0
        self.width, self.height = tile_size, tile_size

    def draw(self):
        self.img_size = pygame.transform.scale(self.img, (self.width, self.height))
        try:
            for i in range(WIDTH // tile_size):
                self.x = i * tile_size
                for j in range(HEIGHT // tile_size):
                    self.y = j * tile_size
                    WIN.blit(self.img, (self.x, self.y))
        except:
            raise RuntimeError("Can't draw background")

    def update(self):
        self.draw()

class Paddle:
    speed = 15
    def __init__(self, img, x, y):
        self.img = img
        self.img_size = pygame.transform.scale(self.img, (100, 16))
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, self.img_size.get_width(), self.img_size.get_height())

    def draw(self):
        self.img_size = pygame.transform.scale(self.img, (100, 16))
        WIN.blit(self.img_size, (self.rect))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed

    def update(self, keys):
        self.draw()
        self.move(keys)

class Ball:
    x_speed = 7
    y_speed = 6
    def __init__(self, img, x, y):
        self.img = img
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
    
    def draw(self):
        WIN.blit(self.img, (self.rect))

    def control_movement(self, collide_obj_one, collide_obj_two, health_obj, heart, brick, brick_list):
        if game_start == True:
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed

        def  check_collision():
            global game_start, start_msg
            global score, damages, average

            collision_tolerance = 5

            if collide_obj_one.rect.colliderect(self.rect):
                    if abs(self.rect.bottom - collide_obj_one.rect.bottom) < collision_tolerance:
                        self.y_speed *= -1
            if self.rect.right > WIDTH or self.rect.left < 0:
                self.x_speed *= -1
            if self.rect.top < 0:
                self.y_speed *= -1

            if self.rect.bottom >= HEIGHT:
                self.rect.center = ([self.x - 100, self.y - 300])
                if len(health_obj) > 0:
                    health_obj.pop()
                    game_start =  False
                
                if len(health_obj) <= 0:
                    try:
                        game_start = False
                        score = 0
                        damages = 0
                        average = 0
                        heart.draw()
                        brick.draw()

                    except:
                        raise ArithmeticError
                    finally:
                        print("Game Continued!")

                if score > 0:
                    try:
                        random_score = random.randrange(10, 15)
                        score -=  random_score
                    except:
                        raise TypeError
                else:
                    score = 0

        def collision_brick():
            global score, damages, average
            global game_start, game_finish

            collision_tolerance = 10
            self.finish_point = 0

            row_count = 0
            for row in collide_obj_two:
                brick_count = 0
                for brick in row:
                    if self.rect.colliderect(brick[0]):
                        if abs(self.rect.bottom - brick[0].top) < collision_tolerance and self.y_speed > 0: # collision from above
                            self.y_speed *= -1
                        if abs(self.rect.top - brick[0].bottom) < collision_tolerance and self.y_speed < 0: # collision from top
                            self.y_speed *= -1
                        if abs(self.rect.right - brick[0].left) < collision_tolerance and self.x_speed > 0: # collision from right
                            self.x_speed *= -1
                        if abs(self.rect.left - brick[0].right) < collision_tolerance and self.x_speed < 0: # collision from left
                            self.x_speed *= -1
                        collide_obj_two[row_count][brick_count][0] = (-1000, 0, 0, 0)  # displacing the bricks from the screen
                        
                        try:
                            random_score = random.randrange(2, 5)
                            score += random_score
                            damages += 1
                            self.finish_point = damages
                            average = float(score / damages)

                        except:
                            raise ZeroDivisionError
                    brick_count += 1    # incrementing the iterators
                row_count += 1          # " " " " 

            if self.finish_point >= total:
                game_finish = True

        check_collision()
        collision_brick()


    def update(self, obj_one, obj_two,  obj_three, heart, brick, brick_list):
        global start_msg, game_start

        self.draw()
        self.control_movement(obj_one, obj_two, obj_three, heart, brick, brick_list)

        if game_start != False:
            start_msg = " "
        elif game_finish is not False:
            start_msg = " "
        else:
            start_msg = "Press Space to start!"

class Brick:
    def __init__(self):
        self.img = brick_img
        self.x, self.y = 0, 0
        self.width, self.height = 32, 16
        self.bricks = []

    def draw(self):
        try:
            # defining list to store each brick data
            brick_individual = []
            # loop to create the bricks width wise
            for i in range(rows):
                brick_list = []
                # oop to create bricks height wise
                for j in range(cols):
                    self.x = i * self.width
                    self.y = j * self.height + 100
                    # compiling the above data into a rect tuple
                    brick_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    # stroing each brick
                    brick_individual = [brick_rect]
                    # append it to a list to store it in column form
                    brick_list.append(brick_individual)
                # finally compile it into a  complete brick form
                self.bricks.append(brick_list)
        except:
            raise RuntimeError("Could not create")
        
    def draw_bricks(self):
        for row in self.bricks:
            img_pos = 0
            for brick in row:
                WIN.blit(self.img[img_pos // 2], (brick[0]))
                img_pos += 1
            if img_pos >= 12:
                img_pos = 0
            else:
                img_pos += 1
        
    def update(self):
        self.draw_bricks()

class Heart:
    def __init__(self):
        self.img = heart_img
        self.x, self.y, self.width, self.height = 0, 2, 26, 26
        self.counter = 0
        self.heart_store = []

    def draw(self):
        for i in range(3):
            self.x = i * self.width + 75
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.heart_store.append(self.rect)

    def draw_hearts(self):
        for item in self.heart_store:
            WIN.blit(self.img, item)

        lives = FONT.render("Lives:  ", 1, ('white'))
        WIN.blit(lives, (10, 4))

    def update(self):
        self.draw_hearts()

def analysis_bar():
    def create_score():
        score_font = FONT.render("Score: " + str(score), 1, ('white'))
        WIN.blit(score_font, (10, 50))

    def bricks_destroyed():
        bricks_destroy_font = FONT.render("Damage: " + str(damages), 1, ('white'))
        WIN.blit(bricks_destroy_font, (WIDTH - 140,4))

    def destroy_speed():
        avg_font = FONT.render("Average: " + str(average), 1, ('white'))
        WIN.blit(avg_font, (WIDTH - 180, 50))

    # surfaces
    bg_surf = pygame.Surface((WIDTH, 90))
    bg_surf.fill((20, 20, 20, 0))
    WIN.blit(bg_surf, (0, 0))

    # functions
    create_score()
    bricks_destroyed()
    destroy_speed()

def display_start_font():
    FONTS = pygame.font.SysFont("cambria", 30)
    start_font = FONTS.render("" + str(start_msg), 1, ('gold'))
    WIN.blit(start_font, (WIDTH // 2 - 150, HEIGHT // 2 - 60))

def display_winner_text():
    global finish_msg

    finish_msg = "Congratulations"
    FONTS = pygame.font.SysFont("cambria", 30)
    font = FONTS.render("" + str(finish_msg), 1, ('gold'))
    WIN.blit(font, (WIDTH // 2 - 150, HEIGHT // 2 - 60))

def detect_finish(brick, ball):
    global game_start, game_finish, start_msg, finish_counter, score, average, damages
    if game_finish is not False:
        display_winner_text()
        game_start = False
        finish_counter += 1

    if finish_counter >= FPS*2:
        game_finish = False  
        score, damages, average = 0, 0, 0 
        brick.draw()
        ball.rect.center = ([400, 400])
    if game_finish is False:
        finish_counter = 0
        

# importing the modules
import pygame
import sys
import os
from os import path
import random

pygame.init()

# window width and height
WIDTH, HEIGHT = 900, 800
FPS = 60
# setting up the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Consolas", 22)
# loading images from the directory
bg_img = [
    pygame.image.load(path.join("Assets", "Background", "1.png")), pygame.image.load(path.join("Assets", "Background", "2.png")), pygame.image.load(path.join("Assets", "Background", "3.png")), pygame.image.load(path.join("Assets", "Background", "4.png"))
]
paddle_img = [
    pygame.image.load(path.join("Assets", "Paddle", "1.png")), pygame.image.load(path.join("Assets", "Paddle", "2.png")), pygame.image.load(path.join("Assets", "Paddle", "3.png")), pygame.image.load(path.join("Assets", "Paddle", "4.png")), pygame.image.load(path.join("Assets", "Paddle", "5.png")), pygame.image.load(path.join("Assets", "Paddle", "6.png"))
]
ball_img = [
    pygame.image.load(path.join("Assets", "Ball", "1.png")), pygame.image.load(path.join("Assets", "Ball", "2.png")), pygame.image.load(path.join("Assets", "Ball", "3.png")), pygame.image.load(path.join("Assets", "Ball", "4.png")), pygame.image.load(path.join("Assets", "Ball", "5.png")), pygame.image.load(path.join("Assets", "Ball", "6.png"))
]

# bricks images in seperate lists each identified by their color name
brick_img = [
    pygame.image.load(path.join("Assets", "Bricks", "brown", "1.png")), pygame.image.load(path.join("Assets", "Bricks", "gold", "1.png")), pygame.image.load(path.join("Assets", "Bricks", "green", "1.png")), pygame.image.load(path.join("Assets", "Bricks", "grey", "1.png")), pygame.image.load(path.join("Assets", "Bricks", "pink", "1.png")), pygame.image.load(path.join("Assets", "Bricks", "red", "1.png"))
]

# heart images for lives
heart_img = pygame.transform.scale(pygame.image.load(path.join("Assets", "Heart", "1.png"), ), (26, 26))

# button images
play_btn = [
    pygame.image.load(path.join("Assets", "Button", "play.png")), pygame.image.load(path.join("Assets", "Hover", "play_hover.png"))
]
ball_btn = [
    pygame.image.load(path.join("Assets", "Button","ball.png")), pygame.image.load(path.join("Assets", "Hover", "ball_hover.png"))
]
paddle_btn = [
    pygame.image.load(path.join("Assets", "Button", "paddle.png")), pygame.image.load(path.join("Assets", "Hover", "paddle_hover.png"))
]
bg_btn = [
    pygame.image.load(path.join("Assets", "Button", "bg.png")), pygame.image.load(path.join("Assets", "Hover", "bg_hover.png"))
]
exit_btn = [
    pygame.image.load(path.join("Assets", "Button", "exit.png")), pygame.image.load(path.join("Assets", "Hover", "exit_hover.png"))
] 

# gradient images
rand_bg_img = [
    pygame.transform.scale(pygame.image.load("Assets/Background/gradient_one.png"), (WIDTH, HEIGHT)), pygame.transform.scale(pygame.image.load("Assets/Background/gradient_two.png"), (WIDTH, HEIGHT))
]
rand_bg = random.choice(rand_bg_img)
# creating variables
tile_size = 50
bg_user_choice = 2
paddle_user_choice = 0
ball_user_choice = 0
rows =  WIDTH // 32
cols =  HEIGHT // (16*4)
score = 0
damages = 0
average = float(0) 
game_start = False
start_msg = ""
total = rows * cols
game_finish = False
finish_msg = ""
finish_counter = 0

# main game function
def main():
    # global variables
    global game_start, start_msg
    # local variables
    run =  True

    # creating instances 
    bg = Background(bg_img[bg_user_choice])
    paddle = Paddle(paddle_img[paddle_user_choice], WIDTH // 2, HEIGHT - 70)
    ball = Ball(ball_img[ball_user_choice], paddle.x, paddle.y - 10)
    brick = Brick()
    brick.draw()
    heart = Heart()
    heart.draw()

    def draw_window():
        WIN.fill(('gold'))

        bg.update()
        paddle.update(keys)
        ball.update(paddle, brick.bricks, heart.heart_store, heart, brick, brick.bricks)
        brick.update()
        analysis_bar()
        display_start_font()
        detect_finish(brick, ball)
        heart.update()

        pygame.display.update()

    while run:

        CLOCK.tick(FPS)
        keys = pygame.key.get_pressed()
        draw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_start = True

    pygame.quit()

def paddle_menu():
    running = True
    user_choice = 0
    global paddle_user_choice

    def display_content():
        FONTS = pygame.font.SysFont("gillsans", 22)
        bg_font = FONTS.render("Select the paddle from the following: ", 1, ('black'))
        next_item = FONTS.render("Next", 1, ('white'))
        next_rect = next_item.get_rect()
        next_rect.x, next_rect.y = 500, 380

        WIN.blit(bg_font, (250, 100))
        pygame.draw.rect(WIN, ('purple'), (300, 250, 250, 300), 2)
        paddle_img_scale = pygame.transform.scale(paddle_img[user_choice], (100, 16))
        WIN.blit(paddle_img_scale, (350, 380))
        try:
            WIN.blit(next_item, (next_rect))
        except:
            print("Error")
    while running:
        pos = pygame.mouse.get_pos()
        len_of_list = 6
        next_rect = pygame.Rect(500, 380, 43, 24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_rect.collidepoint(pos):
                    user_choice += 1

        if user_choice >= len_of_list:
            user_choice = 0
        paddle_user_choice = user_choice

        WIN.blit(rand_bg_img[0], (0, 0))
        display_content()
        pygame.display.update()

def ball_menu():
    running = True
    user_choice = 0
    global ball_user_choice

    def display_content():
        FONTS = pygame.font.SysFont("gillsans", 22)
        bg_font = FONTS.render("Select the ball from the following: ", 1, ('black'))
        next_item = FONTS.render("Next", 1, ('white'))
        next_rect = next_item.get_rect()
        next_rect.x, next_rect.y = 500, 380

        WIN.blit(bg_font, (250, 100))
        pygame.draw.rect(WIN, ('purple'), (300, 250, 250, 300), 2)
        WIN.blit(ball_img[user_choice], (390, 390))
        try:
            WIN.blit(next_item, (next_rect))
        except:
            print("Error")
    while running:
        pos = pygame.mouse.get_pos()
        len_of_list = 6
        next_rect = pygame.Rect(500, 380, 43, 24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_rect.collidepoint(pos):
                    user_choice += 1

        if user_choice >= len_of_list:
            user_choice = 0
        ball_user_choice = user_choice

        WIN.blit(rand_bg_img[1], (0, 0))
        display_content()
        pygame.display.update()

def background_menu():
    running = True
    user_choice = 0
    global bg_user_choice

    def display_content():
        FONTS = pygame.font.SysFont("gillsans", 22)
        bg_font = FONTS.render("Select the background from the following: ", 1, ('black'))
        next_item = FONTS.render("Next", 1, ('white'))
        next_rect = next_item.get_rect()
        next_rect.x, next_rect.y = 500, 380

        WIN.blit(bg_font, (250, 100))
        pygame.draw.rect(WIN, ('purple'), (300, 250, 250, 300), 2)
        WIN.blit(bg_img[user_choice], (390, 350))
        try:
            WIN.blit(next_item, (next_rect))
        except:
            print("Error")

    while running:
        pos = pygame.mouse.get_pos()
        len_of_list = 4
        next_rect = pygame.Rect(500, 380, 43, 24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_rect.collidepoint(pos):
                    user_choice += 1

        if user_choice >= len_of_list:
            user_choice = 0
        bg_user_choice = user_choice
        WIN.blit(rand_bg_img[0], (0, 0))
        display_content()
        pygame.display.update()

def main_menu():
    running = True
    # defining rectangle arguments
    x_pos = WIDTH // 3 + 40
    height = 92
    # defining the rects
    play_rect = pygame.Rect(x_pos, 70, 174, height)
    paddle_rect = pygame.Rect(x_pos - 10, 220, 199, height)
    ball_rect = pygame.Rect(x_pos, 370, 169, height)
    bg_rect = pygame.Rect(x_pos - 40, 520, 248, height)
    exit_rect = pygame.Rect(x_pos, 670, 169, height)

    def random_background():

        rand_bg_scale = pygame.transform.scale(rand_bg, (WIDTH, HEIGHT))
        WIN.blit(rand_bg_scale, (0, 0))

    while running:
        CLOCK.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

       # try:
            if play_rect.collidepoint(mouse_pos):
                play_img = play_btn[1]
                if pygame.mouse.get_pressed()[0] == 1:
                    main()
            else:
                play_img = play_btn[0]
                
            if paddle_rect.collidepoint(mouse_pos):
                paddle_imgs = paddle_btn[1]
                if pygame.mouse.get_pressed()[0] == 1:
                    paddle_menu()
            else:
                paddle_imgs = paddle_btn[0]
                
            if ball_rect.collidepoint(mouse_pos):
                ball_imgs = ball_btn[1]
                if pygame.mouse.get_pressed()[0] == 1:
                    ball_menu()
            else:
                ball_imgs = ball_btn[0]
                
            if bg_rect.collidepoint(mouse_pos):
                bg_imgs = bg_btn[1]
                if pygame.mouse.get_pressed()[0] == 1:
                    background_menu()
            else:
                bg_imgs = bg_btn[0]
                
            if exit_rect.collidepoint(mouse_pos):
                exit_img = exit_btn[1]
                if pygame.mouse.get_pressed()[0] == 1:
                    running = False
                    sys.exit()
            else:
                exit_img = exit_btn[0]
       # except:
            #print("Finsihed")
            
        random_background()

        WIN.blit(play_img, (play_rect))
        WIN.blit(paddle_imgs, (paddle_rect))
        WIN.blit(ball_imgs, (ball_rect))
        WIN.blit(bg_imgs, (bg_rect))
        WIN.blit(exit_img, (exit_rect))

        pygame.display.update()

main_menu()