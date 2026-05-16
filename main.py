from pygame import *
from random import randint, random

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys[K_d] and self.rect.x < win_w - 70:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx - 7, self.rect.y, 15, 20, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_h:
            global lost
            lost += 1
            self.rect.y = randint(-65, 0)
            self.rect.x = randint(20, win_w - 20)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_h:
            self.rect.y = randint(-65, 0)
            self.rect.x = randint(20, win_w - 20)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_w = 700
win_h = 500
lost = 0
score = 0

window = display.set_mode((win_w, win_h))

display.set_caption("Shooter")

background = transform.scale(
    image.load("galaxy.jpg"),
    (win_w, win_h)
)

mixer.init()
mixer.music.load("music.mp3")
mixer.music.play()

font.init()
font_text = font.Font("Tektur-Medium.ttf", 36)
font_title = font.Font("Tektur-Medium.ttf", 120)

player = Player("rocket.png", win_w / 2 - 65 / 2, win_h - 65, 65, 65, 4)

enemies = sprite.Group()
for _ in range(5):
    enemy = Enemy("ufo.png", randint(20, win_w - 20), randint(-30, 0), 
    65, 45, 
    random() + randint(1, 2))
    enemies.add(enemy)

asteroids = sprite.Group()
for _ in range(3):
    asteroid = Asteroid("asteroid.png", randint(20, win_w - 20), randint(-30, 0), 
    65, 45, 
    random() + randint(1, 2))
    asteroids.add(asteroid)

bullets = sprite.Group()
sound_bullet = mixer.Sound("blaster.mp3")

text_win = font_title.render("YOU WIN!", True, (72, 255, 59))
text_lose = font_title.render("YOU LOSE!", True, (232, 123, 123))

clock = time.Clock()
FPS = 60
run = True
finish = False
result_text = text_lose
start_time = time.get_ticks()

is_reload = False
current_counter_bullet = 0
reload_time = time.get_ticks()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not is_reload:
                sound_bullet.play()
                player.fire()
                current_counter_bullet += 1
                if current_counter_bullet >= 5:
                    is_reload = True
                    reload_time = time.get_ticks()

    if not finish:
        window.blit(background, (0, 0))

        enemies_colide = sprite.groupcollide(enemies, bullets, True, True)
        for i in enemies_colide:
            score += 1
            enemy = Enemy("ufo.png", randint(20, win_w - 20), randint(-30, 0), 
            65, 45, 
            random() + randint(1, 2))
            enemies.add(enemy)

        asteroids_collide = sprite.spritecollide(player, asteroids, False)
        for _ in asteroids_collide:
            finish = True
            result_text = text_lose
            start_time = time.get_ticks()

        player_colide =  sprite.spritecollide(player, enemies, False)
        for i in player_colide:
            finish = True
            result_text = text_lose
            start_time = time.get_ticks()

        text_lost = font_text.render(
            f"Пропущено: {str(lost)}", 
            True, (255, 255, 255))

        window.blit(text_lost, (10, 45))

        text_score = font_text.render(
            f"Счет: {str(score)}", 
            True, (255, 255, 255))

        window.blit(text_score, (10, 5))
        
        if is_reload:
            reload_text = font_text.render("Перезадаряка...", True, (255, 10, 10))
            window.blit(reload_text, (win_w / 2 - 150, win_h - 60))
            current_time = time.get_ticks()
            if current_time - reload_time >= 3000:
                is_reload = False
                current_counter_bullet = 0

        if score >= 10:
            finish = True
            result_text = text_win
            start_time = time.get_ticks()

        if lost >= 3:
            finish = True
            result_text = text_lose
            start_time = time.get_ticks()

        player.update()
        player.reset()

        enemies.update()
        enemies.draw(window)

        asteroids.update()
        asteroids.draw(window)

        bullets.update()
        bullets.draw(window)
    else:
        if result_text == text_win:
            window.blit(result_text, (80, 150))
        else:
            window.blit(result_text, (50, 150))
    
        current_time = time.get_ticks()
        if current_time - start_time >= 3000:
            lost = 0
            score = 0
            current_counter_bullet = 0
            finish = False

            enemies.empty()
            for i in range(5):
                enemy = Enemy("ufo.png", randint(20, win_w - 20), randint(-30, 0), 
                65, 45, 
                random() + randint(1, 2))
                enemies.add(enemy)

            asteroids.empty()
            for _ in range(3):
                asteroid = Asteroid("asteroid.png", randint(20, win_w - 20), randint(-30, 0), 
                65, 45, 
                random() + randint(1, 2))
                asteroids.add(asteroid)

            bullets.empty()


    display.update()
    clock.tick(FPS)