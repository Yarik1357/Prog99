import pygame
pygame.init()

from maps import *

#win_w, win_h = 800, 500
win_w, win_h = 1050, 700

window = pygame.display.set_mode((win_w, win_h))

block_size = 85

fps = 60
clock= pygame.time.Clock()

background = pygame.image.load("img/bobo.png")
background = pygame.transform.scale(background, (win_w, win_h))

# pygame.mixer_music.load("snd/music1.mp3")
# pygame.mixer_music.play(-1)
# pygame.mixer_music.set_volume(0.2)


class GameSprite:
    def __init__(self, x, y, w, h, image ):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Pers(GameSprite):
    def __init__(self, x, y, w, h, image, speed, images, images2):
        super().__init__(x, y, w, h, image)
        self.images_r = []
        
        
        for im in images:
            self.images_r.append(pygame.transform.scale(im, (w, h)))
        
        self.speed = speed
        self.state = "stay"
        self.count_anime = 60

        self.images_l = []
        
        
        for im in images2:
            self.images_l.append(pygame.transform.scale(im, (w, h)))

        self.images = self.images_r

    # def move(self, key_left, key_right):
    #     k = pygame.key.get_pressed()
    #     if k[key_right]:
    #         self.images = self.images_r
    #         if self.rect.right <= win_w:
    #             self.rect.x += self.speed 
    #             self.state = "walk"
    #     elif k[key_left]:
    #         self.images = self.images_l
    #         if self.rect.left >= 0:
    #             self.rect.x -= self.speed
    #             self.state = "walk"
    #     elif k[pygame.K_w]:
    #         if self.rect.y >= 0:
    #             self.rect.y -= self.speed

    #     elif k[pygame.K_s]:
    #         if self.rect.bottom <= win_h:
    #             self.rect.y += self.speed

    #     else:
    #         self.state = "stay"
        
    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_d]:
            self.images = self.images_r
            if self.rect.right <= win_w:
                self.rect.x += self.speed  
                self.state = "walk"
        elif k[pygame.K_a]:
            self.images = self.images_l
            if self.rect.left >= 0:
                self.rect.x -= self.speed
                self.state = "walk"

        elif k[pygame.K_w]:
            if self.rect.y >= 0:
                self.rect.y -= self.speed
                self.state = "walk"

        elif k[pygame.K_s]:
            if self.rect.bottom <= win_h:
                self.rect.y += self.speed
                self.state = "walk"
        else:
            self.state = "stay"


    def animation(self):
        

        if self.state == "stay":

            self.image = self.images[0]
        elif self.state == "walk":
            print(self.count_anime)
            if self.count_anime >= 40:
                self.image = self.images[1]
            elif 20 < self.count_anime < 40:
                self.image = self.images[2]
            elif 0 < self.count_anime <= 20:
                self.image = self.images[3]
            else:
                self.count_anime = 60
            self.count_anime -= 2.8
            

        



player_img_r = [pygame.image.load("img/1.png"),
              pygame.image.load("img/2.png"),
              pygame.image.load("img/3.png"),
              pygame.image.load("img/4.png")

]

player_img_l = [pygame.transform.flip(pygame.image.load("img/1.png"), True, False),
              pygame.transform.flip(pygame.image.load("img/2.png"), True, False),
              pygame.transform.flip(pygame.image.load("img/3.png"), True, False),
              pygame.transform.flip(pygame.image.load("img/4.png"), True, False)

]

block_img = pygame.image.load("img/block.png")
block2_img = pygame.image.load("img/block2.png")


player = Pers(20, win_h - 120, 62, 75, player_img_r[0], 3, player_img_r, player_img_l)
game = True

blocks = []
x, y = 0, 0

for line in lvl:
    for simv in line:
        if simv == "1":
            b = GameSprite(x ,y, block_size, block_size, block_img)
            blocks.append(b)
        if simv == "2":
            b = GameSprite(x ,y, block_size, block_size, block2_img)
            blocks.append(b)
            
        x += block_size
    x = 0
    y += block_size


while game:

    window.blit(background, (0,0))
    player.update()
    # player.move(pygame.K_a, pygame.K_d)
    player.move()
    player.animation()
    for b in blocks:
            b.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game =  False
    pygame.display.update()
    clock.tick(fps)
