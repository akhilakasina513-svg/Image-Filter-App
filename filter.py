import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

# Global variables
original_image = None
filtered_image = None


def show_image(image, label):
    """Display image on Tkinter label"""

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(image)
    img.thumbnail((400, 400))

    img_tk = ImageTk.PhotoImage(img)

    label.config(image=img_tk)
    label.image = img_tk


def upload_image():
    global original_image

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp")
        ]
    )

    if not file_path:
        return

    original_image = cv2.imread(file_path)

    show_image(original_image, original_label)

    filtered_label.config(image="")
    filtered_label.image = None


def apply_grayscale():
    global filtered_image

    if original_image is None:
        messagebox.showerror("Error", "Please upload an image first.")
        return

    filtered_image = cv2.cvtColor(
        original_image,
        cv2.COLOR_BGR2GRAY
    )

    show_image(filtered_image, filtered_label)


def apply_blur():
    global filtered_image

    if original_image is None:
        messagebox.showerror("Error", "Please upload an image first.")
        return

    filtered_image = cv2.GaussianBlur(
        original_image,
        (15, 15),
        0
    )

    show_image(filtered_image, filtered_label)


def apply_edges():
    global filtered_image

    if original_image is None:
        messagebox.showerror("Error", "Please upload an image first.")
        return

    gray = cv2.cvtColor(
        original_image,
        cv2.COLOR_BGR2GRAY
    )

    filtered_image = cv2.Canny(
        gray,
        100,
        200
    )

    show_image(filtered_image, filtered_label)


def save_image():
    global filtered_image

    if filtered_image is None:
        messagebox.showerror("Error", "Apply a filter first.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[
            ("JPEG File", "*.jpg"),
            ("PNG File", "*.png")
        ]
    )

    if save_path:
        cv2.imwrite(save_path, filtered_image)
        messagebox.showinfo(
            "Success",
            "Image saved successfully!"
        )


# Main Window
root = tk.Tk()
root.title("Image Filter App")
root.geometry("1000x600")

# Title
title = tk.Label(
    root,
    text="Image Filter App",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

# Buttons Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

upload_btn = tk.Button(
    button_frame,
    text="Upload Image",
    command=upload_image,
    width=15
)
upload_btn.grid(row=0, column=0, padx=5)

gray_btn = tk.Button(
    button_frame,
    text="Grayscale",
    command=apply_grayscale,
    width=15
)
gray_btn.grid(row=0, column=1, padx=5)

blur_btn = tk.Button(
    button_frame,
    text="Blur",
    command=apply_blur,
    width=15
)
blur_btn.grid(row=0, column=2, padx=5)

edge_btn = tk.Button(
    button_frame,
    text="Edge Detection",
    command=apply_edges,
    width=15
)
edge_btn.grid(row=0, column=3, padx=5)

save_btn = tk.Button(
    button_frame,
    text="Save Image",
    command=save_image,
    width=15
)
save_btn.grid(row=0, column=4, padx=5)

# Image Frame
image_frame = tk.Frame(root)
image_frame.pack(pady=20)

# Original Image Section
original_text = tk.Label(
    image_frame,
    text="Original Image",
    font=("Arial", 12, "bold")
)
original_text.grid(row=0, column=0)

original_label = tk.Label(
    image_frame,
    width=400,
    height=400,
    relief="solid"
)
original_label.grid(row=1, column=0, padx=20)

# Filtered Image Section
filtered_text = tk.Label(
    image_frame,
    text="Filtered Image",
    font=("Arial", 12, "bold")
)
filtered_text.grid(row=0, column=1)

filtered_label = tk.Label(
    image_frame,
    width=400,
    height=400,
    relief="solid"
)
filtered_label.grid(row=1, column=1, padx=20)

root.mainloop()