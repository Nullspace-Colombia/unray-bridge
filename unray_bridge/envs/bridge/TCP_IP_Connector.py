""" 
    Server - server.py

    Server Class utilities definition to create a simple 
    TCP/IP communication. 
    =====================================================
    Classes 
    =====================================================
     - ClientHandler
     - ServerHandler
    ====================================================
    
    QUICK START GUIDE 
    =====================================================
        To check the 
    =====================================================
"""
import socket, sys
import numpy as np





class ClientHandler():
    __BUFFER_DATA_SIZE = 256
    """
    Client Handler 
    
    """
    def __init__(self, ip = 'localhost', port = 10010): 
        self.connected = False 
        self.ip = ip 
        self.port = port 
        self.socket_args = {'family': socket.AF_INET, 'type': socket.SOCK_STREAM}
        self.client_dictionary = self.socket_args
        
        
    def set_socket(self):
        self.sock = socket.socket(**self.socket_args)

    def get_socket(self):
        return self.sock

    
    def connect(self, sock): 
        
        server_address = (self.ip, self.port)
        print('[ CONNECTION ] connecting to {} port {}'.format(*server_address))

        count = 1
        group_count = 1
        
        while not self.connected:
            try:
                sock.connect(server_address)
                self.connected = True 
            except: 
                count += 1
                if count % 4 == 0: 
                    print("Trying to connect...")        
                    group_count += 1
                    if group_count % 5 == 0: 
                        
                        break 
            return sock

        if not self.connected: 
            print("Connection Timeout!")          
            return False              
        else:
            print('[ CONNECTION ] Connected with server!')
            self.connected = False # Restart for future connections 
            return True # If Connection is realized 
        
        

    def send(self, msg, sock,  __BUFFER_DATA_SIZE = 32):
        if not self.connected:
            assert "No server connection. Please check"
        print("[ SEND ]", end = " ")
        #data_size = len(msg)
        #data_sent = b''
        sock.send(msg)
        print(msg)
        
    
    def recv(self, expected_bytes, sock):
        
        res = b''
        #respuesta = np.emtpy(1, dtype=np.single)
        nuevos_datos = b''
        self.sock.setblocking(True)
       
        try:
            while len(res) < expected_bytes:
                nuevos_datos = sock.recv(expected_bytes - len(res))
                if not nuevos_datos:
                    # Handle disconnection
                    break    
                res+=nuevos_datos
                
        except socket.error as e:
            print(f"Error : {e}")
            #respuesta = np.frombuffer(res, dtype=np.single)
            #print(respuesta)
            #respuesta = np.append(np.frombuffer(nuevos_datos, dtype=np.single))       
        finally:
            sock.setblocking(False)
        #print(res)
        respuesta = np.frombuffer(res, dtype=np.double)
        print("[ RECV ]", end = " " )   
        print(respuesta)

        return respuesta 
        


    def close(self, sock): 
        print("Closing connection...")
        self.connected = False
        sock.close()
        print("Connection closed! Bye.")



class ServerHandler():
    
    """
    Server Handler 

    """
    def __init__(self, IP = 'localhost', PORT = 10000, max_connections = 2):
        self._IP   = IP
        self._PORT = PORT 
        self._MAX_CONNECTIONS = max_connections

        self.callback = None 
        self.number_connections = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self._IP, self._PORT)

        self.sock.bind(self.server_address)
        self.sock.listen(10)
       
    def start(self, __BUFFER_DATA_SIZE = 256):
        print('[ SERVER ] Begining server on {}:{} | TCP/IP'.format(*self.server_address))
        while True:
            connection, client_address = self.sock.accept() # Wait for connections 
            # Connected Procedure 
            self.new_connection()
            print('[ NEW ] {}:{} connected! ({}, {})'.format(*client_address, self.number_connections, self._MAX_CONNECTIONS)) 

            try:
                while True:
                    data = connection.recv(__BUFFER_DATA_SIZE)
                    
                    # print('received {!r}'.format(data), end = " ")
                    #  print(f"converted to: {np.frombytes(data)}")
                    if data:
                        print(f'Action: {np.frombuffer(data, dtype = np.float16) * 2}')
                        
                        connection.sendall(data)
                    else:
                        print('no data from', client_address)
                        break
            except:
                print("[ WARN ] No callback config. Please use ServerHandler.set_callback(fcn)")


    def get_connections(self):
        return self.number_connections

    def new_connection(self):
        self.number_connections += 1

    def shutdown(self): 
        self.sock.close() 

    def set_callback(self, fcn = None): 
        self.callback = fcn 

    def test_connection(self): 
        pass 



