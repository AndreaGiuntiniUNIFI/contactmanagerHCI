from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import pickle
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import weakref
import os
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import Global


""" Questo bottone serve per eliminare un contatto dalla rubrica. L'id del bottone sara'
relativo all'indice del contatto visualizzato, che rende l'eliminazione immediata"""

class ImageButtonDelete(ButtonBehavior, Image):
    def on_press(self):
        i = int(self.id)
        if os.path.getsize(Global.contacts_filename) > 0:
            pkl_file = open(Global.contacts_filename, 'rb')
            mydict = pickle.load(pkl_file)

            del mydict.get("email")[i]
            del mydict.get("name")[i]
            del mydict.get("surname")[i]
            del mydict.get("phone")[i]
            del mydict.get("notes")[i]

            output = open(Global.contacts_filename, 'wb')
            pickle.dump(mydict, output)
            output.close()
            Global.sm.current = 'main'


""" Questo bottone permette di modificare le informazioni di contatto. In modo simile al bottone per l'eliminazione,
vine passato l'indice sul quale modificare i dati"""


class ImageButtonEdit(ButtonBehavior, Image):

    def on_press(self):
        if os.path.getsize(Global.contacts_filename) > 0:
            pkl_file = open(Global.contacts_filename, 'rb')
            mydict = pickle.load(pkl_file)

            i = int(self.id)

            mydict["email"][i] = Global.sm.current_screen.ids.email.text
            mydict["name"][i] = Global.sm.current_screen.ids.name.text
            mydict["surname"][i] = Global.sm.current_screen.ids.surname.text
            mydict["phone"][i] = Global.sm.current_screen.ids.phone.text

            output = open(Global.contacts_filename, 'wb')
            pickle.dump(mydict, output)
            output.close()
            Global.sm.current = 'main'


"""Questo bottone permette di visualizzare le note di un contatto, serve con lo stesso meccanisco utilizzato
precedentemente. Le note verranno visualizzate in un popup"""


class ImageButtonNotes(ButtonBehavior, Image):

    def on_press(self):
        if os.path.getsize(Global.contacts_filename) > 0:
            pkl_file = open(Global.contacts_filename, 'rb')
            mydict = pickle.load(pkl_file)
            txt = dict(mydict)
            notes = txt.get("notes")[int(self.id)]
            popup = Popup(title='Notes',
                          content=Label(text=notes),
                          size_hint=(None, None), size=(300, 300))
            popup.open()
            pkl_file.close()


""" Pagina per la visualizzazione del singolo contatto. EXTRA: I campi sono modificabili"""


class viewContact(Screen):
    def __init__(self, **kwargs):
        super(viewContact, self).__init__(**kwargs)

    def on_enter(self, *largs):
        if os.path.getsize(Global.contacts_filename) > 0:
            pkl_file = open(Global.contacts_filename, 'rb')
            mydict = pickle.load(pkl_file)

            # Definisco il layout, mostrando i dati e due bottoni per modifica e cancellazione
            layoutContact = GridLayout(rows=2, cols=2, spacing=10, size_hint_y=None,
                                       pos_hint={'top': 0.45 + self.size_hint[1] / 5})

            layoutContactNotes = GridLayout(cols=1, size_hint_y=None,
                                            pos_hint={'top': 0.7 + self.size_hint[1] / 5})

            layoutRabbishEdit = GridLayout(cols=2, size_hint_y=None,
                                           pos_hint={'top': 0.20 + self.size_hint[1] / 5})

            # Scorro il dizionario mostrando le informazioni relative al contatto
            for i in range(0, len(mydict["name"])):
                txt = dict(mydict)
                email = txt.get("email")[i]
                if email == Global.EMAIL:
                    # Resetto gli elementi grafici
                    self.clear_widgets()
                    self.add_widget(self.ids.actionbar)

                    name = txt.get("name")[i]
                    surname = txt.get("surname")[i]
                    phone = txt.get("phone")[i]

                    # Definisco le texbox per editare i valori del contatto
                    name = TextInput(text=name)
                    name2 = TextInput(text=surname)
                    name3 = TextInput(text=email)
                    name4 = TextInput(text=str(phone))
                    name6 = Label(text="Notes")
                    name5 = ImageButtonNotes(id=str(i), source='images/notes.png')

                    # Bottone per eliminazione
                    btnRabbish = ImageButtonDelete(id=str(i), source='images/delete.png', size_hint_y=None, height=40)

                    layoutContactNotes.add_widget(name6)
                    layoutContactNotes.add_widget(name5)
                    layoutContact.add_widget(name)
                    layoutContact.add_widget(name2)
                    layoutContact.add_widget(name3)
                    layoutContact.add_widget(name4)

                    # Bottone per modifiche
                    btnEdit = ImageButtonEdit(
                        id=str(i),
                        source='images/edit.png', size_hint_y=None, height=40)

                    layoutRabbishEdit.add_widget(btnEdit)
                    layoutRabbishEdit.add_widget(btnRabbish)

                    """ Collego gli id agli elementi aggiunti dinamicamente,utilizzando la libreria weakref, in modo tale da poterli riestrarli successivamente.
                    Questo viene fatto perche' il binding degli id agli elmenti viene fatto al loading di kivy, quindi non vale per gli elementi creati in modo
                    dinamico"""

                    self.add_widget(layoutContactNotes)
                    self.add_widget(layoutContact)
                    self.add_widget(layoutRabbishEdit)
                    self.ids['name'] = weakref.ref(name)
                    self.ids['surname'] = weakref.ref(name2)
                    self.ids['email'] = weakref.ref(name3)
                    self.ids['phone'] = weakref.ref(name4)
                    Global.VIEW = True

                    pkl_file.close()


