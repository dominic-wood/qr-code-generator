import qrcode
from PIL import Image, ImageDraw
import svgwrite

DEFAULT_FG = "#000000"
DEFAULT_BG = "#FFFFFF"

ERROR_CORRECTION_LEVELS = {
    "Low (7%)": qrcode.constants.ERROR_CORRECT_L,
    "Medium (15%)": qrcode.constants.ERROR_CORRECT_M,
    "High (25%)": qrcode.constants.ERROR_CORRECT_Q,
    "Highest (30%)": qrcode.constants.ERROR_CORRECT_H,
}

class QRCodeGenerator:
    def __init__(self, size: int = 10, error_correction: int = qrcode.constants.ERROR_CORRECT_H,
                 fg_color: str = DEFAULT_FG, bg_color: str = DEFAULT_BG) -> None:
        self.size = size
        self.error_correction = error_correction
        self.fg_color = fg_color
        self.bg_color = bg_color

    def generate(self, data: str, logo_img: Image.Image | None = None) -> Image.Image:
        """
        Generate a QR code image with optional logo overlay.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=self.error_correction,
            box_size=self.size,
            border=2
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.fg_color, back_color=self.bg_color).convert("RGB")

        if logo_img:
            logo_size = min(img.size) // 4
            logo = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
            mask = Image.new("L", logo.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)
            img.paste(logo, pos, mask)

        return img

    def save_as_svg(self, img: Image.Image, filepath: str) -> None:
        """
        Save a simplified SVG version of the QR code.
        Note: This is a simplified export. For a detailed vector export,
        further logic is required to draw each QR module.
        """
        dwg = svgwrite.Drawing(filepath, size=(f"{img.width}px", f"{img.height}px"))
        dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill=self.bg_color))
        dwg.save()
