class  IPData:
    
    def __init__(self) :
        self.ip = None
        self.port = None

class PlayerData:
    
    def __init__(self):
        self.tcp = IPData()
        self.udp =IPData()



class SiteInfo:
    
    
    def __init__(self,data):
        
        
        cursor = 0
        
        self.type = data[cursor]
        cursor+=1
    
        self.site_name_size = data[cursor]
        cursor+=1
        
        self.site_name = str(data[cursor:cursor+self.site_name_size],'ascii')
        cursor+=self.site_name_size
        
        self.site_desc_size = data[cursor]
        cursor+=1
        
        self.site_desc = str(data[cursor:cursor+self.site_desc_size],'ascii')
        cursor+=self.site_desc_size
        
        
        self.radio_stn_count = data[cursor]
        cursor+=1
        self.radio_stn_list = []
        
    
        for i in range(self.radio_stn_count):
            # print(cursor,data[cursor+1])
            rsd = data[cursor:cursor+14+data[cursor+1]]
            cursor =cursor+14+data[cursor+1]
            
            self.radio_stn_list.append(
                RadioStnInfo(rsd)
            )
        # print(len(self.radio_stn_list))

class RadioStnInfo:
    
    def __init__(self,data) :
        
        
        cursor = 0
        
        self.radio_stn_number = data[cursor]
        cursor+=1 
        
        self.radio_stn_name_size = data[cursor]
        cursor+=1 
        
        self.radio_stn_name = str(data[cursor:cursor+self.radio_stn_name_size],'ascii')
        cursor+=self.radio_stn_name_size
        
        self.multicast_address = str(data[cursor])+"." + str(data[cursor+1])+"." + str(data[cursor+2])+"." + str(data[cursor+3])
        cursor+=4
        
        self.data_port = int.from_bytes(data[cursor:cursor+2], byteorder='big')
        cursor+=2
        
        self.info_port = int.from_bytes(data[cursor:cursor+2], byteorder='big')
        cursor+=2
        
        self.bit_rate = int.from_bytes(data[cursor:cursor+4], byteorder='big')
        cursor+=4


class Information:
    
    def __init__(self,data):
        self.type = data[0]
        self.song_name_size = data[1]
        self.song_name = str(data[2:self.song_name_size+2],'ascii')
        self.remaining_time_in_sec = int.from_bytes(data[self.song_name_size+2:self.song_name_size+4],byteorder='big')
        self.next_song_name_size =data[self.song_name_size+4]
        self.next_song_name = str(data[self.song_name_size+5:self.next_song_name_size+self.song_name_size+5],'ascii')    