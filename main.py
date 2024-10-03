import qrcode
import cv2
import imutils
from io import BytesIO
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from kivy.core.window import Window

# Set the window size
Window.size = (412, 732)

camera_id = 0
delay = 1
window_name = 'OpenCV QR Code'
qcd = cv2.QRCodeDetector()
cap = cv2.VideoCapture(camera_id)

KV = '''
ScreenManager:
    LoginScreen:
    SignupScreen:
    DashboardScreen:
    CameraScreen:
    ReceiveScreen:
    QRScreen:
    SuccessScreen:

<LoginScreen>:
    name: 'login'
    FloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDLabel:
            text: "Welcome Back"
            halign: 'center'
            font_style: 'H4'
            bold: True
            pos_hint: {'center_y': 0.8}
        MDTextField:
            id: login_email
            hint_text: "Email"
            icon_right: "email"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5, 'center_y': 0.55}
        MDTextField:
            id: login_password
            hint_text: "Password"
            icon_right: "lock"
            password: True
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        MDRaisedButton:
            text: "Login"
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            size_hint_x: 0.9
            on_release: app.animate_button(self)
        MDTextButton:
            text: "Don't have an account? Sign up"
            pos_hint: {'center_x': 0.5, 'center_y': 0.2}
            on_release: root.manager.current = 'signup'

<SignupScreen>:
    name: 'signup'
    FloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDLabel:
            text: "Create Account"
            halign: 'center'
            font_style: 'H4'
            bold: True
            pos_hint: {'center_y': 0.8}
        MDTextField:
            id: signup_email
            hint_text: "Email"
            icon_right: "email"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5, 'center_y': 0.55}
        MDTextField:
            id: signup_password
            hint_text: "Password"
            icon_right: "lock"
            password: True
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        MDRaisedButton:
            text: "Sign Up"
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            size_hint_x: 0.9
            on_release: app.animate_button(self)
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_x": 0.1, "center_y": 0.95}
            on_release: root.manager.current = 'login'

<DashboardScreen>:
    name: 'dashboard'
    FloatLayout:
        MDLabel:
            text: "Your Balance"
            halign: 'center'
            font_style: 'H4'
            bold: True
            pos_hint: {'center_y': 0.8}
        MDLabel:
            text: "$5000"
            halign: 'center'
            font_style: 'H3'
            pos_hint: {'center_y': 0.6}
        MDRaisedButton:
            text: "Send"
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5, 'center_y': 0.2}
            on_release:
                app.on_cam_click()
                root.manager.current = 'camera'
        MDIconButton:
            icon: "logout"
            pos_hint: {"center_x": 0.1, "center_y": 0.95}
            on_release: root.manager.current = 'login'
        MDRaisedButton:
            text: "Receive"
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            on_release: root.manager.current = 'receive'

<ReceiveScreen>:
    name: 'receive'
    FloatLayout:
        MDTextField:
            id: amount
            hint_text: "Amount to be received"
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        MDRaisedButton:
            text: "Confirm"
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
            size_hint_x: 0.9
            on_release: app.generate_qr(amount.text)

<QRScreen>:
    name: 'qr'
    FloatLayout:
        Image:
            id: qr_code_img
            size_hint: 0.8, 0.8
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        MDRaisedButton:
            text: "Back to Dashboard"
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            on_release:
                root.manager.current = 'dashboard'

<CameraScreen>:
    name: 'camera'
    BoxLayout:
        orientation: 'vertical'
        Image:
            id: img

<SuccessScreen>:
    name: 'success'
    FloatLayout:
        MDLabel:
            text: "QR code scanned successfully!"
            halign: 'center'
            pos_hint: {'center_y': 0.5}
        MDRaisedButton:
            text: "Back to Dashboard"
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            on_release: root.manager.current = 'dashboard'
'''

class LoginScreen(Screen):
    pass

class SignupScreen(Screen):
    pass

class DashboardScreen(Screen):
    pass

class ReceiveScreen(Screen):
    pass

class QRScreen(Screen):
    pass

class CameraScreen(Screen):
    pass

class SuccessScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.username = None
        self.capture = None
        return Builder.load_string(KV)

    def login(self):
        login_screen = self.root.get_screen('login')
        self.username = login_screen.ids.login_email.text
        self.root.current = 'dashboard'

    def sign_up(self):
        signup_screen = self.root.get_screen('signup')
        self.username = signup_screen.ids.signup_email.text
        self.root.current = 'dashboard'

    def animate_button(self, button):
        if button.text == "Login":
            self.root.current = 'dashboard'
            img = qrcode.make('Some data here')
            img.save("some_file.png")
        elif button.text == "Sign Up":
            self.root.current = 'dashboard'

    def send(self):
        print("Send button clicked")

    def on_cam_click(self):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_camera_frame, 1.0 / 30.0)

    def load_camera_frame(self, dt):
        ret, frame = self.capture.read()
        if ret:
            ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
            if ret_qr:
                for s, p in zip(decoded_info, points):
                    if s:
                        print(f"QR Code detected: {s}")
                        self.capture.release()
                        Clock.unschedule(self.load_camera_frame)
                        self.root.current = 'success'
                        return
                    else:
                        color = (0, 0, 255)
                    frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
            frame = imutils.resize(frame, width=375, height=200)
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            img = self.root.get_screen('camera').ids.img
            img.texture = image_texture

    def generate_qr(self, amount):
        data = f'{self.username} received {amount}'
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        texture = CoreImage(buf, ext='png').texture
        self.root.get_screen('qr').ids.qr_code_img.texture = texture
        self.root.current = 'qr'

if __name__ == '__main__':
    MyApp().run()
