import pygame, sys, socket, pickle, os, time, random
from pygame.locals import * #imports additional pygame modules

pygame.init()
screen_width=600
screen_height=800
host = "" # server ip addr here
port = 8889
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

#img
bg = pygame.image.load(os.path.join("img", "backGame.jpg"))
bg = pygame.transform.scale(bg, (screen_width, screen_height)) #resize bg to screen resolution
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

        #sterowanie strzalki/wsad + kolizja gracz - sciana (rowniez gracz nie moze przekroczyc srodka boiska)
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.radius - 15:
            self.x += speed
        if keys[pygame.K_LEFT] and self.x > 0 + self.radius + 15:
            self.x -= speed
        if keys[pygame.K_DOWN] and self.y < screen_height/2 - self.radius and self.id == 0:
            self.y += speed
        if keys[pygame.K_DOWN] and self.y < screen_height - self.radius - 15 and self.id == 1:
            self.y += speed
        if keys[pygame.K_UP] and self.y > 0 + self.radius + 15 and self.id == 0:
            self.y -= speed
        if keys[pygame.K_UP] and self.y > screen_height/2 + self.radius and self.id == 1:
            self.y -= speed

class Ball():
    def __init__(self, x, y, ball_color, radius):
        self.x = x
        self.y = y
        self.ball_color = ball_color
        self.radius = radius

    def draw(self, screen):
        #pygame.draw.circle(screen, self.ball_color, (self.x, self.y), self.radius) #zostawic dla testow kolizji
        screen.blit(puck, (self.x - self.radius, self.y - self.radius))

    def move(self, change_direction, speed): # automatic movement
        #test
        if change_direction == 0:
            self.y += speed
        elif change_direction == 1:
            self.y -= speed

        #later more directions etc.

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

def collisionPlayerPuck(playerObject, puckObject):
    pass

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

        player.move(2)
        ball.move(1, 5)

        # drawing
        screen.blit(bg, (0, 0))
        player.draw(screen)
        player2.draw(screen)
        ball.draw(screen) #draw only one ball, ignore 1 of 2 ball objects
        clock.tick(60) #fps
        pygame.display.flip()

        #print("player obj",player)
        #print("ball obj", ball)

startScreen()
main()