from setuptools import setup

setup(
    name='webvid',
    version='0.0.2',
    # packages=['IPL', 'PHUB', 'get_m3u8'],
    packages=['webvid'],
    url='',
    license='',
    author='subrata',
    author_email='subratamondal11@gmail.com',
    description='download videos from multiple websites',
    entry_points={
        'console_scripts': [
            'webvid = webvid:DownloadLink',
        ],
    },
    install_requires=["selenium==4.2.0",
                      "colorama==0.4.4",
                      "ffmpeg-python==0.2.0",
                      "m3u8==2.0.0",
                      "requests==2.25.1"
                      ]
)
