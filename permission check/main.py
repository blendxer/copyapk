from kivy.app import App
from kivy.lang import Builder
import plyer, os


kv = '''
BoxLayout:
    Button:
        id: check
        text: 'check permission'
        on_release: app.check()


'''

class application(App):
    def build(self):
        return Builder.load_string(kv)

    def check(self):
        place = plyer.storagepath.get_pictures_dir()
        file = os.path.isdir(place)
        if file:
            self.root.ids.check.text = 'yes' ## you have the permission
        else:
            self.root.ids.check.text = 'no'  ## you don't have the permission

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key in [27, 1001]:
            self.root.ids.check.text += 'get back'
        # do what you want, return True for stopping the propagation
        return True 
application().run()
