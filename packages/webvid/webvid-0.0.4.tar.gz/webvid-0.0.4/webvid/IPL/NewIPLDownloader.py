import datetime
import os
import time
import threading
import colorama
import ffmpeg
import m3u8
import requests
from webvid.get_m3u8 import get_m3u8_link

# name_and_url = []
# location = '/home/subrata/Downloads/'
symbols = '-\|/'
video_name = ''
video_ts = 'video.ts'
audio_ts = 'audio.ts'
home_dir = os.path.expanduser('~')
download_dir = '/Downloads/'
download_path = home_dir + download_dir

if not os.path.isdir(download_path):
    print(f'dir {download_path} not exists, creating dir...')
    os.makedirs(download_path)


# def DownloadLink():
#     user_input = input("Provide the link to download the video : ")  # get the user input
#     # user_input = 'https://www.iplt20.com/video/46347/hardik-sends-ashwins-carrom-ball-into-stands'
#     downloader(user_input, location='/home/subrata/Downloads/')  # pass the input string to downloader function
#     # download_thread = threading.Thread(target=downloader(user_input), name="Downloader", args=some_args)
#     #     timenow = datetime.datetime.today().__str__()
#     #     if len(video_name) > 0:
#     #         print('Downloading : ', timenow, video_name)
#     # time.sleep(5)


def downloader(user_input, location):  # take the input from DownloadLink function
    global video_name

    if os.path.isdir(location):
        if location[-1] != '/':
            location = location + '/'
    else:
        location = download_path

    # videourl = "https://www.iplt20.com/video/46347/hardik-sends-ashwins-carrom-ball-into-stands"
    videourl = user_input  # take the url with a different name
    m3u8url = get_m3u8_link.m3u8_link(videourl)  # call IPLm3u8url function and provide the url to get m3u8 file link
    m3u8urlget = m3u8url.m3u8url_get()
    video_name = m3u8urlget[0] + '.mp4'  # get the video title add extension to the video name
    m3u8_link = m3u8urlget[1]  # get the m3u8 url
    print('      Video Name : ', video_name)
    print('         Web url : ', user_input)
    print('  m3u8 Link Name : ', m3u8_link)
    print('')

    video_path = location + video_name

    file_exists = os.path.exists(video_path)
    if file_exists:
        print(f"File {video_path} already exists...")
        return

    download_link(m3u8_link)
    # download_video()
    # download_audio()

    # (ffmpeg.input(m3u8_link).output(video_path).global_args('-loglevel', 'quiet').run())

    # wait = os.wait()
    # print(wait)

    # (ffmpeg
    #  .input(m3u8_link)
    #  .output(video_path)
    #  .global_args('-loglevel', 'quiet')
    #  .run()
    #  )

    # stream = ffmpeg.input(m3u8_link)    # take m3u8 url as input
    # stream = ffmpeg.output(stream, video_path)  # add stream link and provide output video name
    # ffmpeg.run(stream)                  # download the video

    # timenow = datetime.datetime.today().__str__()
    # print("Video downloaded successfully : ", timenow, video_path)
    track_video_process(video_path)


def track_video_process(video_path):
    start_time = time.time()
    # print('video_path', video_path)
    # render = (ffmpeg.input('video.ts').output(video_path).global_args('-i', 'audio.ts', '-loglevel', 'quiet').run())
    render_thread = threading.Thread(target=video_process, name="video_process", args=(video_path,), daemon=True)
    render_thread.start()
    while render_thread.is_alive():
        for symbol in symbols:
            # print(symbol)
            print(f"\r {symbol}", end="\r")
            time.sleep(0.100)
    print('Video Processing Ends...')
    end_time = time.time()
    execution_time = str(end_time - start_time).split('.')[0]
    print(f'Video Processing Time {execution_time} secs')
    print("Video downloaded : ", video_path)
    print("= " * 60)

    if os.path.exists(video_ts):
        os.remove(video_ts)
    if os.path.exists(audio_ts):
        os.remove(audio_ts)
    print('')


def video_process(video_path):
    print("Video processing...")
    # (ffmpeg.input('video.ts').output(video_path).global_args('-loglevel', 'quiet').run())
    (ffmpeg.input(video_ts).output(video_path).global_args('-i', audio_ts, '-loglevel', 'quiet').run())


# video_name = ''


############################################################################################
def download_link(m3u8_link):
    m3u8_master = m3u8.load(m3u8_link)
    # # m3u8_master = m3u8.loads(r.text)
    # # print(m3u8_master.data)
    # # for x in m3u8_master.data:
    # #     print(x)
    all_videos = m3u8_master.data['playlists']
    all_audios = m3u8_master.data['media']
    # # print(all_videos)
    # # print(all_audios)
    #
    # # print(all_videos[0])
    # # print(all_videos[0]['uri'])
    # # print(all_videos[0]['stream_info']['resolution'])
    video_list = []
    for video in all_videos:
        # print(video)
        videos = video['stream_info']['resolution']
        video_list.append(videos)
        # print(resolutions)
    video_list = list(set(video_list))
    # # print(video_list)
    dict1 = {}
    for x in video_list:
        # print(x)
        split = x.split("x")
        pixels = (int(split[0]) * int(split[1]))
        dict1[x] = pixels
        # print(pixels)
    # # print(dict1)
    # # print(dict1.values())
    # key_list = list(dict1.keys())
    val_list = list(dict1.values())
    val_list.sort()
    val_list.reverse()
    # # print(val_list)
    resDict = {}
    for x in val_list:
        resKey = (list(dict1.keys())[list(dict1.values()).index(x)])
        resDict[resKey] = x
    # print(resDict.keys())
    resolutions = resDict.keys()
    # print(resolutions)
    resCount = len(resolutions)
    #
    resolutionList = []
    for x in resolutions:
        # print(x)
        resolutionList.append(x)
    # print(resolutionList)
    #
    # # ask user input
    resno = 1
    for resolution in resolutions:
        print(f"{resno}. {resolution}")
        resno += 1
    #
    choice = int(input("Select video resolution : "))
    #
    selectedRes = ""
    if choice in range(1, resCount + 1):
        print(choice)
        selectedRes = resolutionList[choice - 1]
        print("You have selected resolution", selectedRes)
    else:
        print("Please select a valid resolution")
        exit()
    #
    # aa = input("Press enter to download the video...")
    #
    # timenow = datetime.datetime.today().__str__()
    # print("Video downloading started : ", timenow)

    print("= " * 60)
    videoName = [x for x in all_videos if x['stream_info']['resolution'] == selectedRes]
    # print(videoName)
    vurl = videoName[0]['uri']
    # # vinfo = videoName[0]['stream_info']
    # vres = videoName[0]['stream_info']['resolution']
    audio_id = videoName[0]['stream_info']['audio']
    # print('Resolution : ', vres)
    # print('Video m3u8 url : ', vurl)  # url of video m3u8
    #
    audioName = [x for x in all_audios if x['group_id'] == audio_id]
    aurl = audioName[0]['uri']
    # print("Audio m3u8 url : ", aurl)  # url of audio m3u8
    #
    # print("= " * 60)
    vreq = requests.get(vurl)  # video m3u8 link fetch
    areq = requests.get(aurl)  # audio m3u8 link fetch
    vpl = m3u8.loads(vreq.text)  # video play list
    apl = m3u8.loads(areq.text)  # audio play list
    download_video(vpl)
    download_audio(apl)


def download_video(vpl):
    timenow = datetime.datetime.today().__str__()
    print("Video downloading started : ", timenow)
    start_time = time.time()
    segments = vpl.data['segments']
    all = len(segments)
    count = 1
    with open(video_ts, 'wb') as f:
        for segment in segments:
            # print('Segments', count, '/', all)
            url1 = segment['uri']
            # print("Downloading Video : ", url1)
            r2 = requests.get(url1)
            f.write(r2.content)
            # print("\nDone\n")
            progressbar(count, all)
            count += 1
    print(colorama.Fore.RESET)
    timenow = datetime.datetime.today().__str__()
    print("Video Successfully Downloaded", timenow)
    end_time = time.time()
    execution_time = str(end_time - start_time).split('.')[0]
    print(f'Video Downloading Time {execution_time} secs')


def download_audio(apl):
    timenow = datetime.datetime.today().__str__()
    print("\nAudio downloading started : ", timenow)
    start_time = time.time()
    segments = apl.data['segments']
    all = len(segments)
    count = 1
    with open(audio_ts, 'wb') as f:
        for segment in segments:
            # print('Segments', count, '/', all)
            url1 = segment['uri']
            # print("Downloading Audio : ", url1)
            r2 = requests.get(url1)
            f.write(r2.content)
            # print("\nDone\n")
            progressbar(count, all)
            count += 1
    print(colorama.Fore.RESET)
    end_time = time.time()
    execution_time = str(end_time - start_time).split('.')[0]
    timenow = datetime.datetime.today().__str__()
    print("Audio Successfully Downloaded", timenow)
    print(f'Audio Downloading Time {execution_time} secs')
    print('')


################################################################################################################


def progressbar(progress, total, color=colorama.Fore.RED):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(color + f"\r|{bar}| {percent:.2f}%", end="\r")
    if progress == total:
        print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%", end="\r")

# if __name__ == '__main__':
#     DownloadLink()  # main program starts
