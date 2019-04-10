from kivy.app import App
from kivy.lang import Builder
import Global
from kivy.uix.gridlayout import GridLayout
from contacts import mainScreen
from newcontact import addContact
from searchcontact import searchContact
from singlecontact import viewContact

emailHome = ""

Builder.load_file('./contactmanager.kv')


# Definisco la classe per il layout
class DateGrid(GridLayout):

    def __init__(self, **kwargs):
        super(DateGrid, self).__init__(**kwargs)


# Ritorna il riferimento allo screen
class contactManager(App):

    def build(self):
        return Global.sm


if __name__ == '__main__':
    # Creo gli elementi per lo screen manager

    Global.sm.add_widget(mainScreen(name='main'))
    Global.sm.add_widget(addContact(name='add'))
    Global.sm.add_widget(searchContact(name='search'))
    Global.sm.add_widget(viewContact(name='view'))
    contactManager().run()
