# importing required modules
import socket
import threading


HOST='127.0.0.1'
PORT=1234           #between 0 to 65535
LISTENER_LIMIT= 4
active_clients=[]


# function to listen for upcoming messages from a client
def listen_for_messages(client,username):
    while 1:
        message=client.recv(2048).decode('utf-8')
        if message != '':
            final_mssg=username + '~' + message
            send_messages_to_all(final_mssg)
        else:
            print("The message send from client is empty.")

# function to send message to a single client
def send_message_to_client(client,message):
    client.sendall(message.encode())


#function to send any new message to all the clients that
#are currently connected to server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1],message)
    


# function to handle client
def client_handler(client):
    #server will listen to client message that will contain the username
    while 1:
        username=client.recv(2048).decode('utf-8')      #recv()function to any mssg
        if username != '':
            active_clients.append((username,client))
            break

        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages,args=(client,username,)).start()

# main
def main():

    #creating the socket class object
    #AF_INET:  to use IPv4 addresses
    # SOCK_STREAM: to use TCP packets for communication
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print(f"Running the server on {HOST}{PORT}")


    # try catch block
    try:
        server.bind((HOST,PORT))
        print("Successfully binded")

    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # setting server limit
    server.listen(LISTENER_LIMIT)


    #while to keep listening to client connections
    while True:
        
        client,address=server.accept()
        print(f"Successfully connected to client{address[0]}{address[1]}")

        threading.Thread(target=client_handler,args=(client,)).start()


if __name__=='__main__':
    main()