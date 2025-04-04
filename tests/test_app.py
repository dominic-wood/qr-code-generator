import unittest
from unittest.mock import MagicMock
from app import QRGeneratorApp  # Importing the app class directly


class TestQRGeneratorApp(unittest.TestCase):
    
    def setUp(self):
        # Mocking tkinter and ttkbootstrap components
        self.root_mock = MagicMock()  # Mocking the root (tkinter window)
        self.app = QRGeneratorApp(self.root_mock)  # Instantiate the app with the mock root
    
    def test_set_content_prefix(self):
        # Test setting content prefix in the URL entry
        self.app.url_entry = MagicMock()  # Mocking the URL entry widget
        self.app.set_content_prefix("https://")  # Calling the method
        # Checking if the delete and insert methods were called correctly
        self.app.url_entry.delete.assert_called_with(0, "end")
        self.app.url_entry.insert.assert_called_with(0, "https://")
    
    def test_update_status(self):
        # Test the update status method
        self.app.update_status("Test Status")  # Calling the method
        # Checking if the status message was set correctly
        self.app.status_var.set.assert_called_with("Status: Test Status")

    def test_apply_template(self):
        # Test applying a template
        self.app.update_color_ui = MagicMock()  # Mocking the color update method
        self.app.apply_template("Default")  # Applying the "Default" template
        # Checking if the color UI update method was called
        self.app.update_color_ui.assert_called()
    
    def test_generate_qr(self):
        # Test QR code generation (mocking dependencies)
        self.app.validate_inputs = MagicMock(return_value=True)  # Mocking the validation method
        self.app.generate_qr()  # Calling the generate_qr method
        # Checking if the status update method was called with the expected message
        self.app.update_status.assert_called_with("Generating QR Code...")
        
if __name__ == '__main__':
    unittest.main()
