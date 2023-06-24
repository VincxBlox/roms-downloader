from tkinter import *
from tkinter import Tk
from tkinter.ttk import Progressbar
from tkinter import filedialog
from zipfile import ZipFile
import os
import requests

class ROMExtractorGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("ROM Extractor")
        self.window.geometry("500x500")
        self.window.resizable(False, False)
        self.setup_step1_options()

    def setup_step1_options(self):
        self.clear_window()

        label = Label(self.window, text="Step 1: Select an option")
        label.pack(pady=10)

        link_button = Button(self.window, text="Link", command=self.select_link)
        link_button.pack(pady=5)

        file_button = Button(self.window, text="File", command=self.select_file)
        file_button.pack(pady=5)

    def select_link(self):
        self.clear_window()

        label = Label(self.window, text="Step 1: Enter the link to the .zip file")
        label.pack(pady=10)

        self.zip_link_var = StringVar()
        zip_link_entry = Entry(self.window, textvariable=self.zip_link_var, width=50)
        zip_link_entry.pack(pady=10)

        next_button = Button(self.window, text="Next", command=self.setup_step2_options)
        next_button.pack()

    def select_file(self):
        self.clear_window()

        label = Label(self.window, text="Step 1: Select the .zip file")
        label.pack(pady=10)

        file_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
        self.zip_link_var = StringVar()
        self.zip_link_var.set(file_path)

        next_button = Button(self.window, text="Next", command=self.setup_step2_options)
        next_button.pack()

    def setup_step2_options(self):
        self.clear_window()

        label = Label(self.window, text="Step 2: Select an option")
        label.pack(pady=10)

        options = [
            'genesis', 'gba', 'nds', 'nes', 'snes', 'gb', 'dsiware', 'sms'
        ]

        self.choice_var = StringVar()
        self.choice_var.set(options[0])

        option_menu = OptionMenu(self.window, self.choice_var, *options)
        option_menu.pack(pady=10)

        if self.choice_var.get() == 'other':
            next_button = Button(self.window, text="Next", command=self.setup_step2_destination)
        else:
            next_button = Button(self.window, text="Install", command=self.install_rom_file)
        next_button.pack()

        back_button = Button(self.window, text="Back", command=self.setup_step1_options)
        back_button.place(x=10, y=10)

    def setup_step2_destination(self):
        self.clear_window()

        label = Label(self.window, text="Step 2: Enter the destination directory")
        label.pack(pady=10)

        self.destination_var = StringVar()
        destination_entry = Entry(self.window, textvariable=self.destination_var, width=50)
        destination_entry.pack(pady=10)

        install_button = Button(self.window, text="Install", command=self.install_rom_file)
        install_button.pack()

        back_button = Button(self.window, text="Back", command=self.setup_step2_options)
        back_button.place(x=10, y=10)

    def install_rom_file(self):
        link = self.zip_link_var.get()
        destination = self.get_destination_path()

        if not link:
            print("Please enter the link to the .zip file.")
            return

        if not destination:
            print("Please enter a valid destination directory.")
            return

        self.download_extract_move(link, destination)

        # Clear the input fields
        self.zip_link_var.set("")
        if self.choice_var.get() == 'other':
            self.destination_var.set("")

    def download_extract_move(self, link, destination):
        # Create the destination directory if it doesn't exist
        if not os.path.exists(destination):
            if destination != "other":
                print("Directory Doesn't Exist")
                return

            os.makedirs(destination)

        # Download the .zip file
        response = requests.get(link, stream=True)
        file_name = link.split("/")[-1]
        file_path = os.path.join(destination, file_name)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        downloaded_size = 0

        progress_bar = Progressbar(self.window, length=200, mode='determinate')
        progress_bar.pack(pady=10)

        with open(file_path, 'wb') as file:
            for data in response.iter_content(block_size):
                downloaded_size += len(data)
                file.write(data)
                progress = min(int(downloaded_size * 100 / total_size), 100)
                progress_bar['value'] = progress
                self.window.update()

        # Extract the .zip file
        with ZipFile(file_path, 'r') as zip_file:
            zip_file.extractall(destination)

        # Remove the .zip file
        os.remove(file_path)

        progress_bar.destroy()
        finished_label = Label(self.window, text="Finished!")
        finished_label.pack(pady=10)

        print("Installation complete!")

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def run(self):
        self.window.mainloop()

    def get_destination_path(self):
        destination_options = {
            'genesis': r'G:\roms\gen',
            'gba': r'G:\roms\gba',
            'nds': r'G:\roms\nds',
            'nes': r'G:\roms\nes',
            'snes': r'G:\roms\snes',
            'gb': r'G:\roms\gb',
            'dsiware': r'G:\roms\dsiware',
            'sms': r'G:\roms\sms',
            'other': None
        }

        choice = self.choice_var.get().lower()
        return destination_options.get(choice, None)

gui = ROMExtractorGUI()
gui.run()
