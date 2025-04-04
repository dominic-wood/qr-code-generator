import datetime
import os
import webbrowser
from io import BytesIO

import ttkbootstrap as tb
from tkinter import filedialog, messagebox, colorchooser
from tkinter.ttk import Notebook
from PIL import Image, ImageTk, ImageDraw
from qr_generator import QRCodeGenerator, ERROR_CORRECTION_LEVELS, DEFAULT_FG, DEFAULT_BG


class QRGeneratorApp:
    def __init__(self, root: tb.Window) -> None:
        self.root = root
        self.root.title("QR Code Studio")
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        self.root.minsize(700, 800)

        icon_image = Image.open("assets/qr-code-app.png")
        self.root.iconphoto(True, ImageTk.PhotoImage(icon_image))
        self.history_data = {}

        # Instance variables
        self.generated_img = None
        self.logo_img = None
        self.logo_path = None
        self.last_save_dir = None
        self.current_qr_data = None

        self.templates = {
            "Default": {"fg": "#000000", "bg": "#FFFFFF", "shape": "square"},
            "Dark Mode": {"fg": "#FFFFFF", "bg": "#121212", "shape": "square"},
            "Colorful": {"fg": "#FF6B6B", "bg": "#4ECDC4", "shape": "rounded"},
            "Professional": {"fg": "#2C3E50", "bg": "#ECF0F1", "shape": "square"},
            "Gradient": {"fg": "#6A11CB", "bg": "#2575FC", "shape": "circle"}
        }

        self.setup_ui()

    def setup_ui(self) -> None:
        """Setup the modern UI components."""
        self.notebook = Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        generator_tab = tb.Frame(self.notebook)
        self.notebook.add(generator_tab, text="Generator")

        # Header with icon and title
        header = tb.Frame(generator_tab)
        header.pack(fill="x", pady=(0, 15))
        self.app_icon = tb.Label(header, text="🔳", font=("Arial", 24))
        self.app_icon.pack(side="left", padx=5)
        tb.Label(header, text="QR Code Studio", font=("Segoe UI", 18, "bold"), bootstyle="dark").pack(side="left")

        # Main content frames
        content_frame = tb.Frame(generator_tab, bootstyle="light")
        content_frame.pack(fill="both", expand=True)

        left_panel = tb.Frame(content_frame, width=400, padding=15)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)

        right_panel = tb.Frame(content_frame, padding=15)
        right_panel.pack(side="right", fill="both", expand=True)

        # URL Input
        url_frame = tb.LabelFrame(left_panel, text="CONTENT", bootstyle="info", padding=10)
        url_frame.pack(fill="x", pady=(0, 15))
        self.url_entry = tb.Entry(url_frame, font=("Segoe UI", 11), bootstyle="light")
        self.url_entry.pack(fill="x", pady=5, ipady=5)
        self.url_entry.insert(0, "https://")

        quick_btns = tb.Frame(url_frame)
        quick_btns.pack(fill="x", pady=(5, 0))
        btn_width = 5
        tb.Button(quick_btns, text="URL", command=lambda: self.set_content_prefix("https://"),
                  bootstyle="outline", width=btn_width).pack(side="left", padx=2)
        tb.Button(quick_btns, text="Email", command=lambda: self.set_content_prefix("mailto:"),
                  bootstyle="outline", width=btn_width).pack(side="left", padx=2)
        tb.Button(quick_btns, text="Phone", command=lambda: self.set_content_prefix("tel:"),
                  bootstyle="outline", width=btn_width).pack(side="left", padx=2)
        tb.Button(quick_btns, text="WiFi", command=self.add_wifi_config,
                  bootstyle="outline", width=btn_width).pack(side="left", padx=2)

        # Design Settings
        settings_frame = tb.LabelFrame(left_panel, text="DESIGN", bootstyle="info", padding=10)
        settings_frame.pack(fill="x", pady=(0, 15))

        tb.Label(settings_frame, text="Templates:", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 5))
        template_frame = tb.Frame(settings_frame)
        template_frame.pack(fill="x", pady=(0, 10))
        self.selected_template = tb.StringVar(value="Default")
        template_btn_width = 8
        for template in self.templates:
            tb.Radiobutton(
                template_frame,
                text=template,
                value=template,
                variable=self.selected_template,
                command=lambda t=template: self.apply_template(t),
                bootstyle="info-toolbutton",
                width=template_btn_width,
            ).pack(side="left", padx=2, pady=2)

        tb.Label(settings_frame, text="Size & Error Correction:", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 5))
        size_ec_frame = tb.Frame(settings_frame)
        size_ec_frame.pack(fill="x", pady=5)
        tb.Label(size_ec_frame, text="Size:", font=("Segoe UI", 9)).pack(side="left", padx=5)
        self.size_slider = tb.Scale(size_ec_frame, from_=1, to=20, value=10, bootstyle="info")
        self.size_slider.pack(side="left", fill="x", expand=True, padx=5)
        tb.Label(size_ec_frame, text="EC:", font=("Segoe UI", 9)).pack(side="left", padx=(10, 5))
        self.ec_combo = tb.Combobox(
            size_ec_frame, values=list(ERROR_CORRECTION_LEVELS.keys()),
            state="readonly", font=("Segoe UI", 9), width=10
        )
        self.ec_combo.pack(side="left", padx=5)
        self.ec_combo.set("High (25%)")

        # Color Pickers
        colors_frame = tb.Frame(settings_frame)
        colors_frame.pack(fill="x", pady=10)
        # Foreground
        fg_frame = tb.Frame(colors_frame)
        fg_frame.pack(side="left", fill="x", expand=True, padx=5)
        tb.Label(fg_frame, text="Foreground:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        fg_color_frame = tb.Frame(fg_frame)
        fg_color_frame.pack(fill="x", pady=2)
        self.color_fg_entry = tb.Entry(fg_color_frame, width=10, font=("Segoe UI", 9))
        self.color_fg_entry.pack(side="left", fill="x", expand=True)
        self.color_fg_entry.insert(0, DEFAULT_FG)
        self.fg_color_btn = tb.Button(
            fg_color_frame,
            command=lambda: self.choose_color(self.color_fg_entry, self.fg_color_btn),
            width=2
        )
        self.fg_color_btn.pack(side="left", padx=5)
        # Background
        bg_frame = tb.Frame(colors_frame)
        bg_frame.pack(side="left", fill="x", expand=True, padx=5)
        tb.Label(bg_frame, text="Background:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        bg_color_frame = tb.Frame(bg_frame)
        bg_color_frame.pack(fill="x", pady=2)
        self.color_bg_entry = tb.Entry(bg_color_frame, width=10, font=("Segoe UI", 9))
        self.color_bg_entry.pack(side="left", fill="x", expand=True)
        self.color_bg_entry.insert(0, DEFAULT_BG)
        self.bg_color_btn = tb.Button(
            bg_color_frame,
            command=lambda: self.choose_color(self.color_bg_entry, self.bg_color_btn),
            width=2,
            bootstyle="outline-info"
        )
        self.bg_color_btn.pack(side="left", padx=5)

        # Logo Options
        logo_frame = tb.LabelFrame(settings_frame, text="LOGO", bootstyle="info", padding=10)
        logo_frame.pack(fill="x", pady=(10, 0))
        self.logo_btn = tb.Button(logo_frame, text="Add Logo", command=self.add_logo, bootstyle="outline-info", width=10)
        self.logo_btn.pack(side="left", padx=2)
        self.remove_logo_btn = tb.Button(logo_frame, text="Remove", command=self.remove_logo, state="disabled", bootstyle="outline-danger", width=10)
        self.remove_logo_btn.pack(side="left", padx=2)

        # Action Buttons
        action_frame = tb.Frame(left_panel)
        action_frame.pack(fill="x", pady=(10, 0))
        action_btn_width = 10
        self.generate_btn = tb.Button(action_frame, text="Generate", command=self.generate_qr, bootstyle="success-outline", width=action_btn_width)
        self.generate_btn.pack(side="left", padx=2)
        self.save_btn = tb.Button(action_frame, text="Save", command=self.save_qr, state="disabled", bootstyle="primary-outline", width=action_btn_width)
        self.save_btn.pack(side="left", padx=2)
        self.copy_btn = tb.Button(action_frame, text="Copy", command=self.copy_to_clipboard, state="disabled", bootstyle="info-outline", width=action_btn_width)
        self.copy_btn.pack(side="left", padx=2)

        # Right Panel: Preview & History
        preview_frame = tb.LabelFrame(right_panel, text="PREVIEW", bootstyle="info", padding=15)
        preview_frame.pack(fill="both", expand=True)
        self.qr_canvas = tb.Canvas(preview_frame, width=250, height=250, bg="white", relief="ridge", bd=0, highlightthickness=0)
        self.qr_canvas.pack(pady=10)
        detail_frame = tb.Frame(preview_frame)
        detail_frame.pack(fill="x", pady=(5, 0))
        self.qr_size_label = tb.Label(detail_frame, text="Size: -", font=("Segoe UI", 9))
        self.qr_size_label.pack(side="left", padx=5)
        self.qr_type_label = tb.Label(detail_frame, text="Type: -", font=("Segoe UI", 9))
        self.qr_type_label.pack(side="left", padx=5)
        self.qr_date_label = tb.Label(detail_frame, text="Generated: -", font=("Segoe UI", 9))
        self.qr_date_label.pack(side="left", padx=5)
        test_frame = tb.Frame(preview_frame)
        test_frame.pack(fill="x", pady=(10, 0))
        tb.Button(test_frame, text="Test QR Code", command=self.test_qr_code, bootstyle="warning-outline").pack(side="left", padx=5)

        history_frame = tb.LabelFrame(right_panel, text="HISTORY", bootstyle="info", padding=10)
        history_frame.pack(fill="both", expand=True, pady=(5, 0))
        self.history_listbox = tb.Treeview(history_frame, columns=("date", "content"), show="headings", height=4)
        self.history_listbox.heading("date", text="Date")
        self.history_listbox.heading("content", text="Content")
        self.history_listbox.column("date", width=100)
        self.history_listbox.column("content", width=200)
        self.history_listbox.pack(fill="both", expand=True)
        self.history_listbox.bind("<Double-1>", self.on_history_item_double_click)

        self.status_frame = tb.Frame(self.root, bootstyle="light")
        self.status_frame.pack(fill="x", padx=10, pady=(0, 5))
        self.status_var = tb.StringVar()
        self.status_bar = tb.Label(self.status_frame, textvariable=self.status_var, font=("Segoe UI", 9), bootstyle="inverse-light")
        self.status_bar.pack(side="left", fill="x", expand=True)
        self.progress = tb.Progressbar(self.status_frame, mode="determinate", bootstyle="info-striped")
        self.progress.pack(side="right", padx=(5, 0))
        self.update_status("Ready to generate QR codes")

    def set_content_prefix(self, prefix: str) -> None:
        """Set the content prefix for the URL entry."""
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, prefix)

    def update_color_ui(self, color: str, entry_widget: tb.Entry, button_widget: tb.Button) -> None:
        entry_widget.delete(0, "end")
        entry_widget.insert(0, color)
        self.update_color_button_style(color)
        self.update_color_swatch(button_widget, color)

    def choose_color(self, entry_widget: tb.Entry, button_widget: tb.Button) -> None:
        initial_color = entry_widget.get()
        color_tuple = colorchooser.askcolor(title="Choose Color", initialcolor=initial_color)
        if color_tuple[1]:
            self.update_color_ui(color_tuple[1], entry_widget, button_widget)

    def update_color_button_style(self, color: str) -> None:
        style = tb.Style()
        style_name = f"{color}.TButton"
        if not style.lookup(style_name, "background"):
            style.configure(style_name, background=color, foreground=color, borderwidth=1, focusthickness=0, relief="solid")

    def update_color_swatch(self, button: tb.Button, color: str) -> None:
        try:
            swatch = Image.new("RGB", (16, 16), color)
            swatch_photo = ImageTk.PhotoImage(swatch)
            button.swatch_image = swatch_photo
            button.config(image=swatch_photo, compound="left", text="")
        except Exception as e:
            print(f"Error creating color swatch: {e}")
            button.config(text=color)

    def apply_template(self, template_name: str) -> None:
        template = self.templates.get(template_name)
        if template:
            self.update_color_ui(template["fg"], self.color_fg_entry, self.fg_color_btn)
            self.update_color_ui(template["bg"], self.color_bg_entry, self.bg_color_btn)
            self.update_status(f"Template applied: {template_name}")

    def update_status(self, message: str) -> None:
        self.status_var.set(f"Status: {message}")

    def add_wifi_config(self) -> None:
        wifi_window = tb.Toplevel(self.root)
        wifi_window.title("WiFi Configuration")
        wifi_window.geometry("400x300")
        tb.Label(wifi_window, text="WiFi Network Configuration", font=("Segoe UI", 12)).pack(pady=10)

        form_frame = tb.Frame(wifi_window)
        form_frame.pack(pady=10, padx=20, fill="x")
        tb.Label(form_frame, text="SSID:").grid(row=0, column=0, sticky="e", pady=5)
        ssid_entry = tb.Entry(form_frame)
        ssid_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        tb.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5)
        password_entry = tb.Entry(form_frame, show="*")
        password_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        tb.Label(form_frame, text="Security:").grid(row=2, column=0, sticky="e", pady=5)
        security_combo = tb.Combobox(form_frame, values=["WPA", "WEP", "None"])
        security_combo.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        security_combo.set("WPA")

        def apply_wifi_config() -> None:
            ssid = ssid_entry.get()
            password = password_entry.get()
            security = security_combo.get()
            if not ssid:
                messagebox.showerror("Error", "SSID is required!")
                return
            if security != "None" and not password:
                messagebox.showerror("Error", "Password is required for secured networks!")
                return
            wifi_config = f"WIFI:T:{security};S:{ssid};P:{password};;"
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, wifi_config)
            wifi_window.destroy()

        btn_frame = tb.Frame(wifi_window)
        btn_frame.pack(pady=10)
        tb.Button(btn_frame, text="Cancel", command=wifi_window.destroy, bootstyle="danger-outline").pack(side="left", padx=5)
        tb.Button(btn_frame, text="Apply", command=apply_wifi_config, bootstyle="success-outline").pack(side="left", padx=5)

    def format_url(self, url: str) -> str:
        url = url.strip()
        if not url.startswith(("http://", "https://", "mailto:", "tel:", "sms:", "WIFI:")):
            if "@" in url and "." in url:
                return f"mailto:{url}"
            return f"https://{url}"
        return url

    def add_logo(self) -> None:
        filepath = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.svg"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                from PIL import Image  # Ensure PIL.Image is imported
                self.logo_img = Image.open(filepath)
                self.logo_path = filepath
                self.remove_logo_btn.config(state="normal")
                self.update_status(f"Logo loaded: {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def remove_logo(self) -> None:
        self.logo_img = None
        self.logo_path = None
        self.remove_logo_btn.config(state="disabled")
        self.update_status("Logo removed")

    def validate_inputs(self) -> bool:
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL or text content!")
            return False
        try:
            _ = self.color_fg_entry.get() or DEFAULT_FG
            _ = self.color_bg_entry.get() or DEFAULT_BG
        except Exception:
            messagebox.showerror("Error", "Invalid color values!")
            return False
        return True

    def generate_qr(self) -> None:
        if not self.validate_inputs():
            return

        self.update_status("Generating QR Code...")
        self.progress["value"] = 30
        self.root.update_idletasks()

        try:
            url = self.format_url(self.url_entry.get())
            size = int(self.size_slider.get())
            ec_level = ERROR_CORRECTION_LEVELS[self.ec_combo.get()]
            fg_color = self.color_fg_entry.get() or DEFAULT_FG
            bg_color = self.color_bg_entry.get() or DEFAULT_BG

            # Use the QRCodeGenerator module
            from qr_generator import QRCodeGenerator  # Import here if needed
            qr_gen = QRCodeGenerator(size=size, error_correction=ec_level, fg_color=fg_color, bg_color=bg_color)
            img = qr_gen.generate(url, logo_img=self.logo_img)
            self.generated_img = img
            self.current_qr_data = url

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            content_preview = url[:30] + "..." if len(url) > 30 else url
            item_id = self.history_listbox.insert("", "end", values=(timestamp, content_preview))
            self.history_data[item_id] = {"image": self.generated_img.copy(), "content": url}

            self.update_qr_preview(img)
            self.save_btn.config(state="normal")
            self.copy_btn.config(state="normal")
            self.progress["value"] = 100
            self.update_status("QR Code generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
            self.progress["value"] = 0
            self.update_status("Error generating QR Code")

    def on_history_item_double_click(self, event) -> None:
        selected_items = self.history_listbox.selection()
        if selected_items:
            item_id = selected_items[0]
            history_item = self.history_data.get(item_id)
            if history_item:
                img = history_item["image"]
                self.generated_img = img  # update current image if needed
                self.current_qr_data = history_item["content"]
                self.update_qr_preview(img)
                self.update_status("Recalled QR code from history.")

    def update_qr_preview(self, img) -> None:
        self.qr_canvas.delete("all")
        canvas_width = self.qr_canvas.winfo_width()
        canvas_height = self.qr_canvas.winfo_height()
        preview_size = min(canvas_width, canvas_height) - 20
        preview_img = img.resize((preview_size, preview_size), Image.Resampling.LANCZOS)
        self.qr_preview_img = ImageTk.PhotoImage(preview_img)
        x_pos = (canvas_width - preview_size) // 2
        y_pos = (canvas_height - preview_size) // 2
        self.qr_canvas.create_image(x_pos, y_pos, image=self.qr_preview_img, anchor="nw")
        self.qr_size_label.config(text=f"Size: {img.size[0]}x{img.size[1]}")
        qr_type = "URL" if self.current_qr_data and self.current_qr_data.startswith("http") else "Text"
        self.qr_type_label.config(text=f"Type: {qr_type}")
        self.qr_date_label.config(text=f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

    def save_qr(self) -> None:
        if not self.generated_img:
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        initial_dir = self.last_save_dir if self.last_save_dir else None
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=f"QR_Code_{timestamp}",
            initialdir=initial_dir,
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("SVG files", "*.svg"),
                ("PDF files", "*.pdf"),
                ("All Files", "*.*"),
            ],
        )
        if filepath:
            try:
                if filepath.lower().endswith(".svg"):
                    from qr_generator import QRCodeGenerator
                    qr_gen = QRCodeGenerator(bg_color=self.color_bg_entry.get() or DEFAULT_BG)
                    qr_gen.save_as_svg(self.generated_img, filepath)
                else:
                    self.generated_img.save(filepath)
                self.last_save_dir = os.path.dirname(filepath)
                original_text = self.save_btn.cget("text")
                self.save_btn.config(text="Saved!", bootstyle="success")
                self.update_status(f"QR Code saved to: {os.path.basename(filepath)}")
                self.save_btn.after(3000, lambda: self.save_btn.config(text=original_text, bootstyle="primary-outline"))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
                self.update_status("Error saving QR Code")

    def copy_to_clipboard(self) -> None:
        if self.generated_img:
            try:
                output = BytesIO()
                self.generated_img.save(output, format="PNG")
                data = output.getvalue()
                output.close()
                self.root.clipboard_clear()
                self.root.clipboard_append(data)
                self.update_status("QR Code copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")

    def test_qr_code(self) -> None:
        if not self.generated_img or not self.current_qr_data:
            messagebox.showwarning("Warning", "No QR code generated to test!")
            return

        if self.current_qr_data.startswith(("http://", "https://")):
            try:
                webbrowser.open(self.current_qr_data)
                self.update_status(f"Opening: {self.current_qr_data}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open URL: {str(e)}")
        else:
            messagebox.showinfo("QR Content", f"QR Code contains:\n\n{self.current_qr_data}")


if __name__ == "__main__":
    root = tb.Window(themename="yeti")
    app = QRGeneratorApp(root)
    root.mainloop()
