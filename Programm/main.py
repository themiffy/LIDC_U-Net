from sqlite3 import DatabaseError
import matplotlib.pyplot as plt
import pydicom as dicom
import glob
import numpy as np

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from PIL import Image, ImageTk

from predict import make_prediction
from utilities import structuralize_dataset

global DATA

if __name__ == "__main__":

    def refreshValues():
        try:
            chooseCT['values'] = list(serNumbers)
            
        except:
            print('Choose files first!')

    def study_selected(*args):
        global img
        global canvas

        cur_study = DATA[int(chooseCT.get())]
        array = cur_study[len(DATA[int(chooseCT.get())])//2].pixel_array #первый ключ - серия, второй - номер снимка (средний снимок)
        
        img =  ImageTk.PhotoImage(image=Image.fromarray(array).resize((256,256), resample = Image.NEAREST))
        canvas.create_image(0,0, anchor="nw", image=img)
        study_info.config(text = f'Изображений в серии: {len(cur_study)},\n' +
                                f'Модальность: {cur_study[0].Modality}')


    ######################################## Buttons commands #####################################

    def btn1_com():
        global file
        file = filedialog.askopenfilename(filetypes = (("Jpeg images","*.jpg"),("all files","*.*")))

        pred, image = make_prediction(file)

        alpha = 0.2 # amount of transparency
        f, axarr = plt.subplots(1,3)
        axarr[0].imshow(pred)
        axarr[1].imshow(image)
        axarr[2].imshow(pred * alpha + image * (1-alpha))
        plt.show()

    def openCT():
        filenames = glob.glob(filedialog.askdirectory() + '/*') # выбираю папку и записываю имена файлов

        global ar_dicoms
        global DATA
        global serNumbers
        serNumbers = set()
        ar_dicoms = []

        for file in filenames: # Читаю dicom
            try:
                ar_dicoms.append(dicom.dcmread(file))
                serNumbers.add(ar_dicoms[-1].SeriesNumber)
            except:
                print('\nFile', file.split('/')[-1], 'is not DICOM!\n')

        
        DATA = structuralize_dataset(ar_dicoms, serNumbers)


        # Вывожу инфу в интерфейс
        chooseCT['state'] = 'readonly'
        filecount.config(text = f'Количество файлов {len(ar_dicoms)}\n' + 
                                f'Количество серий {len(serNumbers)}:\n') # Информация о файлах
        

        

        
        

    ###############################################################################################


    master = Tk()
    master.title('Программа')
    master.geometry('500x500')
    
    btn1 = Button(master, text="Загрузить изображение", command = btn1_com, padx=5, pady=5)
    #btn1.grid(column = 0, row = 0)
    btn1.place(x = 350, y = 450)

    btn2 = Button(master, text="   Открыть папку с DICOM    ", command = openCT, padx=5, pady=5)
    #btn2.grid(column = 0, row = 1)
    btn2.place(x = 6, y = 6)

    filecount = Label(master)
    filecount.place(x = 20, y = 35)

    ctlabel = Label(master, text = 'Серия КТ:')
    ctlabel.place(x = 20, y = 80)
    i = 30
    chooseCT = ttk.Combobox(master, values = [], state="disabled", postcommand=refreshValues)
    chooseCT.bind("<<ComboboxSelected>>", study_selected)
    chooseCT.place(x = 5, y = 105)

    spectlabel1 = Label(master, text = 'Серия ОФЭКТ:')
    spectlabel1.place(x = 20, y = 135)

    chooseSPECT = ttk.Combobox(master, values = [], state="disabled")
    #chooseSPECT.bind("<<ComboboxSelected>>", study_selected)
    chooseSPECT.place(x = 5, y = 160)

    spectlabel2 = Label(master, text = 'Файл ОФЭКТ:')
    spectlabel2.place(x = 20, y = 195)

    chooseSPECTfile = ttk.Combobox(master, values = [], state="disabled")
    #chooseSPECT.bind("<<ComboboxSelected>>", study_selected)
    chooseSPECTfile.place(x = 5, y = 220)
    
    

    canvas = Canvas(master, width = 256, height = 256)
    canvas.place(x = 235, y = 5)

    study_info = Label(master)
    study_info.place(x = 265, y = 265)

    master.mainloop()
