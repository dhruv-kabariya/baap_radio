from socket import socket,AF_INET,SOCK_STREAM

from data_models import SiteInfo


class TCP:
    
    def __init__(self) -> None:
        self.s = socket(AF_INET,SOCK_STREAM)
        self.buf = 256
        self.data = None

    def connect(self,ip,port):
        assert type(port) == int
        assert len(ip) < 16 
        # print(ip)
        # print(port)
        try:
            self.s.connect((ip,port))
        except :
            print("TCP : Error in Connection")
        
        try:
            self.s.send((1).to_bytes(1,'big'))
        except :
            print("TCP : Error in Send TCP")

        try:
            self.data = self.s.recv(self.buf)
        except :
            print("TCP : Error in Reciving TCP")
            
        # print(self.data)
        try:
            self.data = SiteInfo(self.data)
        except:
            print("TCP : Error in Data Parse")
        
        try:
            self.s.close()
        except:
            print("TCP : Error in Closing Socket")
            
        

        
    
    
    
    