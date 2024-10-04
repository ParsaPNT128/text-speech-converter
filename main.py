from tkinter import *
from tkinter import messagebox
import tkinter as tk
import speech_recognition as sr
import pyttsx3

# main
engine = pyttsx3.init()
recognizer = sr.Recognizer()
root = tk.Tk()
root.title('Text And Speech Converter')
root.geometry('500x300')
root.resizable(False, False)

def change_screen(option):
    if option.get() == 'Speech to Text':
        text_frame.pack_forget()
        speech_frame.pack(fill='both', expand=True)
    else:
        speech_frame.pack_forget()
        text_frame.pack(fill='both', expand=True)

def convert_to_speech(txt):
    print(txt.strip())
    if txt.strip() != '':
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 150)

        engine.save_to_file(txt, 'voice.mp3')
        engine.runAndWait()

        save_label.config(text='Voice saved As voice.mp3')
    else:
        messagebox.showerror('Empty Input', 'Please enter a text.')

def convert_to_text():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        listening_label.config(text='Listening...')
        try:
            listening_label.config(text='Rocognizing...')
            txt = recognizer.recognize_google(audio)
            listening_label.config(text='Done.')
            recognized_text.insert(tk.END, txt)
        except sr.UnknownValueError:
            listening_label.config(text="Couldn't understand audio.")

# option menu
frames = ['Text to Speech', 'Speech to Text']
selected_value = tk.StringVar(root, value=frames[0])
option_menu = tk.OptionMenu(root, selected_value, *frames, command=lambda option: change_screen(selected_value))
option_menu.pack(pady=10)

# text frame
text_frame = tk.Frame(root)

enter_text_frame = tk.Frame(text_frame)
enter_text_label = tk.Label(enter_text_frame, text='Enter a Text:')
enter_text = Text(enter_text_frame, wrap=tk.WORD, width=45, height=10)
convert_to_text_button = tk.Button(text_frame, text='Convert Text To Speech', command=lambda: convert_to_speech(enter_text.get("1.0",END)))
save_label = tk.Label(text_frame, text='')

text_frame.pack(fill='both', expand=True)
enter_text_frame.pack()
enter_text_label.grid(row=0, column=0)
enter_text.grid(row=0, column=1)
convert_to_text_button.pack(pady=10)
save_label.pack()

# speech frame
speech_frame = tk.Frame(root)

convert_to_text_button = tk.Button(speech_frame, text='Convert Speech To Text', command=convert_to_text)
recognized_text_frame = tk.Frame(speech_frame)
recognized_text_label = tk.Label(recognized_text_frame, text='Recognized Text:')
recognized_text = Text(recognized_text_frame, wrap=tk.WORD, width=45, height=10)
listening_label = tk.Label(speech_frame, text='')

convert_to_text_button.pack(pady=5)
recognized_text_frame.pack(pady=10)
recognized_text_label.grid(row=0, column=0)
recognized_text.grid(row=0, column=1)
listening_label.pack()


root.mainloop()