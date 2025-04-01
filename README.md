# QR Code Generator

A simple Python application that generates QR codes from URLs with customisable appearance.

## Features

- Generate QR codes from any URL
- Customize foreground and background colors
- Adjust QR code size (1-20)
- Preview generated QR code
- Save QR code as PNG image with timestamped filename
- User-friendly graphical interface

## Requirements

- Python 3.6+
- Required packages:
  - `qrcode`
  - `pillow` (PIL)
  - `tkinter` (usually included with Python)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/jobbieontheknee/qr-code-generator.git
   cd qr-code-generator
2. Install required packages:
   ```bash
   pip install qrcode pillow
## Usage
1. Run the application
   ```bash
   python qr_generator.py
2. Enter the URL you want to encode
3. Customise apperance
    * Set the foreground colour (default: black)
    * Set the background colour (default: white)
    * Adjust size (1-20, default: 10)
4. Click "Generate QR Code"
5. Save your QR code by clicking "Save QR Code"

## Customisation Options
| Parameter | Description | Default Value |
| :--- | :--- | :--- |
| URL | Website address to encode | -
| Foreground Colour | QR code colour (name or hex value) | black
| Background Colour | Background colour (name of hex value) | white
| Size | Controls QR code density (1-20) | 10|

## Troubleshooting
* "Invalid URL" error: Make sure to include the full URL (e.g., https://example.com)
* Colour not working: Use standard colour names or hex values (e.g., #FF000 for red)
* Size limitations: Values outside 1-20 will be reset to default

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements. 

## License
This project is licenced under the MIT License - see the [LICENSE](https://license/) file for details.

## Acknowledgements
* [QRCode Python Library](https://github.com/lincolnloop/python-qrcode)
* [Pillow (PIL Fork)](https://python-pillow.org/)