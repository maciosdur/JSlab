import tkinter as tk
from gui.app import HTTPLogViewer

def main():
    root = tk.Tk()
    app = HTTPLogViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()