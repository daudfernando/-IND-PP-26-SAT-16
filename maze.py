# menghubungkan modul
from pygame import *


# Parent Class
class GameSprite(sprite.Sprite):
    # properti parent Class
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    # method update sprite
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Untuk membuat hero Eater Pacman
class Player(GameSprite):
    def __init__(
        self,
        player_image,
        player_x,
        player_y,
        size_x,
        size_y,
        player_x_speed,
        player_y_speed,
    ):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)


        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    
    # supaya bisa bergerak
    def update(self):
        """moves the character using the current horizontal and vertical speed"""
        # Kontrol Kanan Kiri (Sumbu X)
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed


        platforms_touched = sprite.spritecollide(self, barriers, False)
        # Kontrol Ke Kanan perlu dicegah tembus dinding
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        # Kontrol Ke Kiri perlu dicegah tembus dinding
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)


        # Kontrol Atas Bawah (Sumbu Y)
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed


        platforms_touched = sprite.spritecollide(self, barriers, False)
        # Kontrol Ke Atas perlu dicegah tembus dinding
        if self.y_speed > 0:
            for p in platforms_touched:
               self.y_speed = 0
               if p.rect.top < self.rect.bottom:
                   self.rect.bottom = p.rect.top
        
        # Kontrol Ke Bawah perlu dicegah tembus dinding
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)
    
    #method nembak
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)


# Kelas Musuh (otomatis gerak)
class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    
    #update geraknya musuh
    def update(self):
        if self.rect.x <= 420: #w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed




# Membuat kelas bullet
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    
    # pergerak bullet yang dimunculkan
    def update(self):
        self.rect.x += self.speed
        # menghilang ketika sampai ujung layar kanan
        if self.rect.x > win_width+10:
            self.kill()


      


# membuat window appsnya
win_width = 700
win_height = 500
display.set_caption("Maze Game v.2")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)  # warna biru muda
barriers = sprite.Group()




# buat objek bullet dan monster
bullets = sprite.Group()
monsters = sprite.Group()


# membuat dinding
w1 = GameSprite("platform2.png", win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite("platform2_v.png", 370, 100, 50, 400)


barriers.add(w1)
barriers.add(w2)


# sprite - spritenya
packman = Player("hero.png", 5, win_height - 80, 80, 80, 0, 0)
monster = Enemy("cyborg.png", win_width - 80, 180, 80, 80, 5)
final_sprite = GameSprite("pac-1.png", win_width - 85, win_height - 100, 80, 80)


monsters.add(monster)


finish = False


# looping game
run = True
while run:
    # berjalan tiap 0.05
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0


    if not finish:
        window.fill(back)  # fill in the window with color
        packman.update()
        bullets.update()
        packman.reset()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()


        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)




        # kondisi kalah
        if sprite.spritecollide(packman, monsters, False):
            finish = True


            img = image.load("game-over_1.png")
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))


        # kondisi menang
        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load("thumb.jpg")
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))


    time.delay(50)
    display.update()


