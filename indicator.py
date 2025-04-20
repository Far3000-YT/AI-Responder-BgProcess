import tkinter as tk
import os
import time #although tkinter.after is preferred for scheduling

#determine the base directory for the status file (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_FILE = os.path.join(BASE_DIR, ".ai_status")

#check status file interval ms
CHECK_INTERVAL_MS = 250 #check 4 times per second

#define colors
COLOR_READY = "black"
COLOR_BUSY = "yellow"

root = tk.Tk()
root.title("AI Status Indicator") #title won't be visible with overrideredirect

root.geometry("5x5+0+0") #width x height + x_offset + y_offset
#set always on top
root.attributes("-topmost", True)
#remove window decorations
root.overrideredirect(True)
root.resizable(False, False)

#create canvas for colored square
canvas = tk.Canvas(root, width=5, height=5, highlightthickness=0) #highlightthickness=0 removes canvas border
canvas.pack()

#create rectangle on canvas
status_square = canvas.create_rectangle(0, 0, 5, 5, fill=COLOR_READY, outline="") #outline="" removes border

def update_indicator_color(is_busy):
    """updates the color of the square based on status"""
    color = COLOR_BUSY if is_busy else COLOR_READY
    canvas.itemconfig(status_square, fill=color)

def check_status():
    """checks the status file and updates the indicator"""
    file_exists = os.path.exists(STATUS_FILE)
    update_indicator_color(file_exists)
    #schedule next check
    root.after(CHECK_INTERVAL_MS, check_status)

#initial check
check_status()

print("AI Status Indicator script running...")
print(f"Monitoring status file: {STATUS_FILE}")
#start tkinter event loop
root.mainloop()

print("AI Status Indicator script stopped.")