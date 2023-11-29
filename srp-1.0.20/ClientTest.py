import socket
import srp

def run_client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.137.129', 5005))
    
    for i in range(5):
        with open('C:/Users/keita/Desktop/client files/test1.py',"r") as f:
            string = f.read()
        print(string)
        
        # SRP Client Logic
        username = 'user'
        password = string

        usr = srp.User(username, str(password))
        uname, A = usr.start_authentication()

        # Send username and A to server
        client.send(username.encode())
        client.send(A)

        # Receive salt and B from server
        salt = client.recv(1024)
        B = client.recv(1024)

        # Process challenge
        M = usr.process_challenge(salt, B)
        client.send(M)

        # Receive HAMK from server and verify session
        HAMK = client.recv(1024)
        usr.verify_session(HAMK)

        if usr.authenticated():
            print("FILES ARE THE SAME")
        else:
            print("FILES ARE NOT THE SAME")
            
            
        
    client.close()

run_client()
