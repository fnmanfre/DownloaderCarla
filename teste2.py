import threading
import sys
from tkinter import *
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.helpers import reset_cache
from tkinter import filedialog

reset_cache()

class Downloader:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title('YouTube Downloader')
        self.window.resizable(0, 0)
        self.window.geometry('720x360+720+400')

        self.livre = True
        self.logado = False

        # Widgets principais
        self.frame = Frame(self.window, pady=50)
        self.frame.pack(fill='x')

        self.label_insert = Label(self.frame, text='Insira o link:', font='Arial 12')
        self.label_insert.pack(side='left')

        self.link = Entry(self.frame, font='Arial 12', width=35)
        self.link.pack(side='left')

        self.play = Button(self.frame, text='Baixar', font='Arial 12', command=self.download)
        self.play.pack(side='left')

        # Radio buttons para modo
        self.radio_frame = Frame(self.window)
        self.radio_frame.pack()

        Radiobutton(self.radio_frame, text='Livre', value=1, font='Arial 16', command=self.validate_livre).pack(side='left')
        Radiobutton(self.radio_frame, text='Logado', value=2, font='Arial 16', command=self.validate_logado).pack(side='left')

        # Caixa de mensagem para autenticação
        self.msg_box = Text(self.window, height=5, width=80, wrap='word', state='disabled')
        self.msg_box.pack(pady=10)

        self.window.mainloop()

    def validate_livre(self):
        self.livre = True
        self.logado = False

    def validate_logado(self):
        self.livre = False
        self.logado = True

    def write_message(self, message):
        """Exibe mensagens na caixa de texto."""
        self.msg_box.config(state='normal')
        self.msg_box.insert(END, message + '\n')
        self.msg_box.config(state='disabled')
        self.msg_box.see(END)

    def download(self):
        link = self.link.get()
        threading.Thread(target=self.process_download, args=(link,)).start()

    def process_download(self, link):
        try:
            pasta = filedialog.askdirectory()
            if not pasta:
                return

            if self.livre:
                yt = YouTube(link, on_progress_callback=on_progress)
            else:
                # Redirecionar stdout para capturar as mensagens
                original_stdout = sys.stdout
                sys.stdout = StdoutRedirector(self.write_message)

                yt = YouTube(link, on_progress_callback=on_progress, use_oauth=True, allow_oauth_cache=True)
                
                # Restaurar stdout
                sys.stdout = original_stdout

            yt.streams.get_highest_resolution().download(pasta)
            self.write_message("Download completo!")
        except Exception as e:
            self.write_message(f"Erro: {e}")


class StdoutRedirector:
    """Classe para redirecionar stdout para um método específico."""
    def __init__(self, write_func):
        self.write_func = write_func

    def write(self, message):
        self.write_func(message.strip())

    def flush(self):
        pass


Downloader()