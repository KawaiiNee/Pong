import pygame
from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, K_w, K_a, K_d, K_s)
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
paddle_size = (25, 95)
ball_size = (20, 20)


class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.surf = pygame.Surface(paddle_size)
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH // 7, SCREEN_HEIGHT // 2
            )
        )

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_a]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(2, 0)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 2)

        if self.rect.left < 0:  # in left and top side, any coordinates less than zero is off the screen
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH // 4:
            self.rect.right = SCREEN_WIDTH // 4
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.surf = pygame.Surface(paddle_size)
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH - (SCREEN_WIDTH // 7), SCREEN_HEIGHT // 2
            )
        )

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        # any coordinates less than zero is off the screen
        if self.rect.left < SCREEN_WIDTH - (SCREEN_WIDTH // 4):
            self.rect.left = SCREEN_WIDTH - (SCREEN_WIDTH // 4)
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


ball_image = pygame.image.load('mine.png')
ball_image = pygame.transform.scale(ball_image, ball_size)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = ball_image.convert()
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            )
        )
        self.speed = 1
        self.run = True

    def update(self):
        if not (pygame.sprite.spritecollideany(player1, balls) or pygame.sprite.spritecollideany(player2, balls)) and self.run\
                and ((self.rect.top > 0) or (self.rect.bottom < SCREEN_HEIGHT)):
            # side = random.randint(1, 2)
            # if side == 1:
            #     # self.rect.move_ip(random.randint(-self.speed, 0), random.randint(-self.speed, self.speed))
            #     self.rect.move_ip(-2, 2)
            # else:
            #     # self.rect.move_ip(random.randint(0, self.speed), random.randint(-self.speed, self.speed))
            #     self.rect.move_ip(2, 2)
            self.rect.move_ip(1, 1)

        # direction = []
        # if pygame.sprite.spritecollideany(player1, balls) or pygame.sprite.spritecollideany(player2, balls)\
        #         or (self.rect.top < 0) or (self.rect.bottom > SCREEN_HEIGHT):
        #     if self.rect.left < 0:  # left
        #         direction.insert(0, -self.speed)
        #     if self.rect.left > 0:  # right
        #         direction.insert(0, self.speed)
        #     if self.rect.top < 0:  # top
        #         direction.insert(1, -self.speed)
        #     if self.rect.top > 0:  # bottom
        #         direction.insert(1, self.speed)
        #
        # # Top = 0, left = 0
        # # bottom = +1, right = +1
        #
        #     self.rect.move_ip(direction)
        #
        # if len(direction) > 2:
        #     direction.clear()

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.move_ip(1, -1)

        if self.rect.right < 0 or self.rect.left < 0:
            self.kill()
            return True  # to give signal when to replenish/recreate the ball object


player1 = Player1()
player2 = Player2()

ball = Ball()
balls = pygame.sprite.Group()
balls.add(ball)

players = pygame.sprite.Group()
players.add(player1)
players.add(player2)

all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)

ADD_BALL = pygame.USEREVENT + 1

is_active = True

while is_active:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_active = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                is_active = False
        elif event.type == ADD_BALL:
            if Ball().update():  # if the ball is out of the screen, create a new ball
                ball = Ball()
                balls.add(ball)
                all_sprites.add(ball)

    pressed_keys = pygame.key.get_pressed()

    players.update(pressed_keys)

    screen.fill((0, 0, 0))

    balls.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    pygame.display.flip()


pygame.quit()


# PONG GAME

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 840, 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")


class Player1(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y, rect_width, rect_height):
        super(Player1, self).__init__()
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.velocity = 2
        self.hit_area = (self.rect_x, self.rect_y, self.rect_x +
                         self.rect_width, self.rect_y + self.rect_height)

    def move(self):
        if keys[pygame.K_w] and self.rect_y > 0:
            self.rect_y -= self.velocity
        if keys[pygame.K_s] and (self.rect_y + self.rect_height) < SCREEN_HEIGHT:
            self.rect_y += self.velocity
        if keys[pygame.K_a] and self.rect_x > 0:
            self.rect_x -= self.velocity
        if keys[pygame.K_d] and self.rect_x < SCREEN_WIDTH // 5:
            self.rect_x += self.velocity

    def update(self):
        self.move()
        pygame.draw.rect(screen, (255, 255, 255), (self.rect_x,
                         self.rect_y, self.rect_width, self.rect_height))
        # update the hit area of paddle
        self.hit_area = (self.rect_x, self.rect_y, self.rect_x +
                         self.rect_width, self.rect_y + self.rect_height)

        # score
        text1 = score_font.render(f"Score = {p1_score}", True, (50, 50, 255))
        text2 = score_font.render(f"Score = {p2_score}", True, (255, 50, 50))
        screen.blit(text1, (SCREEN_WIDTH // 22, SCREEN_HEIGHT // 22))
        screen.blit(text2, (SCREEN_WIDTH - (text2.get_width() +
                    SCREEN_WIDTH // 22), SCREEN_HEIGHT // 22))


class Player2(Player1):
    def move(self):
        if keys[pygame.K_UP] and self.rect_y > 0:
            self.rect_y -= self.velocity
        if keys[pygame.K_DOWN] and (self.rect_y + self.rect_height) < SCREEN_HEIGHT:
            self.rect_y += self.velocity
        if keys[pygame.K_LEFT] and self.rect_x > SCREEN_WIDTH - (SCREEN_WIDTH // 5):
            self.rect_x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect_x < SCREEN_WIDTH - self.rect_width:
            self.rect_x += self.velocity


class Ball(pygame.sprite.Sprite):
    # score notifying purpose
    font = pygame.font.SysFont('comicsans', 50, True)
    text = None

    def __init__(self, rect_x, rect_y, radius):
        super(Ball, self).__init__()
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.radius = radius
        self.velocity = 1
        self.off_screen = False
        self.restarting_position = [self.rect_x, self.rect_y]
        self.stag = True
        self.right = True
        self.left = False
        self.up = False
        self.down = False

    def update(self):
        if not self.off_screen:
            self.move()
            pygame.draw.circle(screen, (255, 0, 0),
                               (self.rect_x,  self.rect_y), self.radius)
        else:
            # notifying a player have score
            screen.blit(Ball.text, (SCREEN_WIDTH // 2 - (Ball.text.get_width() //
                        2), SCREEN_HEIGHT // 2 - (Ball.text.get_height() // 2)))
            pygame.display.update()
            # need to delay before moving again the ball
            i = 0
            while i < 600:
                pygame.time.delay(10)
                i += 10
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 600
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            i = 600
                            pygame.quit()
            # ball resetting
            self.rect_x = self.restarting_position[0]
            self.rect_y = self.restarting_position[1]
            self.stag = True
            self.right = True
            self.off_screen = False

    def move(self):
        self.hit_boundary()
        # solely considering that the ball will always land first at the top of the screen
        if self.stag:
            self.rect_x += self.velocity
            self.rect_y += self.velocity
        else:
            # these conditions will dictate what is the current position of the ball
            # where does it bounce and where would it go next
            for paddle in paddles:
                # ball bouncing conditionals
                # to fix - if the ball hit the top and bottom side of the paddle

                # on the right side
                if self.rect_y in range(paddle.hit_area[1], paddle.hit_area[3] + 1) and self.rect_x + self.radius in range(paddle.hit_area[0], paddle.hit_area[0] + 1):
                    self.left = True
                    self.right = False
                # bounce on the left side
                elif self.rect_y in range(paddle.hit_area[1], paddle.hit_area[3] + 1) and self.rect_x - self.radius in range(paddle.hit_area[2], paddle.hit_area[2] + 1):
                    self.right = True
                    self.left = False
                # on the bottom
                elif self.rect_y + self.radius > SCREEN_HEIGHT or (self.rect_x in range(paddle.hit_area[0] - 1, paddle.hit_area[2]) and self.rect_y + self.radius > paddle.hit_area[1]):
                    self.down = True
                    self.up = False
                # on the top
                elif self.rect_y - self.radius < 0 or (self.rect_x in range(paddle.hit_area[0] - 1, paddle.hit_area[2]) and self.rect_y - self.radius < paddle.hit_area[3]):
                    self.up = True
                    self.down = False

        if not self.stag:
            # if the ball heading towards right
            if self.right:
                # if the ball bounced from bottom
                if self.down:
                    self.rect_x += self.velocity
                    self.rect_y -= self.velocity
                # if the ball bounced from top
                else:
                    self.rect_x += self.velocity
                    self.rect_y += self.velocity
            else:
                if self.up:
                    self.rect_x -= self.velocity
                    self.rect_y += self.velocity
                else:
                    self.rect_x -= self.velocity
                    self.rect_y -= self.velocity

        global p1_score, p2_score
        # check if the ball is out of the screen
        if self.rect_x + self.radius < 0 or self.rect_x - self.radius > SCREEN_WIDTH:
            self.off_screen = True
            if self.right:
                p1_score += 1
                Ball.text = Ball.font.render(
                    'Player 1 score', True, (50, 50, 255))
            else:
                p2_score += 1
                Ball.text = Ball.font.render(
                    'Player 2 score', True, (255, 50, 50))

    # checked if the ball collides on boundaries and falsifies self.stag(not yet hit a boundary) attribute
    def hit_boundary(self):
        if self.rect_y + self.radius > SCREEN_HEIGHT or self.rect_y - self.radius < 0:
            self.stag = False
            return True


player1 = Player1(SCREEN_WIDTH // 7, (SCREEN_HEIGHT // 2) - 70, 25, 140)
player2 = Player2(SCREEN_WIDTH - (SCREEN_WIDTH // 7),
                  (SCREEN_HEIGHT // 2) - 70, 25, 140)

ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 8)

paddles = pygame.sprite.Group()
paddles.add(player1)
paddles.add(player2)

all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)

p1_score = 0
p2_score = 0
# pygame.font can take 4 arguments: Name of the font, size, boolean value if you want it to be bold, same for italicize
score_font = pygame.font.SysFont('comicsans', 24, True)


def screen_update():
    screen.fill((0, 0, 0))
    for entity in all_sprites:
        entity.update()

    pygame.display.update()


is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False

    keys = pygame.key.get_pressed()

    screen_update()


pygame.quit()
