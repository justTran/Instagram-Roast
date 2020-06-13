import glob, json, math, threading
import tkinter as tk
from description import *
from imagePrediction import *
from PIL import Image, ImageTk, ExifTags
from session import *
from tkinter import filedialog
from tkinter import messagebox

class unpopularInstagram(tk.Frame):

    def __init__(self, master = None):
        self.images = []
        self.threads = []
        self.results = []
        self.master = master
        self.menubar = tk.Menu(self.master)
        self.nice = False
        self.path = None
        self.score = None
        self.session = None
        self.settingsWindow = None
        self.master.title('Unpopular Instagram')
        self.createGUI()

    def createGUI(self):
        self.about = tk.Menu(self.menubar, tearoff = 0)
        self.about.add_command(label = "Configure Credentials", command = self.settingsMenu)
        self.menubar.add_cascade(label = "Settings", menu = self.about)
        self.directorySelector = tk.Button(self.master, text = "Select the awful directory", width = 22, command = self.getDirectory)
        self.beginProcess = tk.Button(self.master, text = "Shame you", width = 22, command = self.start)
        self.directoryLabel = tk.Label(text="No Directory Selected")
        self.toggle = tk.Checkbutton(self.master, text = "Toggle Nice Mode", command = self.toggleExtrema)
        self.directorySelector.grid(row = 0, column = 0)
        self.directoryLabel.grid(row = 0, column = 1)
        self.beginProcess.grid(row = 1, column = 0)
        self.toggle.grid(row = 1, column = 1)

    def toggleExtrema(self):
        if not self.nice:
            self.directorySelector.configure(text = "Select the directory friend")
            self.beginProcess.configure(text = "Find the popular image")
            self.nice = True
        else:
            self.directorySelector.configure(text = "Select the awful directory")
            self.beginProcess.configure(text = "Shame you")
            self.nice = False
        root.update()

    def updateGUI(self, lock):
        if lock: self.beginProcess.configure(state="disable")
        else: self.beginProcess.configure(state="normal")
        root.update()
        
    def getDirectory(self):
        if self.nice: title = "Choose the directory to find your masterpiece"
        else: title = "Roast this directory, dipshit"

        self.path = filedialog.askdirectory(title = title, mustexist = True)
        self.directoryLabel.configure(text = self.path)
        root.update()

    def start(self):
        if self.path is None:
            messagebox.showwarning("Warning", "You have not selected a directory!")
            return

        if self.images != []: del self.images[:]
        if self.results != []: del self.results[:]

        for types in [glob.glob(self.path + e) for e in ['/*.jpg', '/*.png']]:
            if len(types) != 0:
                total = len(types)
            self.results.extend(types)

        currentIndex = 0
        end = math.floor(total/4)
        for i in range(1, 5):
            t = threading.Thread(target=self.processImages, args=[currentIndex, end])
            self.threads.append(t)
            t.start()

            currentIndex = end + 1
            if (i != 3): end = math.floor(total/4)*(i+1)
            else: end = total

        for i in range(0, 4):
            self.threads[i].join()

        try:
            self.images = sorted(self.images, reverse = self.nice, key = lambda x: x[1])
            self.score = self.images[0][1]
            arg = self.images[0][0].replace('/', '\\')
            t2 = threading.Thread(target = self.postAbomination, args = [arg])
            t2.start()
            self.updateGUI(True)
            self.showImage(self.images[0][0])

        except IndexError:
            messagebox.showwarning("Warning", "None of the images found are compatible!")
            self.updateGUI(False)

    def processImages(self, start, end):
        for i in range(start, end):
            self.images.append(tuple([self.results[i], imagePrediction(self.results[i]).getValue()]))

    def showImage(self, path):
        imageWindow = tk.Toplevel()
        imageWindow.title(f"Result Image: Score of {self.score}")
        height = imageWindow.winfo_screenheight()
        width = imageWindow.winfo_screenwidth()
        load = Image.open(path)
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation': break
                
            exif = dict(load._getexif().items())

            if exif[orientation] == 3: load = load.transpose(Image.ROTATE_180)
            elif exif[orientation] == 6: load = load.transpose(Image.ROTATE_270)
            elif exif[orientation] == 8: load = load.transpose(Image.ROTATE_90)
        except:
            pass

        [iWidth, iHeight] = load.size

        if (iWidth > width) or (iHeight > height):
            iHeight *= 0.25
            iWidth *= 0.25
        
        render = ImageTk.PhotoImage(load.resize((int(iWidth), int(iHeight))))
        self.resultImage = tk.Label(imageWindow, image = render)
        self.stats = tk.Label(imageWindow, text = (f"Popularity score of: {self.score}"))
        self.resultImage.image = render
        self.resultImage.pack()
        self.stats.pack()
        imageWindow.mainloop()

    def saveSettings(self, username, password):
        if (len(username) == 0) or (len(password) == 0):
            messagebox.showwarning("Warning", "Credentials cannot be empty.")
            return

        data = {"username" : username,
                "password" : password}

        try:
            with open('settings.json', 'w') as f:
                json.dump(data, f)

        except FileNotFoundError as e:
            with open('settings.json', 'w') as f:
                json.dump(data, f)
        finally:
            self.settingsWindow.destroy()

    def settingsMenu(self):
        uname = tk.StringVar()
        pword = tk.StringVar()
        self.settingsWindow = tk.Toplevel()
        userLabel = tk.Label(self.settingsWindow, text = 'Username: ')
        passLabel = tk.Label(self.settingsWindow, text = 'Password: ')
        userEntry = tk.Entry(self.settingsWindow, textvariable = uname)
        passEntry = tk.Entry(self.settingsWindow, textvariable = pword, show = '*')
        acceptButton = tk.Button(self.settingsWindow, text = "Confirm", command = lambda: self.saveSettings(uname.get(), pword.get()))
        userLabel.grid(row = 0, column = 0)
        userEntry.grid(row = 0, column = 1)
        passLabel.grid(row = 1, column = 0)
        passEntry.grid(row = 1, column = 1)
        acceptButton.grid(row = 2, column = 0)
        self.settingsWindow.geometry("200x70")
        self.settingsWindow.mainloop()

    def postAbomination(self, image):
        try:
            with open('settings.json', 'r') as f:
                creds = json.load(f)

        except FileNotFoundError as e:
            messagebox.showerror("Warning", "Credentials not initiated! Go to the settings menu to set them.")
            self.updateGUI(False)
            return

        if self.session is None:
            self.session = Session(creds['username'], creds['password'])
            if not self.session.authenticate():
                messagebox.showerror("Warning", "Invalid Credentials")
                self.session.destroy()
                self.session = None
                self.updateGUI(False)
                return

        try:
            descText = Descriptions(self.score).getDescrption() + " -some awful instagram bot"
            self.session.uploadImage(image, descText)
            self.updateGUI(False)
        except:
            messagebox.showwarning("Warning", "There was an issue uploading your image!")
            self.updateGUI(False)

    def cleanup(self):
        if self.session:
            self.session.destroy()
            self.session = None

        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = unpopularInstagram(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup)
    root.config(menu=app.menubar)
    root.mainloop()