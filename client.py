import pygame, sys, socket, pickle, os, time, random
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
        self.speed = 5 #must be also changed in server's ball object
        self.speed_y = 0
        self.p1, self.p2 = 0, 0

    def draw(self, screen):
        #pygame.draw.circle(screen, self.ball_color, (self.x, self.y), self.radius) #zostawic dla testow kolizji
        screen.blit(puck, (self.x - self.radius, self.y - self.radius))

    def move(self, player1, player2): # automatic movement and checking collision
        #radius player = 25, radius puke = 15
        #print(player1.id)

        self.x += self.speed
        #self.y += self.speed

        '''
        #beta puck - player collision - now bugged if move player up or down.. (solution - check testing prints below)
        if self.x + 45 <= player1.x:
            if self.y - 5 <= player1.y and self.y + 5 >= player1.y:
                self.speed *= -1
                #print("test p1")

        if self.x - 45 >= player2.x:
            if self.y - 5 <= player2.y and self.y + 5 >= player2.y:
                self.speed *= -1
                #print("test p2")
        '''

        #print(self.y, player1.y)
        #print(self.speed)
        print(self.p1, self.p2)

        #puck - bands collision and points counter - all working..
        if self.x <= 0 + 35: #left band
            if self.y <= 400 and self.y >= 200:#if hits the goal
                self.p1 += 1
                self.x, self.y = 640, 300 #move puck to middle area
            self.speed *= -1 #and change direction to scorer side

        if self.x >= screen_width - 35: #right band
            if self.y <= 400 and self.y >= 200:  # if hits the goal
                self.p2 += 1
                self.x, self.y = 640, 300 #same as above
            self.speed *= -1 #same as above


        if self.y <= 0 + 30: #upper band
            self.speed = 0 #now only stop puck
        if self.y >= screen_height - 30: #lower band
            self.speed =0 #now only stop puck

    def get_score(self):
        return self.p1, self.p2

    def draw_score(self): #here or outside this class?
        pass

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

        # drawing
        screen.blit(bg, (0, 0))
        player.draw(screen)
        player2.draw(screen)
        ball.draw(screen) #draw only one ball, ignore other ball object
        clock.tick(60) #fps
        pygame.display.flip()

startScreen()
main()