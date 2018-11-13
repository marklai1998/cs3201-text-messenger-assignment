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
        try:
            address = (self.HOST, self.PORT)
            self.SERVER = socket(AF_INET, SOCK_STREAM)
            self.SERVER.bind(address)
            self.SERVER.listen(5)
            logging.debug("Accepting connection at port %i" % self.PORT)
            thread = Thread(target=self.acceptConnections)
            thread.start()
        except:
            self.master.backToMain()
            messagebox.showerror("Error", "Fail to bind port")
            logging.error("Fail to bind port")

    def stopServer(self):
        try:
            logging.debug("Stopping Server")
            self.broadcast(bytes("*SERVER_STOP*", "utf8"))
            self.SERVER.close()
            self.SERVER = None
        except:
            pass

    def acceptConnections(self):
        while self.SERVER is not None:
            try:
                client, client_address = self.SERVER.accept()
                logging.debug("%s:%s has connected." % client_address)
                client.send(
                    bytes("What is your name", "utf8"))
                self.addresses[client] = client_address
                Thread(target=self.handleClient, args=(client,)).start()
            except:
                logging.debug('Server Stopped')
                break

    def handleClient(self, client):
        try:
            name = client.recv(self.bufferSize).decode("utf8")
            welcome = 'Welcome %s!' % name
            client.send(bytes(welcome, "utf8"))
            msg = "%s has joined the room!" % name
            self.broadcast(bytes(msg, "utf8"))
            self.clients[client] = name

            while self.SERVER is not None:
                try:
                    msg = client.recv(self.bufferSize)
                    self.broadcast(msg, name+": ")
                except:
                    try:
                        client.send(bytes("*SERVER_STOP*", "utf8"))
                        client.close()
                    except:
                        pass
                    del self.clients[client]
                    self.broadcast(
                        bytes("%s has left the chat." % name, "utf8"))
                    break
        except:
            pass

    def broadcast(self, msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8")+msg)
