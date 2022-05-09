import os,sys,argparse
import threading,logging


from tcp_server import start_tcp_server
from streamingstation import start_udp_stations

def start_udp_server(music_dir,data):
    
    
    stations = os.listdir(music_dir)
    ip=  "239.192.10."
    port =  50000-2
    data = data
    
    data["radio_stn_count"] = 0
    data["radio_stn_info"] = []
    udp_channels = []
    for i in range(len(stations)):
        s_ip = ip+str(i+1)
        port +=2 
        t = threading.Thread(target=start_udp_stations,args=(s_ip,port,port+1,music_dir,stations[i]),daemon=True)
        udp_channels.append(t)
        t.start()        
        data["radio_stn_count"]+=1
        data["radio_stn_info"].append(
        {
            'radio_stn_number': i+1,
            'radio_stn_name_size': len(stations[i]),
            'radio_stn_name': stations[i],
            'multicast_address': s_ip,
            'data_port': port,
            'info_port': port+1,
            'bit_rate':  2048,
        }    
        )
    
    return data
    

def start_server(ip,port,music_dir):
    
    radio_detail = {
        "site_name" : "Dude FM",
        "site_desc" : "Only Play HollyWood and Bollywood Songs",  
    }
    
    # create udp stations as per folder 
    data = start_udp_server(music_dir,radio_detail)

    #create thread for tcp port
    # tcp = threading.Thread(target=
    # print(data)
    start_tcp_server(ip,port,data)
    
    
            
        
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-ip","--ip",default="127.0.0.1",type=str,help="Enter Ip of connection")
    parser.add_argument("-p","--port",default=8000,type=int,help="Enter port of connection")
    parser.add_argument("-m","--music",default="music/",type=str,help="Music Directory")
    
    args = parser.parse_args()
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    if not os.path.isdir(args.music):
        
        logging.info('Server : The path specified does not exist')
        logging.info('Server : Server Shutting Down')
        sys.exit()

    
    start_server(args.ip,args.port,args.music)
    
    
    
    
    