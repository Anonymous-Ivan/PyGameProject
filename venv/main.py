import pygame, os, sys, random
from os import path


pygame.init()
size = width, height = 500, 800
FPS = 60
all_sprites = pygame.sprite.Group()
boss_sprite = pygame.sprite.Group()
b_eggs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enem = pygame.sprite.Group()
enem_2 = pygame.sprite.Group()
screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()
dir_sound = path.join(path.dirname(__file__), 'sounds')
dir_data = path.join(path.dirname(__file__), 'data')
pygame.mixer.music.load("sounds/pause.wav")
clock = pygame.time.Clock()
btn_sound = pygame.mixer.Sound(path.join(dir_sound, 'btn.wav'))
shoot_sound = pygame.mixer.Sound(path.join(dir_sound, 'pew.wav'))
egg_sound = pygame.mixer.Sound(path.join(dir_sound, 'egg.wav'))
boom_sound = pygame.mixer.Sound(path.join(dir_sound, 'boom.wav'))
lost_sound = pygame.mixer.Sound(path.join(dir_sound, 'lose.wav'))
menu_snd = pygame.mixer.Sound(path.join(dir_sound, 'menu.wav'))
game_snd = pygame.mixer.Sound(path.join(dir_sound, 'game.wav'))

explosion_anim = {}
explosion_anim['bb'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(dir_data, filename)).convert()
    img.set_colorkey((0, 0, 0))
    img_sm = pygame.transform.scale(img, (30, 30))
    explosion_anim['bb'].append(img_sm)

xx = 0
yy = 0
p = 0
time = 0
score = 0
f = open("High_Score.txt", mode="r")

high_score = str(f.read()).split('\n')[-2]

f.close()
q = open("High_Score.txt", mode="a")


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
    color = (255, 255, 0)

    if text == str(high_score):
        color = (0, 255, 255)

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
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


def printed(mess, x, y, fnt_clr = (250, 250, 250), fnt="Usually-font.otf", fnt_size=15):
    fnt = pygame.font.Font(fnt, fnt_size)
    txt = fnt.render(mess, True, fnt_clr)
    screen.blit(txt, (x, y))


def pause():
    paused = True
    flPause = False
    pygame.mixer.music.play(-1)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    flPause = not flPause
                    if flPause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
        printed("Pause. Press *enter* to continue", 100, 300)
        printed("Press *space* to back to menu", 100, 350)


        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            paused = False
            pygame.mixer.music.pause()
            pygame.mixer.Sound.play(game_snd)

        if key[pygame.K_SPACE]:
            paused = False
            pygame.mixer.music.pause()
            menu()

        pygame.display.update()
        clock.tick(15)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


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
        shoot_sound.play()


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 70))
        self.image = boss_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.speedy = 5
        self.speedx = 5

    def update(self):
        if self.rect.x >= 50 and self.rect.y == 50:
            self.rect.x += self.speedx
        if self.rect.x == 300:
            self.rect.y += self.speedy
        if self.rect.y == 500:
            self.rect.x -= self.speedx
        if self.rect.x == 50:
            self.rect.y -= self.speedy
        global xx, yy, time
        xx = self.rect.x
        yy = self.rect.y
        time += 1
        if time == 10:
            e = Boss_Eggs()
            all_sprites.add(e)
            enem_2.add(e)
            time = 0


class Boss_Eggs(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image = g_egg
        self.rect = self.image.get_rect()
        self.rect.x = xx + 50
        self.rect.y = yy + 50
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

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


class Buttons:
    def __init__(self, w, h, off_clr, on_clr):
        self.w = w
        self.h = h
        self.off = off_clr
        self.on = on_clr

    def draw_but(self, x, y, text, act=None, fnt_sz=15):
        ms = pygame.mouse.get_pos()
        clk = pygame.mouse.get_pressed()

        if x < ms[0] < x + self.w:
            if y < ms[1] < y + self.h:
                pygame.draw.rect(screen, (207, 197, 242), (x, y, self.w, self.h))

                if clk[0] == 1:
                    pygame.mixer.Sound.play(btn_sound)
                    pygame.time.delay(300)

                    if act is not None:
                        act()

        else:
            pygame.draw.rect(screen, (14, 6, 45), (x, y, self.w, self.h))

        printed(mess=text, x=x + 10, y=y + 10, fnt_size=fnt_sz)


#функция для кнопки "Score"

def prnt_score():
    global high_score, score
    bck = pygame.image.load("bkrnd.jpg")
    pygame.mixer.Sound.play(menu_snd)
    sc = True
    while sc:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.stop(menu_snd)
                    game()
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.Sound.stop(menu_snd)
                    menu()

        pygame.display.flip()
        screen.blit(bck, (0, 0))
        printed(f"Your best score: {high_score}!", 100, 300,
                 fnt_clr=(250, 250, 250), fnt="Gomawo.ttf", fnt_size=40)


def game_over():
    global high_score, score
    g_o = pygame.image.load("game over.jpg")
    rtrn = Buttons(w=200, h=70, off_clr=(14, 0, 45), on_clr=(207, 197, 242))
    back = Buttons(w=200, h=70, off_clr=(14, 0, 45), on_clr=(207, 197, 242))
    stop = True
    while stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                if score > int(high_score):
                    high_score = score
                    print(str(high_score).strip(), file=q, end='\n')
                quit()

        screen.blit(g_o, (0, 0))
        printed("GAME OVER!", 150, 300, fnt_clr=(250, 250, 250), fnt="Usually-font.otf", fnt_size=30)
        pygame.mixer.Sound.play(lost_sound)

        # кнопка возобновления игры после поражения

        rtrn.draw_but(150, 370, "Try Again", game, 30)
        back.draw_but(150, 450, "Menu", menu, 30)
        player.hp = 10
        if score > int(high_score):
            high_score = score
            print(str(high_score).strip(), file=q, end='\n')
        score = 0

        pygame.display.update()
        clock.tick(100)



# подгрузка изображений

player_image = load_image('ship.png', -1)
enemy_image = load_image('egg.png', -1)
bullet_image = load_image('bullet.png', -1)
boss_image = load_image('UFO.png', -1)
g_egg = load_image('g_egg.png', -1)
player = Player()
all_sprites.add(player)


def game():
    global score, high_score
    score = 0
    bck = pygame.image.load("bkrnd.jpg")

    # спавн яиц

    for i in range(8):
        e = Enemy()
        all_sprites.add(e)
        enem.add(e)
    pygame.mixer.Sound.stop(lost_sound)
    pygame.mixer.Sound.play(game_snd, -1)
    running = True
    num_hits = 0
    boss_spawn_counter = 0
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.Sound.stop(game_snd)
                    pause()

        all_sprites.update()

        # проверка на игрок + враг
        boom = pygame.sprite.spritecollide(player, enem, True, pygame.sprite.collide_circle)
        for hit in boom:
            boom_sound.play()
            expl = Explosion(hit.rect.center, 'bb')
            all_sprites.add(expl)
            player.hp -= 2
            if player.hp <= 0:
                pygame.mixer.Sound.stop(game_snd)
                game_over()
                running = False

            m = Enemy()
            all_sprites.add(m)
            enem.add(m)

        boom2 = pygame.sprite.spritecollide(player, enem_2, True, pygame.sprite.collide_circle)
        for hit in boom2:
            boom_sound.play()
            player.hp -= 2
            if player.hp <= 0:
                pygame.mixer.Sound.stop(game_snd)
                game_over()
                running = False

            # проверка на пулю + враг
        bulletsss = pygame.sprite.groupcollide(enem, bullets, True, True)

        for hit in bulletsss:
            egg_sound.play()
            score += 5
            expl = Explosion(hit.rect.center, 'bb')
            all_sprites.add(expl)
            e = Enemy()
            all_sprites.add(e)
            enem.add(e)
            boss_spawn_counter += 1

        if boss_spawn_counter == 50:
            for elem in enem:
                elem.kill()

            b = Boss()
            all_sprites.add(b)
            boss_sprite.add(b)
            boss_spawn_counter = 0

        bulle = pygame.sprite.groupcollide(enem_2, bullets, True, True)
        for i in bulle:
            egg_sound.play()
            expl = Explosion(i.rect.center, 'bb')
            all_sprites.add(expl)

        # босс + пуля
        boss_check = pygame.sprite.groupcollide(boss_sprite, bullets, False, True)

        for hit in boss_check:
            num_hits += 1

        if num_hits == 30:
            for elem in boss_sprite:
                boom_sound.play()
                expl = Explosion(elem.rect.center, 'bb')
                all_sprites.add(expl)
                elem.kill()
                score += 300
            for i in range(8):
                e = Enemy()
                all_sprites.add(e)
                enem.add(e)
            num_hits = 0


        screen.blit(screen, screen_rect)
        screen.blit(bck, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, width / 2, 10)
        draw_text(screen, str(high_score), 18, width / 4, 10)
        draw_hp_bar(screen, 390, 10, player.hp)
        pygame.display.flip()

    if score > int(high_score):
        high_score = score
        print(str(high_score).strip(), file=q, end='\n')


def exitt():
    global score, high_score
    if score > int(high_score):
        high_score = score
        print(str(high_score).strip(), file=q, end='\n')
    quit()


def menu():
    global high_score, score
    menu_bck = pygame.image.load("fon.jpg")
    start = Buttons(w=200, h=70, off_clr=(14, 0, 45), on_clr=(207, 197, 242))
    ext = Buttons(w=200, h=70, off_clr=(14, 0, 45), on_clr=(207, 197, 242))
    scr = Buttons(w=200, h=70, off_clr=(14, 0, 45), on_clr=(207, 197, 242))
    pygame.mixer.Sound.stop(lost_sound)
    pygame.mixer.Sound.play(menu_snd)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False
                pygame.quit()
                if score > int(high_score):
                    high_score = score
                    print(str(high_score).strip(), file=q, end='\n')
                quit()


            key = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if key[pygame.K_SPACE]:
                    prnt_score()
                pygame.mixer.Sound.play(btn_sound)
                pygame.mixer.Sound.stop(menu_snd)

        screen.blit(menu_bck, (0, 0))
        start.draw_but(160, 350, "START", game, 50)
        scr.draw_but(160, 450, "Score", prnt_score, 50)
        ext.draw_but(160, 550, "EXIT", exitt, 50)

        pygame.display.update()
        clock.tick(60)


menu()

pygame.quit()
q.close()
quit()
