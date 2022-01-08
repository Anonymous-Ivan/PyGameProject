import pygame, os, sys, random

pygame.init()
size = width, height = 500, 800
FPS = 60
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enem = pygame.sprite.Group()
screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


font_name = pygame.font.match_font('Times New Roman')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_hp_bar(surf, x, y, a):
    if a < 0:
        a = 0
    bar_lenght = 100
    bar_height = 10
    fill = (a / 10) * bar_lenght
    outline_rect = pygame.Rect(x, y, bar_lenght, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, (255, 255, 0), fill_rect)
    pygame.draw.rect(surf, (0, 0, 255), outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((45, 46))
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 20
        self.speed = 0
        self.hp = 10

    def update(self):
        self.speed = 0
        what = pygame.key.get_pressed()
        if what[pygame.K_LEFT]:
            self.speed = -5
        if what[pygame.K_RIGHT]:
            self.speed = 5
        self.rect.x += self.speed
        if self.rect.x >= width - 55:
            self.rect.x = width - 55
        if self.rect.x <= 0:
            self.rect.x = 5

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height + 10:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 15))
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

# подгрузка изображений


player_image = load_image('ship.png', -1)
enemy_image = load_image('egg.png', -1)
bullet_image = load_image('bullet.png', -1)
player = Player()
all_sprites.add(player)
score = 0
# спавн яиц

for i in range(8):
    e = Enemy()
    all_sprites.add(e)
    enem.add(e)

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # проверка на игрок + враг
    boom = pygame.sprite.spritecollide(player, enem, True, pygame.sprite.collide_circle)
    for hit in boom:
        player.hp -= 2
        if player.hp <= 0:
            running = False
        m = Enemy()
        all_sprites.add(m)
        enem.add(m)

        # проверка на пулю + враг
    bulletsss = pygame.sprite.groupcollide(enem, bullets, True, True)
    for hit in bulletsss:
        score += 5
        e = Enemy()
        all_sprites.add(e)
        enem.add(e)

    screen.fill((0, 0, 0))
    screen.blit(screen, screen_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, width / 2, 10)
    draw_hp_bar(screen, 390, 10, player.hp)
    pygame.display.flip()

pygame.quit()
