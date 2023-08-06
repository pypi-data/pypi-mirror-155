import datetime
import time
import colorama
import requests
import m3u8
import os
from webvid.get_m3u8 import get_m3u8_link


# name_and_url = []
# location = '/home/subrata/Downloads/'
home_dir = os.path.expanduser('~')
download_dir = '/Downloads/'
download_path = home_dir + download_dir

if not os.path.isdir(download_path):
    print(f'dir {download_path} not exists, creating dir...')
    os.makedirs(download_path)


def downloader(user_input, location):  # take the input from DownloadLink function
    if os.path.isdir(location):
        if location[-1] != '/':
            location = location + '/'
    else:
        location = download_path

    # videourl = "https://www.pornhub.org/view_video.php?viewkey=ph620726157674f"
    videourl = user_input  # take the url with a different name

    m3u8url = get_m3u8_link.m3u8_link(videourl)# call IPLm3u8url function and provide the url to get m3u8 file link
    m3u8urlget = m3u8url.m3u8url_get()
    video_name = m3u8urlget[0] + '.mp4'  # get the video title add extension to the video name
    m3u8_link = m3u8urlget[1]  # get the m3u8 url
    # print("= " * 60)
    print('')
    print('Video Name : ', video_name)
    print('   Web url : ', user_input)
    print(' Link Name : ', m3u8_link)

    # print("= " * 60)
    r = requests.get(m3u8_link)
    m3u8_master = m3u8.loads(r.text)
    data = m3u8_master.data
    parts = data['playlists']
    # print(data)
    # print("-- " * 20)
    x = parts[0]
    breakurl = m3u8_link.split('/')[0:-1]
    preUrl = '/'.join(breakurl) + '/'
    fullurl = preUrl + x['uri']
    print('  Full url : ', fullurl)
    print('')

    video_path = location + video_name
    file_exists = os.path.exists(video_path)
    if file_exists:
        print(f"File {video_path} already exists...")
        return

    # print("-- " * 20)
    r1 = requests.get(fullurl)
    m3u8_master1 = m3u8.loads(r1.text)
    data1 = m3u8_master1.data
    # print(data1)
    # print("-- " * 20)

    parts1 = data1['segments']
    # x1 = parts1[0]
    # print(parts1)
    breakurl1 = fullurl.split('/')[0:-1]
    # print(breakurl1)
    preUrl1 = '/'.join(breakurl1) + '/'
    # print(preUrl1)
    # fullurl1 = preUrl1 + x1['uri']
    # print('fullurl1', fullurl1)

    count = len(parts1)
    downloading = 0
    chunk_size = 256

    print("= " * 60)
    timenow = datetime.datetime.today().__str__()
    print("Video downloading started : ", timenow)
    start_time = time.time()
    with open(video_path, 'wb') as f:
        for x1 in parts1:
            downloading += 1
            fullurl1 = preUrl1 + x1['uri']
            # print("Downloading : ", fullurl1)
            # print(downloading, '/', count)

            # Download method 1
            # r = requests.get(fullurl1, stream=True)
            # for chunk in r.iter_content(chunk_size=chunk_size):
            #     f.write(chunk)

            # Download method 2
            r = requests.get(fullurl1)
            f.write(r.content)

            progressbar(downloading, count)
    print(colorama.Fore.RESET)
    timenow = datetime.datetime.today().__str__()
    print("Video Successfully Downloaded", timenow)
    end_time = time.time()
    execution_time = str(end_time - start_time).split('.')[0]
    print('')
    print(f'Video Downloading Time {execution_time} secs')
    print("Video downloaded : ", video_path)
    print("= " * 60)


def DownloadLink():
    user_input = input("Provide the link to download the video : ")  # get the user input
    # user_input = "https://www.pornhub.org/view_video.php?viewkey=ph61c45cd492c2b"
    downloader(user_input)  # pass the input string to downloader function


def progressbar(progress, total, color=colorama.Fore.RED):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(color + f"\r|{bar}| {percent:.2f}%", end="\r")
    if progress == total:
        print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%", end="\r")


if __name__ == '__main__':
    DownloadLink()  # main program starts

    # print(IPLm3u8url("https://www.pornhub.org/view_video.php?viewkey=ph623329f2c4fad"))
