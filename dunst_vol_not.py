import subprocess
from gpiozero import RotaryEncoder, Button
from signal import pause

# GPIO pin assignments
ENCODER_A = 4
ENCODER_B = 17
BUTTON = 27

# Persistent notification ID
notification_id = "991049"

# Function to get current volume
def get_volume():
    result = subprocess.run(["amixer", "get", "Master"], capture_output=True, text=True)
    lines = result.stdout.split("\n")
    for line in lines:
        if "%" in line:
            volume = int(line.split("[")[1].split("%")[0])
            muted = "off" in line
            return volume, muted
    return 0, False  # Default value if parsing fails

# Function to set volume
def set_volume(change):
    volume, muted = get_volume()
    new_volume = max(0, min(100, volume + change))  # Keep volume between 0-100
    subprocess.run(["amixer", "set", "Master", f"{new_volume}%"])
    send_notification(new_volume, muted, change)

# Function to toggle mute
def toggle_mute():
    subprocess.run(["amixer", "set", "Master", "toggle"])
    volume, muted = get_volume()
    send_notification(volume, muted, 0)  # No volume change on mute toggle

# Function to send a progress bar notification
def send_notification(volume, muted, change):
    # Set the icon directory
    icon_dir = "/usr/share/icons/Volume/"

    # Determine the appropriate icon based on the action
    if muted:
        icon = f"{icon_dir}muted.png"  # Full path to mute icon
        message = "Muted"
    elif change > 0:
        icon = f"{icon_dir}volume-up.png"  # Full path to volume up icon
        message = f"{volume}%"
    elif change < 0:
        icon = f"{icon_dir}volume-down.png"  # Full path to volume down icon
        message = f"{volume}%"
    else:
        icon = f"{icon_dir}muted.png" if muted else f"{icon_dir}volume-up.png"
        message = "Muted" if muted else f"{volume}%"


    subprocess.run([
        "dunstify", "-r", notification_id, "-h", f"int:value:{volume}",
        "-i", icon, "-u", "normal", "-h", "string:x-dunst-stack-tag:volume",
        message
    ])
# Rotary Encoder setup
encoder = RotaryEncoder(ENCODER_A, ENCODER_B, wrap=True)
encoder.when_rotated_clockwise = lambda: set_volume(5)
encoder.when_rotated_counter_clockwise = lambda: set_volume(-5)

# Button setup
button = Button(BUTTON, pull_up=True)
button.when_pressed = toggle_mute

print("Rotary encoder volume control running...")
pause()  # Keep script running
