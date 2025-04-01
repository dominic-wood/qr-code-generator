import datetime
import qrcode
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

DEFAULT_SIZE = 10
DEFAULT_FG = "black"
DEFAULT_BG = "white"

def format_url(url):
    """Ensure URL has correct http/https prefix."""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return "https://" + url  # Default to HTTPS
    return url

def generate_qr():
    """Generate QR code from user input."""
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL!")
        return

    try:
        size = int(size_entry.get() or DEFAULT_SIZE)
        if not 1 <= size <= 20:
            messagebox.showwarning("Warning", "Size should be between 1-20. Using default.")
            size = DEFAULT_SIZE
    except ValueError:
        messagebox.showwarning("Warning", "Invalid size. Using default.")
        size = DEFAULT_SIZE

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=2
    )
    qr.add_data(format_url(url))
    qr.make(fit=True)
    
    img = qr.make_image(
        fill_color=color_fg_entry.get() or DEFAULT_FG,
        back_color=color_bg_entry.get() or DEFAULT_BG
    ).convert("RGB")

    # Update global reference and display
    global generated_img
    generated_img = img
    
    # Display preview
    preview_img = img.resize((200, 200), Image.Resampling.LANCZOS)
    qr_label.img_tk = ImageTk.PhotoImage(preview_img)
    qr_label.config(image=qr_label.img_tk)
    
    save_btn.config(state="normal")

def save_qr():
    """Save QR code with timestamped filename."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        initialfile=f"QR_Code_{timestamp}.png",
        filetypes=[("PNG files", "*.png"), ("All Files", "*.*")]
    )
    
    if filepath:
        generated_img.save(filepath)
        save_btn.config(text="Saved!", state="normal", bg="green")
        save_btn.after(3000, lambda: save_btn.config(
            text="Save QR Code",
            bg=root.cget("bg"),
            state="normal"
        ))

# GUI Setup
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x600")
root.resizable(False, False)

# Create consistent style elements
label_style = {"font": ("Arial", 12), "pady": 5}
entry_style = {"font": ("Arial", 12)}
button_style = {"font": ("Arial", 12), "pady": 5}

# URL Input
tk.Label(root, text="Enter URL:", **label_style).pack()
url_entry = tk.Entry(root, **entry_style, width=40)
url_entry.pack()

# Color Settings
for label, default in [("Foreground Color:", DEFAULT_FG), ("Background Color:", DEFAULT_BG)]:
    tk.Label(root, text=label, **label_style).pack()
    entry = tk.Entry(root, **entry_style, width=20)
    entry.pack()
    entry.insert(0, default)
    if "Foreground" in label:
        color_fg_entry = entry
    else:
        color_bg_entry = entry

# Size Input
tk.Label(root, text="Size (1-20):", **label_style).pack()
size_entry = tk.Entry(root, **entry_style, width=10)
size_entry.pack()
size_entry.insert(0, str(DEFAULT_SIZE))

# Action Buttons
generate_btn = tk.Button(root, text="Generate QR Code", command=generate_qr, **button_style)
generate_btn.pack()

save_btn = tk.Button(root, text="Save QR Code", command=save_qr, state="disabled", **button_style)
save_btn.pack()

# QR Code Display
qr_label = tk.Label(root)
qr_label.pack(pady=10)

root.mainloop()