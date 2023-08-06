#smarthome.py
class SmartHome:
    """
    Class SmartHome เป็นข้อมูลที่เกี่ยวข้องกับการทำ SmartHome DIY
    มีชื่อเพจ Blog ช่อง Yuotube
    
    Example
    -----------------------
    smarthome = SmartHome()
    smarthome.show_name()
    smarthome.show_youtube()
    smarthome.about()
    smarthome.show_art()
    -----------------------
    """

    def __init__(self):
        self.name = 'Smart Home Thailand'
        self.page = 'https://www.facebook.com/'

    def show_name(self):
        print('สวัสดี ชาว DIY SmartHome ต้อนรับเข้าสู่ {}'.format(self.name))

    def show_youtube(self):
        print('https://www.google.com')

    def about(self):
        text = """
        SmartHome_Thailand , Blog นำเสนอการ DIY ในบ้านด้วยอุปกรณ์ Smart Device
        มีคำอธิบาย หรือคู่มือ DIY ใน case ต่างๆ สามารถติดตาม DIY case ใหม่ๆได้เลยครับ
        ทางช่องทาง Blog / YouTube / Blockdit
        """
        print(text)

    def show_art(self):
        text = """
        Smart Home x
        .-. _______|
        |=|/     /  \\
        | |_____|_""_|
        |_|_[X]_|____|
        """
        print(text)

if __name__ == '__main__':
    smarthome = SmartHome()
    smarthome.show_name()
    smarthome.show_youtube()
    smarthome.about()
    smarthome.show_art()