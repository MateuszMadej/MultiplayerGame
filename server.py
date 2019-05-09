import socket, sys, pickle
from _thread import *

class Player():
    def __init__(self, x, y, player_width, player_height, player_color):
        self.x = x
        self.y = y
        self.player_width = player_width
        self.player_height = player_height
        self.player_color = player_color

host = "192.168.8.113" #ip addr here
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket created

# bind socket to local host and port
try:
    s.bind((host, port))
except socket.error as msg:
    print("Bind failed. Error Code: " + str(msg[0]))
    sys.exit()

# start listening on socket
s.listen(2) # for only 2 connections
print("Socket now listening.")
players = [Player(100,100,50,50,(255,255,0)), Player(200,200, 50,50, (0,255,0))] #two players starting position



def client_thread(conn, player):
    # Return the pickled representation of the object as a string - pickle.dumps
    # sending message to connected client (only takes strings) - conn.send
    conn.send(pickle.dumps(players[player]))
    while True: #infinite loop so that function do not terminate and thread do not end
        # Receiving from client - 2048 bits
        data = pickle.loads(conn.recv(2048))
        players[player] = data
        #print(player)

        if not data:
            print("Disconnected")
            break
        else:
            if player == 1:
                reply = players[0]
            else:
                reply = players[1]

            print("Received: ", data)
            print("Sending : ", reply)

        conn.sendall(pickle.dumps(reply)) #Send data to the socket.

    print("Disconnected")
    conn.close() #close connetion

player = 0 #current player id
while True:
    conn, addr = s.accept()
    print("Connected with: ", addr)
    # start new thread, takes first argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(client_thread, (conn, player))
    player +=1 #next player id


s.close() #close socket