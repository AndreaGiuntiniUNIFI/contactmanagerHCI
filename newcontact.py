from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import pickle
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os
import Global
import collections

""" Pagine relativa all'aggiunta di un contatto alla rubrica. Recupero le informazione dalle textbox
 e le inserisco nel dizionario"""


class addContact(Screen):

    def __init__(self, **kwargs):
        super(addContact, self).__init__(**kwargs)

    def callback(self):

        # Recupero le informazioni
        _ = self.ids
        name = _.name_input.text
        surname = _.surname_input.text
        email = _.email_input.text
        phone = _.phone_input.text
        notes = _.notes_input.text

        contact = [('name', name), ('surname', surname), ('email', email), ('phone', phone), ('notes', notes)]

        """ Se il file esiste, aggiungo il nuovo contatto alla rubrica, aprendo prima in lettura per appendere i dati
        e poi in scrittura.
        """
        if os.path.getsize(Global.contacts_filename) > 0:
            pkl_file = open(Global.contacts_filename, 'rb')
            mydict2 = pickle.load(pkl_file)

            for key, value in contact:
                mydict2[key].append(value)

            pkl_file.close()
            output = open(Global.contacts_filename, 'wb')
            pickle.dump(mydict2, output)
            output.close()
        else:
            # Visto che non ci sono contatti, dichiaro il dizionario e scrivo direttamente
            contactDict = collections.defaultdict(list)

            for key, value in contact:
                contactDict[key].append(value)

            output = open(Global.contacts_filename, 'wb')
            pickle.dump(contactDict, output)
            output.close()

        # Definisco il layout per il popup
        layout = GridLayout(cols=1, padding=10)
        btn = Button(text='Ok!', )
        text = Label(text='A new contact has been added!')
        layout.add_widget(text)
        layout.add_widget(btn)

        popup = Popup(title='Contacts',
                      content=layout,
                      size_hint=(None, None), size=(300, 300))

        btn.bind(on_press=popup.dismiss)
        popup.open()

        # Resetto i valori delle texbox
        _.name_input.text = "Name"
        _.surname_input.text = "Surname"
        _.email_input.text = "Email"
        _.phone_input.text = "Phone number"
        _.notes_input.text = "Notes"
        Global.sm.current = 'main'

