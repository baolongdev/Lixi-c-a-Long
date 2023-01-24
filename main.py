import pygame, sys, random, math, time
from pygame.locals import *

pygame.init()

game_state = 0
paused = False
vec = pygame.math.Vector2
FPS = 60
FramePerSec = pygame.time.Clock()

# Menu
press_y = 650
press_y1 = 650
scroll = 0
curtain_y = -1300

# Stats
score = 0
score_max = 0
spd = 3
player_pos = vec(0, 0)

# Movement
ACC = 1.2
FRIC = -0.10

# Screen Information
WIDTH = 360
HEIGHT = 640

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill((0, 255, 255))

pygame.display.set_caption("Lì xì")

# Load Fonts
total_font = pygame.font.Font("data/assets/BaiJamjuree-Bold.ttf", 68)
font = pygame.font.Font("data/assets/BaiJamjuree-Bold.ttf", 40)
score_font = pygame.font.Font("data/assets/BaiJamjuree-Bold.ttf", 26)
credit_font = pygame.font.Font("data/assets/BaiJamjuree-Bold.ttf", 12)

# Load Music
L = ["data/audio/Tet-Dong-Day-Khoa.mp3",
     "data/audio/Nam-Qua-Da-Lam-Gi-Noo-Phuoc-Thinh.mp3",
     "data/audio/Chuyện Cũ Bỏ Qua - Bích Phương.mp3"]
# Load Sounds
chop_sfx = ["data/audio/chop.mp3"]
score_sfx = pygame.mixer.Sound("data/audio/score.wav")
# Load Sprites
bg = pygame.image.load("data/assets/bg.png").convert_alpha()
# element menu
Mgold = pygame.image.load("data/menu/gold.png").convert_alpha()
Mcake = pygame.image.load("data/menu/cake.png").convert_alpha()
Mframe = pygame.image.load("data/menu/frame.png").convert_alpha()
Mlogo1 = pygame.image.load("data/menu/logo1.png").convert_alpha()
Lclound = pygame.image.load("data/menu/Lclound.png").convert_alpha()
Rclound = pygame.image.load("data/menu/Rclound.png").convert_alpha()
Mlogo2 = pygame.image.load("data/menu/logo2.png").convert_alpha()
Mstart = pygame.image.load("data/menu/start.png").convert_alpha()
Luckymoney = pygame.image.load("data/menu/Lucky money.png").convert_alpha()
# element
Msmall_start = pygame.image.load("data/menu/small start.png").convert_alpha()
Luckymoney2 = pygame.image.load("data/assets/Luckymoney2.png").convert_alpha()
Cat_hand = pygame.image.load("data/assets/hand_Cat.png").convert_alpha()
dotted_line = pygame.image.load("data/assets/dotted_line.png").convert_alpha()

icon = pygame.image.load("data/assets/icon.png").convert_alpha()

pygame.display.set_icon(icon)


def sine(speed, time, how_far, overallY):
    t = pygame.time.get_ticks() / 2 % time
    x = t
    y = math.sin(t / speed) * how_far + overallY
    y = int(y)
    return y

def centerElementW(element, WIDTH, HEIGHT, saiso = 0):
    return element.get_rect(center=((WIDTH//2) + saiso, HEIGHT))
def centerElementH(element, WIDTH, HEIGHT, saiso = 0):
    return element.get_rect(center=(WIDTH, (HEIGHT//2) + saiso))
def centerElementWH(element, WIDTH, HEIGHT, saiso = 0):
    return element.get_rect(center=((WIDTH//2) + saiso, (HEIGHT//2) + saiso))

def background():
    global scroll
    scroll -= .5
    if scroll < -640:
        scroll = 0
    SCREEN.blit(bg, (0, scroll))

def music():
    if not pygame.mixer.music.get_busy():
        filename = random.choice(L)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.02)
        pygame.mixer.music.play()

def main_menu():
    global press_y
    global press_y1
    # credits = credit_font.render("©BaoLong 2023", True, (0, 0, 0))
    # SCREEN.blit(credits, centerElementW(credits, WIDTH, 620))

    SCREEN.blit(Mframe, centerElementWH(Mframe, WIDTH, HEIGHT))
    SCREEN.blit(Mlogo1, centerElementW(Mlogo1, WIDTH, 230, 8))
    SCREEN.blit(Mlogo2, centerElementW(Mlogo2, WIDTH, 75))

    y = sine(160.0, 2000, 10.0, 320)
    SCREEN.blit(Lclound, (-80, y))
    SCREEN.blit(Rclound, (250, y))

    if press_y > 460:
        press_y = press_y * 0.99

    SCREEN.blit(Mgold, (-60, press_y + 30))
    SCREEN.blit(Mcake, (220, press_y + 40))
    SCREEN.blit(Luckymoney, centerElementW(Luckymoney, WIDTH, press_y+130, 8))


    if int(press_y) == 457:
        if press_y1 > 460:
            press_y1 = press_y1 * 0.99
        SCREEN.blit(Mstart, centerElementW(Mstart, WIDTH, press_y1 - 80))
    if int(press_y1) == 457:
        best_score = score_font.render(str(score_max), True, (255, 255, 255))
        SCREEN.blit(best_score, centerElementW(best_score, WIDTH, 370, -5))

def scoreboard():
    y = sine(200.0, 1280, 10.0, 40)
    show_score = score_font.render(str(score), True, (255, 255, 255))
    SCREEN.blit(Mstart, centerElementW(Mstart, WIDTH, y+30, 8))
    SCREEN.blit(show_score, centerElementW(show_score, WIDTH, y+25, 4))

def game_over():
    global game_state
    game_state = 0
    time.sleep(0.5)

def play_game():
    global game_state
    global score
    global spd
    game_state = 1
    score = 0
    spd = 3

class Hand(pygame.sprite.Sprite):
    def __init__(self, hand_side):
        super().__init__()
        self.new_spd = random.uniform(2.5, 3)
        self.new_y = 0
        self.offset_x = 0
        self.new_x = sine(100.0, 1280, 20.0, self.offset_x)
        self.side = hand_side
        self.can_score = True

        if self.side == 1:
            self.image = pygame.image.load(
                "data/assets/left_hand.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.offset_x = random.randint(-50, 120)
            self.new_y = -320
        elif self.side == 0:
            self.image = pygame.image.load(
                "data/assets/right_hand.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.offset_x = random.randint(260, 380)
            self.new_y = -40

    def move(self, rand_x, rand_xx):
        self.new_x = sine(100.0, 620, 20.0, self.offset_x)
        self.new_y += self.new_spd
        self.rect.center = (self.new_x, self.new_y)

        if self.rect.top > player_pos.y - 35 and self.can_score:
            global score
            score += 1
            self.can_score = False
            pygame.mixer.Sound.play(score_sfx)

        if (self.rect.top > HEIGHT):
            self.rect.bottom = 0
            # Play Kung Fu Sound
            self.new_spd = random.uniform(0.5, 8)
            if self.side == 1:
                self.offset_x = random.randint(-50, 120)
                self.new_y = -320
            elif self.side == 0:
                self.offset_x = random.randint(260, 380)
                self.new_y = -40
            if self.new_spd >= 6:
                self.new_spd = 8
                filename = random.choice(chop_sfx)
                chop = pygame.mixer.Sound(filename)
                pygame.mixer.Sound.play(chop)
            self.can_score = True

    def draw(self, surface):
        SCREEN.blit(dotted_line, (0, self.rect.y+36))
        surface.blit(self.image, self.rect)

    def reset(self, side):
        self.new_spd = random.uniform(0.5, 8)
        self.can_score = True
        if self.side == 1:
            self.offset_x = random.randint(-50, 120)
            self.new_y = -320
            self.new_x = 0
        elif self.side == 0:
            self.offset_x = random.randint(260, 380)
            self.new_y = -40
            self.new_x = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/assets/small_Luckymoney.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = vec((180, 550))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = +ACC
        if pressed_keys[K_UP]:
            self.acc.y = -ACC
        if pressed_keys[K_DOWN]:
            self.acc.y = +ACC

        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        global player_pos
        player_pos = self.pos

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
        if self.pos.y < 200:
            self.pos.y = 200
        self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        SCREEN.blit(Cat_hand, (self.rect.x + 38, self.rect.y + 100))

    def reset(self):
        self.pos = vec((180, 550))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)


# Sprite Setup
P1 = Player()
H1 = Hand(0)
H2 = Hand(1)

# Sprite Groups
hands = pygame.sprite.Group()
hands.add(H1)
hands.add(H2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(H1)
all_sprites.add(H2)

def main():
    global game_state
    global paused
    while game_state != 2:
        # Main Menu
        while game_state == 0:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    play_game()
            background()
            main_menu()
            music()
            pygame.display.update()
            FramePerSec.tick(FPS)
        # Gameplay
        while game_state == 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if not paused:
                P1.update()
                H1.move(260, 380)
                H2.move(-50, 100)
            background()
            P1.draw(SCREEN)
            H1.draw(SCREEN)
            H2.draw(SCREEN)
            scoreboard()

            if pygame.sprite.spritecollide(P1, hands, False, pygame.sprite.collide_mask):
                global score_max
                if score > score_max:
                    score_max = score
                time.sleep(0.5)
                P1.reset()
                H1.reset(0)
                H2.reset(1)
                game_over()
            pygame.display.update()
            FramePerSec.tick(FPS)

if __name__ == '__main__':
    main()
