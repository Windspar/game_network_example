import queue
from pygame import Vector2
from pygame.time import Clock
from server import Server
from setting import *

class Player:
    def __init__(self):
        self.send_data = queue.Queue()
        self.position = Vector2()
        self.velocity = 0.02
        self.jump_velocity = 0.05
        self.jump_y = 0
        self.jumping = False
        self.falling = False
        self.move_left = False
        self.move_right = False
        self.movement_updated = False
        self.max_jump = 10

    def do_jump(self):
        if not self.jumping and not self.falling:
            self.jumping = True
            self.jump_y = self.position.y

    def update(self, delta, send):
        if self.falling:
            self.position.y += self.jump_velocity * delta
            if self.position.y >= self.jump_y:
                self.falling = False
                self.position.y = self.jump_y

        if self.jumping:
            self.position.y -= self.jump_velocity * delta
            self.movement_updated = True
            if self.position.y <= self.jump_y - self.max_jump:
                self.jumping = False
                self.falling = True

        if self.move_left:
            self.position.x -= self.velocity * delta
            self.movement_updated = True

        if self.move_right:
            self.position.x += self.velocity * delta
            self.movement_updated = True

        if self.movement_updated:
            send(MOVEMENT + " {} {}".format(*self.position))

class GameServer(Server):
    def __init__(self, host='0.0.0.0', port=9012, max_connection=4):
        Server.__init__(self, host, port, max_connection)
        self.players = {}
        self.clock = Clock()
        self.delta = 0
        self.fps = 60
        self.delay = 1000 / self.fps

    def accepting(self, socket):
        self.players[socket] = Player()

    def recieving(self, socket, data):
        if data.startwith(JUMP):
            self.players[socket].do_jump()
        elif data.startwith(MOVE_LEFT):
            self.players[socket].move_left()
        elif data.startwith(MOVE_RIGHT):
            self.players[socket].move_right()

    def disconnect(self, socket):
        pass

    def broadcasting(self, socket):
        pass

    def send(self, data):
        for player in self.players:
            player.send_data.put(data)

    def server_loop(self):

        for player in self.players:
            player.update(self.delta, self.send)

        self.delta = self.clock.tick(self.fps)
