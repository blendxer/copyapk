from kivy.app import App
from kivy.lang import Builder
import plyer, os
from android.permissions import request_permissions, Permission
tt = 'check'
try:
    from android.permissions import check_permission
except Exception:
    tt = 'no'

try:
    import android
except Exception:
    pass

kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        id: check
        text: 'check permission path'
        on_release: app.check()

    Button:
        id: check_string
        text: app.te() +  ' string'
        on_release: app.check_string()

    Button:
        id : objeck_check
        text: 'objeck check'
        on_release: app.objeck_check()
'''

class application(App):
    def build(self):
        return Builder.load_string(kv)

    def check(self):
        place = plyer.storagepath.get_pictures_dir()
        file = os.scandir(place)
        name = 'row'
        for i in file:
            name += i.name
        self.root.ids.check.text = name

    def check_string(self):
        a = check_permission('android.permission.WRITE_EXTERNAL_STORAGE')
        if a:
            self.root.ids.check_string.text = 'the string check work'
        else:
            self.root.ids.check_string.text = 'dont work'+ str(a)

    def objeck_check(self):
        a = check_permission(permission.WRITE_EXTERNAL_STORAGE)
        if a:
            self.root.ids.objeck_check.text = 'the string check work'
        else:
            self.root.ids.objeck_check.text = 'dont work'+ str(a)
    
    def te(self):
        return tt

application().run()
