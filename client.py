from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import logging
import tkinter as tk
from tkinter import ttk, messagebox
logging.getLogger().setLevel(10)

backgroundColor = "#151515"
textColor = "#e6e6e6"


class getClient(ttk.Frame):
    bufferSize = 1024

    def __init__(self, master, IP, PORT):
        self.master = master
        self.IP = IP
        self.PORT = PORT

        ttk.Style().theme_use('default')
        ttk.Frame.__init__(self, style="mainFrame.TFrame")

        messagesFrame = ttk.Frame(self)
        self.textInput = tk.StringVar()
        scrollbar = ttk.Scrollbar(messagesFrame)
        self.messageList = tk.Listbox(messagesFrame, height=15,
                                      width=50, yscrollcommand=scrollbar.set, borderwidth=0, font=('Rajdhani', 15))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.messageList.pack(side=tk.LEFT, fill=tk.BOTH)
        self.messageList.pack(fill="both", expand=1)
        messagesFrame.pack(side="top", fill="both", expand=1)

        sendButtonStyle = ttk.Style()
        sendButtonStyle.theme_use('default')
        sendButtonStyle.configure("clientSend.TButton", background="#2196f3", padding=(5, 7, 5, 7), borderwidth=0,
                                  foreground="#FFF", font=('Rajdhani', 12))
        sendButtonStyle.map("clientSend.TButton", background=[
            ('focus', "#1976d2")])
        exitButtonStyle = ttk.Style()

        exitButtonStyle.theme_use('default')
        exitButtonStyle.configure("clientExit.TButton", background="#1976d2", padding=(10, 7, 10, 7), borderwidth=0,
                                  foreground="#FFF", font=('Rajdhani', 12))
        exitButtonStyle.map("clientSend.TButton", background=[
            ('focus', "#1976d2")])

        inputFrame = ttk.Frame(self)
        ttk.Entry(inputFrame, textvariable=self.textInput, style="field.TEntry", font=('Rajdhani', 15)).pack(
            side="left", expand=1)
        ttk.Button(
            inputFrame, text="Send", command=lambda: self.send(self.textInput.get()), style="clientSend.TButton").pack(side="left", expand=1)
        ttk.Button(inputFrame, text="Exit",
                   command=lambda: master.backToMain(), style="clientExit.TButton").pack(side="left", expand=1)
        inputFrame.pack(side="bottom", fill="x")

    def startClient(self):
        try:
            address = (self.IP, self.PORT)
            self.CLIENT = socket(AF_INET, SOCK_STREAM)
            self.CLIENT.connect(address)
            logging.debug("Connected Server at %s:%i" % (self.IP, self.PORT))
            thread = Thread(target=self.receive)
            thread.start()
        except:
            self.master.backToMain()
            messagebox.showerror("Error", "Server Not Found")
            logging.error("Server Not Found")

    def stopClient(self):
        try:
            logging.debug("Stopping Client")
            self.CLIENT.close()
            self.CLIENT = None
        except:
            pass

    def receive(self):
        while self.CLIENT is not None:
            try:
                msg = self.CLIENT.recv(self.bufferSize).decode("utf8")
                logging.debug("Message received: %s " % (msg))
                if msg != "*SERVER_STOP*":
                    self.messageList.insert(tk.END, msg)
                else:
                    self.master.backToMain()
                    messagebox.showerror("Error", "Connection Lost")
                    logging.error("Connection Lost")
                    break
            except:
                logging.debug('Client Stopped')
                break

    def send(self, message):
        self.textInput.set("")
        self.CLIENT.send(bytes(message, "utf8"))
