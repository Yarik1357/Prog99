import pygame
pygame.init()

from maps import *

from random import randint

pygame.time.set_timer(pygame.USEREVENT, 5000)

win_w, win_h = 1050, 700

window = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption("Menu 0.1")

block_size = 65

fps = 60
clock= pygame.time.Clock()

background = pygame.image.load("img/bobo.png")
background = pygame.transform.scale(background, (win_w, win_h))

# pygame.mixer_music.load("snd/music1.mp3")
# pygame.mixer_music.play(-1)
# pygame.mixer_music.set_volume(0.2)

class Button:
    def __init__(self, x, y, w, h, image1, image2):
        self.rect = pygame.Rect(x, y, w, h)
        self.image1 = pygame.transform.scale(image1, (w, h))
        self.image2 = pygame.transform.scale(image2, (w, h))
        self.image = self.image1

    def reset(self, x, y):
        self.animate(x, y)
        window.blit(self.image, (self.rect.x, self.rect.y))

    def animate(self, x, y):
        if self.rect.collidepoint(x, y):
            self.image = self.image2
        else:
            self.image = self.image1


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
        self.vector = None
        self.count = 10
        self.shooting = False
        
        for im in images2:
            self.images_l.append(pygame.transform.scale(im, (w, h)))

        self.images = self.images_r

    
        
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

        if self.shooting:
            self.count -= 1
            if self.count == 0:
                self.shooting = False
                self.count = 10
        
    
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
    def shoot(self, x, y, speed):
        if not self.shooting:
            self.vector = (pygame.Vector2(self.rect.x, self.rect.y)-pygame.Vector2(x, y)).normalize()
            dx = self.vector[0] * speed
            dy = self.vector[1] * speed       
            print(self.vector)
            b = Bullet(self.rect.centerx, self.rect.y , 15, 20, bullet_img, dx, dy)
            self.shooting = True
            

bullets = []
class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, dx, dy):
        super().__init__(x, y, w, h, image)
        self.dx, self.dy = dx, dy
        
        bullets.append(self)

        
        
    def move(self):
        self.rect.x -= self.dx
        self.rect.y -= self.dy
        if self.rect.y <= -20:
            bullets.remove(self)

class Enemy(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.dx = 0
        self.dy = 0
       
    def move(self):
        self.rect.x -= self.dx
        self.rect.y -= self.dy
        vector = (pygame.Vector2(self.rect.x, self.rect.y)-pygame.Vector2(player.rect.x, player.rect.y)).normalize()
        self.dx = vector[0] * self.speed
        self.dy = vector[1] * self.speed

play_img = pygame.image.load("menu/Play.png")
options_img = pygame.image.load("menu/options.png")
quit_img = pygame.image.load("menu/Quit.png")
quit_img2 = pygame.image.load("menu/Quit3.png")
update_img = pygame.image.load("menu/Update.png")

click_snd = pygame.mixer.Sound("menu/click.mp3")

btn_play = Button(win_w//2-100, (win_h-10)//5, 200, 50, play_img, play_img)
btn_options = Button(win_w//2-100, (win_h-10)//5*2, 200, 50, options_img, options_img)
btn_quit = Button(win_w//2-100, (win_h-10)//5*3, 200, 50, quit_img, quit_img2)

btn_menu = Button(win_w//2-100, (win_h-10)//2, 200, 50, update_img, update_img)
btn_menu2 = Button(0, 0, 50, 20, update_img, update_img)



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

block_img = pygame.image.load("img/block3.png")
block2_img = pygame.image.load("img/grass.png")
bullet_img = pygame.image.load("img/bullet1.png")
ghost_img = pygame.image.load("img/ghost.png")


player = Pers(20, win_h - 120, 62, 75, player_img_r[0], 3, player_img_r, player_img_l)


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

enemies = []
for i in range(6):
    enemy = Enemy(randint(0, win_w-50), randint(-700, 0), 40, 50, ghost_img, 3)
    enemies.append(enemy)
    

finish = False
screen = "menu"
game = True

while game:

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if screen == "menu":
        window.blit(background, (0, 0))
        btn_play.reset(mouse_x, mouse_y)
        btn_options.reset(mouse_x, mouse_y)
        btn_quit.reset(mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game =  False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if btn_options.rect.collidepoint(x, y):
                        click_snd.play()
                        screen = "options"
                    elif btn_play.rect.collidepoint(x, y):
                        click_snd.play()
                        screen = "play"
                    elif btn_quit.rect.collidepoint(x, y):
                        click_snd.play()
                        game = False
    
    elif screen == "options":
        window.blit(background, (0, 0))
            
            

        btn_menu.reset(mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if btn_menu.rect.collidepoint(x, y):
                    click_snd.play()
                    screen = "menu"


    elif screen == "play":
        
        # window.blit(background, (0, 0))
        btn_menu2.reset(mouse_x, mouse_y)

        if not finish:
           
            window.blit(background, (0, 0))
            btn_menu2.reset(mouse_x, mouse_y)
            player.update()
            player.move()
            player.animation()
            # enemy.update()
            # enemy.move()
            for b in blocks:
                b.update()

            for enemy in enemies:
                enemy.update()
                enemy.move()

                if player.rect.colliderect(enemy.rect):
                    finish = True

                for bullet in bullets:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.rect.x, enemy.rect.y = randint(0, win_w-50), randint(-700, 0)
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        enemies.append(enemy)
                        
            
            for bullet in bullets:
                    
                    bullet.update()
                    bullet.move()      

            
            
         
                
            
            
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                print(x, y)
                player.shoot(x, y, 12)
                # player.vector = (pygame.Vector2(player.rect.x, player.rect.y)-pygame.Vector2(x, y)).normalize()

               
                # print(player.vector)

            
                if btn_menu2.rect.collidepoint(x, y):


                    finish = False
                    click_snd.play()
                    screen = "menu"

    pygame.display.update()
    clock.tick(fps)








