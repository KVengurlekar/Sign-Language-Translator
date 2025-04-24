import os
import speech_recognition as sr
import tkinter as tk
from tkinter import Label, Entry, Button, Toplevel, messagebox, Frame
from PIL import Image, ImageTk, ImageSequence
import threading

# Path where GIFs and letter images are stored
DATABASE_PATH = "C:/Users/Admin/Documents/App/Images"

# Speech-to-Text Class
class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize_speech(self, callback):
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=7)
                text = self.recognizer.recognize_google(audio)
                print("Recognized:", text)
                callback(text)
            except sr.WaitTimeoutError:
                show_error_window("No speech detected. Try again.")
                callback(None)
            except sr.UnknownValueError:
                show_error_window("Could not understand the audio.")
                callback(None)
            except sr.RequestError:
                show_error_window("Speech Recognition API is unavailable.")
                callback(None)

# Text-to-Sign Language Converter
class TextToSignLanguage:
    def __init__(self, image_dir):
        self.image_dir = image_dir

    def get_sign_image(self, word):
        try:
            gif_path = os.path.join(self.image_dir, f"{word}.gif")
            if os.path.exists(gif_path):
                return Image.open(gif_path)
            return None
        except Exception as e:
            show_error_window(f"Image load error: {str(e)}")
            return None

# Show error in a separate popup window
def show_error_window(message):
    error_win = Toplevel()
    error_win.title("Error")
    Label(error_win, text=message, font=("Arial", 12), fg="red").pack(padx=20, pady=20)
    Button(error_win, text="OK", command=error_win.destroy).pack(pady=10)

# Handle speech recognition result
def handle_speech_result(text, window):
    if text:
        window.destroy()
        first_word = text.lower().split()[0]
        display_sign_image(first_word)
    else:
        messagebox.showinfo("Info", "No valid speech input detected.")

# Start speech recognition
def speak_function(root_window):
    root_window.destroy()
    listening_window = Toplevel()
    listening_window.title("Listening for Speech")
    listening_window.configure(bg="#E3F2FD")

    Label(listening_window, text="Listening...", font=("Arial", 12), bg="#E3F2FD").pack(pady=10)

    def process_speech():
        speech_to_text = SpeechToText()
        speech_to_text.recognize_speech(lambda text: handle_speech_result(text, listening_window))

    threading.Thread(target=process_speech, daemon=True).start()

# Show main button window
def show_buttons():
    global button_window
    button_window = Toplevel()
    button_window.title("Sign Language Translator")
    button_window.configure(bg="#E3F2FD")

    Label(button_window, text="Sign Language Translator", font=("Arial", 18, "bold"), bg="#E3F2FD").pack(pady=10)

    button_frame = Frame(button_window, bg="#E3F2FD")
    button_frame.pack(pady=10)

    Button(button_frame, text="Speak", font=("Arial", 12), bg="#4CAF50", fg="white",
           command=lambda: speak_function(button_window)).grid(row=0, column=0, padx=5, pady=5)

    Button(button_frame, text="Text", font=("Arial", 12), bg="#2196F3", fg="white",
           command=lambda: text_button(button_window)).grid(row=0, column=1, padx=5, pady=5)

    Button(button_frame, text="Exit", font=("Arial", 12), bg="#C70039", fg="white",
           command=button_window.destroy).grid(row=0, column=2, padx=5, pady=5)

# Text input window
def text_button(root_window):
    root_window.destroy()
    text_window = Toplevel()
    text_window.title("Text to Sign Language")
    text_window.configure(bg="#E3F2FD")

    Label(text_window, text="Enter Text:", font=("Arial", 12), bg="#E3F2FD").pack(pady=10)
    text_entry = Entry(text_window, font=("Arial", 12))
    text_entry.pack(pady=5)

    Button(text_window, text="Convert", font=("Arial", 12), bg="#4CAF50", fg="white",
           command=lambda: display_sign_image(text_entry.get().lower(), text_window)).pack(pady=5)

    Button(text_window, text="Back", font=("Arial", 12), bg="#C70039", fg="white",
           command=lambda: [text_window.destroy(), show_buttons()]).pack(pady=5)

# Show word gif or fallback to letter-by-letter
def display_sign_image(word, parent_window=None):
    try:
        if parent_window:
            parent_window.destroy()

        text_to_sign = TextToSignLanguage(DATABASE_PATH)
        sign_image = text_to_sign.get_sign_image(word)

        if sign_image and sign_image.format == "GIF":
            play_gif_animation(sign_image)
        else:
            display_letters_as_images(word)
    except Exception as e:
        show_error_window(f"Error: {str(e)}")

# Animate GIF frames
def play_gif_animation(image):
    window = Toplevel()
    window.title("Sign Language GIF")
    label = Label(window)
    label.pack()

    frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(image)]

    def update(index):
        if index < len(frames):
            label.config(image=frames[index])
            window.after(100, update, index + 1)
        else:
            window.destroy()
            show_buttons()

    update(0)

# Show each letter's image (jpg/png) in sequence
def display_letters_as_images(word):
    letter_window = Toplevel()
    letter_window.title("Letter-by-Letter Sign Display")
    frame = Frame(letter_window)
    frame.pack(padx=10, pady=10)

    images = []
    for letter in word:
        for ext in ["jpg", "png"]:
            image_path = os.path.join(DATABASE_PATH, f"{letter}.{ext}")
            if os.path.exists(image_path):
                image = Image.open(image_path).resize((100, 100))
                photo = ImageTk.PhotoImage(image)
                images.append(photo)
                break

    if not images:
        show_error_window(f"No images found for '{word}'.")
        return

    label = Label(frame)
    label.pack()

    def show_next(index=0):
        if index < len(images):
            label.config(image=images[index])
            letter_window.after(1000, show_next, index + 1)
        else:
            letter_window.destroy()
            show_buttons()

    show_next()

# Launch app
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_buttons()
    root.mainloop()
