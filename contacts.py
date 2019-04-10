from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import pickle
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import os
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import Global
import numpy as np

"""Dichiarazione della pagina principale"""


class mainScreen(Screen):

    def __init__(self, **kwargs):
        super(mainScreen, self).__init__(**kwargs)

    def on_enter(self):

        # Pulisco i widget della pagina e poi li riaggiungo, in modo tale da evitare conflitti negli elementi
        self.clear_widgets()
        self.add_widget(self.ids.action)
        self.add_widget(self.ids.dg2)
        self.add_widget(self.ids.dg1)

        # Se la rubrica non e' vuota
        if os.path.getsize(Global.contacts_filename) > 0:
            pkl_file = open(Global.contacts_filename, 'rb')
            mydict = pickle.load(pkl_file)

            # Definisco il layout della pagina principale per quanto riguarda i contatti
            layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
            layout.bind(minimum_height=layout.setter('height'))
            layoutbtn = GridLayout(cols=5, spacing=10, size_hint_y=None)

            txt = dict(mydict)

            # Se e' stato settato l'ordinamento secondo un campo
            if Global.FIELD != "":

                # Prendo gli indici in base al tipo di ordinamento
                if Global.SORT == "asc":
                    order = np.argsort(txt.get(Global.FIELD))
                    txt.get(Global.FIELD).sort()

                else:

                    order = np.argsort(txt.get(Global.FIELD))[::-1][:len(txt.get(Global.FIELD))]
                    txt.get(Global.FIELD).sort(reverse=True)

                indexes = ["name", "surname", "email", "phone"]

                # Utilizzo gli indici trovati precedentemente per ordinare i campi rimanenti
                for z in indexes:
                    if Global.FIELD != z:
                        txt[z] = [txt[z][i] for i in order]

            # Estraggo i contatti e li appendo al layout
            for i in range(0, len(mydict["name"])):
                name = str(txt.get("name")[i])
                surname = str(txt.get("surname")[i])
                email = str(txt.get("email")[i])
                phone = str(txt.get("phone")[i])

                name = Label(text=name)
                name2 = Label(text=surname)
                name3 = Label(text=email)
                name4 = Label(text=phone)

                layoutbtn.add_widget(name)
                layoutbtn.add_widget(name2)
                layoutbtn.add_widget(name3)
                layoutbtn.add_widget(name4)

                btn = ImageButtonArrow(id=email, source='images/right-arrow.png')

                layoutbtn.add_widget(btn)

            # Il layout dei contatti verra' attaccato ad una scrollview per facilitarne la visualizzazione
            root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height),
                              pos_hint={'top': 0.50 + self.size_hint[1] / 5})

            self.add_widget(root)
            layout.add_widget(layoutbtn)
            root.add_widget(layout)

    def popup(self, obj):

        popup = Popup(title=obj.text,
                      size_hint=(None, None), size=(300, 300))
        popup.open()


# Bottone per ordinare dal basso all'alto.

class ImageButtonOrderAsc(ButtonBehavior, Image):

    # Funzione che viene generata alla pressione del bottone
    def on_press(self):
        # Layout generato dinamicamente che diventera' il contenuto del Pop up
        layout = GridLayout(cols=1, padding=10)
        label = Label(text="Select field")
        btnName = Button(text='name')
        btnSurname = Button(text='surname')
        btnEmail = Button(text='email')
        btnPhone = Button(text='phone')

        # Aggiungo i bottoni al layout principale
        layout.add_widget(label)
        layout.add_widget(btnName)
        layout.add_widget(btnSurname)
        layout.add_widget(btnEmail)
        layout.add_widget(btnPhone)

        # A questo punto integro il layout nel popup
        popup = Popup(title="Order Ascendent",
                      content=layout,
                      size_hint=(None, None), size=(300, 300))

        popup.open()

        """Per ciascun possibile bottone con il valore per il quale e' possibile ordinare, andro' a fare il binding di due funzioni,
        una per far chiudere il popup, e un'altra per settare il valore globale del modo in cui vengono ordinati i valori, e secondo
        quale campo. In questo modo, l'ordinamento persistera' all'interno dell'applicazione fino alla chiusura
        """

        btnName.bind(on_press=ImageButtonOrderAsc.sortBy)
        btnName.bind(on_press=popup.dismiss)

        btnSurname.bind(on_press=ImageButtonOrderAsc.sortBy)
        btnSurname.bind(on_press=popup.dismiss)

        btnEmail.bind(on_press=ImageButtonOrderAsc.sortBy)
        btnEmail.bind(on_press=popup.dismiss)

        btnPhone.bind(on_press=ImageButtonOrderAsc.sortBy)
        btnPhone.bind(on_press=popup.dismiss)

    def sortBy(self):
        Global.SORT = "asc"
        Global.FIELD = self.text

        mainScreen.on_enter(Global.sm.current_screen)


# Ragionamenti analoghi valgano per il bottone relativo all'ordinamento reverse

class ImageButtonOrderDesc(ButtonBehavior, Image):

    def on_press(self):
        layout = GridLayout(cols=1, padding=10)
        label = Label(text="Select field")
        btnName = Button(text='name')
        btnSurname = Button(text='surname')
        btnEmail = Button(text='email')
        btnPhone = Button(text='phone')

        layout.add_widget(label)
        layout.add_widget(btnName)
        layout.add_widget(btnSurname)
        layout.add_widget(btnEmail)
        layout.add_widget(btnPhone)

        popup = Popup(title="Order Descendent",
                      content=layout,
                      size_hint=(None, None), size=(300, 300))

        popup.open()
        btnName.bind(on_press=ImageButtonOrderDesc.sortBy)
        btnName.bind(on_press=popup.dismiss)

        btnSurname.bind(on_press=ImageButtonOrderDesc.sortBy)
        btnSurname.bind(on_press=popup.dismiss)

        btnEmail.bind(on_press=ImageButtonOrderDesc.sortBy)
        btnEmail.bind(on_press=popup.dismiss)

        btnPhone.bind(on_press=ImageButtonOrderDesc.sortBy)
        btnPhone.bind(on_press=popup.dismiss)

    def sortBy(self):
        Global.SORT = "desc"
        Global.FIELD = self.text

        mainScreen.on_enter(Global.sm.current_screen)


""" Questo bottone invece viene generato per ogni riga estratta dal file dei contatti. I bottoni saranno
generati dinamicamente nella pagina di home. Ciascuno avra' come id l'email relativa alla riga, quindi quello che
vado a fare e' settare una variabile di applicazione EMAIL che verra' successivamente usata per mostrare le informazioni di
contatto nella pagina di vista.
"""


class ImageButtonArrow(ButtonBehavior, Image):

    def on_press(self):
        Global.EMAIL = self.id
        Global.sm.current = 'view'
