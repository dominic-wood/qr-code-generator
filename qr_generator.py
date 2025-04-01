import datetime
import qrcode
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

# Function to ensure URL has correct prefix
def format_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # Default to HTTPS
    return url

# Function to generate QR code
def generate_qr():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL!")
        return

    url = format_url(url)  # Fix missing http/https
    fill_color = color_fg_entry.get() or "black"
    back_color = color_bg_entry.get() or "white"
    
    try:
        size = int(size_entry.get() or 10)
        if size < 1 or size > 20:
            messagebox.showwarning("Warning", "Size should be between 1-20. Using default (10).")
            size = 10
    except ValueError:
        messagebox.showwarning("Warning", "Invalid size. Using default (10).")
        size = 10

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    # Save the QR code as 'generated_qr.png'
    global generated_img
    generated_img = img

    # Load image for preview
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk

    # Keep the Save button visible
    save_btn.config(state="normal")

# Function to save QR code with custom filename
def save_qr():
    current_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"QR_Code_{current_date}.png"
    filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                            initialfile=default_filename,
                                            filetypes=[("PNG files", "*.png"),
                                                       ("All Files", "*.*")])
    if filepath:
        generated_img.save(filepath)
        save_btn.config(text="QR Code Saved!", state="normal", bg="Green", fg="black")

        save_btn.after(3000, lambda: save_btn.config(text="Save QR Code", state="disabled"))

# GUI Setup
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x600")
root.resizable(False, False)

# URL Input
tk.Label(root, text="Enter URL:", font=("Arial", 12)).pack(pady=5)
url_entry = tk.Entry(root, width=40, font=("Arial", 12))
url_entry.pack(pady=5)

# Foreground Color
tk.Label(root, text="Foreground Color:", font=("Arial", 12)).pack(pady=5)
color_fg_entry = tk.Entry(root, width=20, font=("Arial", 12))
color_fg_entry.pack(pady=5)
color_fg_entry.insert(0, "black")

# Background Color
tk.Label(root, text="Background Color:", font=("Arial", 12)).pack(pady=5)
color_bg_entry = tk.Entry(root, width=20, font=("Arial", 12))
color_bg_entry.pack(pady=5)
color_bg_entry.insert(0, "white")

# QR Code Size
tk.Label(root, text="Size (1-20):", font=("Arial", 12)).pack(pady=5)
size_entry = tk.Entry(root, width=10, font=("Arial", 12))
size_entry.pack(pady=5)
size_entry.insert(0, "10")

# Generate Button
generate_btn = tk.Button(root, text="Generate QR Code", font=("Arial", 12), command=generate_qr)
generate_btn.pack(pady=10)

# Save Button
save_btn = tk.Button(root, text="Save QR Code", font=("Arial", 12), state="disabled", command=save_qr)
save_btn.pack(pady=10)

# QR Code Display
qr_label = tk.Label(root)
qr_label.pack(pady=10)

# Run GUI
root.mainloop()
