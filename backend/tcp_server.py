import logging
from socket import socket,AF_INET,SOCK_STREAM

def send_data(data):
    # print(data)
    types = (10).to_bytes(1,'big')
    site_name_size = len(data["site_name"]).to_bytes(1,'big')
    site_name = bytes(data["site_name"],'ascii')
    site_desc_size = len(data["site_desc"]).to_bytes(1,'big')
    site_desc = bytes(data["site_desc"],'ascii')
    radio_stn_count = (data["radio_stn_count"]).to_bytes(1,'big')
    radio_stn_info = get_all_info(data["radio_stn_info"])
    
    return types+site_name_size+site_name+site_desc_size + site_desc + radio_stn_count + radio_stn_info


def get_all_info(station_name):

    stn_info = bytes("",'ascii')
    data = station_name
    for i in data:
        stn_info += station_info(i["radio_stn_number"],i["radio_stn_name"],i["multicast_address"],i["data_port"],i["info_port"],i["bit_rate"])
        # print(len(stn_info))
    return stn_info

def station_info(stn_no, stn_name, m_addr, m_port, info_port, bit_rate):

    
    radio_stn_number = (stn_no).to_bytes(1,"big")
    radio_stn_name_size = len(stn_name).to_bytes(1,"big")
    radio_stn_name = bytes(stn_name,"ascii")
    multicast_address = b''
    data_port = (m_port).to_bytes(2,"big")
    info_port = (info_port).to_bytes(2,"big")
    bit_rate = (bit_rate).to_bytes(4,"big")
    for i in m_addr.split("."):
        multicast_address +=int(i).to_bytes(1,"big")
    # print(len(data_port))
    
    return radio_stn_number+radio_stn_name_size+radio_stn_name+multicast_address+data_port+info_port+bit_rate


def start_tcp_server(ip,port,data):
   
    buf = 256

    s = socket(AF_INET,SOCK_STREAM)
    s.bind((ip,port))
    info = f"Server running on {ip}:{port}"
    logging.info(f"TCP : {info}")

    s.listen(10)

    while True:
        c, addr = s.accept() 
        
        
        logging.info(f"TCP : Get Request from {addr}")
        rdata  = c.recv(buf)
        logging.info(f"TCP : {addr} : {rdata}")
        if(rdata[0] == 1):
            c.send(send_data(data))
        else:
            c.send("Invalid Data Send")
    