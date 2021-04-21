from kivymd.app import MDApp
from kivymd.uix.picker import MDTimePicker
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import  NumericProperty, StringProperty , ColorProperty ,ListProperty
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager
from kivy.graphics import  Color, Line
from kivy.config import Config
from kivy.storage.jsonstore import JsonStore
from kivy.uix.image import Image as K_Image
from bidi.algorithm import get_display
from PIL import Image, ImageDraw
from kivy.metrics import  dp
import arabic_reshaper
import datetime
import colorsys
import os, sys


_font_path = os.path.join('tex','Insan-Regular.ttf')
LabelBase.register(name='arabic',
fn_regular= _font_path)


from jnius import autoclass




device_size = Window.size

save_image_path = r'tex/tbk.jpg'
save_thumb = r'tex/ttn.png'
changed_background = r'tex/cbg.jpg'
changed_thumb = r'tex/ctn.png'
dev_background = r'tex/defbg.jpg'
dev_thumb = r'tex/defthum.png'

current_background_load = r'tex/defbg.jpg'
current_thumb_load = r'tex/defthum.png'






store_json = JsonStore(r'tex/theme_json.json')

lessons= {}
_text_path = r'tex/confi.txt'
with open(_text_path,'r+', encoding = 'utf-8') as f:
    text_file = f.read()
    _s_lines = text_file.splitlines()
    if len(_s_lines):
        first_line = _s_lines[0]
        lessons = eval(first_line)


####   load theme
#_theme_file_path = r'C:\Users\abdul\Desktop\tex\tar.txt'
theme_load = {'lessons_text_color':(1,1,1),'lessons_canvas_color':[0,0,0,0.7],
                'lessons_font_size':19,'meet_link_canvas_color':[0,0,0,0.7],
                'current_background':dev_background,'current_thumb':dev_thumb}
# with open(_theme_file_path,'r+', encoding = 'utf-8') as f:
#     text_file = f.read()
#     _s_lines = text_file.splitlines()
#     if len(_s_lines):
#         first_line = _s_lines[0]
#         theme_load = eval(first_line)


theme_list_ids = ['lessons_text_color','lessons_canvas_color','lessons_font_size',
                   'meet_link_canvas_color','current_background','current_thumb' ]
for i in range(len(theme_load)):
    theme_load[theme_list_ids[i]] = store_json.get(theme_list_ids[i])['name']
        
# store_json.put('lessons_text_color',name =theme_load['lessons_text_color'])
# store_json.put('lessons_canvas_color',name =theme_load['lessons_canvas_color'])
# store_json.put('lessons_font_size',name =theme_load['lessons_font_size'])
# store_json.put('meet_link_canvas_color',name =theme_load['meet_link_canvas_color'])
# store_json.put('current_background',name =theme_load['current_background'])
# store_json.put('current_thumb',name =theme_load['current_thumb'])

lessons_arange = {'from_sonday':0,'to_sonday':1,'from_monday':2,'to_monday':3, 'from_tuesday':4, 'to_tuesday':5, 'from_wednesday':6,
                    'to_wednesday':7, 'from_thursday':8, 'to_thursday':9, 'from_saturday':10, 'to_saturday':11}


ckeck_color_id = {'sonday':['sonday','from_sonday','from_sonday_label','to_sonday','to_sonday_label'],
                  'monday':['monday','from_monday','from_monday_label','to_monday','to_monday_label'],
                  'tuesday':['tuesday','from_tuesday','from_tuesday_label','to_tuesday','to_tuesday_label'],
                  'wednesday':['wednesday','from_wednesday','from_wednesday_label','to_wednesday','to_wednesday_label'],
                  'thursday':['thursday','from_thursday','from_thursday_label','to_thursday','to_thursday_label'],
                  'saturday':['saturday','from_saturday','from_saturday_label','to_saturday','to_saturday_label']}

active_button = {'sonday':False, 'monday':False,'tuesday':False,'wednesday':False,
                'thursday':False,'saturday':False}

week_day = {'sunday':[0,1],'monday':[2,3],'tuesday':[4,5],'wednesday':[6,7],'thursday':[8,9],'saturday':[10,11]}

active_child = {'from_sonday':'sonday','to_sonday':'sonday',
                'from_monday':'monday','to_monday':'monday',
                'from_tuesday':'tuesday','to_tuesday':'tuesday',
                'from_wednesday':'wednesday','to_wednesday':'wednesday',
                'from_thursday':'thursday','to_thursday':'thursday',
                'from_saturday':'saturday','to_saturday':'saturday'}
class Meet_Lobby(ScreenManager):
    check_color = {'sonday':True, 'monday':True, 'tuesday': True, 'wednesday':True,
                    'thursday':True, 'saturday': True}
    time_senter = None
    add_start_text= False
    edit_mode = False
    today_lessons = {}
    other_day_lessons = {}
    day_night_from = None
    day_night_to = None
    box_canvas= None
    calender_font_size = NumericProperty(18)
    ############  change background
    thumb_image = StringProperty( theme_load['current_thumb']) 
    current_background =  theme_load['current_background'] 
    just_move_old_background = False
    not_select_yet = True
    sel_image = StringProperty('')
    ############  theme change
    lessons_text_color = theme_load['lessons_text_color']
    lessons_canvas_color = theme_load['lessons_canvas_color']
    lessons_font_size = theme_load['lessons_font_size']
    meet_link_canvas_color = ListProperty( theme_load['meet_link_canvas_color'])
    #######
    b_today_lessons = {}
    time_dir = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.image_background_.source = self.current_background
        self.th_image = False
        if not len(lessons):
            self.lab = Label(text='you can add lessons though the button',color=(1,0,0,1))
            self.ids['main_lobby'].add_widget(self.lab)
            self.add_start_text= True
        else:
            self.change_calender()

    def change_calender(self):
        self.today_lessons = {}
        self.other_day_lessons = {}
        self.ids['lessons_table'].clear_widgets()
        
        if self.box_canvas:
            self.box_canvas.clear_widgets()
        day = datetime.datetime.now().strftime("%A").lower()
        if not day == 'friday':
            _from, _to = week_day[day]
            for i in lessons:
                time_start = lessons[i][_from]
                time_end = lessons[i][_to]
                link = lessons[i][-1]
                if time_start:
                    self.today_lessons[i] = [time_start, time_end, link]

            for i in lessons:
                if not i in self.today_lessons:
                    link = lessons[i][-1]
                    self.other_day_lessons[i] = link
                    

            self.b_today_lessons.clear()
            self.time_dir.clear()
            time_dir_num = None
            extra_lessons = []
            for i in self.today_lessons:
                name = i
                time = int(self.today_lessons[i][0].replace(':',''))
                if not time in self.time_dir:
                    self.time_dir[time] = [name]
                else:
                    extra_lessons.append(name)

            time_dir_num= sorted(self.time_dir)
            for i in time_dir_num:
                name = self.time_dir[i][0]
                values = self.today_lessons[name]
                self.b_today_lessons[name] = list(values)


            def ali(row_time):
                time = int(row_time.replace(':',''))
                if time > 1200:
                    new_time = time - 1200
                    new_time = str(new_time).zfill(4)
                    new_time = new_time[:2]+ ':' +new_time[2:4]
                    new_time = new_time +' '+'م'
                    return new_time
                else:
                    return row_time+' '+'ص'
            self.today_lessons = self.b_today_lessons

        else:
            for i in lessons:
                link = lessons[i][-1]
                self.other_day_lessons[i] = link


        label_height = dp(25)
        button_height = dp(50)
        root_width = Window.size[0]
        if len(self.today_lessons):
            today_lab = Button(text= self.to_arabic('دروس اليوم'),size_hint_y=None,height= label_height,
                    font_name='arabic',background_normal='',background_color=(0,0,0,0),color=(self.lessons_text_color),
                    background_down='',font_size=dp(self.lessons_font_size))

            self.ids['lessons_table'].add_widget(today_lab)            
            y_pos= 0
            wid = dp(13)
            _shift = dp(5)
            other_day_button = len(self.other_day_lessons)*button_height+dp(30)
            self.box_canvas = BoxLayout()
            for k in range(len(self.today_lessons)):
                with self.box_canvas.canvas.before:

                    Color(*self.lessons_canvas_color)
                    Line(points=(wid+_shift,wid+dp(y_pos)+other_day_button, 
                                wid+_shift,button_height-2*wid+dp(y_pos)+other_day_button,
                                root_width-wid-_shift,button_height-2*wid+dp(y_pos)+other_day_button,
                                root_width-wid-_shift,wid+dp(y_pos)+other_day_button),close=True, width=wid)
                    y_pos+=50
            self.ids['lessons_table'].add_widget(self.box_canvas)

            for j in self.today_lessons:
                box = BoxLayout(size_hint_y = None, height = button_height)

                time_button = Button(text ='   {} - {}[size=0]Q?$8x{}Q?$8x[/size]'.format(ali(self.today_lessons[j][0]),ali(self.today_lessons[j][1]),
                self.today_lessons[j][-1]),font_name = 'arabic',background_normal='',markup = True,color=(self.lessons_text_color), background_color=(0,0,0,0),
                valign='middle', halign='left', font_size =dp(self.lessons_font_size))
                time_button.bind(on_release=self.open_link)

                name_button = Button(text = '{}[size=0]Q?$8x{}Q?$8x[/size]'.format(j,self.today_lessons[j][-1]),font_name= 'arabic',
                background_normal='',markup = True, color=(self.lessons_text_color), background_color=(0,0,0,0),
                valign='middle', halign='right', font_size = dp(self.lessons_font_size))
                name_button.bind(on_release=self.open_link)

                
                box.add_widget(time_button)
                box.add_widget(name_button)
                self.ids['lessons_table'].add_widget(box)

            # if len(extra_lessons):
            #     today_lab = Button(text= self.to_arabic('تضارب'),size_hint_y=None,height= label_height,
            #         font_name='arabic',background_normal='',background_color=(0,0,0,0),color = self.lessons_text_color,
            #         background_down='',font_size=dp(self.lessons_font_size))
            #     self.ids['lessons_table'].add_widget(today_lab)

            #     for i in extra_lessons:
            #         box = BoxLayout(size_hint_y = None, height = button_height)


        else:
            today_lab = Button(text= self.to_arabic('لايوجد اليوم دروس'),size_hint_y=None,height= label_height,
                    font_name='arabic',background_normal='',background_color=(0,0,0,0), color= self.lessons_text_color,
                    background_down='',font_size=dp(self.lessons_font_size))
            self.ids['lessons_table'].add_widget(today_lab)

        if len(self.other_day_lessons):
            today_lab_2 = Button(text= self.to_arabic('باقي الدروس'),size_hint_y=None,height= label_height,
                    font_name='arabic',background_normal='',background_color=(0,0,0,0), color =self.lessons_text_color,
                    background_down='',font_size=dp(self.lessons_font_size))
            self.ids['lessons_table'].add_widget(today_lab_2)

            y_pos= 8
            _shift = dp(5)
            wid = dp(13)
            self.box_canvas_2 = BoxLayout()
            for k in range(1,len(self.other_day_lessons)+1):
                with self.box_canvas_2.canvas.before:
                    Color(*self.lessons_canvas_color)
                    Line(points=(wid+_shift,wid+dp(y_pos), 
                                wid+_shift,button_height-2*wid+dp(y_pos),
                                root_width-wid-_shift,button_height-2*wid+dp(y_pos),
                                root_width-wid-_shift,wid+dp(y_pos)),close=True, width=wid)
                    y_pos+=50
            self.ids['lessons_table'].add_widget(self.box_canvas_2)
            
            for j in self.other_day_lessons:
                tex = '{}[size=0]Q?$8x{}Q?$8x[/size]'.format(j,self.other_day_lessons[j])
                bt = Button(text=tex,font_name='arabic',size_hint_y=None,height=button_height,
                background_normal='',background_color=(0,0,0,0),markup = True,font_size=dp(self.lessons_font_size),color=(self.lessons_text_color))
                bt.bind(on_release=self.open_link)
                self.ids['lessons_table'].add_widget(bt)

        
        else:
            today_lab_2 = Button(text= self.to_arabic('لايوجد دروس أخرى'),size_hint_y=None,height= label_height,
                    font_name='arabic',background_normal='',background_color=(0,0,0,0), color= self.lessons_text_color,
                    background_down='',font_size=dp(self.lessons_font_size))
            self.ids['lessons_table'].add_widget(today_lab_2)
        self.ids['lessons_table'].height = (label_height*2)+(len(self.today_lessons)+len(self.other_day_lessons))*button_height

    
    def open_link(self, link):
        text = link.text
        link =  text.split('Q?$8x')[1]
        
        if not self.edit_mode:
            try:
                link = link.split('.com/')[-1]
                url = f'http://meet.google.com/{link}'
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                browserIntent = Intent()
                browserIntent.setAction(Intent.ACTION_VIEW)
                browserIntent.setData(Uri.parse(url))
                PythonActivity.mActivity.startActivity(browserIntent)

            except Exception as e:
                exc_tb = sys.exc_info()[2]
                err = str(e).join(str(exc_tb.tb_lineno))
                self.toaster(err)



        else:
            try:
                active_days = [False for i in range(1,13)]
                obj = text.split('Q?$8x')[0].replace('[size=0]','')
                values = lessons[obj]
                _list = [0,2,4,6,8,10]
                for i in _list:
                    if values[i]:
                        active_days[i] = True
                active_days = active_days[0:13:2]
                for i in range(1,7):
                    if active_days[i-1]:
                        tex = 'check_day_{}'.format(i)
                        self.ids[tex].active = True
                for i in lessons_arange:
                    if values[lessons_arange[i]]:
                        self.ids[i].text = values[lessons_arange[i]]
                        self.ids[i].background_color = 0.3,0.3,0.3  
                self.ids['mat_name'].text = obj
                self.ids['link'].text = values[-1]
                self.current = 'meet_adder'
            except Exception as e:
                exc_tb = sys.exc_info()[2]
                err = str(e).join(str(exc_tb.tb_lineno))
                self.toaster(err)

            

    def editor(self):
        if not self.edit_mode:
            self.ids['editor_mode'].text = self.to_arabic('ألغ التحرير')
            self.edit_mode = True
            if len(lessons):
                self.toaster(self.to_arabic('أختر المادة التي تريد التعديل عليها'))
            else:
                self.toaster(self.to_arabic('لايوجد دروس لكي يتم التعديل عليها'))
        else:
            self.ids['editor_mode'].text = self.to_arabic('تحرير')
            self.edit_mode = False

    def class_del(self):

        if self.ids['mat_name'].text in lessons:
            lessons.pop(self.ids['mat_name'].text)
            AAA.text_saver()
        Ar_text.str = ''
        for i in active_button:
            if i:
                for k in ckeck_color_id:
                    self.ids[k].color = 0.6,0.6,0.6
        for i in range(1,7):
            tex = 'check_day_{}'.format(i)
            self.ids[tex].active = False
        for i in active_button:
            active_button[i] = False


        self.ids['link'].text = ''
        #self.ids['mat_name'].text = ''
        self.remove_old_text()
        self.change_calender()

    def to_arabic(self, text):
        a = get_display(arabic_reshaper.reshape(str(text)))
        return(a)

    def toaster(self, message):
        pop = Popup(title=message,title_font='arabic',size_hint_y=None,pos=(0,dp(100)),
        title_size='20sp')
        pop.open()
###########3  Time Setter ############

    def remove_old_text(self):
        text = self.ids.mat_name.text


    def show_time_picker(self):
        picker = MDTimePicker()
        picker.bind(time= self.get_time)
        s = active_child[self.time_senter]
        if active_button[s]:
            picker.open()
        
    def get_time(self, picker_widget, time):
        hour = str(time.hour).zfill(2)
        minute = str(time.minute).zfill(2)
        self.ids[self.time_senter].text = '{}:{}'.format(hour, minute)

    def whose_sent_time(self, senter):
        self.time_senter = senter

    def color_check(self, s):
        _list = ['to','from']
        if self.check_color[s] == True:
            active_button[s] = True
            for i in ckeck_color_id[s]:
                self.ids[i].color = 1,1,1
                first = i.split('_')[0]
                if first in _list:
                    self.ids[i].background_color = 0.3,0.3,0.3
            self.check_color[s] = False
        else:
            self.check_color[s] = True
            for i in ckeck_color_id[s]:
                self.ids[i].color = [0.6]*3
                active_button[s] = False
                first = i.split('_')[0]
                if first in _list:
                    self.ids[i].background_color = 1,1,1,0


    def make_new_lesson(self):
        False_list = [False for i in range(13)]
        active_day=[] 
        times = {}
        name = self.ids['mat_name'].text
        link = self.ids['link'].text
        link = link.strip().replace(' ','').replace('  ','')
        _list = []
        for i in active_button:
            if active_button[i]:
                active_day.append(i)

            
        if not name == '':
            if not link == '':
                if  len(active_day):
                    for i in active_day:
                        all_time = ckeck_color_id[i]
                        for j in all_time:
                            seperate = j.split('_')
                            if len(seperate)== 2:
                                times[j] = self.ids[j].text


                    for i in times:
                        for j in lessons_arange:
                            if i == j:
                                _list = False_list
                                _list[lessons_arange[j]] = times[i]

                    _list[12] = link
                    lessons[name] = _list
                    self.current = 'meet_lobby'
                    
                    self.change_calender()
                    for i in active_button:
                        active_button[i] = False

                    for k in active_day:
                        for j in ckeck_color_id[k]:
                            seperate = j.split('_')
                            if len(seperate) ==2:
                                self.ids[j].text= '00:00'
                    for i in range(1,7):
                        tex = 'check_day_{}'.format(i)
                    
                        self.ids[tex].active = False
                    self.ids['link'].text = ''
                    #self.ids['mat_name'].text = ''
                    self.remove_old_text()
                    #Ar_text.str = ''
                    AAA.text_saver()
                    if self.add_start_text:
                        self.ids['main_lobby'].remove_widget(self.lab)

                else:
                    self.toaster(self.to_arabic('أضف يوم الى الجدول'))

            else:
                self.toaster(self.to_arabic('أدخل الرابط'))

        else:
            self.toaster(self.to_arabic('أدخل أسم'))

    def clean_list(self):
        self.ids['link'].text = ''
        #self.ids['mat_name'].text = ''
        self.remove_old_text()
        #Ar_text.str = ''
        
        for i in active_button:
            if i:
                for k in ckeck_color_id:
                    self.ids[k].color = 0.6,0.6,0.6
        for i in range(1,7):
            tex = 'check_day_{}'.format(i)
            self.ids[tex].active = False
        for i in active_button:
            active_button[i] = False

#########     setting method ##########


    color_type = 'text_color'
    textcolor = ColorProperty(theme_load['lessons_text_color'])
    canvascolor = ColorProperty(theme_load['lessons_canvas_color'])
    canvasopacity = NumericProperty(theme_load['lessons_canvas_color'][-1])
    number = 0
    check_color_ids = ['color_slider_h','color_slider_s', 'color_slider_v']
    def check_color_2(self):
        self.number +=1
        rgb = [0,0,0]
        hsv = [0,0,0]
        if self.color_type == 'text_color':
            if self.number % 2 == 1:
                for i in range(3):
                    hsv[i] = self.ids[self.check_color_ids[i]].value
                rgb = tuple(colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))
                self.textcolor = rgb
                hsv = colorsys.rgb_to_hsv(self.canvascolor[0],self.canvascolor[1],self.canvascolor[2])
                for i in range(3):
                    self.ids[self.check_color_ids[i]].value = hsv[i]

            self.ids['text_color'].active = False
            self.ids['canvas_color'].active = True
            self.color_type = 'canvas_color'
        else:
            if self.number % 2 == 1:
                for i in range(3):
                    hsv[i] = self.ids[self.check_color_ids[i]].value
                rgb = tuple(colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))
                self.canvascolor = rgb
                hsv = colorsys.rgb_to_hsv(self.textcolor[0],self.textcolor[1],self.textcolor[2])
                for i in range(3):
                    self.ids[self.check_color_ids[i]].value = hsv[i]

            self.ids['text_color'].active = True
            self.ids['canvas_color'].active = False
            self.color_type = 'text_color'

    def apply_new_setting(self):
        if self.number == 0:
            hsv = [0,0,0]
            for i in range(3):
                hsv[i] = self.ids[self.check_color_ids[i]].value
            rgb = self.convert_color(hsv, 'rgb')
            self.lessons_text_color = rgb
            self.textcolor = rgb

        if self.number == 2:
            hsv = [0,0,0]
            for i in range(3):
                hsv[i] = self.ids[self.check_color_ids[i]].value
            rgb = self.convert_color(hsv, 'rgb')
            self.lessons_canvas_color = rgb
            self.canvascolor = rgb

        if self.number > 2:
            if self.color_type == 'text_color':
                hsv = [0,0,0]
                for i in range(3):
                    hsv[i] = self.ids[self.check_color_ids[i]].value
                rgb = tuple(colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))
                self.textcolor = rgb

            if self.color_type == 'canvas_color':
                hsv = [0,0,0]
                for i in range(3):
                    hsv[i] = self.ids[self.check_color_ids[i]].value
                rgb = tuple(colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))
                self.canvascolor = rgb

            self.lessons_text_color = self.textcolor
            self.lessons_canvas_color = self.canvascolor

        if len(self.lessons_canvas_color) == 3:
            self.lessons_canvas_color= list(self.lessons_canvas_color)+ [self.ids['text_trans_slider'].value,]
        if len(self.lessons_canvas_color) == 4:
            self.lessons_canvas_color[3] = self.ids['text_trans_slider'].value
        self.lessons_font_size = self.ids['text_size_slider'].value
        self.lessons_text_color = self.textcolor
        self.ids['link_lab'].color = self.lessons_text_color
        self.meet_link_canvas_color = self.lessons_canvas_color


        # theme_load = {'lessons_text_color':self.lessons_text_color ,
        #             'lessons_canvas_color':self.lessons_canvas_color,
        #             'lessons_font_size':self.lessons_font_size,
        #             'meet_link_canvas_color':self.lessons_canvas_color,
        #             'current_background': self.ids.image_background_.source,
        #                 }

        store_json.put('lessons_font_size',name = self.lessons_font_size)
        store_json.put('lessons_canvas_color',name = self.lessons_canvas_color)
        store_json.put('lessons_text_color',name = self.lessons_text_color)
        store_json.put('meet_link_canvas_color',name = self.meet_link_canvas_color)
        store_json.put('current_background',name = self.ids.image_background_.source)

        if self.th_image:
           # theme_load['current_thumb'] = self.th_image.source
            store_json.put('current_thumb',name = self.th_image.source)

        else:
            #theme_load['current_thumb'] = self.thumb_image
            store_json.put('current_thumb',name = self.thumb_image)

        if self.just_move_old_background or not self.not_select_yet:
            if os.path.isfile(changed_background):
                os.remove(changed_background)
            if os.path.isfile(changed_thumb):
                os.remove(changed_thumb)
            
            os.rename(save_image_path , changed_background)
            os.rename(save_thumb , changed_thumb)
            #self.sel_image = ''
            self.just_move_old_background = False
            self.not_select_yet = True
            self.ids['image_background_'].source = changed_background
            self.ids['image_background_'].reload()

            theme_load['current_background'] = changed_background
            theme_load['current_thumb'] = changed_thumb
            store_json.put('current_thumb',name = changed_thumb)
            store_json.put('current_background',name = changed_background)
                        
        # with open(_theme_file_path,'r+', encoding = 'utf-8') as f:
        #     f.truncate()
        #     f.write(str(theme_load))
        
        self.change_calender()

    def recover_setting(self):
        self.ids['text_size_slider'].value = self.lessons_font_size
        self.ids['text_trans_slider'].value = self.lessons_canvas_color[-1]
        
        rgb = [0,0,0]
        hsv = [0,0,0]
        if self.ids['text_color'].active:
            for i in range(3):
                rgb[i] = self.lessons_text_color[i]
            hsv = colorsys.rgb_to_hsv(rgb[0],rgb[1],rgb[2])
            for i in range(3):
                self.ids[self.check_color_ids[i]].value = hsv[i]
        else:
            for i in range(3):
                rgb[i] = self.lessons_canvas_color[i]
            hsv = colorsys.rgb_to_hsv(rgb[0],rgb[1],rgb[2])
            for i in range(3):
                self.ids[self.check_color_ids[i]].value = hsv[i]

    def cancel_new_setting(self):
        if self.th_image:
            #self.th_image.source = self.thumb_image
            self.th_image.source = store_json.get('current_thumb')['name']
        else:
            #self.thumb_image = dev_thumb
            self.thumb_image = store_json.get('current_thumb')['name']
            

    def dev_setting(self):
        self.lessons_text_color = (1,1,1)
        self.lessons_canvas_color = [0,0,0,0.7]
        self.lessons_font_size = 19
        self.ids['link_lab'].color = (1,1,1)
        self.meet_link_canvas_color = [0,0,0,0.7]
        self.ids['display_time'].color = (1,1,1)
        self.ids['display_name'].color = (1,1,1)
        self.ids.text_trans_slider.value = 0.7
        
        self.canvascolor =[0,0,0,0.7]
        self.textcolor = [1,1,1]
        self.canvasopacity = 0.7
        if self.color_type == 'text_color':
            for i in range(3):
                self.ids[self.check_color_ids[i]].value = 1
        else:
            for i in range(3):
                self.ids[self.check_color_ids[i]].value = 0

        if os.path.isfile(changed_background):
            os.remove(changed_background)
        if os.path.isfile(changed_thumb):
            os.remove(changed_thumb)
        self.ids.image_background_.source = dev_background
        if self.th_image:
            self.th_image.source = dev_thumb
        else:
            self.thumb_image = dev_thumb
        self.change_calender()

        # theme_load = {'lessons_text_color':(1,1,1) ,
        #               'lessons_canvas_color':[0,0,0,0.7],
        #               'lessons_font_size':19,
        #               'meet_link_canvas_color':[0,0,0,0.7],
        #               'current_background':dev_background,
        #               'current_thumb': dev_thumb
        #                 }
        
        store_json.put('lessons_font_size',name =19)
        store_json.put('lessons_canvas_color',name = [0,0,0,0.7])
        store_json.put('lessons_text_color',name = (1,1,1))
        store_json.put('meet_link_canvas_color',name = [0,0,0,0.7])
        store_json.put('current_background',name = dev_background)
        store_json.put('current_thumb',name = dev_thumb)

        
        # with open(_theme_file_path,'r+', encoding = 'utf-8') as f:
        #     f.truncate()
        #     f.write(str(theme_load))

    def convert_color(self, color, mode):
        color_back = None
        if mode == 'rgb':
            color_back = colorsys.hsv_to_rgb(color[0],color[1],color[2])
        if mode == 'hsv':
            color_back = colorsys.rgb_to_hsv(color[0],color[1],color[2])
        return color_back


################# files chooser ###########

    def select_image(self, sel):
        image_extenion = ['png','jpg','jpeg']
        if sel:
            extenion = sel[0].split('.')[-1]
            if extenion.lower() in image_extenion:
                self.not_select_yet = False
                self.sel_image = sel[0]


    def apply_new_background(self):
        if not self.not_select_yet:
            extension = ['png','jpg','jpeg']
            ex = self.sel_image.split('.')
            if ex[-1].lower() in extension:
                size = os.path.getsize(self.sel_image)
                if size < 10000000:
                    self.pross_image()
                else:
                    self.toaster(self.to_arabic('حجم الصوره كبير جداً'))
            else:
                self.toaster(self.to_arabic(' الصوره غير صالحة'))
        else:
            self.pross_image()
        

    def pross_image(self):
        scatter_vector = self.ids.image_scatter.pos
        image_vector = self.ids.image_in_scatter.pos
        scale = self.ids.image_scatter.scale
        
        x = scatter_vector[0] + image_vector[0]*scale - (device_size[0]/4 + device_size[0]*0.05)
        clean_image = Image.new('RGB',device_size,(0,0,0))

        fuckingy = (device_size[1]* 0.4+ device_size[1]/2 + device_size[1]*0.05) - ( scatter_vector[1] + image_vector[1]*scale + self.ids.image_in_scatter.size[1]*2.5*0.4*scale)

        if self.not_select_yet:
            img = Image.open(self.current_background)
            new_size = (int(img.size[0]*scale),int(img.size[1]*scale))
            resizeed_image = img.resize(new_size)
            Image.Image.paste(clean_image, resizeed_image, (int(x*2.5),int(fuckingy*2.5)))
            self.current = 'setting_panel_name'
            clean_image.save(save_image_path)
            self.just_move_old_background = True
            self.add_thumbs()
        else:
            img = Image.open(self.sel_image)
            new_size = (int(img.size[0]*scale),int(img.size[1]*scale))
            resizeed_image = img.resize(new_size)
            Image.Image.paste(clean_image, resizeed_image, (int(x*2.5),int(fuckingy*2.5)))
            self.current = 'setting_panel_name'
            clean_image.save(save_image_path)
            self.add_thumbs()
            
    def add_thumbs(self):
        r = 12
        canvas_height = 70
        img = Image.open(save_image_path)
        img_crop = img.crop((0,img.size[1]/2-canvas_height/2,device_size[0],img.size[1]/2+canvas_height/2))
        alphaback = Image.new('RGBA',(device_size[0],canvas_height),color=(0,0,0,0))
        mask = Image.new("L", (device_size[0],canvas_height), 0)
        draw = ImageDraw.Draw(mask)

        draw.line((r, canvas_height/2, device_size[0]-r, canvas_height/2), fill=255,width=canvas_height+1)
        draw.line((0, canvas_height/2, device_size[0], canvas_height/2), fill=255,width=canvas_height-r)
        draw.ellipse((0,0,r*2,r*2),fill=255)
        draw.ellipse((0,canvas_height-2*r,r*2,canvas_height),fill=255)
        draw.ellipse((device_size[0]-2*r,0,device_size[0],r*2),fill=255)
        draw.ellipse((device_size[0]-2*r,canvas_height-2*r,device_size[0],canvas_height),fill=255)

        com = Image.composite(img_crop , alphaback, mask)
        result =  com.crop((0,0,device_size[0],canvas_height))
        result.save(save_thumb)
        self.ids['thumb_container'].clear_widgets()
        self.th_image = K_Image(source=save_thumb,size_hint=(None,None),
                                size= (device_size[0], 70))
        self.th_image.reload()
        self.ids['thumb_container'].add_widget(self.th_image)
        



    def cancel_new_image(self):
        self.not_select_yet = True
        self.sel_image = StringProperty('')
        self.just_move_old_background = False
        self.not_select_yet = True
        
        




class to_from_label(Label):
    def to_arabic(self, text):
        a = get_display(arabic_reshaper.reshape(str(text)))
        return(a)


class AAA():
    def text_saver():
        if  len(lessons):
            
            with open(_text_path,'w', encoding = 'utf-8') as f:
                #f.truncate()
                f.write(str(lessons))
        # else:
        #     with open(_text_path,'w') as f:
        #         f.truncate()

class Ar_text(TextInput):
    max_chars = NumericProperty(60)  
    str = StringProperty()
    def __init__(self, **kwargs):
        super(Ar_text, self).__init__(**kwargs)
        self.text = get_display(arabic_reshaper.reshape(""))

    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return
        self.str = self.str+substring
        self.text = get_display(arabic_reshaper.reshape(self.str))
        substring = ""

        super(Ar_text, self).insert_text(substring, from_undo)

    def do_backspace(self, from_undo=True, mode='bkspc'):
        self.str = self.str[0:len(self.str)-1]
        self.text = get_display(arabic_reshaper.reshape(self.str))
    

def old_text_arab():
    pass


class meet_libApp(MDApp):
    def build(self):
        return Meet_Lobby()

if __name__ == '__main__':
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    Config.set('graphics', 'borderless', '1')
    Config.set('graphics', 'rotation', 90)
    meet_libApp().run()


 




