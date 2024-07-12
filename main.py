import flet as ft
import qrcode
import io
from PIL import Image
import base64

class QRCodeGeneratorApp:
    def __init__(self, page):
        self.page = page
        self.qr_img = None

        self.entry = ft.TextField(label="Digite o texto para gerar o QR Code", width=300)
        self.generate_btn = ft.ElevatedButton(text="Gerar QR Code", on_click=self.generate_qr_code)
        self.qr_image = ft.Image()
        self.save_btn = ft.ElevatedButton(text="Salvar  QR Code", on_click=self.save_qr_code, disabled=True)

        self.file_picker = ft.FilePicker(on_result=self.save_file_result)
        self.page.overlay.append(self.file_picker)

        self.page.add(
            ft.Column(
                [
                    self.entry,
                    self.generate_btn,
                    self.qr_image,
                    self.save_btn
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        # Gerar QR Code padrão
        self.generate_default_qr_code()

    def generate_default_qr_code(self):
        data = "Default QR Code"
        self.generate_qr_code_from_data(data)

    def generate_qr_code(self, e):
        data = self.entry.value
        self.generate_qr_code_from_data(data)

    def generate_qr_code_from_data(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        self.qr_img = qr.make_image(fill_color="black", back_color="white")
        img_io = io.BytesIO()
        self.qr_img.save(img_io, 'PNG')
        img_io.seek(0)

        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        self.qr_image.src_base64 = img_base64
        self.qr_image.update()

        self.save_btn.disabled = False
        self.page.update()

    def save_qr_code(self, e):
        self.file_picker.save_file(
            dialog_title="Save QR Code",
            file_name="qrcode.png",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=['png','jpg'] 
        )



    def save_file_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            img_io = io.BytesIO()
            self.qr_img.save(img_io, format='PNG')
            with open(e.path, "wb") as f:
                f.write(img_io.getvalue())
            self.save_btn.disabled = True
            self.page.update()

def main(page: ft.Page):
    page.title = "QR Code Generator"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.window.width = 400
    page.window.height = 600
    app = QRCodeGeneratorApp(page)
    page.update()
ft.app(target=main)
