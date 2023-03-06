import string
from tkinter import *
from tkinter.ttk import *
import os
import time
from tkinter.ttk import *
from pathlib import Path
from tkinter.messagebox import *
import shutil
import function #module que nous avons crées contenant quatres fonctions l une pour les icones des fichiers en fontions de leurs extensions
                #une pour le calcul de la taille des dossiers , une pour le nombre de fichiers d un dossiers
                #une pour le nombre de dossier d'un dossier (ces 3 dernieres fonctions seront utilises au niveau de la fonctions property(proprieté)
from distutils.dir_util import copy_tree
import threading
from tkinter.simpledialog import *
import send2trash

# personnalisation de la fenetre principale (ajout d un titre a notre fenetre , taille minimale et logo)
tk = Tk()
tk.title("FTBfile")
tk.minsize(1080, 1080)
tk.iconbitmap('images/explorer_personal_icon-icons.com_71977_ico32.ico')

#definition de toutes les images qui seront utiliseqs

img_dir = PhotoImage(file='images/sparklesfolderblank_99348 (1).png')
img_pc = PhotoImage(file='images/Desktop_Acer_43256.png')
img_disk = PhotoImage(file='images/hd_hardware_harddisk_9894.png')
img_open = PhotoImage(file='images/open-file_40455.png')
img_copy = PhotoImage(file='images/Copy_26996.png')
img_copy1 = PhotoImage(file='images/Copy_26996(1).png')
img_paste = PhotoImage(file='images/Paste_26994.png')
img_paste1 = PhotoImage(file='images/Paste_26994(1).png')
img_close = PhotoImage(file='images/exit_closethesession_close_6317(1).png')
img_new_dir = PhotoImage(file='images/new_folder_black_13778 (1).png')
img_move = PhotoImage(file='images/file_move_icon_138617.png')
img_search = PhotoImage(file='images/Search.png')
img_infors = PhotoImage(file='images/information_info_1565.png')
img_cut = PhotoImage(file='images/scissors_icon-icons.com_66285.png')
img_cut1 = PhotoImage(file='images/scissors_icon-icons.com_66285(1).png')
img_next = PhotoImage(file='images/redo-arrow_icon-icons.com_53912.png')
img_back = PhotoImage(file='images/arrow-address-back_icon-icons.com_54065.png')
img_rename = PhotoImage(file='images/gui_rename_icon_157599.png')
img_rename1 = PhotoImage(file='images/gui_rename_icon_157599(1).png')
img_delete = PhotoImage(file='images/document_delete_256_icon-icons.com_75995.png')
img_delete1 = PhotoImage(file='images/document_delete_256_icon-icons.com_75995(1).png')
img_refresh = PhotoImage(file='images/refresh_arrow_1546 (1).png')
img_download = PhotoImage(file='images/downloadfolder_99367.png')
img_document = PhotoImage(file='images/documentediting_editdocuments_text_documentedi_2820.png')
img_videos = PhotoImage(file='images/Video file (1).png')
img_images = PhotoImage(file='images/iPhoto_photo_picture_camera_2661.png')
img_music = PhotoImage(file='images/Library Music.png')
img_desktop = PhotoImage(file='images/Desktop.png')
img_user = PhotoImage(file='images/User (1).png')


# creation barre outils et acces rapide

Framebouton = LabelFrame(tk)
Framebouton.pack(side=TOP, fill=BOTH, padx=5, pady=0)
Frameoutils = LabelFrame(tk)
Frameoutils.pack(side=TOP, fill=X, padx=5, pady=2)
outils = LabelFrame(Framebouton, text='Outils')
outils.grid(row=0, column=0)
copy = Button(outils, text="Copier", image=img_copy, width=55, height=55, compound='top', bg='white', state=DISABLED)
copy.grid(row=0, column=0)
paste = Button(outils, text="Coller", image=img_paste, width=55, height=55, compound='top', bg='white', state=DISABLED)
paste.grid(row=0, column=1)
cut = Button(outils, text="Couper", image=img_cut, width=55, height=55, compound='top', bg='white')
cut.grid(row=0, column=2)
propriete = Button(outils, text="Propriétés", image=img_infors, width=55, height=55, compound='top', bg='white', state=DISABLED)
propriete.grid(row=0, column=6)
new = Button(outils, text="Nouveau", image=img_new_dir, width=55, height=55, compound='top', bg='white', state=DISABLED)
new.grid(row=0, column=4)
delete = Button(outils, text="Supprimer", image=img_delete, width=55, height=55, compound='top', bg='white', state=DISABLED)
delete.grid(row=0, column=5)
rename = Button(outils, text="Renommer", image=img_rename, width=55, height=55, compound='top', bg='white', state=DISABLED)
rename.grid(row=0, column=3)
accesrapide = LabelFrame(Framebouton, text='Accès rapide')
accesrapide.grid(row=0, column=1)
User = Button(accesrapide, image=img_user, text="User", width=55, height=55, compound='top', bg='white')
User.grid(row=0, column=0)
Desktop = Button(accesrapide, image=img_desktop, text="Desktop", width=55, height=55, compound='top', bg='white')
Desktop.grid(row=0, column=1)
Download = Button(accesrapide, image=img_download, text="Download",width=55, height=55,  compound='top', bg='white')
Download.grid(row=0, column=2)
Doc = Button(accesrapide, image=img_document, text="Documents",width=55, height=55, compound='top', bg='white')
Doc.grid(row=0, column=3)
Videos = Button(accesrapide, image=img_videos, text="Videos",width=55, height=55, compound='top', bg='white')
Videos.grid(row=0, column=4)
Music = Button(accesrapide, image=img_music, text="Music",width=55, height=55, compound='top', bg='white')
Music.grid(row=0, column=5)
Images = Button(accesrapide, image=img_images, text="Images",width=55, height=55, compound='top', bg='white')
Images.grid(row=0, column=6)

# creation de la barre contenant le chemin absolu

back = Button(Frameoutils, bg='white', image=img_back, width=20, height=17, state=DISABLED)
back.grid(row=0, column=0)
nextbouton = Button(Frameoutils, bg='white', image=img_next, width=20, height=17, state=DISABLED)
nextbouton.grid(row=0, column=1)
refresh = Button(Frameoutils, bg='white',width=20, height=17, image=img_refresh)
refresh.grid(row=0, column=2)
paneoutils = PanedWindow(Frameoutils, orient=HORIZONTAL, bg='white')
paneoutils.grid(row=0, column=3)
barre_recherche = Entry(Frameoutils, width=80)
chemin_acces = Label(Frameoutils, width=108, bg='white')
paneoutils.add(chemin_acces)
paneoutils.add(barre_recherche)
search = Button(Frameoutils, bg='white', image=img_search, height=17, width=20)
search.grid(row=0, column=4, sticky=SE)

# conteneur des dossiers et fichiers (pane) (il contient l'arborescence de gauche et de droite)

pane = PanedWindow(tk, orient=HORIZONTAL, bg='grey')
panedossiers = PanedWindow(tk, bg='grey')
pane.pack(side=TOP,expand="True", fill=BOTH, padx=5, pady=2)

#il contiendra le nombre d'elements qui sont dans un repertoire il se trouve au fond

FrameBas = LabelFrame(tk)
FrameBas.pack(fill=BOTH, padx=5, pady=0)
Nbre_Dir_File = Label(FrameBas, bg='white')
Nbre_Dir_File.pack(fill=X)

# ajout de panedossiers dans le pane defini ci haut qui contiendra l'arborescence de gauche
pane.add(panedossiers)
#style des arbres
style = Style()
style.theme_use("clam")
style.configure("Treeview")
# creations arbres de gauche et de sa barre de defilement
treescroll = Scrollbar(panedossiers)
treescroll.pack(side=RIGHT, fill=Y)
tree = Treeview(panedossiers, yscrollcommand=treescroll.set)
tree.pack(expand=True, fill=BOTH, side=LEFT)
treescroll.config(command=tree.yview)

# ajout d un titre a notre arbre ainsi qu'une image
tree.heading('#0', text='Ce PC', anchor=W, image=img_pc)

# drive est un tableau contenant toutes les lettres de l'alphabet en lettre majusules
drive = string.ascii_uppercase
# declaration d'un tableau qui contiendra les disk reconnus par la machine
valid_drives = []
# expliquer dans le compte rendu
def AjoutDisk():
    global drive
    global valid_drives
    for each_drive in drive:
        if os.path.exists(each_drive + ":\\"):
            if each_drive + ":\\" in valid_drives:
                pass
            else:
                valid_drives.append(each_drive + ":\\")
                node = tree.insert(parent='', index='end', text=each_drive + ":\\", image=img_disk)
                tree.insert(parent=node, index='end')
    tk.after(5, AjoutDisk)

thread0 = threading.Thread(target=AjoutDisk)
thread0.start()
# expliquer dans le compte rendu
def DeleteDisk():
    global drive
    global valid_drives
    for each_drive in valid_drives:
        if os.path.exists(each_drive):
            pass
        else:
            valid_drives.remove(each_drive)
            for x in tree.get_children():
                if tree.item(x)['text']==each_drive:
                    tree.delete(x)
                else:
                    pass
    tk.after(5, DeleteDisk)

thread1 = threading.Thread(target=DeleteDisk)
thread1.start()

# expliquer dans le compte rendu
def treeDossiers(r):
    racine = tree.selection()
    x = tree.get_children(racine)
    for i in x:
        tree.delete(i)
    parent = tree.parent(racine)
    if parent != '':
        b = os.path.join(tree.item(parent)['text'], tree.item(racine)['text'])
        while parent != '':
            parent = tree.parent(parent)
            b = os.path.join(tree.item(parent)['text'], b)
        chemin_absolu = Path(b)
    else:
        b = tree.item(racine)['text']
        chemin_absolu = Path(b)
    try:
        for entry in os.listdir(chemin_absolu):
            try:
                path1 = Path(b + "\\" + entry)
                if path1.is_dir():
                    try:
                        node = tree.insert(parent=racine, index='end', text=entry, image=img_dir)
                        tree.insert(parent=node, index='end')
                    except OSError as e:
                        showerror(title="Erreur", message=str(e))
            except OSError as e:
                showerror("Erreur", message=str(e))
    except OSError as e:
        showerror("Erreur", message=str(e))
    chemin_acces.config(text=chemin_absolu)

tree.bind("<<TreeviewOpen>>", treeDossiers)

# creation du widget qui contiendra l'arbre de droite
FrameDirFile = LabelFrame(tk, text='Dossiers & Fichiers')
pane.add(FrameDirFile)

#creation arbre de droite et sa barre de defilement
col = ('Modifier', 'Type', 'Taille')
treescroll1 = Scrollbar(FrameDirFile)
treescroll1.pack(side=RIGHT, fill=Y)
tree1 = Treeview(FrameDirFile, columns=col, yscrollcommand=treescroll1.set)
treescroll1.config(command=tree1.yview)

# Ajout des colonnes
tree1.column('#0', minwidth=100, width=200, anchor=W)
tree1.column('Modifier', minwidth=50, width=100 , anchor=W)
tree1.column('Type', minwidth=50, width= 70, anchor=W)
tree1.column('Taille', width=70, anchor=E)

# Donner des titres au colonnes
tree1.heading('#0', text="Nom", anchor=W)
tree1.heading('Modifier', text="Date Modification", anchor=W)
tree1.heading('Type', text="Type", anchor=W)
tree1.heading('Taille', text="Taille", anchor=W)
tree1.pack(expand=True, fill=BOTH, side=LEFT)

# insertion Dossier et fichier
all_img_file =[] # permet d enregistrer le images des fichiers
chemin = [] # ce tableau contiendra des chemins absolu et on l'utilisera dans les fonctions pageback pagenext

# cette fonction permet d inserer des elements dans l'arbre de droite
def insertion(t,path, text):
    if path.is_dir():
        try:
            t.insert(parent='', index=0, text=text,
                     values=[time.ctime(os.path.getmtime(path)), 'Dossier',
                             '', path], image=img_dir)
        except OSError as e:
            showerror("Erreur", message=str(e))
    else:
        try:
            img_file = function.icon(path)
            t.insert(parent='', index='end', text=text,
                     values=[time.ctime(os.path.getmtime(path)), 'Fichier' + (os.path.splitext(path)[1]).upper(),
                             str(os.path.getsize(path)) + ' Byte(s)', path], image=img_file)
            all_img_file.append(img_file)
        except OSError as e:
            showerror("Erreur", message=str(e))

# toutes cette foncions me permettent d acceder rapideement au bureau, a documents, images ,videos.......
def insertionDoc():
    try:
        for x in tree1.get_children():
            tree1.delete(x)
        for entry in os.listdir(os.path.join(Path.home(),'Documents')):
            try:
                path1 = Path(os.path.join(os.path.join(Path.home(),'Documents')), entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror("Erreur", message=str(e))
    except OSError as e:
        showerror("Erreur", message=str(e))
    chemin_acces.config(text=os.path.join(Path.home(),'Documents'))
    back.config(state=NORMAL)
    nextbouton.config(state=NORMAL)
    new.config(state=NORMAL)
    chemin.append(os.path.join(Path.home(),'Documents'))
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))


Doc.config(command=insertionDoc)

def insertionuser():
    try:
        for x in tree1.get_children():
            tree1.delete(x)
        for entry in os.listdir(Path.home()):
            try:
                path1 = Path(os.path.join(Path.home()), entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror("Erreur", message=str(e))
    except OSError as e:
        showerror("Erreur", message=str(e))
    chemin_acces.config(text=Path.home())
    back.config(state=NORMAL)
    nextbouton.config(state=NORMAL)
    new.config(state=NORMAL)
    chemin.append(Path.home())
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))


User.config(command=insertionuser)

def insertionDownload():
    try:
        for x in tree1.get_children():
            tree1.delete(x)
        for entry in os.listdir(os.path.join(Path.home(),'Downloads')):
            try:
                path1 = Path(os.path.join(os.path.join(Path.home(),'Downloads')), entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror("Erreur", message=str(e))
    except OSError as e:
        showerror("Erreur", message=str(e))
    chemin_acces.config(text=os.path.join(Path.home(),'Downloads'))
    back.config(state=NORMAL)
    nextbouton.config(state=NORMAL)
    new.config(state=NORMAL)
    chemin.append(os.path.join(Path.home(),'Downloads'))
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))


Download.config(command=insertionDownload)
def insertionVideos():
    try:
        for x in tree1.get_children():
            tree1.delete(x)
        for entry in os.listdir(os.path.join(Path.home(),'Videos')):
            try:
                path1 = Path(os.path.join(os.path.join(Path.home(),'Videos')), entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror("Erreur", message=str(e))
    except OSError as e:
        showerror("Erreur", message=str(e))
    chemin_acces.config(text=os.path.join(Path.home(),'Videos'))
    back.config(state=NORMAL)
    nextbouton.config(state=NORMAL)
    new.config(state=NORMAL)
    chemin.append(os.path.join(os.path.join(Path.home(),'Videos')))
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))


Videos.config(command=insertionVideos)
def insertionMusic():
    try:
        for x in tree1.get_children():
            tree1.delete(x)
        for entry in os.listdir((os.path.join(Path.home(),'Music'))):
            try:
                path1 = Path(os.path.join(os.path.join(Path.home(),'Music')), entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror("Erreur", message=str(e))
    except OSError as e:
        showerror("Erreur", message=str(e))
    chemin_acces.config(text=os.path.join(Path.home(),'Music'))
    back.config(state=NORMAL)
    nextbouton.config(state=NORMAL)
    new.config(state=NORMAL)
    chemin.append(os.path.join(os.path.join(Path.home(),'Music')))
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))


Music.config(command=insertionMusic)
def insertionImages():
    try:
        for x in tree1.get_children():
            tree1.delete(x)
        for entry in os.listdir((os.path.join(Path.home(),'Pictures'))):
            try:
                path1 = Path(os.path.join(os.path.join(Path.home(),'Pictures')), entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror("Erreur", message=str(e))
    except OSError as e:
        showerror("Erreur", message=str(e))
    chemin_acces.config(text=os.path.join(Path.home(),'Pictures'))
    back.config(state=NORMAL)
    nextbouton.config(state=NORMAL)
    new.config(state=NORMAL)
    chemin.append(os.path.join(Path.home(),'Pictures'))
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))


Images.config(command=insertionImages)

def insertionDesktop():
    try:
        for x in tree1.get_children():
            tree1.delete(x)
        for entry in os.listdir(os.path.join(Path.home(),'Desktop')):
            try:
                path1 = Path(os.path.join(os.path.join(os.path.join(Path.home(),'Desktop')), entry))
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror("Erreur", message=str(e))
    except OSError as e:
        showerror("Erreur", message=str(e))
    chemin_acces.config(text= os.path.join(Path.home(),'Desktop'))
    back.config(state=NORMAL)
    nextbouton.config(state=NORMAL)
    new.config(state=NORMAL)
    chemin.append(os.path.join(Path.home(),'Desktop'))
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))

Desktop.config(command=insertionDesktop)
insertionDesktop()

# expliquer dans le compte rendu

def treeDossiersFichiers(f):
    global k
    k = 0
    global tree1
    for x in tree1.get_children():
        tree1.delete(x)
    racine = tree.selection()
    parent = tree.parent(racine)
    if parent != '':
        b = os.path.join(tree.item(parent)['text'], tree.item(racine)['text'])
        while parent != '':
            parent = tree.parent(parent)
            b = os.path.join(tree.item(parent)['text'], b)
        chemin_absolu = Path(b)
    else:
        b = tree.item(racine)['text']
        chemin_absolu = Path(b)
    try:
        for entry in os.listdir(chemin_absolu):
            try:
                path1 = Path(b + "\\" + entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror("Erreur", message=str(e))
    except OSError as e:
        showerror("Erreur", message=str(e))

    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_absolu))) + " élement(s)"))
    nextbouton.config(state=NORMAL)
    back.config(state=NORMAL)
    new.config(state=NORMAL)

tree.bind("<<TreeviewSelect>>", treeDossiersFichiers)

# ouverture d un fichier ou Dossiers
def openFichiersDossiers(h):
    global chemin
    try:
        racine = tree1.selection()
        b = (tree1.item(racine)['values'])[3]
        chemin_absolu = Path(b)
    except IndexError:
        pass
    if chemin_absolu.is_dir():
        for x in tree1.get_children():
            tree1.delete(x)
        try:
            for entry in os.listdir(chemin_absolu):
                try:
                    path1 = Path(b + "\\" + entry)
                    insertion(tree1, path1, entry,)
                except OSError as e:
                    showerror("Erreur", message=str(e))
        except OSError as e:
                    showerror("Erreur", message=str(e))
        chemin_acces.config(text=chemin_absolu)
        chemin.append(chemin_acces.cget("text"))
        Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_absolu))) + " élement(s)"))
    else:
        try:
            os.startfile(chemin_absolu)
        except OSError as e:
            showerror("Erreur", message=str(e))
    delete.config(state=DISABLED)
    rename.config(state=DISABLED)
    propriete.config(state=DISABLED)
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    back.config(state=NORMAL)

tree1.bind("<<Button-1>>", openFichiersDossiers)
tree1.bind('<KeyPress-Return>',openFichiersDossiers)


# afficher le chemin absolu dans la barre de chemin
def affiche_chemin_absolu(f):
    global chemin
    global chemin1
    racine = tree.selection()
    parent = tree.parent(racine)
    if parent != '':
        a = tree.item(parent)['text']
        b = os.path.join(a, tree.item(racine)['text'])
        while parent != '':
            parent = tree.parent(parent)
            a = tree.item(parent)['text']
            b = os.path.join(a, b)
        chemin_absolu = Path(b)
    else:
        b = tree.item(racine)['text']
        chemin_absolu = Path(b)
    chemin_acces.config(text=chemin_absolu)
    chemin.append(chemin_acces.cget("text"))

tree.bind('<ButtonRelease>', affiche_chemin_absolu)

i = 2 # cet entier nous permettra de nous balader dans le tableau chemin pour realiser des page precedentes page suivant elle sera utiliser par
      #pageback et pagenext
def pageBack():
    nextbouton.config(state=NORMAL)
    global back
    global i
    global img_file
    for x in tree1.get_children():
        tree1.delete(x)
    if len(chemin) - i >= 0:
      try:
        for entry in os.listdir(chemin[len(chemin) - i]):
            try:
                path1 = Path(chemin[len(chemin) - i] + "\\" + entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror('Erreur', message=str(e))
                pass
        b = chemin[len(chemin) - i]
        chemin_absolu = Path(b)
        chemin_acces.config(text=chemin_absolu)
        Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_absolu))) + " élement(s)"))
        i = i + 1
      except IndexError:
         pass
    else:
        back.config(state=DISABLED)
        for entry in os.listdir(chemin_acces.cget('text')):
            try:
                path1 = Path(chemin_acces.cget('text') + "\\" + entry)
                insertion(tree1,path1 , entry)
            except OSError as e:
                showerror('Erreur', message=str(e))
    delete.config(state=DISABLED)
    rename.config(state=DISABLED)
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    propriete.config(state=DISABLED)

back.config(command = pageBack)

def pageNext():
    back.config(state=NORMAL)
    global nextbouton
    global i
    for x in tree1.get_children():
        tree1.delete(x)
    if len(chemin) - i >= -1:
      try:
        for entry in os.listdir(chemin[len(chemin) - i+2]):
            try:
                path1 = Path(chemin[len(chemin) - i+2] + "\\" + entry)
                insertion(tree1, path1, entry)
            except OSError  as e:
                showerror('Erreur', message=str(e))
        b = chemin[len(chemin) - i+2]
        chemin_absolu = Path(b)
        chemin_acces.config(text=chemin_absolu)
        Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_absolu))) + " élement(s)"))
        i = i - 1
      except IndexError:
          nextbouton.config(state=DISABLED)
          for entry in os.listdir(chemin_acces.cget('text')):
              try:
                  path1 = Path(chemin_acces.cget('text') + "\\" + entry)
                  insertion(tree1, path1, entry)
              except OSError as e:
                  showerror('Erreur', message=str(e))
          pass
    delete.config(state=DISABLED)
    rename.config(state=DISABLED)
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    propriete.config(state=DISABLED)

nextbouton.config(command = pageNext)

def pageBack2(event):
    nextbouton.config(state=NORMAL)
    global back
    global i
    global img_file
    for x in tree1.get_children():
        tree1.delete(x)
    if len(chemin) - i >= 0:
        try:
            for entry in os.listdir(chemin[len(chemin) - i]):
                try:
                    path1 = Path(chemin[len(chemin) - i] + "\\" + entry)
                    insertion(tree1, path1, entry)
                except OSError as e:
                    showerror('Erreur', message=str(e))
                    pass
            b = chemin[len(chemin) - i]
            chemin_absolu = Path(b)
            chemin_acces.config(text=chemin_absolu)
            Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_absolu))) + " élement(s)"))
            i = i + 1
        except IndexError:
            pass
    else:
        back.config(state=DISABLED)
        for entry in os.listdir(chemin_acces.cget('text')):
            try:
                path1 = Path(chemin_acces.cget('text') + "\\" + entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror('Erreur', message=str(e))
    delete.config(state=DISABLED)
    rename.config(state=DISABLED)
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    propriete.config(state=DISABLED)

tk.bind('<KeyPress-BackSpace>', pageBack2)

#expliquez dans le compte rendu
def NewDir():
    try:
        name = askstring("Creation nouveau dossier"," Entrez le nom du nouveau dossier")
        try:
            path = os.path.join(chemin_acces.cget('text'), name)
            os.mkdir(path)
        except TypeError:
            pass
    except OSError as e:
        showerror('Erreur', message=str(e))
    for x in tree1.get_children():
        tree1.delete(x)
    for entry in os.listdir(chemin_acces.cget('text')):
        try:
            path1 = Path(chemin_acces.cget('text')+"\\"+entry)
            insertion(tree1, path1, entry)
        except OSError as e:
            showerror('Erreur', message=str(e))
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))
new.config(command=NewDir)

def NewDir2(e):
    try:
        name = askstring("Creation nouveau dossier", " Entrez le nom du nouveau dossier")
        try:
            path = os.path.join(chemin_acces.cget('text') + name)
            os.mkdir(path)
        except TypeError:
            pass
    except OSError as e:
        showerror('Erreur', message=str(e))
    for x in tree1.get_children():
        tree1.delete(x)
    for entry in os.listdir(chemin_acces.cget('text')):
        try:
            path1 = Path(chemin_acces.cget('text') + "\\" + entry)
            insertion(tree1, path1, entry)
        except OSError as e:
            showerror('Erreur', message=str(e))
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))

tk.bind('<Shift-KeyPress-N>', NewDir2)

#Cette fonction permet d'activer les boutons
def ActiveButton(e):
    delete.config(state=NORMAL)
    rename.config(state=NORMAL)
    propriete.config(state=NORMAL)
    copy.config(state=NORMAL)
    cut.config(state=NORMAL)

tree1.bind('<<TreeviewSelect>>', ActiveButton)

#Cette fonction permet de desactiver les boutons
def DesactivedButton(e):
    delete.config(state=DISABLED)
    rename.config(state=DISABLED)
    propriete.config(state=DISABLED)
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)

tree.bind('<Button-1>', DesactivedButton)

#cette fonction affiche le nombres d'elements contenu dans le repertoire ou on se trouve elle s'execute apres chaque 5ms
def selection():
    select = tree1.selection()
    if select:
        Nbre_Dir_File.config(text=str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)   " + str(
            len(select)) + " élement(s) selectionné(s) ")
    else:
        pass
    tk.after(5, selection)
selection()

#expliquez dans le compte rendu
def Delete():
    S=0
    # Je dois faire la corbeille
    try:
        select = tree1.selection()
        for x in select:
            if os.path.isdir((tree1.item(x)['values'])[3]):
                S+=function.folder_size((tree1.item(x)['values'])[3])
            else:
                S += os.path.getsize((tree1.item(x)['values'])[3])
        if S <= 2147483648:
            if askyesno("Notice",
                    "ces dossiers et/ou fichiers seront envoyés vers la corbeille voulez vous continuer?"):
                for x in select:
                    try:
                        send2trash.send2trash((tree1.item(x)['values'])[3])
                    except OSError as e:
                        showerror("Erreur", message=str(e))
        else:
            if askyesno("Notice",
                    "ces dossiers et/ou fichiers seront supprimé definitivement voulez vous vraiment le supprimer?"):
                for x in select:
                    path = (tree1.item(x)['values'])[3]
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
        for x in tree1.get_children():
            tree1.delete(x)
        for entry in os.listdir(chemin_acces.cget('text')):
            try:
                path1 = Path(chemin_acces.cget('text') + "\\" + entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror('Erreur', message=str(e))
    except IndexError:
       pass
    delete.config(state=DISABLED)
    rename.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))

delete.config(command=Delete)

def Delete2(event):
    S = 0
    # Je dois faire la corbeille
    try:
        select = tree1.selection()
        for x in select:
            if os.path.isdir((tree1.item(x)['values'])[3]):
                S += function.folder_size((tree1.item(x)['values'])[3])
            else:
                S += os.path.getsize((tree1.item(x)['values'])[3])
        if S <= 2147483648:
            if askyesno("Notice",
                        "ces dossiers et/ou fichiers seront envoyés vers la corbeille voulez vous continuer?"):
                for x in select:
                    try:
                        send2trash.send2trash((tree1.item(x)['values'])[3])
                    except OSError as e:
                        showerror("Erreur", message=str(e))
        else:
            if askyesno("Notice",
                        "ces dossiers et/ou fichiers seront supprimé definitivement voulez vous vraiment le supprimer?"):
                for x in select:
                    path = (tree1.item(x)['values'])[3]
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
        for x in tree1.get_children():
            tree1.delete(x)
        for entry in os.listdir(chemin_acces.cget('text')):
            try:
                path1 = Path(chemin_acces.cget('text') + "\\" + entry)
                insertion(tree1, path1, entry)
            except OSError as e:
                showerror('Erreur', message=str(e))
    except IndexError:
        pass

    delete.config(state=DISABLED)
    rename.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))

tree1.bind('<Delete>', Delete2)

#expliquez dans le compte rendu
def Rename():
    racine = tree1.focus()
    path = (tree1.item(racine)['values'])[3]
    new_name = askstring("renommer", "Entrez le nouveau nom")
    try:
        if os.path.isdir(path):
            try:
                os.rename(path, os.path.join(chemin_acces.cget("text"), new_name))
            except TypeError:
                pass
        else:
            try:
                os.rename(path,
                          os.path.join(chemin_acces.cget("text"), new_name + (os.path.splitext(path))[1]))
            except TypeError:
                pass
    except OSError as e:
        showerror("Erreur", message=str(e))
    for x in tree1.get_children():
        tree1.delete(x)
    for entry in os.listdir(chemin_acces.cget('text')):
        try:
            path1 = Path(chemin_acces.cget('text') + "\\" + entry)
            insertion(tree1, path1, entry)
        except OSError as e:
            showerror('Erreur', message=str(e))
    rename.config(state=DISABLED)
    delete.config(state=DISABLED)

rename.config(command=Rename)

# cette fonction a pour but de d'actualiser notre arbre de droite
#il peut arriver qu'on crée un nouveau fichier ou dossier avec l explorateur de Windows cela ne sera pas directement afficher dans notre arbre droite
#pour cela nous devons appuyer sur refresh pour actualiser
def Refresh():
    global chemin_acces
    for x in tree1.get_children():
        tree1.delete(x)
    try:
        for entry in os.listdir(chemin_acces.cget("text")):
            try:
                path1 = Path(chemin_acces.cget("text") + "\\" + entry)
                insertion(tree1, path1, entry,)
            except OSError as e:
                showerror("Erreur", message=str(e))
    except OSError as e:
                showerror("Erreur", message=str(e))
    delete.config(state=DISABLED)
    rename.config(state=DISABLED)
    propriete.config(state=DISABLED)
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))

refresh.config(command=Refresh)

#expliquer dans le compte rendu
def property():
    def processProperty():
        racine = tree1.focus()
        parent = tree1.parent(racine)
        if racine:
            path = Path((tree1.item(racine)['values'])[3])

            P = Tk()
            nom = Label(P, text="Nom :")
            nom.grid(column=0, row=0, sticky=W)
            nom1 = Label(P, text=tree1.item(racine)['text'])
            nom1.grid(column=1, row=0, sticky=W)
            type = Label(P, text="Type :")
            type.grid(column=0, row=2, sticky=W)
            if path.is_dir():
                type1 = Label(P, text="Dossier")
                type1.grid(column=1, row=2, sticky=W)
            else:
                type1 = Label(P, text="Fichier" + (os.path.splitext(path)[1]).upper())
                type1.grid(column=1, row=2, sticky=W)
            ch = Label(P, text="Chemin absolu :")
            ch.grid(column=0, row=3, sticky=W)
            ch1 = Label(P, text=(tree1.item(racine)['values'])[3])
            ch1.grid(column=1, row=3, sticky=W)
            size = Label(P, text="Taille :")
            size.grid(column=0, row=4, sticky=W)
            if path.is_dir():
                size1 = Label(P, text=str(function.folder_size(path)) + ' Byte(s)')
            else:
                size1 = Label(P, text=str(os.path.getsize(path)) + ' Byte(s)')
            size1.grid(column=1, row=4, sticky=W)
            if path.is_dir():
                contenu = Label(P, text="Contenu :")
                contenu.grid(column=0, row=5, sticky=W)
                contenu1 = Label(P, text=str(function.nb_Dir(path)) + ' Dossier(s)' + ' ,' + ' ' + str(
                    function.nb_file(path)) + ' Fichier(s)')
                contenu1.grid(column=1, row=5, sticky=W)
            Create = Label(P, text="Crée le:")
            Create.grid(column=0, row=6, sticky=W)
            Create1 = Label(P, text=time.ctime(os.path.getctime(path)))
            Create1.grid(column=1, row=6, sticky=W)
            Modify = Label(P, text="Modifié le:")
            Modify.grid(column=0, row=7, sticky=W)
            Modify1 = Label(P, text=time.ctime(os.path.getmtime(path)))
            Modify1.grid(column=1, row=7, sticky=W)
            ok = Button(P, text="OK", width=15, command=P.destroy)
            ok.grid(column=2, row=8)
            P.title("propriétés")
            P.minsize(395, 50)
            P.iconbitmap('images/explorer_personal_icon-icons.com_71977_ico32.ico')
            propriete.config(state=DISABLED)
            rename.config(state=DISABLED)
            delete.config(state=DISABLED)
            P.mainloop()
        else:
            pass
    Thread = threading.Thread(target=processProperty)
    Thread.start()

propriete.config(command=property)

tabcopy = [] #ce tableau contiendra les chemins absolus des elements sur lequel on a clique
tabcut = [] #ce tableau contiendra les chemins absolus des elements sur lequel on a clique

#expliquer dans le compte rendu
def copie():
    global tabcopy
    for x in tree1.selection():
        try:
            path = (tree1.item(x)['values'])[3]
            tabcopy.append(path)
        except IndexError:
            pass
    tabcut.clear()
    paste.config(state=NORMAL)
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)

copy.config(command=copie)

def copie2(event):
    global tabcopy
    for x in tree1.selection():
        try:
            path = (tree1.item(x)['values'])[3]
            tabcopy.append(path)
        except IndexError:
            pass
    tabcut.clear()
    paste.config(state=NORMAL)
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)

tree1.bind('<Shift-KeyPress-C>',copie2)

#expliquer dans le compte rendu
def couper():
    global tabcut
    for x in tree1.selection():
        try:
            path = (tree1.item(x)['values'])[3]
            tabcut.append(path)
        except IndexError:
            pass
    tabcopy.clear()
    paste.config(state=NORMAL)
    cut.config(state=DISABLED)
    copy.config(state=DISABLED)

cut.config(command=couper)

def couper2(event):
    global tabcut
    for x in tree1.selection():
        try:
            path = (tree1.item(x)['values'])[3]
            tabcut.append(path)
        except IndexError:
            pass
    tabcopy.clear()
    paste.config(state=NORMAL)
    cut.config(state=DISABLED)
    copy.config(state=DISABLED)

tree1.bind('<Shift-KeyPress-X>',couper2)

#expliquer dans le compte rendu
def coller():
    path = chemin_acces.cget("text")
    def processColler():
        try:
            try:
                if len(tabcopy) != 0:
                    showinfo("Copie lancée", "une fois votre copie terminé un message apparaitra")
                    for x in tabcopy:
                        if os.path.isdir(x):
                            copy_tree(x, os.path.join(path, os.path.basename(x)))
                        else:
                            shutil.copy2(x, path)
                    tabcopy.clear()
                else:
                    showinfo("Copie lancée", "une fois votre copie terminé un message apparaitra")
                    for x in tabcut:
                        if os.path.isdir(x):
                            copy_tree(x, os.path.join(path, os.path.basename(x)))
                            shutil.rmtree(x)
                        else:
                            shutil.copy2(x, path)
                            os.remove(x)
                    tabcut.clear()
                if chemin_acces.cget("text") == path:
                    for i in tree1.get_children():
                        tree1.delete(i)
                    for entry in os.listdir(chemin_acces.cget('text')):
                        try:
                            path1 = Path(chemin_acces.cget('text') + "\\" + entry)
                            insertion(tree1, path1, entry)
                        except OSError as e:
                            showerror('Erreur', message=str(e))
                else:
                    pass
                showinfo("Succès", "Copie terminée")
                copy.config(state=DISABLED)
                cut.config(state=DISABLED)
            except IndexError:
                pass
        except PermissionError as e:
            showerror('Erreur', message=str(e))
    Thread = threading.Thread(target=processColler)
    Thread.start()
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))
    paste.config(state=DISABLED)

paste.config(command=coller)

def coller2(event):
    path = chemin_acces.cget("text")

    def processColler():
        try:
            try:
                if len(tabcopy) != 0:
                    showinfo("Copie lancée", "une fois votre copie terminé un message apparaitra")
                    for x in tabcopy:
                        if os.path.isdir(x):
                            copy_tree(x, os.path.join(path, os.path.basename(x)))
                        else:
                            shutil.copy2(x, path)
                    tabcopy.clear()
                else:
                    showinfo("Copie lancée", "une fois votre copie terminé un message apparaitra")
                    for x in tabcut:
                        if os.path.isdir(x):
                            copy_tree(x, os.path.join(path, os.path.basename(x)))
                            shutil.rmtree(x)
                        else:
                            shutil.copy2(x, path)
                            os.remove(x)
                    tabcut.clear()
                if chemin_acces.cget("text") == path:
                    for i in tree1.get_children():
                        tree1.delete(i)
                    for entry in os.listdir(chemin_acces.cget('text')):
                        try:
                            path1 = Path(chemin_acces.cget('text') + "\\" + entry)
                            insertion(tree1, path1, entry)
                        except OSError as e:
                            showerror('Erreur', message=str(e))
                else:
                    pass
                showinfo("Succès", "Copie terminée")
                copy.config(state=DISABLED)
                cut.config(state=DISABLED)
            except IndexError:
                pass
        except PermissionError as e:
            showerror('Erreur', message=str(e))
    Thread = threading.Thread(target=processColler)
    Thread.start()
    copy.config(state=DISABLED)
    cut.config(state=DISABLED)
    Nbre_Dir_File.config(text=(str(len(os.listdir(chemin_acces.cget('text')))) + " élement(s)"))
    paste.config(state=DISABLED)

tk.bind('<Shift-KeyPress-V>',coller2)

#expliquer dans le compte rendu
def recherche():
    search_directory = chemin_acces.cget("text")
    result_path = []
    def processRecherche():
        def Result():
            if len(barre_recherche.get()) != 0:
                if search_directory:
                    for root, dirs, files in os.walk(search_directory):
                        for dir_name in dirs:
                            if (barre_recherche.get()).lower() in str(dir_name).lower():
                                path = os.path.join(root, dir_name)
                                result_path.append(path)

                        for filename in files:
                            if (barre_recherche.get()).lower() in str(filename).lower():
                                path = os.path.join(root, filename)
                                result_path.append(path)
        Thread = threading.Thread(target=Result)
        Thread.start()
        Thread.join()

        for i in tree1.get_children():
            tree1.delete(i)
        for entry in result_path:
            try:
                path1 = Path(entry)
                insertion(tree1, path1, os.path.basename(entry))
            except OSError as e:
                showerror('Erreur', message=str(e))
        Nbre_Dir_File.config(text="Nombre d'élements trouvés " + str(len(result_path)) + " élement(s)")
    Thread = threading.Thread(target=processRecherche)
    Thread.start()

search.config(command=recherche)

def ouvrir_avec():
    racine = tree1.focus()
    if os.path.isfile(tree1.item(racine)['values'][3]):
        try:
            new_path = Path((os.path.splitext(tree1.item(racine)['values'][3]))[0])
            os.rename(os.path.join(chemin_acces.cget('text'), tree1.item(racine)['values'][3]), new_path)
            os.startfile(new_path)
            os.rename(new_path, os.path.join(chemin_acces.cget('text'), tree1.item(racine)['values'][3]))
        except OSError as e:
            showerror("Erreur", message=str(e))
def infors():
    showinfo("A propos","Ceci a été réalisé à l'aide d'un module de Python appelé Tkinter")

#Menu
menubar = Menu(tk)
menuFichier = Menu(menubar, tearoff=0)
'''menuFichier.add_command(label="Ouvrir", image=img_open, compound="left", accelerator="Crtl+O")
menuFichier.add_separator()'''
menuFichier.add_command(label="Fermer", image=img_close, compound="left", command=quit)
menubar.add_cascade(label="Fichier", menu=menuFichier)
menuEdition = Menu(menubar, tearoff=0)
menuEdition.add_command(label="Copier", image=img_copy1, compound="left", accelerator="Shift+C", command=copie)
menuEdition.add_separator()
menuEdition.add_command(label="Coller", image=img_paste1, compound="left", accelerator="Shift+V", command=coller)
menuEdition.add_separator()
menuEdition.add_command(label="Couper", image=img_cut1, compound="left", accelerator="Shift+X", command=couper)
menuEdition.add_separator()
menuEdition.add_command(label="Renommer", image=img_rename1, compound="left", command=Rename)
menuEdition.add_separator()
menuEdition.add_command(label="Supprimer", image=img_delete1, compound="left", command=Delete)
menubar.add_cascade(label="Edition", menu=menuEdition)
menuAide = Menu(menubar, tearoff=0)
menuAide.add_command(label="A propos", command=infors)
menubar.add_cascade(label="Aide", menu=menuAide)
tk.config(menu=menubar)

#menu contextuel

menuContextuel = Menu(tk, tearoff=0)
menuContextuel.add_command(label="Ouvrir avec", command=ouvrir_avec)
menuContextuel.add_separator()
menuContextuel.add_command(label="Copier", command=copie)
menuContextuel.add_separator()
menuContextuel.add_command(label="Coller", command=coller)
menuContextuel.add_separator()
menuContextuel.add_command(label="Couper", command=couper)
menuContextuel.add_separator()
menuContextuel.add_command(label="Renommer", command=Rename)
menuContextuel.add_separator()
menuContextuel.add_command(label="Supprimer", command=Delete)
menuContextuel.add_separator()
menuContextuel.add_command(label="Propriétés", command=property)

menuContextuel2=Menu(tk, tearoff=0)
menuContextuel2.add_command(label="Nouveau Dossier", command=NewDir)

menuContextuel3=Menu(tk, tearoff=0)
menuContextuel3.add_command(label="Nouveau Dossier", command=NewDir)
menuContextuel3.add_separator()
menuContextuel3.add_command(label="Coller", command=coller)

#Cette fonction permettra d'afficher le menu contextuel une fois le bouton droit presse
def affiche(e):
    select = tree1.identify_row(e.y)
    if select:
        tree1.selection_set(select)
        menuContextuel.post(tk.winfo_pointerx(), tk.winfo_pointery())
    else:
        if chemin_acces.cget("text")=='':
            pass
        elif len(tabcopy) >= 1 or len(tabcut) >=1:
            menuContextuel3.post(tk.winfo_pointerx(), tk.winfo_pointery())
        else:
            menuContextuel2.post(tk.winfo_pointerx(), tk.winfo_pointery())

tree1.bind('<Button-3>', affiche)

# affichage de la fenetre
tk.mainloop()