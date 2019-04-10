from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
import pickle
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import os
import Global
from contacts import ImageButtonArrow

"""
EXTRA:
Pagina relativa alla ricerca dei contatti. Permette di cercare in base a una delle variabili di contatto.
"""


class searchContact(Screen):
    def __init__(self, **kwargs):
        super(searchContact, self).__init__(**kwargs)

    def search(self):
        # Resetto gli elementi grafici
        self.clear_widgets()
        self.add_widget(self.ids.action)
        self.add_widget(self.ids.dg1)
        self.add_widget(self.ids.dg2)
        self.add_widget(self.ids.dg3)
        self.add_widget(self.ids.searchvalue)
        self.add_widget(self.ids.btn)

        # Controllo quale checkbox e' attiva
        if self.ids.chk_name.active:
            filter = "name"
        elif self.ids.chk_surname.active:
            filter = "surname"
        elif self.ids.chk_email.active:
            filter = "email"
        elif self.ids.chk_phone.active:
            filter = "phone"
        else:
            filter = "name"

        # Estraggo il valore della ricerca
        value = self.ids.searchvalue.text

        # Faccio lo stesso procedimento della pagina di vista dei contatti nella pagina principale
        if os.path.getsize(Global.contacts_filename) > 0:
            pkl_file = open(Global.contacts_filename, 'rb')
            mydict = pickle.load(pkl_file)

            txt = dict(mydict)

            layoutbtn = GridLayout(cols=5, spacing=10, size_hint_y=None)

            for i in range(0, len(mydict["name"])):
                # Cerchiamo le stringhe tramite il metodo find(), ovvero guardando le substringhe, e non rendiamo la ricerca case sensitive
                if (str(txt.get(filter)[i]).lower()).find(value.lower()) != -1:
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

                    # btn.bind(on_press=self.popup)
                    layoutbtn.add_widget(btn)

            root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height),
                              pos_hint={'top': 0.25 + self.size_hint[1] / 5})

            self.add_widget(root)
            root.add_widget(layoutbtn)
