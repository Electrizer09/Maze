import random

import pygame
import os
import sys

FPS = 50
sprites = []
size = (width, height) = (WIDTH, HEIGHT) = (1000, 1000)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
running = True

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
iwalls_group = pygame.sprite.Group()
end_group = pygame.sprite.Group()
lvbtn_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
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


class LevelButton(pygame.sprite.Sprite):
    def __init__(self, lvl, x, y):
        file = f'data/lv{lvl}b.png'
        super().__init__(lvbtn_group)
        self.image = load_image(file)
        self.rect = self.image.get_rect().move(x - self.image.get_rect().w, y - self.image.get_rect().h)


def maxlvls():
    a = 0
    while True:
        try:
            a += 1
            f = open(f'data/map{a}.txt')
            f.close()
        except FileNotFoundError:
            a -= 1
            return a


max_lvls = maxlvls()


def next_lvl():
    global running
    running = False
    a = False
    endscreen()


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    level_map = []
    mapFile = open(filename, 'r')
    for i in mapFile:
        level_map.append(i.strip())

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    mapFile.close()
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Tile('end', x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def delete_all():
    global all_sprites
    global tiles_group
    global player_group
    global walls_group
    global iwalls_group
    global lvbtn_group
    global player
    global sprites
    for i in sprites:
        i.kill()
    all_sprites.empty()
    tiles_group.empty()
    player_group.empty()
    walls_group.empty()
    iwalls_group.empty()
    lvbtn_group.empty()
    player = None
    lvbtn_group = None
    all_sprites = None
    tiles_group = None
    player_group = None
    walls_group = None
    iwalls_group = None
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    iwalls_group = pygame.sprite.Group()
    lvbtn_group = pygame.sprite.Group()


def get_click(pos, x, y, w, h):
    x1, y1 = pos
    try:
        if x1 >= x and y1 >= y and x1 <= w + x and y1 <= h + y:
            return True
        return False
    except Exception:
        return False


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('data/fon1.png'), (WIDTH, HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                level_select()
                return True
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


def endscreen():
    running = False
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('data/fon2.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return True
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


def level_select():
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('data/fon3.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    lv1b = LevelButton(1, 95, HEIGHT // 2)
    lv2b = LevelButton(2, WIDTH // 2, HEIGHT // 2)
    lv3b = LevelButton(3, WIDTH - 10, HEIGHT // 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if get_click(event.pos, lv1b.rect.x, lv1b.rect.y, lv1b.rect.w, lv1b.rect.h):
                    gamecycle(1)
                    return True
                if get_click(event.pos, lv2b.rect.x, lv2b.rect.y, lv2b.rect.w, lv2b.rect.h):
                    gamecycle(2)
                    return True
                if get_click(event.pos, lv3b.rect.x, lv3b.rect.y, lv3b.rect.w, lv3b.rect.h):
                    gamecycle(3)
                    return True
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        lvbtn_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'wall': load_image('data/Wall Tile.png'),
    'empty': load_image('data/Empty Tile.png'),
    'end': load_image('data/End.png')
}
player_image = load_image('data/Player.png')

tile_width = tile_height = 80


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(walls_group, all_sprites)
        elif tile_type == 'end':
            super().__init__(end_group, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        sprites.append(self)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.speed = 5
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            for i in range(self.speed):
                wall = -1 if pygame.sprite.spritecollideany(self, walls_group) else 1
                self.rect.right += wall
                if wall == -1:
                    break
                if pygame.sprite.spritecollideany(self, end_group):
                    next_lvl()
                    break
        if left:
            for i in range(self.speed):
                wall = -1 if pygame.sprite.spritecollideany(self, walls_group) else 1
                self.rect.right -= wall
                if wall == -1:
                    break
                if pygame.sprite.spritecollideany(self, end_group):
                    next_lvl()
                    break
        if down:
            for i in range(self.speed):
                wall = -1 if pygame.sprite.spritecollideany(self, walls_group) else 1
                self.rect.top += wall
                if wall == -1:
                    break
                if pygame.sprite.spritecollideany(self, end_group):
                    next_lvl()
                    break
        if up:
            for i in range(self.speed):
                wall = -1 if pygame.sprite.spritecollideany(self, walls_group) else 1
                self.rect.top -= wall
                if wall == -1:
                    break
                if pygame.sprite.spritecollideany(self, end_group):
                    next_lvl()
                    break


def gamecycle(lvl):
    global running
    running = True
    player, level_x, level_y = generate_level(load_level(f'data/map{lvl}.txt'))
    camera = Camera()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return True
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(up=True)
        if keys[pygame.K_DOWN]:
            player.move(down=True)
        if keys[pygame.K_LEFT]:
            player.move(left=True)
        if keys[pygame.K_RIGHT]:
            player.move(right=True)
        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    delete_all()
    running = True
    level_select()


start_screen()
