from kivy.app import App
from kivy.lang import Builder
from jnius import autoclass
from kivy.logger import Logger
import android

PythonActivity = autoclass("org.kivy.android.PythonActivity").mActivity
Context = autoclass('android.content.Context')
ContextCompat = autoclass('android.support.v4.content.ContextCompat')
kv = '''
BoxLayout:
    Button:
        id: check
        text: 'check permissions'
        on_release: app.check()
    Button:
        text: 'ask for permissions'
        on_release: app.ask()
'''


class application(App):
    def build(self):
        return Builder.load_string(kv)

    def check(self):
        a = self.check_permission()
        self.root.ids.check.text = str(a)

    def ask(self):
        self.ask_permission(android.permission.READ_EXTERNAL_STORAGE)

    def check_permission(permission, activity=PythonActivity):
        permission_status = ContextCompat.checkSelfPermission(activity,
                                                            permission)

        Logger.info(permission_status)
        permission_granted = 0 == permission_status
        Logger.info("Permission Status: {}".format(permission_granted))
        return permission_granted

    def ask_permission(permission, activity=PythonActivity):
        PythonActivity.requestPermissions([permission])

application().run()