from pygame import *

window = display.set_mode((700, 500))
display.set_caption('Лабиринт')
bg_color = (0, 255, 255)
window.fill(bg_color)

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.w = w
        self.h = h
        self.x = x
        self.y = y

class Pic(GameSprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__(picture, w, h, x, y)
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.direction = 'left'
        if self.rect.x < 600:
            self.direction = 'right'
        while self.direction == 'right':
            self.direction = 'left'
            if self.rect.x > 50:
                self.direction = 'right'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else: self.rect.x += self.speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

user = Player('cumenb.png', 70, 70, 200, 200, 0, 0)
w1 = Pic('stone_wall.jpg', 40, 320, 200, 100)
w2 = Pic('stone_wall.jpg', 320, 40, 200, 170)
w3 = Pic('stone_wall.jpg', 40, 220, 400, 170)
final = Pic('football.png', 40, 40, 300, 250)
winner = transform.scale(image.load('thumb.jpg'), ((700, 500)))
mob =  Enemy('mob.png', 70, 70, 500, 400, 10)
barriers = sprite.Group()
gameover = transform.scale(image.load('gameover.jpg'), ((700, 500)))

barriers.add(w1, w2, w3)

finish = True
run = True
while run:
    time.delay(40)
    window.fill(bg_color)
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_w:
                user.y_speed = -10
            elif e.key == K_a:
                user.x_speed = -10
            elif e.key == K_s:
                user.y_speed = 10
            elif e.key == K_d:
                user.x_speed = 10
        elif e.type == KEYUP:
            if e.key == K_w:
                user.y_speed = 0
            elif e.key == K_a:
                user.x_speed = 0
            elif e.key == K_s:
                user.y_speed = 0
            elif e.key == K_d:
                user.x_speed = 0
    
    if finish != False: 
        user.reset()
        w1.reset()
        w2.reset()
        w3.reset()
        final.reset()
        mob.reset()
        user.update()
        mob.update()
        if sprite.collide_rect(user, final):
            finish = True
            window.blit(winner, (0,0))
        if sprite.collide_rect(user, mob):
            finish = True
            window.blit(gameover, (0,0))
    display.update()
    