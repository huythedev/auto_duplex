# Universal Auto Duplex Wrapper

A lightweight software solution (Virtual Printer + Python Watcher) that simulates the "Manual Duplex" feature (auto-splitting pages, printing odd sides, prompting a popup to reload paper, and printing even sides) for **any single-sided printer** (Canon LBP2900, HP 1020, etc.).

Instead of manually remembering odd/even pages and struggling with paper orientation, this tool automates the entire process. Just print once, wait for the popup, drop the paper back into the tray, and click OK.

## System Requirements
1. Windows OS.
2. [Python 3.x](https://www.python.org/downloads/)
3. [SumatraPDF Portable](https://www.sumatrapdfreader.org/download-free-pdf-viewer) (`SumatraPDF.exe`)
4. Virtual printer software like [PDF24 Creator](https://tools.pdf24.org/en/creator)

## Installation & Configuration

### Step 1: Clone the Tool
1. Create a root directory (e.g., `C:\AutoDuplex`).
2. Clone this repo (containing `main.py`, `autoduplex.bat`) into that directory.
3. Download `SumatraPDF.exe` (Portable version) and place it in the same directory.

### Step 2: Install Python Dependencies
Open Terminal/CMD and run:
```bash
pip install watchdog pypdf

```

### Step 3: Configure PDF24 (Virtual Printer)

1. Install PDF24 Creator and open **PDF24 Settings**.
2. Go to **PDF Printer** -> **Auto-Save**:
* Check **Enable Auto-Save**.
* Output directory: Point this to a `Spool` folder inside your tool's directory (e.g., `C:\AutoDuplex\Spool`). The Python script will auto-create this folder if it doesn't exist.


3. (Optional) Go to Windows Control Panel, rename the PDF24 printer to something like `Smart Auto Duplex` to easily recognize it when printing.

### Step 4: Configure the Code

Open `main.py`, find this line, and change it to the exact name of your physical printer (check your Control Panel):

```python
PRINTER_NAME = "Canon LBP2900" 

```

## Running & Background Service

* **Method 1 - Run for Debugging:** Open CMD in the tool's directory, type `python main.py`. The CMD window will stay open to show print logs.
* **Method 2 - Run in Background (Daily use):** Double-click `autoduplex.bat`. The code will run completely hidden in the background.
* **Method 3 - Run Pre-built Executable:** Download the `.exe` file from the Release page and place it in your directory (ensure `SumatraPDF.exe` is in the same folder and PDF24 is configured correctly). Just double-click the `.exe` to run it in the background without needing Python installed.

**Auto-start with Windows:**

1. Press `Win + R`, type `shell:startup`, and hit Enter.
2. Right-click either the `autoduplex.bat` file or the downloaded `.exe` file, and select **Create shortcut**.
3. Cut (Ctrl+X) the newly created shortcut and paste (Ctrl+V) it into the `Startup` folder you just opened.

> Done! The tool will now run silently in the background every time you boot up your PC.

## How to Use

1. Open any Word/PDF document.
2. Click Print -> Select the virtual printer (e.g., **Smart Auto Duplex**).
3. Wait for the printer to output all odd pages. A dialog box will pop up on your screen.
4. Take the entire printed stack and place it directly back into the input tray (**do not flip or rotate it**), then click **OK**. The printer will automatically print the remaining even pages perfectly aligned.
