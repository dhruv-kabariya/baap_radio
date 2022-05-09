import socket
import struct,pyaudio,queue,threading
from time import sleep, time
import numpy as np
import streamlit as st

from data_models import Information

buf = 2600*4
q = queue.Queue(maxsize=2000)

def play_audio(info,ip,port,port_info):
    
    print("Playing song")    
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(('',port))

    pa = pyaudio.PyAudio()
    read_size = 2600

    stream = pa.open(
        format=pa.get_format_from_width(2),
        channels=2,
        rate=48000,
        output=True,
        frames_per_buffer=read_size
    )

    mreq = struct.pack('4sl', socket.inet_aton(ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def write_data():

        while True:
            
            data= sock.recv(buf)
            q.put(data)
            # print(data)
    
    t1 = threading.Thread(target=write_data,args=(),daemon=True)
    t1.start()

    def get_info(ip,port,info):
    
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('',port))
        mreq = struct.pack('4sl', socket.inet_aton(ip), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        # info = st.empty()
        
        while True:
            
            data= sock.recv(buf)
            # info.empty()
            # print(data)
            st.session_state["info"] = Information(data)
            
            
            
            # print(f"Song : {sti.song_name} : {sti.remaining_time_in_sec}")

    t2 = threading.Thread(target=get_info,args=(ip,port_info,info),daemon=True)
    t2.start()

    
    while True:
      
      
      if not q.empty():
            
        frame = q.get()
        stream.write(frame)
