import pygame
import os
from pygame import *
from tkinter import messagebox
from tkinter import *
from PIL import Image,ImageTk
import levels

DISPLAY = (800, 640)
DEPTH = 32
FLAGS = 0

# in blocks, 25 x 20

window=Tk()
window.geometry('300x300')
window.title('Platformer')
window.resizable(width=False,height=False)
image=Image.open("entrance.png")
background_image=ImageTk.PhotoImage(image)
background_label = Label(window, image=background_image).place(x=0, y=0, relwidth=1, relheight=1)
lbTitle=Label(window,text="P L A T F O R M E R",fg='blue',bg='yellow',relief='solid',font=("arial",12,"bold")).pack(fill=Y,pady=5,padx=5)
def info():
   messagebox.showinfo( "How To Play", "Use arrow keys to move")
btnPlay = Button(window, text='Play', command=window.destroy, width=10,bg="light yellow").place(relx = 0.5, rely = 0.7, anchor = CENTER)
btnInfo = Button(window, text ="Info", command = info,width=10,bg="light yellow").place(relx = 0.5, rely = 0.8, anchor = CENTER)
btnExit = Button(window, text ="Exit", command = exit,width=10,bg="red").place(relx = 0.5, rely = 0.9, anchor = CENTER)
window.mainloop()

def main():
    pygame.init()
    screen = display.set_mode(DISPLAY, FLAGS, DEPTH)
    display.set_caption("Platformer")
    timer = time.Clock()
    current_level = 1

    up = down = left = right = False
    bg = Surface((32, 32))
    bg.convert()
    bg.fill(Color("#101010"))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []

    x = y = 0
    level = levels.levels[current_level]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            x += 32
        y += 32
        x = 0

    entities.add(player)

    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("quit")
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit("ESCAPE")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False

        # draw background
        for y in range(20):
            for x in range(25):
                screen.blit(bg, (x * 32, y * 32))

        # update player, draw everything else
        player.update(up, down, left, right, platforms)
        entities.draw(screen)

        pygame.display.flip()


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = pygame.image.load(os.path.join('char.png'))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, down, left, right, platforms):
        if up:
            # only jump if on the ground
            if self.onGround:
                self.yvel -= 7
        if down:
            pass
        if left:
            self.xvel = -5
        if right:
            self.xvel = 5
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.4
            # max falling speed
            if self.yvel > 30:
                self.yvel = 30
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    event.post(event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load(os.path.join('wall1.png'))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass


class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load(os.path.join('exit.png'))


if(__name__ == "__main__"):
    main()
