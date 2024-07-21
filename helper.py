import os
from tkinter import PhotoImage
from pathlib import Path


def define_icon(p, master):
    if (os.path.splitext(p))[1] == ".docx" or (os.path.splitext(p))[1] == ".doc" \
            or (os.path.splitext(p))[1] == ".DOCX" or (os.path.splitext(p))[1] == ".DOC":
        img = PhotoImage(file='images/Word_2013_23473 (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".pdf" or (os.path.splitext(p))[1] == ".PDF":
        img = PhotoImage(file='images/adobe_pdf_document_14979 (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".djvu":
        img = PhotoImage(file='images/4202108browsereedgelogo-115709_115592 (1).png')
        return img
    if (os.path.splitext(p))[1] == ".mp4" or (os.path.splitext(p))[1] == ".mkv" or (os.path.splitext(p))[1] == ".avi" \
            or (os.path.splitext(p))[1] == ".MP4" or (os.path.splitext(p))[1] == ".MKV":
        img = PhotoImage(file='images/Videos_31092 (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".xlsx" or (os.path.splitext(p))[1] == ".csv":
        img = PhotoImage(file='images/Excel_2013_23480 (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".png" or (os.path.splitext(p))[1] == ".jpeg" or (os.path.splitext(p))[1] == ".gif" \
            or (os.path.splitext(p))[1] == ".ico" or (os.path.splitext(p))[1] == ".jpg":
        img = PhotoImage(file='images/picture_photo_image_icon_131252.png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".lnk" or (os.path.splitext(p))[1] == ".LNK":
        img = PhotoImage(file='images/shortcut_23045 (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".txt":
        img = PhotoImage(file='images/Text_edit_35243 (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".mp3" or (os.path.splitext(p))[1] == ".m4a":
        img = PhotoImage(file='images/iconfinder-musicmelodysoundaudio36-4105545_113821 (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".iso":
        img = PhotoImage(file='images/61.png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".rar" or (os.path.splitext(p))[1] == ".zip" or (os.path.splitext(p))[1] == ".7z":
        img = PhotoImage(file='images/winrar_14662.png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".exe":
        img = PhotoImage(file='images/Programs (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".pptx" or (os.path.splitext(p))[1] == ".ppt":
        img = PhotoImage(file='images/PowerPoint_2013_23479 (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".pub":
        img = PhotoImage(file='images/Publisher_2013_23475 (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".dll":
        img = PhotoImage(file='images/dll (1).png', master=master)
        return img
    if (os.path.splitext(p))[1] == ".torrent":
        img = PhotoImage(file='images/torrent_icon-icons.com_72051 (1).png', master=master)
        return img
    else:
        img = PhotoImage(file='images/Blank (1).png', master=master)
        return img


def folder_size(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            try:
                total += entry.stat().st_size
            except OSError:
                pass
        elif entry.is_dir():
            try:
                total += folder_size(entry.path)
            except OSError:
                pass

    return total


def nb_file(path):
    nb = 0
    try:
        for file in os.listdir(path):
            path1 = Path(os.path.join(path, file))
            if path1.is_file():
                nb = nb + 1
            else:
                nb = nb + nb_file(path1)
    except OSError:
        pass
    return nb


def nb_dir(path):
    nb = 0
    for elem in os.listdir(path):
        path1 = Path(os.path.join(path, elem))
        try:
            if path1.is_dir():
                nb = nb + nb_dir(path1) + 1
        except OSError:
            pass
    return nb
