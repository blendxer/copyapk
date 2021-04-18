from kivy.app import App
from kivy.lang import Builder
import threading
from android.permissions import request_permissions, Permission
kv = '''
BoxLayout:
	orientation: 'vertical'
	Button:
		id : button
		text: 'download update'
		on_release: app.download()
	Button:
		text: 'ask for permission'
		on_release: app.storage_permissions()

'''


class theapp(App):
	def build(self):
		return Builder.load_string(kv)

	def download(self):
		t = threading.Thread(target= self._thread  )
		t.start()
		self.root.ids.button.text = 'waiting ... '

	def _thread(self):
		try:
			import gspread
			cd = gspread.service_account(filename='credit.json')
			sh = cd.open_by_key('1jjNzQyRd67E7r4Knbq_FjLH-SHz5SHsUG4Q7K5GWzok')
			worksheet = sh.sheet1
			result  = worksheet.get_all_records()
			text = 'the target is {}'.format(result[0]['target'])
			self.root.ids.button.text= text
		except FileNotFoundError:
			self.root.ids.button.text= 'not find the file'
		except ModuleNotFoundError:
			self.root.ids.button.text= 'there is no module'
		except Exception:
			self.root.ids.button.text= 'fail to connect'

	def storage_permissions(self):
		t = threading.Thread(target = self.per_thread)
		t.start()
	def per_thread(self):
		print('dddd')
		request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
		


theapp().run()