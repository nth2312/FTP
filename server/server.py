import os
import random
import socket
import smtplib
from email.message import EmailMessage

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
print(IP)

Port = 8000
BUFFER_SIZE = 4096

Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server_Socket.bind((IP, Port))
Server_Socket.listen()
print("listening..")
username = ["admin"]
password = ["pass"]
FileWithPassword = ["win3.txt"]
FilePassword = ["Win123"]
email = "truonghieu2312@outlook.com.vn"
emailPassword = "Nth23122"
Subject = "FTP Server"
mailServer = "smtp.office365.com"
mailPort = 587


def OTP(connection):
  global SecurityCode
  SecurityCode = random.randint(10000, 99999)
  connection.send("H".encode())
  d_email = str(connection.recv(BUFFER_SIZE).decode())
  if (d_email == ""):
    pass
  else:
    dest_email = d_email
    msg = EmailMessage()
    msg["To"] = dest_email
    msg["From"] = email
    msg["Subject"] = Subject
    body = f"Dear {dest_email}:\n\n" \
           f"Your OTP is: {SecurityCode}\n\n" \
           f"Welcome to our server"
    msg.set_content(body)
    Mail = smtplib.SMTP(mailServer, mailPort)
    Mail.starttls()
    Mail.login(email, emailPassword)
    Mail.send_message(msg=msg, from_addr=email, to_addrs=dest_email)
    Mail.quit()


def SignUp(connection):
  connection.send("H".encode())

  OTP = connection.recv(BUFFER_SIZE).decode()

  if (OTP == str(SecurityCode)):
    Permission = "Permit"
  else:
    Permission = "Deny"
  # print(Permission)
  connection.send(Permission.encode())

  user = connection.recv(BUFFER_SIZE).decode()
  if Permission == "Permit":
    if user != "":
      SignUpInfo = user.split(" ")
      username.append(SignUpInfo[0])
      password.append(SignUpInfo[1])
      # print(username)
      # print(password)
  else:
    pass


def Login(connection):
  connection.send("H".encode())
  LoginInfo = connection.recv(BUFFER_SIZE).decode()
  LoginInfo = LoginInfo.split(" ")
  user = LoginInfo[0]
  passw = LoginInfo[1]
  print(user + passw)
  if user in username and passw in password:
    connection.send("Admit".encode())
  else:
    connection.send("Deny".encode())

def SendFileList(connection, file):
  connection.send(file.encode())

def FindElementIndex(element, list):
  for i in range(len(list)):
    if element == list[i]:
      return i


def SendFile(connection):
  connection.send("Select file..".encode())
  file_name = connection.recv(BUFFER_SIZE).decode()

  if file_name in FileWithPassword:
    connection.send("YES".encode())
    index = FindElementIndex(file_name, FileWithPassword)
    filePassword = FilePassword[index]
    PasswordReturnFromClient = connection.recv(BUFFER_SIZE).decode()
    print(PasswordReturnFromClient)
    print(filePassword)
    if (PasswordReturnFromClient == filePassword):
      permission = "Success"
    else:
      permission = "Deny"
    connection.send(permission.encode())
  else:
    connection.send("NO".encode())
    connection.recv(BUFFER_SIZE)

  FileSend = open(file_name, "rb")
  data = FileSend.read(BUFFER_SIZE)
  while data:
    connection.send(data)
    data = FileSend.read(BUFFER_SIZE)
  connection.close()

  FileSend.close()


def ReceiveFile(connection):
  #Receive File Name
  connection.send("H".encode())
  FileName = connection.recv(BUFFER_SIZE).decode()
  print(FileName)

  #Receive  File Password
  connection.send("H".encode())
  Fpassword = connection.recv(BUFFER_SIZE).decode()[:-1]
  print(Fpassword)
  if Fpassword != "":
    FileWithPassword.append(FileName)
    FilePassword.append(Fpassword)
  print(FileWithPassword)

  #Receive File
  connection.send("H".encode())
  receiveFile = open(FileName, "wb")
  data = connection.recv(BUFFER_SIZE)
  while data:
    receiveFile.write(data)
    data = connection.recv(BUFFER_SIZE)
  receiveFile.close()
  return FileName

def ReceiveFilePass(connection, FileName):
  connection.send("H".encode())

def main():
  while True:
    files = ""
    connection, address = Server_Socket.accept()
    command = connection.recv(BUFFER_SIZE).decode()
    # print(command)
    if (command == "Refresh"):
      path = os.getcwd()
      file_list = os.listdir(path)
      pass
      file_list.remove("server.py")
      for i in file_list:
        files += i + " "
      SendFileList(connection, files)
    if (command == "Download"):
      SendFile(connection)
    if (command == "Send"):
      Filename = ReceiveFile(connection)
      # ReceiveFilePass(connection, Filename)
    if (command == "OTP"):
      OTP(connection)
    if (command == "SignUp"):
      SignUp(connection)
    if (command == "Login"):
      Login(connection)


main()
b = 1