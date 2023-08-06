from setuptools import setup, find_packages
import setuptools
from os.path import dirname, abspath, join, exists

# install_reqs = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setup(
    name='webvid',
    version='0.0.7',
    packages=['webvid.IPL', 'webvid.PHUB', 'webvid.get_m3u8', 'webvid'],
    url='',
    license='',
    author='Subrata',
    author_email='subratamondal11@gmail.com',
    description='download videos from multiple websites',
    entry_points={
        'console_scripts': [
            'webvid = webvid.webvid_download:DownloadLink',  # for console command
        ],
    },
    # install_requires=install_reqs,
    install_requires=["selenium==4.2.0", "colorama==0.4.4", "ffmpeg-python==0.2.0", "m3u8==2.0.0", "requests==2.25.1"],
    data_files=[('/home/subrata/.local/share/man/man1/', ['webvid/man/webvid.1.gz'])],  # man page
)
