from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import logging
logging.getLogger().setLevel(10)


class getServer:
    bufferSize = 1024
    clients = {}
    addresses = {}

    def __init__(self, port):
        self.HOST = ''
        self.PORT = port

    def startServer(self):
        address = (self.HOST, self.PORT)
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(address)
        self.SERVER.listen(5)
        logging.debug("Accepting connection at port %i" % self.PORT)
        thread = Thread(target=self.acceptConnections)
        thread.start()

    def stopServer(self):
        self.SERVER.close()
        self.SERVER = None

    def acceptConnections(self):
        while self.SERVER is not None:
            try:
                client, client_address = self.SERVER.accept()
                logging.debug("%s:%s has connected." % client_address)
                client.send(
                    bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
                self.addresses[client] = client_address
                Thread(target=self.handleClient, args=(client,)).start()
            except:
                logging.debug('Server Stopped')
                break

    def handleClient(self, client):  # Takes client socket as argument.
        try:
            name = client.recv(self.bufferSize).decode("utf8")
            welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
            client.send(bytes(welcome, "utf8"))
            msg = "%s has joined the chat!" % name
            self.broadcast(bytes(msg, "utf8"))
            self.clients[client] = name

            while self.SERVER is not None:
                try:
                    msg = client.recv(self.bufferSize)
                    if msg != bytes("{quit}", "utf8"):
                        self.broadcast(msg, name+": ")
                    else:
                        client.send(bytes("{quit}", "utf8"))
                        client.close()
                        del self.clients[client]
                        self.broadcast(
                            bytes("%s has left the chat." % name, "utf8"))
                        break
                except:
                    self.broadcast(
                        bytes("%s has left the chat." % name, "utf8"))
                    break
        except:
            pass

    def broadcast(self, msg, prefix=""):  # prefix is for name identification.
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8")+msg)
