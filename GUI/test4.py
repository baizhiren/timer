import tkinter as tk


class Gui:
    fullScreen = False

    def __init__(self):
        self.root = tk.Tk()
        self.root.bind("<F11>", self.toggleFullScreen)
        self.root.bind("<Alt-Return>", self.toggleFullScreen)
        self.root.bind("<Control-w>", self.quit)
        self.root.mainloop()

    def toggleFullScreen(self, event):
        if self.fullScreen:
            self.deactivateFullscreen()
        else:
            self.activateFullscreen()

    def activateFullscreen(self):
        self.fullScreen = True

        # Store geometry for reset
        self.geometry = self.root.geometry()

        # Hides borders and make truly fullscreen
        self.root.overrideredirect(True)

        # Maximize window (Windows only). Optionally set screen geometry if you have it
        self.root.state("zoomed")

    def deactivateFullscreen(self):
        self.fullScreen = False
        self.root.state("normal")
        self.root.geometry(self.geometry)
        self.root.overrideredirect(False)

    def quit(self, event=None):
        print("quiting...", event)
        self.root.quit()


if __name__ == '__main__':
    Gui()