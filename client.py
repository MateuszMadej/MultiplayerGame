import pygame, sys, socket, pickle, os
from pygame.locals import * #imports additional pygame modules

pygame.init()
screen_width=600
screen_height=800
host = "" # server ip addr here
port = 8888
screen = pygame.display.set_mode((screen_width, screen_height))

#img
bg = pygame.image.load(os.path.join("img", "backGame.jpg"))
bg = pygame.transform.scale(bg, (screen_width, screen_height)) #resize bg to screen resolution
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
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and self.x < screen_width - self.radius - 15:
            self.x += speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and self.x > 0 + self.radius + 15:
            self.x -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN] and self.y < screen_height/2 - self.radius and self.id == 0:
            self.y += speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN] and self.y < screen_height - self.radius - 15 and self.id == 1:
            self.y += speed
        if keys[pygame.K_w] or keys[pygame.K_UP] and self.y > 0 + self.radius + 15 and self.id == 0:
            self.y -= speed
        if keys[pygame.K_w] or keys[pygame.K_UP] and self.y > screen_height/2 + self.radius and self.id == 1:
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

    def move(self, change_direction): # automatic movement
        #test
        if change_direction == 1:
            self.y += 1
        elif change_direction == 2:
            self.y -= 1

        #later more directions

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
        self.client.connect(self.addr)
        return pickle.loads(self.client.recv(2048)) #Read a pickled object hierarchy from a string

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as msg:
            print(str(msg[0]))

def collisionPlayerPuck(playerObject, puckObject):
    pass

def main():
    ball = Ball(300, 400, (255,0,0), 15) #only for test (will be move to the server)
    sa = ServerActions(port, host)
    player = sa.getP()

    while True:
        player2 = sa.send(player)

        # handle events
        for event in pygame.event.get(): # checking all events
            if event.type == pygame.QUIT:
                sys.exit(0) # quit game
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        player.move(2)
        ball.move(1)

        # drawing
        screen.blit(bg, (0, 0))
        ball.draw(screen)
        player.draw(screen)
        player2.draw(screen)
        pygame.display.flip()

        #print(player.x, player.y)
        #print(ball.x, ball.y)

main()