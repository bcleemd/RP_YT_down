# Qt xcb Plugin Error Solution

The error you're seeing occurs because **Qt 6.5 and later** (which PySide6 uses) requires a system library called `libxcb-cursor0` to run the "xcb" platform plugin on Linux. This library is often not installed by default on newer versions of Ubuntu, Debian, or Linux Mint (like your Linux Mint 22.2).

## 🛠️ Solution

To fix this, you need to install the missing library using your terminal:

```bash
sudo apt update
sudo apt install libxcb-cursor0
```

## 🔍 Verification

After installing, you can verify that the library is found by running:

```bash
ldd .venv/lib/python3.14/site-packages/PySide6/Qt/plugins/platforms/libqxcb.so | grep xcb-cursor
```

It should show a path to the library instead of "not found".

## 🚀 Running the App

Once installed, try running your application again:

```bash
uv run youtube-downloader.py
```
