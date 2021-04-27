import time
from plyer import notification

if __name__ == '__main__':
    while True:
        tex = 'text dont find'
        try:
            with open('time.txt','r',encoding='utf-8') as f:
                tex = f.read()
                
        except Exception:
            pass


        notification.notify(
        title = "وقت المحاضره قد حان",
        message=tex)
            
        time.sleep(100)