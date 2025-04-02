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


## Project Structure
The project is organised into two main modules:
- `qr-generator.py`: Contains the core logic for generating QR codes usign the `qrcode` and `pillow` libraries, along with a simplified SVG export function.
- `app.py`: Houses the graphical user interface with `tkinter` and `ttkbootstrap`. This module manages user interactions, including content prefix management, design customisation, history mangagment, and clipboard operations.

## 🖼️ Interface

![QR Code Generator Preview](<qr_preview.png>)

## Requirements

- Python 3.6+
- Required packages:
  - `qrcode`
  - `pillow`
  - `ttkbootsrap`
  - `svgwrite`
  - `requests` 

- **NOTE**: `tkinter` is usually bunded with Python. For enhanced clipboard functionality on Windows, consider installing `pywin32`. 

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/jobbieontheknee/qr-code-generator.git
   cd qr-code-generator
   ```
2. Install required packages:

   ```bash
   pip install qrcode pillow ttkbootstrap svgwrite requests
   ```
   *Optional (for clipboard support on Windows)*
   ```bash
   pip install pywin32
   ```

## Usage
1. Run the application

   ```bash
   python app.py
   ```
2. **Enter Content**
    - Type or paste the content you want to encode.
    - Use the quick buttons to clear the text box and insert the correct prefic (e.g., `https://`, `mailto:`, `tel:`) or configure WiFi credentials.
3. **Customise Appearance**
    - Adjust foreground and background colours using the visual colour pickers.
    - Set QR size (1-20) and error correction level.
    - Optionally select a built-in template or upload a logo.
4. **Generate and Preview**
   - Click **Generate** to preview the QR code in the live preview panel.
   - The preview panel displays additional metadata such as size and the generation timestamp.  
5. **Save, Copy or Test**
   - Save the QR code as PNG, JPEG, SVG or PDF.
   - Copy the QR code image to the clipboard. 
   - Double-click a history entry to recall a previously generated QR code.
   - Use the **Test QR Code** button to open the URL in your browser or display the content.

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
- **"Invalid URL" error**: Ensure full protocol is included (e.g. `https://example.com`)
- **Colour not displaying properly**: Use valid hex values (e.g. `#FF0000`) or colour picker
- **QR not displaying logo**: Ensure the image is a supported format (PNG, JPG, BMP, etc.)
- **Copy to clipboard fails**: Clipboard support may depend on OS and Python version

## Contributing
Contributions are welcome! Feel free to open issues, suggest features, or submit pull requests.

## License
This project is licenced under the MIT License - see the [LICENSE](https://license/) file for details.

## Acknowledgements
* [QRCode Python Library](https://github.com/lincolnloop/python-qrcode)
* [Pillow (PIL Fork)](https://python-pillow.org/)
* [ttkbootstap](https://github.com/israel-dryer/ttkbootstrap)
* [svgwrite](https://github.com/mozman/svgwrite)