import string
from tkinter import *
import os
import time
from tkinter.ttk import *
from pathlib import Path
from tkinter.messagebox import *
import shutil
from distutils.dir_util import copy_tree
import threading
from tkinter.simpledialog import *
import send2trash
import helper


class FileManager(Tk):

    MAX_SIZE_TO_TRASH = 2147483648

    # drive est un tableau contenant toutes les lettres de l'alphabet en lettre majusules
    __drives = string.ascii_uppercase
    # ce tableau contiendra les chemins absolus des elements sur lequel on a clique
    tabcopy = []
    # ce tableau contiendra les chemins absolus des elements sur lequel on a clique
    tabcut = []

    def __init__(self):
        super().__init__()
        # declaration d'un tableau qui contiendra les disk reconnus par la machine
        self.valid_drives = []
        # ce tableau contiendra des chemins absolus et on l'utilisera dans les fonctions go_back go_next
        self.paths = []
        # permet de se balader dans le tableau paths
        self.pos_paths = 2

        # permet d'enregistrer les images des fichiers pour qu'elles ne disparaissent par dans l'arborescence de droite
        self.all_img_file = []

        self.load_images()
        self.setupUi()
        self.add_disk()
        self.remove_disk()
        self.add_action_btn()

        # style des arbres
        self.style = Style(master=self)
        self.style.theme_use("clam")
        self.style.configure(self)

        # définitions de tous les handlers
        def left_tree_open_handler(event: Event):
            self.populate_left_directory_tree(event)

        def left_tree_select_handler(event: Event):
            self.populate_right_directory_tree(event)

        def left_tree_release_handler(event: Event):
            self.display_absolute_path(event)

        def open_file_or_dir_handler(event: Event):
            self.open_file_or_dir(event)

        def go_back_handler(event: Event):
            self.go_back()

        def create_new_dir_handler(event: Event):
            self.create_new_dir()

        def desactived_button(event: Event):
            self.btn_delete.config(state=DISABLED)
            self.btn_rename.config(state=DISABLED)
            self.btn_property.config(state=DISABLED)
            self.btn_copy.config(state=DISABLED)
            self.btn_cut.config(state=DISABLED)

        def actived_button(event: Event):
            self.btn_delete.config(state=NORMAL)
            self.btn_rename.config(state=NORMAL)
            self.btn_property.config(state=NORMAL)
            self.btn_copy.config(state=NORMAL)
            self.btn_cut.config(state=NORMAL)

        def delete_handler(event: Event):
            self.delete()

        def copy_handler(event: Event):
            self.copy()

        def cut_handler(event: Event):
            self.cut()

        def paste_handler(event: Event):
            self.paste()

        def display_menu_contextual(event: Event):
            select = self.right_directory_tree.identify_row(event.y)
            if select:
                self.right_directory_tree.selection_set(select)
                self.menu_contextual.post(self.winfo_pointerx(), self.winfo_pointery())
            else:
                if self.path_access.cget("text") == '':
                    pass
                elif len(self.tabcopy) >= 1 or len(self.tabcut) >= 1:
                    self.menu_contextual_3.post(self.winfo_pointerx(), self.winfo_pointery())
                else:
                    self.menu_contextual_2.post(self.winfo_pointerx(), self.winfo_pointery())

        # ajout de tous les évènements
        self.bind('<KeyPress-BackSpace>', go_back_handler)
        self.bind('<Shift-KeyPress-N>', create_new_dir_handler)
        self.bind('<Alt-F4>', lambda e: self.quit)

        self.left_directory_tree.bind("<<TreeviewOpen>>", left_tree_open_handler)
        self.left_directory_tree.bind("<<TreeviewSelect>>", left_tree_select_handler)
        self.left_directory_tree.bind("<ButtonRelease>", left_tree_release_handler)
        self.left_directory_tree.bind('<Button-1>', desactived_button)

        self.right_directory_tree.bind("<<Button-1>>", open_file_or_dir_handler)
        self.right_directory_tree.bind('<Double-Button-1>', open_file_or_dir_handler)
        self.right_directory_tree.bind('<KeyPress-Return>', open_file_or_dir_handler)
        self.right_directory_tree.bind('<Delete>', delete_handler)
        self.right_directory_tree.bind('<Shift-KeyPress-C>', copy_handler)
        self.right_directory_tree.bind('<Shift-KeyPress-X>', cut_handler)
        self.right_directory_tree.bind("<<TreeviewSelect>>", actived_button)
        self.right_directory_tree.bind('<Shift-KeyPress-V>', paste_handler)
        self.right_directory_tree.bind('<Button-3>', display_menu_contextual)


    def setupUi(self):
        self.pane_container = PanedWindow(self, orient=HORIZONTAL, bg='grey')
        self.title("FTBfile")
        self.minsize(1080, 1080)
        self.iconbitmap('images/explorer_personal_icon-icons.com_71977_ico32.ico')
        self.create_toolbar()
        self.create_menu()
        self.create_contextual_menu()
        self.create_path_bar()
        self.create_left_directory_treeview()
        self.create_right_directory_treeview()
        self.create_bottom_bar()

    def load_images(self):
        self.__img_dir = PhotoImage(file='images/sparklesfolderblank_99348 (1).png', master=self)
        self.__img_pc = PhotoImage(file='images/Desktop_Acer_43256.png',  master=self)
        self.__img_disk = PhotoImage(file='images/hd_hardware_harddisk_9894.png',  master=self)
        self.__img_open = PhotoImage(file='images/open-file_40455.png', master=self)
        self.__img_copy = PhotoImage(file='images/Copy_26996.png', master=self)
        self.__img_copy1 = PhotoImage(file='images/Copy_26996(1).png', master=self)
        self.__img_paste = PhotoImage(file='images/Paste_26994.png', master=self)
        self.__img_paste1 = PhotoImage(file='images/Paste_26994(1).png', master=self)
        self.__img_close = PhotoImage(file='images/exit_closethesession_close_6317(1).png', master=self)
        self.__img_new_dir = PhotoImage(file='images/new_folder_black_13778 (1).png', master=self)
        self.__img_move = PhotoImage(file='images/file_move_icon_138617.png', master=self)
        self.__img_search = PhotoImage(file='images/Search.png', master=self)
        self.__img_infors = PhotoImage(file='images/information_info_1565.png', master=self)
        self.__img_cut = PhotoImage(file='images/scissors_icon-icons.com_66285.png', master=self)
        self.__img_cut1 = PhotoImage(file='images/scissors_icon-icons.com_66285(1).png', master=self)
        self.__img_next = PhotoImage(file='images/redo-arrow_icon-icons.com_53912.png', master=self)
        self.__img_back = PhotoImage(file='images/arrow-address-back_icon-icons.com_54065.png', master=self)
        self.__img_rename = PhotoImage(file='images/gui_rename_icon_157599.png', master=self)
        self.__img_rename1 = PhotoImage(file='images/gui_rename_icon_157599(1).png', master=self)
        self.__img_delete = PhotoImage(file='images/document_delete_256_icon-icons.com_75995.png', master=self)
        self.__img_delete1 = PhotoImage(file='images/document_delete_256_icon-icons.com_75995(1).png', master=self)
        self.__img_refresh = PhotoImage(file='images/refresh_arrow_1546 (1).png', master=self)
        self.__img_download = PhotoImage(file='images/downloadfolder_99367.png', master=self)
        self.__img_document = PhotoImage(file='images/documentediting_editdocuments_text_documentedi_2820.png', master=self)
        self.__img_videos = PhotoImage(file='images/Video file (1).png', master=self)
        self.__img_images = PhotoImage(file='images/iPhoto_photo_picture_camera_2661.png', master=self)
        self.__img_music = PhotoImage(file='images/Library Music.png', master=self)
        self.__img_desktop = PhotoImage(file='images/Desktop.png', master=self)
        self.__img_user = PhotoImage(file='images/User (1).png', master=self)

    def create_menu(self):
        menubar = Menu(self)
        menu_file = Menu(menubar, tearoff=0)
        menu_file.add_command(label="Nouvelle fenêtre", image=self.__img_open, compound="left",
                              command=self.open_new_file_manager)
        menu_file.add_command(label="Fermer", image=self.__img_close, compound="left", command=quit)
        menubar.add_cascade(label="Fichier", menu=menu_file)
        menu_edition = Menu(menubar, tearoff=0)
        menu_edition.add_command(label="Copier", image=self.__img_copy1, compound="left", accelerator="Shift+C",
                                 command=self.copy)
        menu_edition.add_separator()
        menu_edition.add_command(label="Coller", image=self.__img_paste1, compound="left", accelerator="Shift+V",
                                 command=self.paste)
        menu_edition.add_separator()
        menu_edition.add_command(label="Couper", image=self.__img_cut1, compound="left", accelerator="Shift+X",
                                 command=self.cut)
        menu_edition.add_separator()
        menu_edition.add_command(label="Renommer", image=self.__img_rename1, compound="left", command=self.rename)
        menu_edition.add_separator()
        menu_edition.add_command(label="Supprimer", image=self.__img_delete1, compound="left", command=self.delete)
        menubar.add_cascade(label="Edition", menu=menu_edition)

        menu_help = Menu(menubar, tearoff=0)
        menu_help.add_command(label="A propos", command=self.infors)
        menubar.add_cascade(label="Aide", menu=menu_help)
        self.config(menu=menubar)

    def create_contextual_menu(self):
        self.menu_contextual = Menu(self, tearoff=0)
        self.menu_contextual.add_command(label="Ouvrir avec", command=self.open_with)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="Copier", command=self.copy)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="Coller", command=self.paste)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="Couper", command=self.cut)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="Renommer", command=self.rename)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="Supprimer", command=self.delete)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label="Propriétés", command=self.property)

        self.menu_contextual_2 = Menu(self, tearoff=0)
        self.menu_contextual_2.add_command(label="Nouveau Dossier", command=self.create_new_dir)

        self.menu_contextual_3 = Menu(self, tearoff=0)
        self.menu_contextual_3.add_command(label="Nouveau Dossier", command=self.create_new_dir)
        self.menu_contextual_3.add_separator()
        self.menu_contextual_3.add_command(label="Coller", command=self.paste)

    def create_toolbar(self):
        frame_boutons = LabelFrame(self)
        frame_boutons.pack(side=TOP, fill=BOTH, padx=5, pady=0)
        outils = LabelFrame(frame_boutons, text='Outils')
        outils.grid(row=0, column=0)
        self.btn_copy = Button(outils, text="Copier", image=self.__img_copy, width=55, height=55, compound='top',
                               bg='white', state=DISABLED)
        self.btn_copy.grid(row=0, column=0)
        self.btn_paste = Button(outils, text="Coller", image=self.__img_paste, width=55, height=55, compound='top',
                                bg='white',
                                state=DISABLED)
        self.btn_paste.grid(row=0, column=1)
        self.btn_cut = Button(outils, text="Couper", image=self.__img_cut, width=55, height=55, compound='top',
                              bg='white')
        self.btn_cut.grid(row=0, column=2)
        self.btn_property = Button(outils, text="Propriétés", image=self.__img_infors, width=55, height=55,
                                   compound='top', bg='white',
                                   state=DISABLED)
        self.btn_property.grid(row=0, column=6)
        self.btn_new = Button(outils, text="Nouveau", image=self.__img_new_dir, width=55, height=55, compound='top',
                              bg='white',
                              state=DISABLED)
        self.btn_new.grid(row=0, column=4)
        self.btn_delete = Button(outils, text="Supprimer", image=self.__img_delete, width=55, height=55, compound='top',
                                 bg='white',
                                 state=DISABLED)
        self.btn_delete.grid(row=0, column=5)
        self.btn_rename = Button(outils, text="Renommer", image=self.__img_rename, width=55, height=55, compound='top',
                                 bg='white',
                                 state=DISABLED)
        self.btn_rename.grid(row=0, column=3)
        frame_quick_access = LabelFrame(frame_boutons, text='Accès rapide')
        frame_quick_access.grid(row=0, column=1)
        self.quick_access_user = Button(frame_quick_access, image=self.__img_user, text="User", width=55, height=55,
                                        compound='top', bg='white')
        self.quick_access_user.grid(row=0, column=0)
        self.quick_access_desktop = Button(frame_quick_access, image=self.__img_desktop, text="Desktop", width=55,
                                           height=55, compound='top',
                                           bg='white')
        self.quick_access_desktop.grid(row=0, column=1)
        self.quick_access_download = Button(frame_quick_access, image=self.__img_download, text="Download", width=55,
                                            height=55, compound='top',
                                            bg='white')
        self.quick_access_download.grid(row=0, column=2)
        self.quick_access_doc = Button(frame_quick_access, image=self.__img_document, text="Documents", width=55,
                                       height=55, compound='top', bg='white')
        self.quick_access_doc.grid(row=0, column=3)
        self.quick_access_videos = Button(frame_quick_access, image=self.__img_videos, text="Videos", width=55,
                                          height=55, compound='top', bg='white')
        self.quick_access_videos.grid(row=0, column=4)
        self.quick_access_music = Button(frame_quick_access, image=self.__img_music, text="Music", width=55, height=55,
                                         compound='top', bg='white')
        self.quick_access_music.grid(row=0, column=5)
        self.quick_access_images = Button(frame_quick_access, image=self.__img_images, text="Images", width=55,
                                          height=55, compound='top', bg='white')
        self.quick_access_images.grid(row=0, column=6)

    def create_path_bar(self):
        frame_tools = LabelFrame(self)
        frame_tools.pack(side=TOP, fill=X, padx=5, pady=2)
        self.back_btn = Button(frame_tools, bg='white', image=self.__img_back, width=20, height=17, state=DISABLED)
        self.back_btn.grid(row=0, column=0)
        self.next_btn = Button(frame_tools, bg='white', image=self.__img_next, width=20, height=17, state=DISABLED)
        self.next_btn.grid(row=0, column=1)
        self.refresh_btn = Button(frame_tools, bg='white', width=20, height=17, image=self.__img_refresh)
        self.refresh_btn.grid(row=0, column=2)
        pane_tools = PanedWindow(frame_tools, orient=HORIZONTAL, bg='white')
        pane_tools.grid(row=0, column=3)
        self.search_bar = Entry(frame_tools, width=80)
        self.path_access = Label(frame_tools, width=108, bg='white')
        pane_tools.add(self.path_access)
        pane_tools.add(self.search_bar)
        self.search_btn = Button(frame_tools, bg='white', image=self.__img_search, height=17, width=20)
        self.search_btn.grid(row=0, column=4, sticky=SE)

    def create_left_directory_treeview(self):
        self.pane_container.pack(side=TOP, expand="True", fill=BOTH, padx=5, pady=2)
        pane_dir = PanedWindow(self, bg='grey')
        self.pane_container.add(pane_dir)
        # creations arbres de gauche et de sa barre de defilement
        left_treescroll = Scrollbar(pane_dir)
        left_treescroll.pack(side=RIGHT, fill=Y)
        self.left_directory_tree = Treeview(pane_dir, yscrollcommand=left_treescroll.set)
        self.left_directory_tree.pack(expand=True, fill=BOTH, side=LEFT)
        left_treescroll.config(command=self.left_directory_tree.yview)

        # ajout d'un titre a notre arbre ainsi qu'une image
        self.left_directory_tree.heading('#0', text='Ce PC', anchor=W, image=self.__img_pc)

    def create_right_directory_treeview(self):
        # creation du widget qui contiendra l'arbre de droite
        frame_dir_file = LabelFrame(self, text='Dossiers & Fichiers')
        self.pane_container.add(frame_dir_file)

        # creation arbre de droite et sa barre de defilement
        col = ('Modifier', 'Type', 'Taille')
        right_treescroll = Scrollbar(frame_dir_file)
        right_treescroll.pack(side=RIGHT, fill=Y)
        self.right_directory_tree = Treeview(frame_dir_file, columns=col, yscrollcommand=right_treescroll.set)
        right_treescroll.config(command=self.right_directory_tree.yview)

        # Ajout des colonnes
        self.right_directory_tree.column('#0', minwidth=100, width=200, anchor=W)
        self.right_directory_tree.column('Modifier', minwidth=50, width=100, anchor=W)
        self.right_directory_tree.column('Type', minwidth=50, width=70, anchor=W)
        self.right_directory_tree.column('Taille', width=70, anchor=E)

        # Donner des titres aux colonnes
        self.right_directory_tree.heading('#0', text="Nom", anchor=W)
        self.right_directory_tree.heading('Modifier', text="Date Modification", anchor=W)
        self.right_directory_tree.heading('Type', text="Type", anchor=W)
        self.right_directory_tree.heading('Taille', text="Taille", anchor=W)
        self.right_directory_tree.pack(expand=True, fill=BOTH, side=LEFT)

    def create_bottom_bar(self):
        bottom_frame = LabelFrame(self)
        bottom_frame.pack(fill=BOTH, padx=5, pady=0)
        self.nb_dir_file = Label(bottom_frame, bg='white')
        self.nb_dir_file.pack(fill=X)

    def add_disk(self):
        for each_drive in FileManager.__drives:
            if os.path.exists(each_drive + ":\\"):
                if not each_drive + ":\\" in self.valid_drives:
                    self.valid_drives.append(each_drive + ":\\")
                    node = self.left_directory_tree.insert(parent='', index='end', text=each_drive + ":\\",
                                                           image=self.__img_disk)
                    self.left_directory_tree.insert(parent=node, index='end')
        self.after(5, self.add_disk)

    def remove_disk(self):
        for each_drive in self.valid_drives:
            if os.path.exists(each_drive):
                pass
            else:
                self.valid_drives.remove(each_drive)
                for x in self.left_directory_tree.get_children():
                    if self.left_directory_tree.item(x)['text'] == each_drive:
                        self.left_directory_tree.delete(x)
                    else:
                        pass
        self.after(5, self.remove_disk)

    def populate_left_directory_tree(self, event: Event):
        racine = self.left_directory_tree.selection()
        children = self.left_directory_tree.get_children(racine)
        for child in children:
            self.left_directory_tree.delete(child)
        parent = self.left_directory_tree.parent(racine)
        if parent != '':
            b = os.path.join(self.left_directory_tree.item(parent)['text'],
                             self.left_directory_tree.item(racine)['text'])
            while parent != '':
                parent = self.left_directory_tree.parent(parent)
                b = os.path.join(self.left_directory_tree.item(parent)['text'], b)
            absolute_path = Path(b)
        else:
            b = self.left_directory_tree.item(racine)['text']
            absolute_path = Path(b)
        try:
            for entry in os.listdir(absolute_path):
                try:
                    path1 = Path(b + "\\" + entry)
                    if path1.is_dir():
                        try:
                            node = self.left_directory_tree.insert(parent=racine, index='end', text=entry,
                                                                   image=self.__img_dir)
                            self.left_directory_tree.insert(parent=node, index='end')
                        except OSError as e:
                            showerror(title="Erreur", message=str(e))
                except OSError as e:
                    showerror("Erreur", message=str(e))
        except OSError as e:
            showerror("Erreur", message=str(e))
        self.path_access.config(text=absolute_path)

    def insertion(self, tree: Treeview, path, text: str):
        if path.is_dir():
            try:
                tree.insert(parent='', index=0, text=text,
                            values=[time.ctime(os.path.getmtime(path)), 'Dossier',
                                    '', path], image=self.__img_dir)
            except OSError as e:
                showerror("Erreur", message=str(e))
        else:
            try:
                img_file = helper.define_icon(path, master=self)
                tree.insert(parent='', index='end', text=text,
                            values=[time.ctime(os.path.getmtime(path)), 'Fichier' + (os.path.splitext(path)[1]).upper(),
                                    str(os.path.getsize(path)) + ' Byte(s)', path], image=img_file)
                FileManager.all_img_file.append(img_file)
            except OSError as e:
                showerror("Erreur", message=str(e))

    # toutes cette fonctions me permettent d'accéder rapidement au bureau, aux documents, images ,videos.......
    def on_quick_access(self, folder_name: str):
        path = Path.home() if folder_name == 'User' else os.path.join(Path.home(), folder_name)
        try:
            for child in self.right_directory_tree.get_children():
                self.right_directory_tree.delete(child)
            for entry in os.listdir(path):
                try:
                    path1 = Path(os.path.join(path), entry)
                    self.insertion(self.right_directory_tree, path1, entry)
                except OSError as e:
                    showerror("Erreur", message=str(e))
        except OSError as e:
            showerror("Erreur", message=str(e))
        self.path_access.config(text=os.path.join(Path.home(), folder_name))
        self.back_btn.config(state=NORMAL)
        self.next_btn.config(state=NORMAL)
        self.next_btn.config(state=NORMAL)
        self.paths.append(path)
        self.btn_copy.config(state=DISABLED)
        self.btn_cut.config(state=DISABLED)
        self.nb_dir_file.config(text=(str(len(os.listdir(path))) + " élément(s)"))

    def on_quick_access_documents(self):
        self.on_quick_access('Documents')

    def on_quick_access_videos(self):
        self.on_quick_access('Videos')

    def on_quick_access_user(self):
        self.on_quick_access('User')

    def on_quick_access_downloads(self):
        self.on_quick_access('Downloads')

    def on_quick_access_music(self):
        self.on_quick_access('Music')

    def on_quick_access_desktop(self):
        self.on_quick_access('Desktop')

    def on_quick_access_images(self):
        self.on_quick_access('Pictures')

    def populate_right_directory_tree(self, event: Event):
        for child in self.right_directory_tree.get_children():
            self.right_directory_tree.delete(child)
        racine = self.left_directory_tree.selection()
        parent = self.left_directory_tree.parent(racine)
        if parent != '':
            b = os.path.join(self.left_directory_tree.item(parent)['text'], self.left_directory_tree.item(racine)['text'])
            while parent != '':
                parent = self.left_directory_tree.parent(parent)
                b = os.path.join(self.left_directory_tree.item(parent)['text'], b)
            absolute_path = Path(b)
        else:
            b = self.left_directory_tree.item(racine)['text']
            absolute_path = Path(b)
        try:
            for entry in os.listdir(absolute_path):
                try:
                    path1 = Path(b + "\\" + entry)
                    self.insertion(self.right_directory_tree, path1, entry)
                except OSError as e:
                    showerror("Erreur", message=str(e))
        except OSError as e:
            showerror("Erreur", message=str(e))

        self.nb_dir_file.config(text=(str(len(os.listdir(absolute_path))) + " élément(s)"))
        self.btn_new.config(state=NORMAL)
        self.back_btn.config(state=NORMAL)
        self.next_btn.config(state=NORMAL)

    def open_file_or_dir(self, event: Event):
        try:
            racine = self.right_directory_tree.selection()
            b = (self.right_directory_tree.item(racine)['values'])[3]
            absolute_path = Path(b)
        except IndexError:
            pass
        if absolute_path.is_dir():
            for child in self.right_directory_tree.get_children():
                self.right_directory_tree.delete(child)
            try:
                for entry in os.listdir(absolute_path):
                    try:
                        path1 = Path(b + "\\" + entry)
                        self.insertion(self.right_directory_tree, path1, entry)
                    except OSError as e:
                        showerror("Erreur", message=str(e))
            except OSError as e:
                showerror("Erreur", message=str(e))
            self.path_access.config(text=absolute_path)
            self.paths.append(self.path_access.cget("text"))
            self.nb_dir_file.config(text=(str(len(os.listdir(absolute_path))) + " élement(s)"))
        else:
            try:
                os.startfile(absolute_path)
            except OSError as e:
                showerror("Erreur", message=str(e))
        self.btn_new.config(state=NORMAL)
        self.next_btn.config(state=NORMAL)
        self.back_btn.config(state=NORMAL)

    def display_absolute_path(self, event: Event):
        racine = self.left_directory_tree.selection()
        parent = self.left_directory_tree.parent(racine)
        if parent != '':
            a = self.left_directory_tree.item(parent)['text']
            b = os.path.join(a, self.left_directory_tree.item(racine)['text'])
            while parent != '':
                parent = self.left_directory_tree.parent(parent)
                a = self.left_directory_tree.item(parent)['text']
                b = os.path.join(a, b)
            absolute_path = Path(b)
        else:
            b = self.left_directory_tree.item(racine)['text']
            absolute_path = Path(b)
        self.path_access.config(text=absolute_path)
        self.paths.append(self.path_access.cget("text"))

    def go_back(self):
        self.next_btn.config(state=NORMAL)
        for x in self.right_directory_tree.get_children():
            self.right_directory_tree.delete(x)
        if len(self.paths) - self.pos_paths >= 0:
            try:
                for entry in os.listdir(self.paths[len(self.paths) - self.pos_paths]):
                    try:
                        path1 = Path(self.paths[len(self.paths) - self.pos_paths] + "\\" + entry)
                        self.insertion(self.right_directory_tree, path1, entry)
                    except OSError as e:
                        showerror('Erreur', message=str(e))
                        pass
                b = self.paths[len(self.paths) - self.pos_paths]
                absolute_path = Path(b)
                self.path_access.config(text=absolute_path)
                self.nb_dir_file.config(text=(str(len(os.listdir(absolute_path))) + " élement(s)"))
                self.pos_paths = self.pos_paths + 1
            except IndexError:
                pass
        else:
            self.back_btn.config(state=DISABLED)
            for entry in os.listdir(self.path_access.cget('text')):
                try:
                    path1 = Path(self.path_access.cget('text') + "\\" + entry)
                    self.insertion(self.right_directory_tree, path1, entry)
                except OSError as e:
                    showerror('Erreur', message=str(e))
        self.btn_delete.config(state=DISABLED)
        self.btn_rename.config(state=DISABLED)
        self.btn_copy.config(state=DISABLED)
        self.btn_cut.config(state=DISABLED)
        self.btn_property.config(state=DISABLED)

    def go_next(self):
        self.back_btn.config(state=NORMAL)
        for child in self.right_directory_tree.get_children():
            self.right_directory_tree.delete(child)
        if len(self.paths) - self.pos_paths >= -1:
            try:
                for entry in os.listdir(self.paths[len(self.paths) - self.pos_paths + 2]):
                    try:
                        path1 = Path(self.paths[len(self.paths) - self.pos_paths + 2] + "\\" + entry)
                        self.insertion(self.right_directory_tree, path1, entry)
                    except OSError as e:
                        showerror('Erreur', message=str(e))
                b = self.paths[len(self.paths) - self.pos_paths + 2]
                absolute_path = Path(b)
                self.path_access.config(text=absolute_path)
                self.nb_dir_file.config(text=(str(len(os.listdir(absolute_path))) + " élement(s)"))
                self.pos_paths = self.pos_paths - 1
            except IndexError:
                self.next_btn.config(state=DISABLED)
                for entry in os.listdir(self.path_access.cget('text')):
                    try:
                        path1 = Path(self.path_access.cget('text') + "\\" + entry)
                        self.insertion(self.right_directory_tree, path1, entry)
                    except OSError as e:
                        showerror('Erreur', message=str(e))
                pass
        self.btn_delete.config(state=DISABLED)
        self.btn_rename.config(state=DISABLED)
        self.btn_copy.config(state=DISABLED)
        self.btn_cut.config(state=DISABLED)
        self.btn_property.config(state=DISABLED)

    def create_new_dir(self):
        try:
            name = askstring("Creation nouveau dossier", " Entrez le nom du nouveau dossier")
            try:
                path = os.path.join(self.path_access.cget('text'), name)
                os.mkdir(path)
            except TypeError:
                pass
        except OSError as e:
            showerror('Erreur', message=str(e))
        for child in self.right_directory_tree.get_children():
            self.right_directory_tree.delete(child)
        for entry in os.listdir(self.path_access.cget('text')):
            try:
                path1 = Path(self.path_access.cget('text') + "\\" + entry)
                self.insertion(self.right_directory_tree, path1, entry)
            except OSError as e:
                showerror('Erreur', message=str(e))
        self.nb_dir_file.config(text=(str(len(os.listdir(self.path_access.cget('text')))) + " élement(s)"))

    def delete(self):
        size = 0
        # Je dois faire la corbeille
        try:
            deleted_dirs = self.right_directory_tree.selection()
            for x in deleted_dirs:
                if os.path.isdir((self.right_directory_tree.item(x)['values'])[3]):
                    size += helper.folder_size((self.right_directory_tree.item(x)['values'])[3])
                else:
                    size += os.path.getsize((self.right_directory_tree.item(x)['values'])[3])
            if size <= FileManager.MAX_SIZE_TO_TRASH:
                if askyesno("Notice",
                            "ces dossiers et/ou fichiers seront envoyés vers la corbeille voulez vous continuer?"):
                    for x in deleted_dirs:
                        try:
                            send2trash.send2trash((self.right_directory_tree.item(x)['values'])[3])
                        except OSError as e:
                            showerror("Erreur", message=str(e))
            else:
                if askyesno("Notice",
                            "ces dossiers et/ou fichiers seront supprimé definitivement voulez vous vraiment le "
                            "supprimer?"):
                    for x in deleted_dirs:
                        path = (self.right_directory_tree.item(x)['values'])[3]
                        if os.path.isdir(path):
                            try:
                                shutil.rmtree(path)
                            except OSError as e:
                                showerror("Erreur", message=str(e))
                        else:
                            try:
                                os.remove(path)
                            except OSError as e:
                                showerror("Erreur", message=str(e))
                else:
                    pass
            for child in self.right_directory_tree.get_children():
                self.right_directory_tree.delete(child)
            for entry in os.listdir(self.path_access.cget('text')):
                try:
                    path1 = Path(self.path_access.cget('text') + "\\" + entry)
                    self.insertion(self.right_directory_tree, path1, entry)
                except OSError as e:
                    showerror('Erreur', message=str(e))
        except IndexError:
            pass
        self.btn_delete.config(state=DISABLED)
        self.btn_rename.config(state=DISABLED)
        self.nb_dir_file.config(text=(str(len(os.listdir(self.path_access.cget('text')))) + " élement(s)"))

    def rename(self):
        racine = self.right_directory_tree.focus()
        path = (self.right_directory_tree.item(racine)['values'])[3]
        new_name = askstring("renommer", "Entrez le nouveau nom")
        try:
            if os.path.isdir(path):
                try:
                    os.rename(path, os.path.join(self.path_access.cget("text"), new_name))
                except TypeError:
                    pass
            else:
                try:
                    os.rename(path,
                              os.path.join(self.path_access.cget("text"), new_name + (os.path.splitext(path))[1]))
                except TypeError:
                    pass
        except OSError as e:
            showerror("Erreur", message=str(e))
        for x in self.right_directory_tree.get_children():
            self.right_directory_tree.delete(x)
        for entry in os.listdir(self.path_access.cget('text')):
            try:
                path1 = Path(self.path_access.cget('text') + "\\" + entry)
                self.insertion(self.right_directory_tree, path1, entry)
            except OSError as e:
                showerror('Erreur', message=str(e))
        self.btn_rename.config(state=DISABLED)
        self.btn_delete.config(state=DISABLED)

    def refresh(self):
        for child in self.right_directory_tree.get_children():
            self.right_directory_tree.delete(child)
        try:
            for entry in os.listdir(self.path_access.cget("text")):
                try:
                    path1 = Path(self.path_access.cget("text") + "\\" + entry)
                    self.insertion(self.right_directory_tree, path1, entry, )
                except OSError as e:
                    showerror("Erreur", message=str(e))
        except OSError as e:
            showerror("Erreur", message=str(e))
        self.btn_delete.config(state=DISABLED)
        self.btn_rename.config(state=DISABLED)
        self.btn_property.config(state=DISABLED)
        self.btn_copy.config(state=DISABLED)
        self.btn_cut.config(state=DISABLED)
        self.nb_dir_file.config(text=(str(len(os.listdir(self.path_access.cget('text')))) + " élement(s)"))

    def property(self):
        def property_process():
            racine = self.right_directory_tree.focus()
            parent = self.right_directory_tree.parent(racine)
            if racine:
                path = Path((self.right_directory_tree.item(racine)['values'])[3])
                P = Tk()
                nom = Label(P, text="Nom :")
                nom.grid(column=0, row=0, sticky=W)
                nom1 = Label(P, text=self.right_directory_tree.item(racine)['text'])
                nom1.grid(column=1, row=0, sticky=W)
                type = Label(P, text="Type :")
                type.grid(column=0, row=2, sticky=W)
                if path.is_dir():
                    type1 = Label(P, text="Dossier")
                else:
                    type1 = Label(P, text="Fichier" + (os.path.splitext(path)[1]).upper())
                type1.grid(column=1, row=2, sticky=W)
                absolute_path_label = Label(P, text="Chemin absolu :")
                absolute_path_label.grid(column=0, row=3, sticky=W)
                absolute_path = Label(P, text=(self.right_directory_tree.item(racine)['values'])[3])
                absolute_path.grid(column=1, row=3, sticky=W)
                size_label = Label(P, text="Taille :")
                size_label.grid(column=0, row=4, sticky=W)
                if path.is_dir():
                    size = Label(P, text=str(helper.folder_size(path)) + ' Byte(s)')
                else:
                    size = Label(P, text=str(os.path.getsize(path)) + ' Byte(s)')
                size.grid(column=1, row=4, sticky=W)
                if path.is_dir():
                    content_label = Label(P, text="Contenu :")
                    content_label.grid(column=0, row=5, sticky=W)
                    content = Label(P, text=str(helper.nb_dir(path)) + ' Dossier(s)' + ' ,' + ' ' + str(
                        helper.nb_file(path)) + ' Fichier(s)')
                    content.grid(column=1, row=5, sticky=W)
                date_label = Label(P, text="Crée le:")
                date_label.grid(column=0, row=6, sticky=W)
                date = Label(P, text=time.ctime(os.path.getctime(path)))
                date.grid(column=1, row=6, sticky=W)
                date_modify_label = Label(P, text="Modifié le:")
                date_modify_label.grid(column=0, row=7, sticky=W)
                date_modify = Label(P, text=time.ctime(os.path.getmtime(path)))
                date_modify.grid(column=1, row=7, sticky=W)
                ok = Button(P, text="OK", width=15, command=P.destroy)
                ok.grid(column=2, row=8, padx=10, pady=10)
                P.title("propriétés")
                P.minsize(395, 50)
                P.iconbitmap('images/explorer_personal_icon-icons.com_71977_ico32.ico')
                self.btn_property.config(state=DISABLED)
                self.btn_rename.config(state=DISABLED)
                self.btn_delete.config(state=DISABLED)
                P.mainloop()
            else:
                pass
        thread = threading.Thread(target=property_process)
        thread.start()

    def copy(self):
        for selected_item in self.right_directory_tree.selection():
            try:
                path = (self.right_directory_tree.item(selected_item)['values'])[3]
                self.tabcopy.append(path)
            except IndexError:
                pass
        self.tabcut.clear()
        self.btn_paste.config(state=NORMAL)
        self.btn_copy.config(state=DISABLED)
        self.btn_cut.config(state=DISABLED)

    def cut(self):
        for selected_item in self.right_directory_tree.selection():
            try:
                path = (self.right_directory_tree.item(selected_item)['values'])[3]
                self.tabcut.append(path)
            except IndexError:
                pass
        self.tabcopy.clear()
        self.btn_paste.config(state=NORMAL)
        self.btn_cut.config(state=DISABLED)
        self.btn_copy.config(state=DISABLED)

    def paste(self):
        path = self.path_access.cget("text")

        def paste_process():
            try:
                try:
                    if len(self.tabcopy) != 0:
                        showinfo("Copie lancée", "une fois votre copie terminé un message apparaitra")
                        for elem in self.tabcopy:
                            if os.path.isdir(elem):
                                copy_tree(elem, os.path.join(path, os.path.basename(elem)))
                            else:
                                shutil.copy2(elem, path)
                        self.tabcopy.clear()
                    else:
                        showinfo("Copie lancée", "une fois votre copie terminé un message apparaitra")
                        for elem in self.tabcut:
                            if os.path.isdir(elem):
                                copy_tree(elem, os.path.join(path, os.path.basename(elem)))
                                shutil.rmtree(elem)
                            else:
                                shutil.copy2(elem, path)
                                os.remove(elem)
                        self.tabcut.clear()
                    if self.path_access.cget("text") == path:
                        for i in self.right_directory_tree.get_children():
                            self.right_directory_tree.delete(i)
                        for entry in os.listdir(self.path_access.cget('text')):
                            try:
                                path1 = Path(self.path_access.cget('text') + "\\" + entry)
                                self.insertion(self.right_directory_tree, path1, entry)
                            except OSError as e:
                                showerror('Erreur', message=str(e))
                    else:
                        pass
                    showinfo("Succès", "Copie terminée")
                    self.btn_copy.config(state=DISABLED)
                    self.btn_cut.config(state=DISABLED)
                except IndexError:
                    pass
            except PermissionError as e:
                showerror('Erreur', message=str(e))

        thread = threading.Thread(target=paste_process)
        thread.start()
        self.btn_copy.config(state=DISABLED)
        self.btn_cut.config(state=DISABLED)
        self.nb_dir_file.config(text=(str(len(os.listdir(self.path_access.cget('text')))) + " élement(s)"))
        self.btn_paste.config(state=DISABLED)

    # expliquer dans le compte rendu
    def search(self):
        search_directory = self.path_access.cget("text")
        result_path = []

        def search_process():
            def result():
                if len(self.search_bar.get()) != 0:
                    if search_directory:
                        for root, dirs, files in os.walk(search_directory):
                            for dir_name in dirs:
                                if (self.search_bar.get()).lower() in str(dir_name).lower():
                                    path = os.path.join(root, dir_name)
                                    result_path.append(path)

                            for filename in files:
                                if (self.search_bar.get()).lower() in str(filename).lower():
                                    path = os.path.join(root, filename)
                                    result_path.append(path)

            thread = threading.Thread(target=result)
            thread.start()
            thread.join()

            for child in self.right_directory_tree.get_children():
                self.right_directory_tree.delete(child)
            for path in result_path:
                try:
                    path1 = Path(path)
                    self.insertion(self.right_directory_tree, path1, os.path.basename(path))
                except OSError as e:
                    showerror('Erreur', message=str(e))
            self.nb_dir_file.config(text="Nombre d'élements trouvés " + str(len(result_path)) + " élement(s)")

        thread = threading.Thread(target=search_process)
        thread.start()

    def infors(self):
        showinfo("A propos", "Ceci a été réalisé à l'aide d'un module de Python appelé Tkinter")

    def open_with(self):
        racine = self.right_directory_tree.focus()
        if os.path.isfile(self.right_directory_tree.item(racine)['values'][3]):
            try:
                new_path = Path((os.path.splitext(self.right_directory_tree.item(racine)['values'][3]))[0])
                os.rename(os.path.join(self.path_access.cget('text'), self.right_directory_tree.item(racine)['values'][3]), new_path)
                os.startfile(new_path)
                os.rename(new_path, os.path.join(self.path_access.cget('text'), self.right_directory_tree.item(racine)['values'][3]))
            except OSError as e:
                showerror("Erreur", message=str(e))

    def open_new_file_manager(self):
        file_manager = FileManager()
        file_manager.mainloop()
    def add_action_btn(self):
        self.quick_access_doc.config(command=self.on_quick_access_documents)
        self.quick_access_music.config(command=self.on_quick_access_music)
        self.quick_access_desktop.config(command=self.on_quick_access_desktop)
        self.quick_access_videos.config(command=self.on_quick_access_videos)
        self.quick_access_user.config(command=self.on_quick_access_user)
        self.quick_access_images.config(command=self.on_quick_access_images)
        self.quick_access_download.config(command=self.on_quick_access_downloads)

        self.back_btn.config(command=self.go_back)
        self.next_btn.config(command=self.go_next)

        self.btn_new.config(command=self.create_new_dir)
        self.btn_delete.config(command=self.delete)
        self.btn_rename.config(command=self.rename)
        self.refresh_btn.config(command=self.refresh)
        self.btn_property.config(command=self.property)
        self.btn_copy.config(command=self.copy)
        self.btn_cut.config(command=self.cut)
        self.btn_paste.config(command=self.paste)
        self.search_btn.config(command=self.search)


