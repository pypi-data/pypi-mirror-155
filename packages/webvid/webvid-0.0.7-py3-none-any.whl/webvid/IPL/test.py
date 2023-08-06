import ffmpeg
import threading
import time
import os.path

file_name = 'aaaa.mp4'
symbols = '-\|/'


def download():
    (ffmpeg.input('video.ts').output(file_name).global_args('-i', 'audio.ts', '-loglevel', 'quiet').run())


def test():
    file_exists = os.path.exists(file_name)
    if not file_exists:
        download_thread = threading.Thread(target=download, name="Downloader", args=(), daemon=True)
        download_thread.start()
        print('Video Processing Started...')
        while download_thread.is_alive():
            for symbol in symbols:
                # print(symbol)
                print(f"\r {symbol}", end="\r")
                time.sleep(0.100)
        print('Video Processing Ends...')
    else:
        print(f"File {file_name} Exists...")
    print('')

test()
