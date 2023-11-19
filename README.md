# VRChat Album Cover Changer

This Python script is designed to enhance your VRChat experience by dynamically changing your avatar's hoodie/other accessories based on the currently playing media cover art. The script retrieves information about the currently playing media from the Windows Media API and sends the corresponding album cover signal to VRChat using OSC.

## Requirements

Make sure you have the following Python packages installed:

- `winsdk` - Windows Media SDK for Python
- `pythonosc` - Python implementation of OSC

```bash
pip install winsdk python-osc
```

## Usage

1. Clone the repository or download the script.
2. Run the script using Python:

```bash
python osc-music.py
```

## Configuration

Ensure that you have the VRChat avatar set up to receive OSC signals for changing the hoodie cover art. The script uses the `SimpleUDPClient` from the `pythonosc` library to send OSC messages.

```python
OSC_CLIENT = SimpleUDPClient("127.0.0.1", 9000)
```
Adjust the IP address and port number accordingly based on your VRChat setup. This should work out of the box though.

## Supported Albums

The script currently supports a predefined set of albums. If the currently playing media matches one of the albums, it changes the hoodie cover art accordingly. Update the `album_cover_dictionary` with your preferred albums and corresponding cover art indices.
Define the indices in your avatar's animator to correspond to specific albums. (Hint, use texture scaling for OVERLAYs with a secondary UV map for the cover to keep the texture high quality with low resolution.)

```python
album_cover_dictionary = {
    "management": 0,
    "twin galaxies": 1,
    "spring island": 2,
    "younger years": 3,
    "ghost city": 4,
    "soft sounds": 5,
    "afterimage": 6
}
```

## Notes

- This script runs with low overhead and is designed to work seamlessly with VRChat.
- It may not support a high variety of music due to the predefined album list.
- It requires manual effort from the avatar creator to add support.

Enjoy your enhanced VRChat avatar experience with dynamically changing hoodie cover art! If you encounter any issues or have suggestions for improvements, feel free to contribute or open an issue.