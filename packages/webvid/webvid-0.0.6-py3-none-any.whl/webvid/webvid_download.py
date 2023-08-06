from webvid.IPL import NewIPLDownloader
from webvid.PHUB import NewphubDownloader
import os


home_dir = os.path.expanduser('~')
download_dir = '/Downloads/'
download_path = home_dir + download_dir


def DownloadLink():
    user_input = input("Provide the link to download the video : ")  # get the user input
    location = input(f"Provide a location to download the video [{download_path}] : ")  # get the user input
    if 'pornhub' in user_input:
        print("PHUB")
        NewphubDownloader.downloader(user_input, location)
    elif 'iplt20' in user_input:
        print("IPL")
        NewIPLDownloader.downloader(user_input, location)
    else:
        print(f"{user_input} is currently not supported...")
        return


if __name__ == '__main__':
    DownloadLink()  # main program starts
