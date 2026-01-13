"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GitHub: https://github.com/WannaBeGhoSt
Discord Async Development: https://discord.gg/SyMJymrV8x
"""

import asyncio
import time
import discordrpc
from discordrpc import Activity
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus
)
import re
import requests
import os
from colorama import init, Fore, Style

os.system("pip install -r requirements.txt")
os.system(
    "sleep 2 && clear >/dev/null 2>&1 &"
    if os.name == "posix"
    else "timeout /t 2 >nul 2>&1 && cls"
)

init(autoreset=True)

# change client name to YouTube Music in discord dev portal first
CLIENT_ID = 1459413725302882410  # add discord app client id

def clsghosty():
    os.system('cls' if os.name == 'nt' else 'clear')

def headerprntghosty():
    print()
    print(Fore.CYAN + Style.BRIGHT + "╭" + "─"*58 + "╮")
    print(
        Fore.CYAN + Style.BRIGHT + "│  " +
        Fore.MAGENTA + Style.BRIGHT + "🎧  GhoSty • YouTube Music RPC".ljust(50) +
        Fore.CYAN + Style.BRIGHT + "│"
    )
    print(Fore.CYAN + Style.BRIGHT + "├" + "─"*58 + "┤")

    print(
        Fore.CYAN + Style.BRIGHT + "│  " +
        Fore.YELLOW + "Discord : " +
        Fore.WHITE + "discord.gg/SGKqVYVzXd".ljust(40) +
        Fore.CYAN + Style.BRIGHT + "│"
    )
    print(
        Fore.CYAN + Style.BRIGHT + "│  " +
        Fore.YELLOW + "GitHub  : " +
        Fore.WHITE + "github.com/WannaBeGhoSt".ljust(40) +
        Fore.CYAN + Style.BRIGHT + "│"
    )

    print(Fore.CYAN + Style.BRIGHT + "╰" + "─"*58 + "╯")
    print()


def searchytmartworkghosty(title, artist):
    try:
        query = f"{title} {artist}".replace(" ", "+")
        search_url = f"https://www.youtube.com/results?search_query={query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            video_id_patterns = [
                r'"videoId":"([a-zA-Z0-9_-]{11})"',
                r'watch\?v=([a-zA-Z0-9_-]{11})',
                r'/vi/([a-zA-Z0-9_-]{11})/',
            ]
            
            video_ids = []
            for pattern in video_id_patterns:
                matches = re.findall(pattern, response.text)
                video_ids.extend(matches)
            
            video_ids = list(dict.fromkeys(video_ids))
            
            if video_ids:
                video_id = video_ids[0]
                
                quality_options = [
                    ('maxresdefault', 'https://i.ytimg.com/vi/{}/maxresdefault.jpg'),
                    ('sddefault', 'https://i.ytimg.com/vi/{}/sddefault.jpg'),
                    ('hqdefault', 'https://i.ytimg.com/vi/{}/hqdefault.jpg'),
                    ('mqdefault', 'https://i.ytimg.com/vi/{}/mqdefault.jpg'),
                ]
                
                for quality_name, url_template in quality_options:
                    thumbnail_url = url_template.format(video_id)
                    
                    try:
                        check = requests.head(thumbnail_url, timeout=3)
                        if check.status_code == 200:
                            return thumbnail_url
                    except Exception:
                        continue
                
                fallback_url = f"https://i.ytimg.com/vi/{video_id}/sddefault.jpg"
                return fallback_url
    except Exception as e:
        print(Fore.RED + f"❌ Error searching artwork: {e}")
    
    return None

async def getminfoghosty():
    try:
        sessions = await GlobalSystemMediaTransportControlsSessionManager.request_async()
        current_session = sessions.get_current_session()
        
        if current_session:
            info = await current_session.try_get_media_properties_async()
            timeline = current_session.get_timeline_properties()
            playback_info = current_session.get_playback_info()
            
            position = timeline.position.total_seconds() if timeline.position else 0
            duration = timeline.end_time.total_seconds() if timeline.end_time else 0
            
            is_playing = playback_info.playback_status == GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING
            
            info_dict = {
                "title": info.title or "Unknown Title",
                "artist": info.artist or "Unknown Artist",
                "album": info.album_title or "",
                "position": position,
                "duration": duration,
                "is_playing": is_playing,
                "app_id": current_session.source_app_user_model_id
            }
            return info_dict
    except Exception as e:
        print(Fore.RED + f"❌ Error fetching media: {e}")
    return None

def main():
    clsghosty()
    headerprntghosty()
    print(Fore.GREEN + "Connecting to Discord")
    
    try:
        rpc = discordrpc.RPC(app_id=CLIENT_ID, output=False)
        print(Fore.GREEN + "✅ Connected to Discord")
        print(Fore.CYAN + "Listening for music\n")
    except Exception as e:
        print(Fore.RED + f"❌ Could not connect to Discord: {e}")
        print(Fore.YELLOW + "Make sure Discord is running")
        input("\nPress Enter to exit")
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    last_song = None
    last_playing_state = None
    artwork_cache = {}
    check_interval = 2

    try:
        while True:
            try:
                media_info = loop.run_until_complete(getminfoghosty())

                if media_info and media_info['title'] != "Unknown Title":
                    current_song = f"{media_info['title']}|{media_info['artist']}"
                    current_state = f"{current_song}|{media_info['is_playing']}"
                    
                    if current_state != last_playing_state:
                        
                        if current_song != last_song:
                            clsghosty()
                            headerprntghosty()
                            print(Fore.GREEN + Style.BRIGHT + "🎶 Now Playing")
                            print(Fore.WHITE + "   ├─ Title  : " + Fore.CYAN + media_info['title'])
                            print(Fore.WHITE + "   └─ Artist : " + Fore.CYAN + media_info['artist'])

                            if media_info['duration'] > 0:
                                duration_min = int(media_info['duration']//60)
                                duration_sec = int(media_info['duration']%60)
                                print(Fore.YELLOW + f"⏱️  Duration: {duration_min}:{duration_sec:02d}")
                            
                            if current_song not in artwork_cache:
                                artwork_url = searchytmartworkghosty(
                                    media_info['title'], 
                                    media_info['artist']
                                )
                                if artwork_url:
                                    artwork_cache[current_song] = artwork_url
                                    print(Fore.GREEN + "✅ Artwork cached")
                                else:
                                    artwork_cache[current_song] = None
                                    print(Fore.YELLOW + "⚠️ No artwork found, using default logo")
                            else:
                                cached_url = artwork_cache[current_song]
                                if cached_url:
                                    print(Fore.CYAN + "🔄 Using cached artwork")
                                else:
                                    print(Fore.CYAN + "🔄 Cache says no artwork available")
                            
                            print(Fore.CYAN + "-"*60)
                            last_song = current_song
                        elif media_info['is_playing'] != (last_playing_state and '|True' in last_playing_state):
                            if media_info['is_playing']:
                                print(Fore.GREEN + "▶️ Resumed")
                            else:
                                print(Fore.RED + "⏸️ Paused")
                        
                        last_playing_state = current_state
                        
                        current_time = int(time.time())
                        start_timestamp = current_time - int(media_info['position'])
                        end_timestamp = start_timestamp + int(media_info['duration'])
                        
                        small_img = 'play' if media_info['is_playing'] else 'pause'
                        small_txt = "Playing" if media_info['is_playing'] else "Paused"
                        
                        activity_data = {
                            "details": media_info['title'][:128],
                            "state": f"{media_info['artist']}"[:128],
                            "act_type": Activity.Listening,
                            "small_image": small_img,
                            "small_text": small_txt,
                        }
                        
                        cached_artwork = artwork_cache.get(current_song)
                        if cached_artwork:
                            activity_data["large_image"] = cached_artwork
                        else:
                            activity_data["large_image"] = "ytmusic_logo"
                        
                        if media_info['duration'] > 0:
                            activity_data["ts_start"] = start_timestamp
                            activity_data["ts_end"] = end_timestamp
                        
                        rpc.set_activity(**activity_data)
                    
                else:
                    if last_song is not None:
                        clsghosty()
                        headerprntghosty()
                        print(Fore.RED + "⏸️ No music playing")
                        last_song = None
                        last_playing_state = None
                    rpc.clear()

            except Exception as e:
                print(Fore.RED + f"⚠️ Error updating presence: {e}")
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print(Fore.MAGENTA + "\n\nStopping")
        rpc.clear()
        rpc.disconnect()
        print(Fore.GREEN + "✅ Disconnected from Discord")
        input("\nPress Enter to exit")

if __name__ == "__main__":
    main()