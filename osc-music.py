
from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

from pythonosc.udp_client import SimpleUDPClient
import os, sys
import hashlib
import gc
import asyncio
import itertools
import time


async def get_media_info() -> dict:
    sessions = await MediaManager.request_async()

    current_session = sessions.get_current_session()

    if current_session:  

        info = await current_session.try_get_media_properties_async()

        info_dict = {song_attr: info.__getattribute__(song_attr) \
            for song_attr in dir(info) if song_attr[0] != '_'}
            
        info_dict['genres'] = list(info_dict['genres'])
      
        pbinfo = current_session.get_playback_info()
        info_dict['status'] = pbinfo.playback_status
      
        tlprops = current_session.get_timeline_properties()
     
        return info_dict

    raise NoMediaRunningException("No media source running.")


def change_cover(cover_int: int, parameter: str = "/avatar/parameters/coverart" ) -> int:
    if cover_int == -1:
        return -1

    OSC_CLIENT.send_message(parameter, cover_int)
    return 0

def generate_song_hash(artist: str, album: str, song: str) -> str:
    song_hash = hashlib.sha256(  (artist            \
                                + album             \
                                + song)             \
                                .encode('utf-8'))   \
                                .hexdigest()
    return song_hash

def return_album_cover(album_name: str) -> int:
    
    album_cover_dictionary = {
        "management"    : 0,
        "twin galaxies" : 1,
        "spring island" : 2,
        "younger years" : 3,
        "ghost city"    : 4,
        "soft sounds"   : 5,
        "afterimage"    : 6
    }
    return album_cover_dictionary\
                    .get(album_name, -1)
    

def music_loop():

    old_song_hash = ""
    spinner = itertools.cycle(SPINNY)

    while True:

        current_media_info = asyncio.run(get_media_info())

        artist, album, song =   [  
                    current_media_info['artist'], \
                    current_media_info['album_title'], \
                    current_media_info['title'] 
        ]

        new_song_hash = generate_song_hash(artist, album, song)
        
        if old_song_hash == new_song_hash:
            print(f"[{next(spinner)}] No change", end="\r")

        else:
            print(f"[+] Currently playing {song} from {album} by {artist}")
            
            current_album_int = return_album_cover(album.lower())

            change_cover(current_album_int) \
            if current_album_int != -1 \
            else print("[!] Undefined album.")
             
            
            old_song_hash = new_song_hash
        

        time.sleep(1)


if __name__ == '__main__':

    OSC_CLIENT  = SimpleUDPClient("127.0.0.1", 9000)
    SPINNY      = ['-','\\','|','/']

    music_loop()

    