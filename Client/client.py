import os
import tkinter as tk
from tkinter import ttk
import socket
from datetime import datetime
import subprocess
from tkinter import messagebox
from tkinter import simpledialog

window = tk.Tk()
window.title("App")
window.geometry("500x380")

file = open("ServerInfor.txt", "r")
Info = file.read().strip().split(" ")
ServerIP = Info[0]
ServerPort = int(Info[1])
BUFFER_SIZE = 4096

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ServerFileList = []
ClientFileList = []
ServerCheck = tk.IntVar()
OtherCheck = tk.IntVar()

def GetFileList():
  path = os.getcwd()
  ClientFileList = os.listdir(path)
  SystemFile = ["client.py", "login.py", "SignUp.py", "login.txt", "IPPort.py", "IsIP.txt", "ServerInfor.txt"]
  for i in SystemFile:
    ClientFileList.remove(i)
  fileList["value"] = ClientFileList
  statusText.insert(tk.END, f"{datetime.now()}: Client file list refreshed\n")

def GetFilePassword():
  password = passwordText.get()
  if password == "":
    return ""
  else:
    return password

def SendFileToServer():
  FileName = fileList.get()
  if (FileName == ""):
    statusText.insert(tk.END, f"{datetime.now()}: Select file to send\n")
  else:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((ServerIP, ServerPort))
    #Send command
    command = "Send"
    clientSocket.send(command.encode())
    clientSocket.recv(BUFFER_SIZE).decode()

    #Send file name
    clientSocket.send(FileName.encode())
    clientSocket.recv(BUFFER_SIZE).decode()

    #Send file password
    FilePassword = GetFilePassword() + "+"
    clientSocket.send(FilePassword.encode())
    clientSocket.recv(BUFFER_SIZE).decode()

    #Send file data
    statusText.insert(tk.END, f"{datetime.now()}: Sending {FileName}..\n")
    file = open(FileName, "rb")
    data = file.read(BUFFER_SIZE)
    while data:
      clientSocket.send(data)
      data = file.read(BUFFER_SIZE)
    file.close()
    statusText.insert(tk.END, f"{datetime.now()}: Completed\n")
    clientSocket.close()


def DownloadFile():
  check = 0
  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  clientSocket.connect((ServerIP, ServerPort))
  FileName = serverFileCombobox.get()
  if (FileName == ""):
    statusText.insert(tk.END, f"{datetime.now()}: Select file from server!\n")
  else:
    #Send file name
    clientSocket.send("Download".encode())
    clientSocket.recv(BUFFER_SIZE).decode()
    clientSocket.send(FileName.encode())

    CheckPassword = clientSocket.recv(BUFFER_SIZE).decode()

    if CheckPassword == "NO":
      clientSocket.send("H".encode())
      check = 1
      pass
    if CheckPassword == "YES":
      top = tk.Toplevel(window)
      top.lift()  # Đặt cửa sổ lên cao nhất
      passw = simpledialog.askstring(title = "Password needed for downloading file", prompt="Password: ")
      clientSocket.send(passw.encode())
      DownloadPermission = clientSocket.recv(BUFFER_SIZE).decode()
      if DownloadPermission == "Deny":
        messagebox.showinfo("Alert", "Invalid password")
        check = 0
      elif DownloadPermission == "Success":
        check = 1

    if (check == 1):
      # Receive file
      statusText.insert(tk.END, f"{datetime.now()}: Downloading {FileName}\n")
      ReceiveFile = open(FileName, "wb")
      data = clientSocket.recv(BUFFER_SIZE)
      while data:
        ReceiveFile.write(data)
        data = clientSocket.recv(BUFFER_SIZE)
      ReceiveFile.close()
      statusText.insert(tk.END, f"{datetime.now()}: Download completed\n")
  clientSocket.close()

def Refresh():
  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  clientSocket.connect((ServerIP, ServerPort))
  clientSocket.send("Refresh".encode())
  files = clientSocket.recv(BUFFER_SIZE).decode()
  files = files.split()
  serverFileCombobox["value"] = files
  statusText.insert(tk.END, f"{datetime.now()}: Server file list refreshed\n")
  clientSocket.close()

def CloseWindow():
  with open('login.txt', 'w') as file:
    file.write("Deny")
  window.destroy()

#download file
DownloadText = tk.Label(window, text = "Download", font = ("Arial", 20))
serverFileCombobox = ttk.Combobox(window, width = 35, heigh = 10)
refreshServerFileList = tk.Button(window, text = "Refresh", width = 10, command = Refresh)
downloadButton = tk.Button(window, text = "Download", width = 10, command = DownloadFile)
passwordInput = tk.Entry(window, width = 33, font = ("Arial", 10))

#send file
SendText = tk.Label(window, text = "Send", font = ("Arial", 20))
fileList = ttk.Combobox(window, width = 35)
refreshClientFileList = tk.Button(window, text = "Refresh", width = 10, command = GetFileList)
sendButton = tk.Button(window, text = "Send", width = 10, command = SendFileToServer)
passwordText = tk.Entry(window, width = 33, font = ("Arial", 10))

#Status text
statusText = tk.Text(window, width = 55, heigh = 5)

#Place grid
DownloadText.place(x = 190, y = 10)
serverFileCombobox.place(x = 50, y = 50)
refreshServerFileList.place(x = 350, y = 50)
downloadButton.place(x = 350, y = 100)
# passwordInput.place(x = 50, y = 100)

SendText.place(x = 215, y = 130)
fileList.place(x = 50, y = 180)
refreshClientFileList.place(x = 350, y = 180)
sendButton.place(x = 350, y = 230)
passwordText.place(x = 50, y = 230)

statusText.place(x = 30, y = 280)

def main():
  window.protocol("WM_DELETE_WINDOW", CloseWindow)
  subprocess.call(['python', 'IPPort.py'])
  with open('login.txt', 'r') as file:
    LoginStatus = file.read().strip()
  if LoginStatus == "Success":
    window.attributes("-topmost", True)
    window.mainloop()
  else:
    pass

main()

