'''
pip install pillow
pip install imageio
pip install wget
pip install webdriver_manager
pip install selenium

Samples:
>>> from anya import AnyaImage
>>> anya = AnyaImage()
>>> anya.show()

or
>>> from anya import AnyaGIFImage
>>> anya = AnyaGIFImage()
>>> anya.show()
'''


from itertools import cycle
import wget
import os
from random import choice
import platform



ISMAC = bool(platform.system() == 'Darwin')

if ISMAC:
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium import webdriver
else:
    from PIL import Image, ImageTk
    import tkinter as tk
    import imageio.v3 as iio



METHODS = ['emoticon', 'blackwhite_image', 'colorful_image']
METHODS_DICT = {1: 'emoticon', 2: 'blackwhite_image', 3: 'colorful_image'}
GIF_LIST = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 19, 20, 21, 23, 26, 27, 30]
TROUBLE_DICT = {8: [1, 2], 12: [1]}



def get_emoticon(txt):
    window = tk.Tk()
    window.wm_title('Anya')
    window.geometry('+1020+100')

    anya = tk.Label(window, text=txt, bg='white', fg='#263238', font=('Lucida Sans Unicode', 45), width=5, height=1)
    anya.grid(column=0, row=0)
    
    window.mainloop()


def get_blackwhite_image():
    if ISMAC:
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        driver.set_window_position(800, 100)
        driver.set_window_size(500, 500)
        driver.get("https://i.imgur.com/4QRGACN.jpeg")
        os.system("pause")
    else:
        window = tk.Tk()
        window.title('Anya')
        window.geometry('+940+100')

        wget.download('https://i.imgur.com/4QRGACN.jpeg', 'image.jpeg')
        img = Image.open('image.jpeg')
        img = img.resize((img.width // 2, img.height // 2))   
        imgTk =  ImageTk.PhotoImage(img)
        os.remove('image.jpeg')

        anya = tk.Label(window, image=imgTk)
        anya.grid(column=0, row=0)

        window.mainloop()


def get_colorful_image():
    if ISMAC:
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        driver.set_window_position(800, 100)
        driver.set_window_size(500, 500)
        driver.get("https://i.imgur.com/UUE7pIH.jpg")
        os.system("pause")
    else:
        window = tk.Tk()
        window.title('Anya')
        window.geometry('+900+100')

        wget.download('https://i.imgur.com/UUE7pIH.jpg', 'image.jpg')
        img = Image.open('image.jpg')
        img = img.resize((img.width // 2, img.height // 2))   
        imgTk =  ImageTk.PhotoImage(img)
        os.remove('image.jpg')

        anya = tk.Label(window, image=imgTk)
        anya.grid(column=0, row=0)

        window.mainloop()


def get_anya(method: str):
    if method == METHODS[0]:
        get_emoticon('\u2313\u203f\u2313')  # ⌓‿⌓
    elif method == METHODS[1]:
        get_blackwhite_image()
    elif method == METHODS[2]:
        get_colorful_image()


class MethodException(Exception):
    pass

class MacMethodException(Exception):
    pass

class AnyaImage():
    '''
    METHODS = ['emoticon', 'blackwhite_image', 'colorful_image']
    METHODS_DICT = {1: 'emoticon', 2: 'blackwhite_image', 3: 'colorful_image'}

    Sample:
    >>> from anya import AnyaImage
    >>> anya = AnyaImage()
    >>> anya.show()
    '''
    def __init__(self, show_method=None):
        if (show_method not in METHODS) and (show_method not in METHODS_DICT) and (show_method != None):
            raise MethodException("Input a wrong method")
        if ISMAC and (show_method == METHODS[0] or show_method == 1):
            raise MacMethodException("Mac user can't choose 'emoticon'")
        
        self.show_method = show_method
        if self.show_method in METHODS_DICT:
            self.show_method = METHODS_DICT[show_method]

        self.methods = METHODS

    def get_methods(self):
        return METHODS

    def show(self):
        if self.show_method:
            get_anya(self.show_method)
        else:
            if ISMAC:
                get_anya(choice(METHODS[1:]))
            else:
                get_anya(choice(METHODS))

if not ISMAC:
    class GIFLabel(tk.Label):
        def setup(self, gif_index):
            fn = f'{gif_index}.gif'
            wget.download(f'https://aniyuki.com/wp-content/uploads/2022/05/aniyuki-anya-spy-x-family-{gif_index}.gif', fn)
            gif = Image.open(fn)
            length = iio.imread(fn).shape[0]
            self.duration = gif.info['duration']

            frames = []
            if gif_index in TROUBLE_DICT:
                trouble_index = TROUBLE_DICT[gif_index]
            else:
                trouble_index =[]
            
            for i in range(length):
                if i in trouble_index:
                    continue
                gif.seek(i)
                frames.append(ImageTk.PhotoImage(gif.copy()))

            self.frames = cycle(frames)
            gif.close()
            os.remove(fn)

        def unload(self):
            self.config(image=None)
            self.frames = None
        
        def next_frame(self):
            if self.frames:
                self.config(image=next(self.frames))
                self.after(self.duration, self.next_frame)
        
        def start(self):
            self.next_frame()


class AnyaGIFImage():
    '''
    Sample:
    >>> from anya import AnyaGIFImage
    >>> anya = AnyaGIFImage()
    >>> anya.show()
    '''
    def __init__(self):
        self.gif_index = choice(GIF_LIST)
    
    def show(self):
        self.gif_index = choice(GIF_LIST)

        if ISMAC:
            driver = webdriver.Edge(EdgeChromiumDriverManager().install())
            driver.set_window_position(850, 100)
            driver.set_window_size(500, 500)
            driver.get(f'https://aniyuki.com/wp-content/uploads/2022/05/aniyuki-anya-spy-x-family-{self.gif_index}.gif')
            # os.system("pause")
            input("Input character to end...")
        else:
            window = tk.Tk()
            window.title('Anya')
            window.geometry('+900+100')

            label = GIFLabel()
            label.setup(gif_index=self.gif_index)
            label.start()
            label.pack()
            
            label.grid(column=0, row=0)
            window.mainloop()

    def download(self):
        '''
        Download only one GIF
        '''
        fn = f'Anya-{self.gif_index}.gif'
        wget.download(f'https://aniyuki.com/wp-content/uploads/2022/05/aniyuki-anya-spy-x-family-{self.gif_index}.gif', fn)
        
        
    def download_all(self):
        '''
        Download all GIFs
        '''
        for gif_index in GIF_LIST:
            fn = f'Anya-{gif_index}.gif'
            wget.download(f'https://aniyuki.com/wp-content/uploads/2022/05/aniyuki-anya-spy-x-family-{gif_index}.gif', fn)


if __name__ == '__main__':  
    anyaImg = AnyaImage()
    anyaGif = AnyaGIFImage()
    anyaGif.show()
    # anyaGif.download()
