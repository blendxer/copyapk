from kivy.app import App
from kivy.lang import Builder
import threading, sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from kivy.uix.popup import Popup
from kivy.metrics import dp


cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

kv = '''
BoxLayout:
    Button:
        id: bt
        text :'not yet'
        on_release: app.down()
'''
class the_app(App):
    def build(self):
        return Builder.load_string(kv)

    def down(self):
        def ali():
            try:
                users_ref = db.collection(u'User')
                docs = users_ref.stream()

                for doc in docs:
                    tex = f'{doc.id} => {doc.to_dict()}'
                    self.root.ids.bt.text = tex

            except Exception as e:
                exc_tb = sys.exc_info()[2]
                err = str(e).join(str(exc_tb.tb_lineno))
                self.toaster(err)
        t = threading.Thread(target=ali)
        t.start()

    def toaster(self,message):
        pop = Popup(title=message,size_hint_y=None,pos=(0,dp(100)),
        title_size='18sp',height=dp(1))
        pop.open()


        

the_app().run()


