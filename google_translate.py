# Import necessary modules for creating the GUI and translation functionality
from tkinter import *  # Import all Tkinter modules
from tkinter import ttk  # Import ttk for themed widgets like Combobox
from googletrans import Translator, LANGUAGES  # Import Translator class and language list from googletrans

# Create the main Tkinter window
root = Tk()  # Initialize the main window (root window)
root.geometry('1100x320')  # Set the size of the window to 1100x320 pixels
root.resizable(0, 0)  # Disable resizing of the window (fixed size)
root['bg'] = 'pink'  # Set the background color of the window to pink
root.title('Real-time translator')  # Set the title of the window

# Create and display a title label at the top of the window
Label(root, text='Language Translator', font='Arial 20 bold').pack()  # Add a title with large, bold text

# Create a label for the input text field
Label(root, text='Enter Text', font='arial 13 bold', bg='white smoke').place(x=165, y=90)  # Position the label at (165, 90)

# Create an entry widget for user input (single-line text input)
Input_text = Entry(root, width=60)  # Create an entry widget with a width of 60 characters
Input_text.place(x=30, y=130)  # Position the input field at (30, 130)

# Create a label for the output text
Label(root, text='Output', font='arial 13 bold', bg='white smoke').place(x=780, y=90)  # Position the label at (780, 90)

# Create a text widget for displaying the translation output
Output_text = Text(root, font='arial 10', height=5, wrap=WORD, padx=5, pady=5, width=50)
# 'height' defines the number of lines, 'width' defines characters per line, 'wrap=WORD' wraps text at word boundaries
# 'padx' and 'pady' add padding inside the widget
Output_text.place(x=600, y=130)  # Position the output widget at (600, 130)

# Define the list of available languages (English, Vietnamese, Japanese)
language = ['English', 'Vietnamese', 'Japanese']  # Limit to the desired languages

# Map language names to their respective language codes
language_code_map = {'English': 'en', 'Vietnamese': 'vi', 'Japanese': 'ja'}

# Create a dropdown Combobox for selecting the destination language
dest_lang = ttk.Combobox(root, values=language, width=22)  # Create a Combobox with the language list as options
dest_lang.place(x=130, y=180)  # Position the dropdown at (130, 180)
dest_lang.set('Vietnamese')  # Set the default value to 'Vietnamese'

# Define a function to perform the translation
def Translate():
    try:
        # Get the input text and the selected language code
        input_text = Input_text.get()  # Get the text entered by the user
        selected_lang = dest_lang.get()  # Get the selected language from the Combobox
        dest_code = language_code_map.get(selected_lang, 'vi')  # Default to Vietnamese ('vi') if no valid selection

        # Create a Translator object from the googletrans library
        translator = Translator()
        
        # Translate the text entered in the Input_text field to the selected language
        translation = translator.translate(input_text, dest=dest_code)
        
        # Clear any previous output in the Output_text widget
        Output_text.delete(1.0, END)  # Remove all text from line 1, character 0 to the end
        
        # Insert the translated text into the Output_text widget
        Output_text.insert(END, translation.text)  # Insert the translated text at the end of the widget
    except Exception as e:
        # Print an error message if the translation fails
        print(f'Translation error: {e}')

# Create a button to trigger the Translate function when clicked
trans_btn = Button(root, text='Translate', font='arial 12 bold', pady=5, command=Translate, bg='orange', activebackground='green')
# 'text' defines the button label, 'command' specifies the function to call on click
# 'bg' sets the button background color, 'activebackground' changes the color when pressed
trans_btn.place(x=500, y=250)  # Position the button at (445, 180)

# Start the Tkinter event loop to display the window and respond to user interactions
root.mainloop()