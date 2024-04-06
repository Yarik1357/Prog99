import pygame
pygame.init()
win_w, win_h = 800, 500

window = pygame.display.set_mode((win_w, win_h))

fps = 60
clock= pygame.time.Clock()

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
    def __init__(self, x, y, w, h, image, speed, images):
        super().__init__(x, y, w, h, image)
        self.images = []
        for im in images:
            self.images.append(pygame.transform.scale(im, (w, h)))

        self.speed = speed
        self.state = "stay"
        self.count_anime = 60

    def move(self, key_left, key_right):
        k = pygame.key.get_pressed()
        if k[key_right]:
            if self.rect.right <= win_w:
                self.rect.x += self.speed 
                self.state = "walk"
        elif k[key_left]:
            if self.rect.left >= 0:
                self.rect.x -= self.speed
                self.state = "walk"

        else:
            self.state = "stay"

    def animation(self):

        if self.state == "stay":

            self.image = self.images[0]
        elif self.state == "walk":
            if self.count_anime >= 40:
                self.image = self.images[1]
            elif 20 < self.count_anime < 40:
                self.image = self.image[2]
            elif 0 < self.count_anime <= 20:
                self.image = self.images[3]
            else:
                self.count_anime = 60
        self.count_anime = -1

        


player_img = [pygame.image.load("img/1.png"),
              pygame.image.load("img/2.png"),
              pygame.image.load("img/3.png"),
              pygame.image.load("img/4.png")

]


player = Pers(20, win_h - 120, 85, 95, player_img[0], 3, player_img)
game = True

while game:

    window.fill((0, 0, 0))
    player.update()
    player.move(pygame.K_a, pygame.K_d)
    player.animation()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game =  False
    pygame.display.update()
    clock.tick(fps)
