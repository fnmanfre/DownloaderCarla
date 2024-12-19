from pytubefix import YouTube
from pytubefix import Playlist
from pytubefix.cli import on_progress
from pytubefix.helpers import reset_cache
from pathlib import Path
import os

link = input('Copie e cole o link da playlist: ')
print()

pasta = Path() / "Download"

os.makedirs(pasta, exist_ok=True)

pl = Playlist(fr"{link}")


for link in pl:
    print(f'Baixando: {link}')
    yt = YouTube(link,
            use_oauth=True,
            allow_oauth_cache=True)
    yt.streams.get_highest_resolution().download(pasta)

print()
print('Download completo')



