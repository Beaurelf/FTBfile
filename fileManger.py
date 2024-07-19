import string
from tkinter import *
from tkinter.ttk import *
import os
import time
from tkinter.ttk import *
from pathlib import Path
from tkinter.messagebox import *
import shutil
import function
from distutils.dir_util import copy_tree
import threading
from tkinter.simpledialog import *
import send2trash


class FileManager:
    __img_dir = None
    __img_pc = None
    __img_disk = None
    __img_open = None
    __img_copy = None
    __img_copy1 = None
    __img_paste = None
    __img_paste1 = None
    __img_close = None
    __img_new_dir = None
    __img_move = None
    __img_search = None
    __img_infors = None
    __img_cut = None
    __img_cut1 = None
    __img_next = None
    __img_back = None
    __img_rename = None
    __img_rename1 = None
    __img_delete = None
    __img_delete1 = None
    __img_refresh = None
    __img_download = None
    __img_document = None
    __img_videos = None
    __img_images = None
    __img_music = None
    __img_desktop = None
    __img_user = None

    def __init__(self):
        self.root: Tk = Tk()
        self.setupUi()

    def launch(self):
        self.root.mainloop()

    def setupUi(self):
        self.load_images()
        self.root.title("FTBfile")
        self.root.minsize(1080, 1080)
        self.root.iconbitmap('images/explorer_personal_icon-icons.com_71977_ico32.ico')
        self.load_images()

    def create_toolbar(self):
        pass

    @classmethod
    def load_images(cls):
        cls.__img_dir = PhotoImage(file='images/sparklesfolderblank_99348 (1).png')
        cls.__img_pc = PhotoImage(file='images/Desktop_Acer_43256.png')
        cls.__img_disk = PhotoImage(file='images/hd_hardware_harddisk_9894.png')
        cls.__img_open = PhotoImage(file='images/open-file_40455.png')
        cls.__img_copy = PhotoImage(file='images/Copy_26996.png')
        cls.__img_copy1 = PhotoImage(file='images/Copy_26996(1).png')
        cls.__img_paste = PhotoImage(file='images/Paste_26994.png')
        cls.__img_paste1 = PhotoImage(file='images/Paste_26994(1).png')
        cls.__img_close = PhotoImage(file='images/exit_closethesession_close_6317(1).png')
        cls.__img_new_dir = PhotoImage(file='images/new_folder_black_13778 (1).png')
        cls.__img_move = PhotoImage(file='images/file_move_icon_138617.png')
        cls.__img_search = PhotoImage(file='images/Search.png')
        cls.__img_infors = PhotoImage(file='images/information_info_1565.png')
        cls.__img_cut = PhotoImage(file='images/scissors_icon-icons.com_66285.png')
        cls.__img_cut1 = PhotoImage(file='images/scissors_icon-icons.com_66285(1).png')
        cls.__img_next = PhotoImage(file='images/redo-arrow_icon-icons.com_53912.png')
        cls.__img_back = PhotoImage(file='images/arrow-address-back_icon-icons.com_54065.png')
        cls.__img_rename = PhotoImage(file='images/gui_rename_icon_157599.png')
        cls.__img_rename1 = PhotoImage(file='images/gui_rename_icon_157599(1).png')
        cls.__img_delete = PhotoImage(file='images/document_delete_256_icon-icons.com_75995.png')
        cls.__img_delete1 = PhotoImage(file='images/document_delete_256_icon-icons.com_75995(1).png')
        cls.__img_refresh = PhotoImage(file='images/refresh_arrow_1546 (1).png')
        cls.__img_download = PhotoImage(file='images/downloadfolder_99367.png')
        cls.__img_document = PhotoImage(file='images/documentediting_editdocuments_text_documentedi_2820.png')
        cls.__img_videos = PhotoImage(file='images/Video file (1).png')
        cls.__img_images = PhotoImage(file='images/iPhoto_photo_picture_camera_2661.png')
        cls.__img_music = PhotoImage(file='images/Library Music.png')
        cls.__img_desktop = PhotoImage(file='images/Desktop.png')
        cls.__img_user = PhotoImage(file='images/User (1).png')

