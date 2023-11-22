import pygame
from pygame import mixer
from fighter import Fighter
mixer.init()
pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Steel Duel")
clock = pygame.time.Clock()
FPS = 144
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000
WARRIOR_SIZE = 162
WARRIOR_SCALE = 8
WARRIOR_OFFSET = [72 * SCREEN_WIDTH // 1920, 40 * SCREEN_HEIGHT // 1080]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 6
WIZARD_OFFSET = [112 * SCREEN_WIDTH // 1920, 85 * SCREEN_HEIGHT // 1080]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)
bg_image = pygame.image.load("assets/images/background/123.jpg").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
count_font = pygame.font.Font("assets/fonts/turok.ttf", 160)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 60)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))


def draw_health_bar(health, x, y):
  scaled_x = x * SCREEN_WIDTH // 1920
  scaled_y = y * SCREEN_HEIGHT // 1080
  scaled_width = 400 * SCREEN_WIDTH // 1920
  scaled_height = 50 * SCREEN_HEIGHT // 1080

  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (scaled_x - 2, scaled_y - 2, scaled_width + 4, scaled_height + 4))
  pygame.draw.rect(screen, RED, (scaled_x, scaled_y, scaled_width, scaled_height))
  pygame.draw.rect(screen, YELLOW, (scaled_x, scaled_y, scaled_width * ratio, scaled_height))


fighter_1 = Fighter(1, 100 * SCREEN_WIDTH // 1920, 425 * SCREEN_HEIGHT // 1080, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 1700 * SCREEN_WIDTH // 1920, 425 * SCREEN_HEIGHT // 1080, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

run = True
while run:
  clock.tick(FPS)
  draw_bg()
  draw_health_bar(fighter_1.health, int(20 * SCREEN_WIDTH / 1920), int(20 * SCREEN_HEIGHT / 1080))
  draw_health_bar(fighter_2.health, int(1500 * SCREEN_WIDTH / 1920), int(20 * SCREEN_HEIGHT / 1080))
  draw_text("P1: " + str(score[0]), score_font, RED, int(20 * SCREEN_WIDTH / 1920), int(60 * SCREEN_HEIGHT / 1080))
  draw_text("P2: " + str(score[1]), score_font, RED, int(1580 * SCREEN_WIDTH / 1920), int(60 * SCREEN_HEIGHT / 1080))
  if intro_count <= 0:
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT,  screen, fighter_1, round_over)
  else:
    draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()
  fighter_1.update()
  fighter_2.update()
  fighter_1.draw(screen)
  fighter_2.draw(screen)
  if not round_over:
    if not fighter_1.alive:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif not fighter_2.alive:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
    screen.blit(victory_img, (930, 0))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      fighter_1 = Fighter(1, 100 * SCREEN_WIDTH // 1920, 425 * SCREEN_HEIGHT // 1080, False, WARRIOR_DATA,
                          warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
      fighter_2 = Fighter(2, 1700 * SCREEN_WIDTH // 1920, 425 * SCREEN_HEIGHT // 1080, True, WIZARD_DATA, wizard_sheet,
                          WIZARD_ANIMATION_STEPS, magic_fx)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_e:
        fighter_1.activate_double_damage()
      if event.key == pygame.K_KP3:
        fighter_2.activate_double_damage()
      if event.key == pygame.K_z:
        fighter_1.activate_damage_reduction()
      if event.key == pygame.K_KP4:
        fighter_2.activate_damage_reduction()
  pygame.display.update()
pygame.quit()