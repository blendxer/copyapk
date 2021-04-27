from kivy import app
from kivy.app import App
from kivy.lang import Builder
import dropbox
from kivy.uix.popup import Popup
from kivy.metrics import dp
import sys
import threading
dbx = dropbox.Dropbox('Bvyb_4giI5QAAAAAAAAAAa-JbxPJ1kvks3wTZn0bO9wxxs72b5zzpaLmWbFIllVK')

kv= '''
BoxLayout:
    Button:
        text: 'do something'
        on_release: app.do()
'''

class application(App):
    def build(self):
        return Builder.load_string(kv)

    def do(self):
        file_name = '/backend/mobile.jpg'
        def ali():
            try:    
                with open('theme_image.jpg',"rb") as f:
                    dbx.files_upload(f.read(),file_name)
                    print('ddddddd')
            except Exception as e:
                exc_tb = sys.exc_info()[2]
                err = str(e).join(str(exc_tb.tb_lineno))
                self.toaster(err)
        t = threading.Thread(target=ali)
        t.start()

    def toaster(self, message):
        pop = Popup(title=message,size_hint_y=None,pos=(0,dp(100)),
        title_size='18sp',height=dp(1))
        pop.open()

application().run()