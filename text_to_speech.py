from tkinter import *  # Import all Tkinter modules for creating the GUI
from tkinter import ttk  # Import ttk for themed widgets like Combobox
from googletrans import Translator  # Import the Translator class from googletrans for text translation
from gtts import gTTS  # Import gTTS for converting text to speech (Google Text-to-Speech)
import pygame  # Import pygame for audio playback
import os  # Import os for file operations (e.g., deleting files)
import time  # Import time for delays (e.g., to give the system time to release files)
import datetime  # Import datetime to generate unique filenames using timestamps

# Initialize pygame mixer for audio playback (necessary to play MP3 files)
pygame.mixer.init()

# Create the main Tkinter window
root = Tk()  # Initialize the Tkinter window
root.geometry('1100x350')  # Set window size to 1100x350 pixels
root.resizable(0, 0)  # Prevent resizing of the window (fixed size)
root['bg'] = 'pink'  # Set the background color of the window to pink
root.title('Real-time translator')  # Set the window title to 'Real-time translator'

# Create and display a title label in the window
Label(root, text='Language Translator', font='Arial 20 bold').pack()

# Create and position a label for the input field
Label(root, text='Enter Text', font='arial 13 bold', bg='white smoke').place(x=165, y=90)

# Create an entry widget (input field) where the user will type the text to translate
Input_text = Entry(root, width=60)
Input_text.place(x=30, y=130)

# Create and position a label for the output (translation) field
Label(root, text='Output', font='arial 13 bold', bg='white smoke').place(x=780, y=90)

# Create a Text widget for displaying the translated text
Output_text = Text(root, font='arial 10', height=5, wrap=WORD, padx=5, pady=5, width=50)
Output_text.place(x=600, y=130)

# Define available languages (English, Vietnamese, Japanese)
language = ['English', 'Vietnamese', 'Japanese']

# Map the language names to their corresponding language codes
language_code_map = {'English': 'en', 'Vietnamese': 'vi', 'Japanese': 'ja'}

# Create a Combobox widget for selecting the target language
dest_lang = ttk.Combobox(root, values=language, width=22)
dest_lang.place(x=130, y=180)  # Place the Combobox at coordinates (130, 180)
dest_lang.set('Vietnamese')  # Set default language to Vietnamese

# Create a status label to show messages (e.g., success or failure)
status_label = Label(root, text='', font='arial 12', fg='green', bg='pink')
status_label.place(x=500, y=300)  # Position the status label

# Function to generate a unique filename based on the current timestamp
def generate_unique_filename():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")  # Format the current date and time
    return f"output_{timestamp}.mp3"  # Return a filename with the timestamp (e.g., output_20250124012345678901.mp3)

# Function to remove old MP3 files from the directory
def remove_old_files(directory=".", extension="mp3"):
    # Loop through all files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith(f".{extension}"):  # Check if the file has the given extension
            file_path = os.path.join(directory, filename)  # Get the full file path
            try:
                os.remove(file_path)  # Try to delete the file
                print(f"File {file_path} has been deleted.")  # Print success message
            except Exception as e:  # Handle any errors that occur during file deletion
                print(f"Error deleting file {file_path}: {e}")

# Function to translate text and convert it to speech
def Translate():
    try:
        # Get the text entered by the user and the selected language code
        input_text = Input_text.get()
        selected_lang = dest_lang.get()  # Get the selected language from the Combobox
        dest_code = language_code_map.get(selected_lang, 'vi')  # Get the language code (default is 'vi' for Vietnamese)

        # Create a Translator object from googletrans
        translator = Translator()

        # Translate the input text to the selected language
        translation = translator.translate(input_text, dest=dest_code)

        # Clear any previous output in the Output_text widget
        Output_text.delete(1.0, END)
        # Insert the translated text into the Output_text widget
        Output_text.insert(END, translation.text)

        # Generate speech from the translated text using gTTS
        tts = gTTS(text=translation.text, lang=dest_code, slow=False)

        # Generate a unique filename for the translated speech (MP3 file)
        mp3_filename = generate_unique_filename()

        # Save the speech to the uniquely named MP3 file
        tts.save(mp3_filename)

        # Stop any currently playing music (if any)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        # Add a small delay to allow the system time to release the file
        time.sleep(0.1)

        # Play the newly created MP3 file using pygame
        pygame.mixer.music.load(mp3_filename)  # Load the MP3 file
        pygame.mixer.music.play()  # Play the MP3 file

        # Update the status label to indicate success
        status_label.config(text="Translation Successful!", fg='green')

        # Optionally, remove old MP3 files from the directory
        remove_old_files()  # This will delete all old MP3 files in the current directory

    except Exception as e:
        print(f'Translation error: {e}')  # Print any errors that occur
        # Update the status label to indicate failure
        status_label.config(text="Translation Failed. Please try again.", fg='red')

# Function to clear input and output fields
def Clear():
    Input_text.delete(0, END)  # Clear the input field
    Output_text.delete(1.0, END)  # Clear the output field
    status_label.config(text='')  # Clear the status label

# Create a button that triggers the Translate function when clicked
trans_btn = Button(root, text='Translate', font='arial 12 bold', pady=5, command=Translate, bg='orange', activebackground='green')
trans_btn.place(x=500, y=220)  # Place the Translate button

# Create a button that clears the input and output fields when clicked
clear_btn = Button(root, text='Clear', font='arial 12 bold', pady=5, command=Clear, bg='lightblue', activebackground='blue')
clear_btn.place(x=600, y=220)  # Place the Clear button

# Start the Tkinter event loop (this keeps the window open and responsive to user input)
root.mainloop()