import unittest
from qr_generator import QRCodeGenerator
from PIL import Image
import os


class TestQRCodeGenerator(unittest.TestCase):
    
    def setUp(self):
        # Setup before each test
        self.qr_gen = QRCodeGenerator(size=10, error_correction=3, fg_color="#000000", bg_color="#FFFFFF")
    
    def test_generate_qr_code(self):
        # Test QR code generation without logo
        img = self.qr_gen.generate("https://example.com")
        self.assertIsInstance(img, Image.Image)
        self.assertGreater(img.size[0], 0)
        self.assertGreater(img.size[1], 0)
        
    def test_generate_qr_code_with_logo(self):
        # Test QR code generation with logo
        logo = Image.new("RGB", (50, 50), (255, 0, 0))  # Red square logo
        img = self.qr_gen.generate("https://example.com", logo_img=logo)
        self.assertIsInstance(img, Image.Image)
        self.assertGreater(img.size[0], 0)
        self.assertGreater(img.size[1], 0)
        
    def test_save_as_svg(self):
        # Test saving the QR code as SVG
        img = self.qr_gen.generate("https://example.com")
        svg_path = "test_qr.svg"
        self.qr_gen.save_as_svg(img, svg_path)
        self.assertTrue(os.path.exists(svg_path))
        os.remove(svg_path)

if __name__ == '__main__':
    unittest.main()
