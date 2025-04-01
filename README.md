# QR Code Studio

A simple Python application for generating QR codes with custom styles, templates, and a preview interface.

## Features

- Generate QR codes from any URL,  email, phone number, or WiFi credentials
- Customise foreground and background colours using a visual colour picker
- Select from built-in design templates (Dark Mode, Colourful, Gradient, etc.)
- Add a logo image to embed in the centre of your QR code
- Adjust QR code size (1-20) and error correction level (Low to Highest)
- Live QR code preview panel with size and metadata display
- Copy QR code to clipboard or save as PNG, JPEG, SVG, or PDF
- Automatically formats content (e.g. adds https://, mailto:, etc.)
- History panel keeps track of recently generated QR codes
- GUI built with ttkbootstrap for a sleek, modern UI

## Requirements

- Python 3.6+
- Required packages:
  - `qrcode`
  - `pillow`
  - `ttkbootsrap`
  - `svgwrite`
  - `requests` 

  You may also require `tkinter` (usually included in Python)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/jobbieontheknee/qr-code-generator.git
   cd qr-code-generator
   ```
2. Install required packages:

   ```bash
   pip install qrcode pillow
   ```

## Usage
1. Run the application

   ```bash
   python qr_generator.py
   ```
2. Enter the content you want to encode:
    - URLs (`https://`)
    - Email addresses (`mailto:`)
    - Phone numbers (`tel:`)
    - WiFi config (use the WiFi button)
3. Customise apperance
    * Foreground/background colours (live swatch shown on button)
    * QR size (1-20)
    * Error correction (Low, Medium, High, Highest)
    * Optional: choose a template or upload a logo
4. Click "**Generate**" to preview the QR code
5. Save, copy, or test your QR code from the preview panel

## Customisation Options
| Parameter | Description | Default Value |
| :--- | :--- | :--- |
| Content | URL, email, phone, or WiFi config | -
| Foreground Colour | QR code colour (visual swatch shown) | `#000000` (black)
| Background Colour | Background colour (visual swatch shown) | `#FFFFFF` (white)
| Size | QR box size (1-20) | 10
| Error Correction | Level of QR code fault tolerance | High (25%)
| Template | Pre-defined style templates | Default
| Logo | Optional image overlay in centre | None |

## Troubleshooting
* **"Invalid URL" error**: Ensure full protocol is included (e.g. `https://example.com`)
* **Colour not displaying properly**: Use valid hex values (e.g. `#FF0000`) or colour picker
* **QR not displaying logo**: Ensure the image is a supported format (PNG, JPG, BMP, etc.)
* **Copy to clipboard fails**: Clipboard support may depend on OS and Python version

## Contributing
Contributions are welcome! Feel free to open issues, suggest features, or submit pull requests.

## License
This project is licenced under the MIT License - see the [LICENSE](https://license/) file for details.

## Acknowledgements
* [QRCode Python Library](https://github.com/lincolnloop/python-qrcode)
* [Pillow (PIL Fork)](https://python-pillow.org/)
* [ttkbootstap](https://github.com/israel-dryer/ttkbootstrap)
* [svgwrite](https://github.com/mozman/svgwrite)