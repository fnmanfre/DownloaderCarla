from tkinter import *
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.helpers import reset_cache
from tkinter import filedialog
import sys, os


def get_resource_path(relative_path):
    """Retorna o caminho absoluto do recurso no modo de execução do PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

image_path = get_resource_path("logo.png")



class Downloader:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title('YouTube Downloader')
        self.window.resizable(0,0)
        self.window.geometry('720x360+720+400') # o + indica o quanto a janela se desloca na tela ao iniciar, para direita e para baixo

        self.img_logo = PhotoImage(file=image_path)
        self.livre = True
        self.logado = False

        self.frame = Frame(self.window, bg='#3b3b3b', pady=50)
        self.frame.pack(fill='x')

        self.label_logo = Label(self.frame, image=self.img_logo, bg='#3b3b3b')
        self.label_logo.pack()

        self.frame2 = Frame(self.window)
        self.frame2.pack()

        self.label_insert = Label(self.frame2, text='   Insira o link:    ',
                                  font='Arial 12')
        self.label_insert.pack(side='left')

        self.link = Entry(self.frame2, font='Arial 22', width=35)
        self.link.pack(side='left')

        self.play = Button(self.frame2, bg='red', relief='flat', fg='white',
                           text=' > ', width=4, height=2,
                           command=lambda: self.donwload(self.link.get()))
        self.play.pack(side='left')

        self.frame3 = Frame(self.window)
        self.frame3.pack()

        self.radio1 = Radiobutton(self.frame3, text='Livre', value=1,
                                   font='Arial 16', 
                                   command=self.validate_livre
                                   ).pack(side='left')
        self.radio2 = Radiobutton(self.frame3, text='Logado', value=2, 
                                  font='Arial 16', 
                                  command=self.validate_logado
                                  ).pack(side='left')
        
        self.window.mainloop()
        
        
    def validate_livre(self):
        self.livre = True
        self.logado = False
            
    def validate_logado(self):
        self.livre = False
        self.logado = True
        
    
    def donwload(self, link):
        try:
            if self.livre:
                pasta = filedialog.askdirectory()
                YouTube(link, on_progress_callback = on_progress).streams.get_highest_resolution().download(pasta)
                self.complete()
            else:
                reset_cache()
                pasta = filedialog.askdirectory()
                YouTube(link, on_progress_callback = on_progress, use_oauth=True, allow_oauth_cache=True).get_highest_resolution().download(pasta)
                self.complete()

        except:
            self.msn()

    def msn(self):
        window = Toplevel()
        window.title('ERRO')
        window.resizable(0,0)
        window.geometry('300x200+300+200')
        text = Label(window, text='Link inválido', pady=30)
        text.pack()

        button_exit = Button(window, text=' OK ', width=10, command=window.destroy)
        button_exit.pack()

    def complete(self):
        window = Toplevel()
        window.title('DOWNLOAD COMPLETO')
        window.resizable(0,0)
        window.geometry('300x200+300+200')
        text = Label(window, text='DOWNLOAD COMPLETO', pady=30)
        text.pack()

        button_exit = Button(window, text=' OK ', width=10, command=window.destroy)
        button_exit.pack()

Downloader()