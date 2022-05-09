import os,wave

class  AudioManager:
    
    def __init__(self,music_dir,station,read_size):
        self.read_size = read_size
        
        music_dir += station
        self.musics = os.listdir(music_dir)
        
        for i in range(len(self.musics)):
            self.musics[i] = music_dir+"/"+self.musics[i]
            
        self.stream = None
        self.current_time = 0
        self.chunktotal = 0
        
        
    def start_streaming(self):
        if(self.stream is None):
            self.stream = wave.open(self.musics[0])
        return self.stream

    def get_info(self):
        return {
            0:self.musics[0].split(".")[-2].split("/")[-1],
            1:self.musics[1].split(".")[-2].split("/")[-1],
            2:self.current_time
        }

    def change_song(self):
        
        self.musics.append(self.musics.pop(0))
        self.current_time = 0
        self.chunktotal = 0
        self.stream = wave.open(self.musics[0])
        
    def get_data(self):
        
        data =self.stream.readframes(self.read_size)
        self.chunktotal = self.chunktotal + self.read_size
        self.current_time = self.chunktotal/float(self.stream.getframerate())
        if(data == b''):
            self.change_song()
            data = self.stream.readframes(self.read_size)
            self.chunktotal = self.chunktotal + self.read_size
            self.current_time = 0
        
        return data
