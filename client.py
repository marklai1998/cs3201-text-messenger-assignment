from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import logging
import tkinter as tk
from tkinter import ttk
logging.getLogger().setLevel(10)


class getClient(ttk.Frame):
    bufferSize = 1024

    def __init__(self, master, IP, PORT):
        self.master = master
        self.IP = IP
        self.PORT = PORT
        ttk.Frame.__init__(self)

        messages_frame = ttk.Frame(self)
        self.textInput = tk.StringVar()  # For the messages to be sent.
        self.textInput.set("Type your messages here.")
        # To navigate through past messages.
        scrollbar = ttk.Scrollbar(messages_frame)
        # Following will contain the messages.
        self.messageList = tk.Listbox(messages_frame, height=15,
                                      width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.messageList.pack(side=tk.LEFT, fill=tk.BOTH)
        self.messageList.pack()
        messages_frame.pack()

        entry_field = ttk.Entry(self, textvariable=self.textInput)
        # entry_field.bind("<Return>", self.send(self.textInput.get()))
        entry_field.pack()
        send_button = ttk.Button(
            self, text="Send", command=lambda: self.send(self.textInput.get()))
        send_button.pack()

        ttk.Button(self, text="Return to start page",
                   command=lambda: master.backToMain()).pack()

    def startClient(self):
        address = (self.IP, self.PORT)
        self.CLIENT = socket(AF_INET, SOCK_STREAM)
        self.CLIENT.connect(address)
        logging.debug("Connected Server at %s:%i" % (self.IP, self.PORT))
        thread = Thread(target=self.receive)
        thread.start()

    def stopClient(self):
        try:
            logging.debug("stopping")
            self.CLIENT.close()
            self.CLIENT = None
        except:
            pass

    def receive(self):
        while self.CLIENT is not None:
            try:
                msg = self.CLIENT.recv(self.bufferSize).decode("utf8")
                self.messageList.insert(tk.END, msg)
            except:  # Possibly client has left the chat.
                logging.debug('Client Stopped')
                break

    def send(self, message):
        self.textInput.set("")  # Clears input field.
        self.CLIENT.send(bytes(message, "utf8"))
