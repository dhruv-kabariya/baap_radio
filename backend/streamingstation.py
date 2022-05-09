import socket,time
import threading,logging

from data_modules import AudioManager

# M_IP = '239.192.0.0'
# M_PORT = 8080



def stream_info(ip,port,manager,station):
    
    logging.info(f"UDP : Channel -> {station} info streaming server started on {ip}:{port}")   
    
    def change_info_bytes(data):
        
        type = (12).to_bytes(1,"big")
        song_name_size = len(data[0]).to_bytes(1,"big")
        song_name = bytes(data[0],'ascii')
        remaining_time_in_sec = int(data[2]).to_bytes(2,"big")
        next_song_name_size = (len(data[1])).to_bytes(1,"big")
        next_song_name = bytes(data[1],'ascii')
        
        return type + song_name_size+song_name + remaining_time_in_sec + next_song_name_size + next_song_name
    
    M_TTL = 1
    
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,M_TTL)
    
    data = None
    
    # sample_rate = wf.getframerate()
    while True:
        if(manager.stream is None):
            continue
        data =change_info_bytes( manager.get_info())
        time.sleep(manager.read_size/manager.stream.getframerate()* manager.stream.getsampwidth())
        sock.sendto(data,(ip,port))


def stream_audio(ip,port,manager,station):
    
    M_TTL = 3
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,M_TTL)
    
    data = None
    
    
    # sample_rate = wf.getframerate()
    manager.start_streaming()
    logging.info(f"UDP : Channel -> {station} audio streaming server started on {ip}:{port}")
    while True:
        
        data = manager.get_data()
        # print(len(data))
        #manager.stream.getframerate()
        # time.sleep(manager.read_size/manager.stream.getframerate()* manager.stream.getsampwidth())
        time.sleep(0.8*manager.read_size/manager.stream.getframerate())
        
        sock.sendto(data,(ip,port))  
        


def start_udp_stations(ip,port_audio,port_info,music_dir,station):
    read_size = 2600
    manager = AudioManager(music_dir,station,read_size)
    
    # p = pyaudio.PyAudio()
    
    # stream = p.open(
    #     format=p.get_format_from_width(wf.getsampwidth()),
    #     channels=wf.getnchannels(),
    #     input=True,
    #     rate=wf.getframerate(),
    #     frames_per_buffer=read_size
    # )

    # create info streaming thread
    
    info = threading.Thread(target=stream_audio,args=(ip,port_audio,manager,station),daemon=True)
    info.start()
    
    
    stream_info(ip,port_info,manager,station)
    
# manager = AudioManager("music/","hollywood",2048)
# stream_audio('224.0.0.251',8000,manager,"hollywood")