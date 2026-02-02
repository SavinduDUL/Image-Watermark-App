import tkinter as tk
from tkinter import filedialog,ttk
from PIL import Image,ImageTk,ImageDraw, ImageFont, ImageEnhance

main_image = None
main_image_tk = None
watermark_image = None
watermark_image_tk = None

class InterFace:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Watermarking App")
        self.window.geometry("1000x600")
        self.window.configure(bg="#f0f0f0")
        
        # Left Frame - Controls
        self.left_frame = tk.Frame(self.window, width=300, bg="#e0e0e0")
        self.left_frame.pack(side="left", fill="y")
        
        # Right Frame - Image Preview
        self.right_frame = tk.Frame(self.window, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True)
        
        # Title Label
        title = tk.Label(self.left_frame, text="Watermark App", bg="#e0e0e0",
        font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        # Upload Button
        upload_btn = tk.Button(
        self.left_frame,
        text="Upload Image",
        command=self.upload_image,
        font=("Arial", 14),
        bg="#562F00",
        fg="white",
        padx=10,
        pady=5
        )
        upload_btn.pack(pady=10)

        # Image Preview Label
        self.preview_label = tk.Label(self.right_frame, bg="white")
        self.preview_label.pack(expand=True)
        
        ## This is the watermark structure
        # Watermark type variable
        self.watermark_type = tk.StringVar(value="text")
        
        # Radio buttons to select type
        text_radio = tk.Radiobutton(self.left_frame, text="Text Watermark", variable=self.watermark_type,
        value="text", bg="#e0e0e0", font=("Arial", 12))
        text_radio.pack(pady=5)


        image_radio = tk.Radiobutton(self.left_frame, text="Image Watermark", variable=self.watermark_type,
        value="image", bg="#e0e0e0", font=("Arial", 12))
        image_radio.pack(pady=5)
                
        # ----- Text Watermark Controls -----
        text_label = tk.Label(self.left_frame, text="Enter Watermark Text:", bg="#e0e0e0",
        font=("Arial", 12))
        text_label.pack(pady=5)


        self.text_entry = tk.Entry(self.left_frame, font=("Arial", 12))
        self.text_entry.pack(pady=5)
        
        # Font size slider
        self.font_size_label = tk.Label(self.left_frame, text="Font Size:", bg="#e0e0e0", font=("Arial", 12))
        self.font_size_label.pack(pady=5)


        self.font_size_slider = tk.Scale(self.left_frame, from_=10, to=100, orient="horizontal", bg="#e0e0e0")
        self.font_size_slider.set(30)
        self.font_size_slider.pack(pady=5)


        # Opacity slider
        self.opacity_label = tk.Label(self.left_frame, text="Opacity (%):", bg="#e0e0e0", font=("Arial", 12))
        self.opacity_label.pack(pady=5)


        self.opacity_slider = tk.Scale(self.left_frame, from_=0, to=100, orient="horizontal", bg="#e0e0e0")
        self.opacity_slider.set(70)
        self.opacity_slider.pack(pady=5)


        # Position dropdown
        self.position_label = tk.Label(self.left_frame, text="Position:", bg="#e0e0e0", font=("Arial", 12))
        self.position_label.pack(pady=5)


        self.position_options = ["Top-left", "Top-right", "Bottom-left", "Bottom-right", "Center"]
        self.position_var = tk.StringVar(value="Bottom-right")
        self.position_menu = ttk.Combobox(self.left_frame, values=self.position_options, textvariable=self.position_var)
        self.position_menu.pack(pady=5)
        
        # Upload watermark image button
        watermark_upload_btn = tk.Button(self.left_frame, text="Upload Watermark Image",
        command=self.upload_watermark_image, font=("Arial", 12),
        bg="#2196F3", fg="white")
        watermark_upload_btn.pack(pady=10)


        # Watermark preview
        self.watermark_preview_label = tk.Label(self.left_frame, bg="#e0e0e0")
        self.watermark_preview_label.pack(pady=5)
        
        
        # Save Button
        self.save_btn = tk.Button(self.left_frame, text="Save Image", command=self.save_image,
        font=("Arial", 14), bg="#4CAF50", fg="white")
        self.save_btn.pack(pady=15)
    
         # Apply Watermark Button
        self.apply_btn = tk.Button(self.left_frame, text="Apply Watermark", command=self.apply_watermark,
        font=("Arial", 14), bg="#FF9800", fg="white")
        self.apply_btn.pack(pady=15)
        # Start the window
        self.window.mainloop()


    def upload_image(self):
        global main_image, main_image_tk
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
            )
        
        main_image = Image.open(file_path)
        
        preview_image = main_image.copy()
        preview_image.thumbnail((600, 500))
        
        main_image_tk = ImageTk.PhotoImage(preview_image)
        
       # Update preview
        self.preview_label.config(image=self.main_image_tk)
        self.preview_label.image = self.main_image_tk
        
        
     # Upload watermark image button
    def upload_watermark_image(self):
        global watermark_image, watermark_image_tk
        file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
                )
        if file_path:
            self.watermark_image = Image.open(file_path)
            
            # optional: scale for preview
            self.watermark_image.thumbnail((150, 150))
            self.watermark_image_tk = ImageTk.PhotoImage(watermark_image)
            self.watermark_preview_label.config(image=watermark_image_tk)
            self.watermark_preview_label.image = watermark_image_tk

    def apply_watermark(self):
        global main_image, main_image_tk
        if main_image is None:
                return
            
        #making a copy of the original image for preview
        watermarked = main_image.copy()
        
        #text watermark
        if self.watermark_type.get() == "text":
            text = self.text_entry.get()
            if text:
                draw = ImageDraw.Draw(watermarked)
                font_size = self.font_size_slider.get()
                
                # Use a default font
                font = ImageFont.truetype("arial.ttf", font_size)
                
                # Text size
                text_width, text_height = draw.textsize(text, font=font)
            
                #position
                pos = self.position_var.get()
                if pos == "Top-left":
                        x, y = 10, 10
                elif pos == "Top-right":
                        x = watermarked.width - text_width - 10
                        y = 10
                elif pos == "Bottom-left":
                        x = 10
                        y = watermarked.height - text_height - 10
                elif pos == "Bottom-right":
                        x = watermarked.width - text_width - 10
                        y = watermarked.height - text_height - 10
                elif pos == "Center":
                        x = (watermarked.width - text_width)//2
                        y = (watermarked.height - text_height)//2
                        
                        # Apply opacity
                opacity = self.opacity_slider.get() / 100
                # Create transparent layer ## check whether self should come with the watermarked
                text_layer = Image.new("RGBA", watermarked.size, (0,0,0,0))
                text_draw = ImageDraw.Draw(text_layer)
                text_draw.text((x, y), text, font=font, fill=(255,255,255,int(255*opacity)))
                watermarked = Image.alpha_composite(watermarked.convert("RGBA"), text_layer)

        # -------- Image Watermark --------
        elif self.watermark_type.get() == "image" and watermark_image:
                wm = watermark_image.copy().convert("RGBA")
                # Resize based on scale slider if you want (optional)
                # wm = wm.resize((int(wm.width * 0.5), int(wm.height * 0.5)))
                # Apply opacity
                opacity = self.opacity_slider.get() / 100
                alpha = wm.split()[3]
                alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
                wm.putalpha(alpha)

                # Position
                pos = self.position_var.get()
                if pos == "Top-left":
                    x, y = 10, 10
                elif pos == "Top-right":
                    x = watermarked.width - wm.width - 10
                    y = 10
                elif pos == "Bottom-left":
                    x = 10
                    y = watermarked.height - wm.height - 10
                elif pos == "Bottom-right":
                    x = watermarked.width - wm.width - 10
                    y = watermarked.height - wm.height - 10
                elif pos == "Center":
                    x = (watermarked.width - wm.width)//2
                    y = (watermarked.height - wm.height)//2

                # Paste watermark
                watermarked.paste(wm, (x, y), wm)

                # Update preview
                preview_image = watermarked.copy()
                preview_image.thumbnail((600, 500))
                main_image_tk = ImageTk.PhotoImage(preview_image)
                self.preview_label.config(image=main_image_tk)
                self.preview_label.image = main_image_tk

               



    def save_image(self):
        global main_image_tk, main_image

        if main_image is None:
            return


        file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                )
        if file_path:
            final_image = main_image.copy()
            if self.watermark_type.get() == "text":
                text = self.text_entry.get()
                if text:
                    draw = ImageDraw.Draw(final_image)
                    font_size = self.font_size_slider.get()
                    font = ImageFont.truetype("arial.ttf", font_size)
                    text_width, text_height = draw.textsize(text, font=font)
                    pos = self.position_var.get()
                if pos == "Top-left":
                    x, y = 10, 10
                elif pos == "Top-right":
                    x = final_image.width - text_width - 10
                    y = 10
                elif pos == "Bottom-left":
                    x = 10
                    y = final_image.height - text_height - 10
                elif pos == "Bottom-right":
                    x = final_image.width - text_width - 10
                    y = final_image.height - text_height - 10
                elif pos == "Center":
                    x = (final_image.width - text_width)//2
                    y = (final_image.height - text_height)//2

                opacity = self.opacity_slider.get() / 100
                text_layer = Image.new("RGBA", final_image.size, (0,0,0,0))
                text_draw = ImageDraw.Draw(text_layer)
                text_draw.text((x, y), text, font=font, fill=(255,255,255,int(255*opacity)))
                final_image = Image.alpha_composite(final_image.convert("RGBA"), text_layer)

            # Image watermark
            elif self.watermark_type.get() == "image" and watermark_image:
                wm = watermark_image.copy().convert("RGBA")
                opacity = self.opacity_slider.get() / 100
                alpha = wm.split()[3]
                alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
                wm.putalpha(alpha)


            pos = self.position_var.get()
            if pos == "Top-left":
                x, y = 10, 10
            elif pos == "Top-right":
                x = final_image.width - wm.width - 10
                y = 10
            elif pos == "Bottom-left":
                x = 10
                y = final_image.height - wm.height - 10
            elif pos == "Bottom-right":
                x = final_image.width - wm.width - 10
                y = final_image.height - wm.height - 10
            elif pos == "Center":
                x = (final_image.width - wm.width)//2
                y = (final_image.height - wm.height)//2
            
            # Save final image
            final_image.convert("RGB").save(file_path)
            tk.messagebox.showinfo("Saved", f"Image saved successfully at:\n{file_path}")

            final_image.paste(wm, (x, y), wm)

           


#create an instance
tk_interface=InterFace()
