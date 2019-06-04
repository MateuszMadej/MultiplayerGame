import pygame, sys, socket, pickle, os, time, random, math
from pygame.locals import * #imports additional pygame modules

pygame.init()
screen_width=1280
screen_height=600
host = "localhost" # server ip addr here
port = 8889
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

#img
bg = pygame.image.load(os.path.join("img", "bg.jpg"))
bg = pygame.transform.scale(bg,(screen_width, screen_height))#resize bg to screen resolution
logo = pygame.image.load(os.path.join("img", "air-hockey.png"))
logo = pygame.transform.scale(logo, (180, 180))
player = pygame.image.load(os.path.join("img", "player1.png"))
player = pygame.transform.scale(player, (50, 50))
player2 = pygame.image.load(os.path.join("img", "player2.png"))
player2 = pygame.transform.scale(player2, (50, 50))
puck = pygame.image.load(os.path.join("img", "puck.png"))
puck = pygame.transform.scale(puck, (30, 30))

class Player():
    def __init__(self, x, y, player_color, radius, id):
        self.x = x
        self.y = y
        self.player_color = player_color
        self.radius = radius
        self.id = id

    def draw(self, screen):
        #pygame.draw.circle(screen, self.player_color, (self.x, self.y), self.radius) #zostawic dla testow kolizji
        if self.id == 0:
            screen.blit(player, (self.x-self.radius, self.y-self.radius))
        elif self.id == 1:
            screen.blit(player2, (self.x-self.radius, self.y-self.radius))

    def move(self, speed): #moving by mouse or keyboard?
        keys = pygame.key.get_pressed()

        #sterowanie strzalki + kolizja gracz - sciana (rowniez gracz nie moze przekroczyc srodka boiska)
        if keys[pygame.K_RIGHT] and self.x < screen_width/2 - self.radius and self.id == 0:
            self.x += speed
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.radius - 15 and self.id == 1:
            self.x += speed
        if keys[pygame.K_LEFT] and self.x > 0 + self.radius + 15 and self.id == 0:
            self.x -= speed
        if keys[pygame.K_LEFT] and self.x > screen_width/2 + self.radius and self.id == 1:
            self.x -= speed
        if keys[pygame.K_DOWN] and self.y < screen_height - self.radius - 15 and self.id == 0:
            self.y += speed
        if keys[pygame.K_DOWN] and self.y < screen_height - self.radius - 15 and self.id == 1:
            self.y += speed
        if keys[pygame.K_UP] and self.y > 0 + self.radius + 15 and self.id == 0:
            self.y -= speed
        if keys[pygame.K_UP] and self.y > 0 + self.radius + 15 and self.id == 1:
            self.y -= speed


class Ball():
    def __init__(self, x, y, ball_color, radius):
        self.x = x
        self.y = y
        self.ball_color = ball_color
        self.radius = radius
        self.speed = 10 #must be also changed in server's ball object
        self.speed_y = 0
        self.size = 60
        self.vx = 5
        self.vy = 2
        self.p1, self.p2 = 0, 0

    def draw(self, screen):
        #z = pygame.draw.circle(screen, self.ball_color, (int(self.x), int(self.y)), self.radius) #zostawic dla testow kolizji
        screen.blit(puck, (self.x - self.radius, self.y - self.radius))
        self.getPoints() #draw points do screen

    def regX(self, d):
        self.vx = d
        return self.vx

    def regY(self, d):
        self.vy = d
        return self.vy

    def up(self):
        self.vy = -2
        return self.vy

    def down(self):
        self.vy = 2
        return self.vy

    def left(self):
        es1 = 0.243 * -10

        if(es1 >= -4):
            es1 = -5

        self.vx = es1

        return self.vx

    def right(self):
        es1 = 0.243 * 10

        if(es1 <= 4):
            es1 = 5

        self.vx = es1

        return self.vx


    def move(self, player1, player2): # automatic movement and checking collision
        self.setY(self.getY() + self.vy)
        self.setX(self.getX() + self.vx)

        if(self.getY() >= screen_height - self.size +30):
            self.setY(self.getY() + self.up())
        elif(self.getY() <= 30):
            self.setY(self.getY() + self.down())

        elif(self.getX() < 30 and (self.getY() < 200 or self.getY() > 400)):
            print("lewatest")
            self.setX(self.getX() + self.right())
        elif(self.getX() >= screen_width - 30 and (self.getY() < 200 or self.getY() > 400)):
            print("prawatest")
            self.setX(self.getX() + self.left())


        if(self.getX() >= screen_width and self.getY() > 200 and self.getY() < 400):
            self.p2+=1
            self.setY(screen_height/2)
            self.setX(screen_width/2)

            es1 = 0.62 * -3
            es2 = 0.532 * -3

            if(es1 >= 0):
                es1 = -1
            elif(es2 >= 0):
                es2 = -1

            self.regX(es1)
            self.regY(es2)

        elif(self.getX() <= 0 and self.getY() > 200 and self.getY() < 400):
            self.p1+=1
            self.setY(screen_height/2)
            self.setX(screen_width/2)

            es1 = 0.44 * 3
            es2 = 0.34 * 3

            if(es1 <= 0):
                es1 = 1
            elif(es2 <= 0):
                es2 = 1

            self.regX(es1)
            self.regY(es2)

        self.collision(player1, player2)

    def collision(self, player1, player2):
        if(math.sqrt((player1.x - self.x)**2 + (player1.y - self.y)**2) <= self.radius + player1.radius):
            es1 = 0.543 * -2

            if(es1 >=0):
                es1 = -1

            self.setX(self.getX() + self.right())
            self.setY(self.getY() + es1)
        elif(math.sqrt((player2.x - self.x)**2 + (player2.y - self.y)**2) <= self.radius + player2.radius):
            es2 = 0.543 * 2

            if(es2 <= 0):
                es2 = 1

            self.setX(self.getX() + self.left())
            self.setY(self.getY() + es2)

    def getY(self):
        return self.y

    def setY(self, ay):
        self.y = ay

    def getX(self):
        return self.x

    def setX(self, ax):
        self.x = ax

    def getPoints(self): #draw message to screen
        message_to_screen(str(self.p1), (0,0,205), 265, "medium")
        message_to_screen(str(self.p2), (0,128,0), -265, "medium")
        #pygame.display.update()



class ServerActions: # connecting to server and sending, receiving data
    def __init__(self, port, host):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = host
        self.port = port
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p #return connected players starting position

    def connect(self):
        self.client.connect(self.addr) #first connect to server
        return pickle.loads(self.client.recv(2048)) #Read a pickled object hierarchy from a string

    def justGet(self): #only used if we are connected
        return pickle.loads(self.client.recv(2048))

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as msg:
            print(str(msg[0]))

def startScreen():
    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill((22,62,115))
        screen.blit(logo, ((screen_width / 2)-90,(screen_height / 2)-40))
        message_to_screen("AirHockey!",(255,255,255),-100,"large")
        message_to_screen("Wciśnij C, aby rozpocząć nową grę lub Q, aby wyjść!",(255,255,255),180)
        pygame.display.update()
        clock.tick(15)

def text_objects(text, color, size):
    smallfont = pygame.font.SysFont("comicsansms", 25)
    medfont = pygame.font.SysFont("comicsansms", 50)
    largefont = pygame.font.SysFont("comicsansms", 80)

    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (screen_width / 2), (screen_height / 2)+y_displace
    screen.blit(textSurf, textRect)

def main():
    sa = ServerActions(port, host)
    player = sa.getP() #connect and get player starting position
    ball = sa.justGet() #just get ball starting position

    while True:
        player2 = sa.send(player)
        ball = sa.send(ball)

        # handle events
        for event in pygame.event.get(): # checking all events
            if event.type == pygame.QUIT:
                sys.exit(0) # quit game
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        player.move(3)
        ball.move(player, player2)
        ball.getPoints()

        # drawing
        screen.blit(bg, (0, 0))
        player.draw(screen)
        player2.draw(screen)
        ball.draw(screen) #draw only one ball, ignore other ball object
        clock.tick(120) #fps
        pygame.display.flip()

startScreen()
main()