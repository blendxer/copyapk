from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
import requests, json, datetime, sys, threading
from kivy.metrics import dp
kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        id:up
        text: 'up button'
        on_release: app.up()

    Button:
        id: down
        text: 'down button'
        on_release: app.down()

'''
class the_app(App):
    fire_url = 'https://meet-test-one-default-rtdb.firebaseio.com/.json'
    def build(self):
        return Builder.load_string(kv)

    def up(self):
        def ali():
            try:
                time = str(datetime.datetime.now())
                time = time.replace('-','').replace(':','').replace('.','').replace(' ','')[:15]
                _data = '{"id":"no","first":"ali","last":"kram"}'.replace('no',str(time))
                requests.patch(url=self.fire_url, json=json.loads(_data))
            except Exception as e:
                exc_tb = sys.exc_info()[2]
                err = str(e).join(str(exc_tb.tb_lineno))
                self.toaster(err)
        t = threading.Thread(target=ali)
        t.start()

    def down(self):
        def ali():
            try:
                data = requests.get(url=self.fire_url)
                tex = data.json()
                self.root.ids.down.text = str(tex)
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


the_app().run()

