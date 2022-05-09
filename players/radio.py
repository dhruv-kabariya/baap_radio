from time import sleep
import streamlit as st
from data_models import IPData,PlayerData,SiteInfo,RadioStnInfo,Information
from tcp import TCP
from udp import play_audio


# with st.container():
#     st.title('Welcome to BAAP RADIO')
buf = 3000*4

st.session_state["is_connected"] = False

global is_connected 
is_connected = False
st.session_state["is_playing"] = False
st.session_state["info"] = None
is_playing = False
tcp_ip = IPData()
playerdata = PlayerData()
tcp = TCP()

def main():
    
    global is_connected 
    if(not is_connected):
        
        title = st.empty()
        title.markdown("<h1 style='text-align: center; color: white;'>Welcome To BAAP Radio</h1>", unsafe_allow_html=True)
        
        ip = st.empty()
        port = st.empty()
        col1,col2 = st.columns([3,1])
        with col1:
            xp= ip.text_input("Enter IP", placeholder= "Ex : 192.168.1.2",)
        with col2:
            xpp= port.text_input("Enter Port",placeholder="Ex: 8000")
        
        bun = st.empty()
            
        if(bun.button('Submit')):
            st_ip = xp.title()
            st_port = int(xpp.title())
                    # st.success(result)
            print(st_ip,st_port)
            mes = st.empty()
            try:
                tcp.connect(st_ip,st_port)
                mes.success("Connected and Data Recevied")
                # sleep(10)
                title.empty()
                ip.empty()
                port.empty()
                bun.empty()
                mes.empty()
            except:
                mes.exception("Error In Connection")
                # sleep(10)
                mes.empty()

                
            global x
            is_connected = True
            play()
    else:
        play()
        

def print_info(info):
    if(st.session_state["info"] is not None):
        sti = st.session_state["info"]
        info.text(f"Playing {sti.song_name} : {str(sti.remaining_time_in_sec)}")
        
def play():
    
    title = st.empty()
    title.title(tcp.data.site_name)

    subs = st.empty()
    # print(tcp.data.site_desc)
    subs.subheader(str(tcp.data.site_desc))

    stn = st.columns(tcp.data.radio_stn_count)
    info = st.empty()
    # print("yues : "+str(tcp.data.radio_stn_count))
    for i in range(tcp.data.radio_stn_count):
        stn[i].text(tcp.data.radio_stn_list[i].radio_stn_name)
        stn[i].text(tcp.data.radio_stn_list[i].multicast_address)
        # stn[i].button('Play')

        stn[i].button('play',on_click=play_audio,args=(info,tcp.data.radio_stn_list[i].multicast_address,tcp.data.radio_stn_list[i].data_port,tcp.data.radio_stn_list[i].info_port),key=i) 
    
    
main()
