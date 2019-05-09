import pygame, sys, socket, pickle

class Player():
    def __init__(self, x, y, player_width, player_height, player_color):
        self.x = x
        self.y = y
        self.player_width = player_width
        self.player_height = player_height
        self.player_color = player_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.player_color, pygame.Rect(self.x, self.y, self.player_width, self.player_height))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= 1

screen_width=450
screen_height=450
host = "192.168.8.113" # server ip addr here
port = 8888
screen = pygame.display.set_mode((screen_width, screen_height))

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


def main():
    # handle events
    sa = ServerActions(port, host)
    player = sa.getP()

    while True:
        player2 = sa.send(player)

        for event in pygame.event.get(): # checking all events
            if event.type == pygame.QUIT:
                sys.exit(0) # quit game
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        player.move()

        # drawing
        screen.fill((0,0,0))
        player.draw(screen)
        player2.draw(screen)
        pygame.display.flip()

main()