import sys
import os
import time
import subprocess
import ctypes
from pypdf import PdfReader, PdfWriter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SPOOL_DIR = os.path.join(BASE_DIR, "Spool")
SUMATRA_PATH = os.path.join(BASE_DIR, "SumatraPDF.exe")

# --- CHANGE PRINTER NAME HERE ---
PRINTER_NAME = "Canon LBP2900" 

def process_and_print(pdf_path):
    print(f"\n[+] Processing file: {pdf_path}")
    
    # Wait for the virtual printer to finish writing the file
    time.sleep(2) 

    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
    except Exception as e:
        print(f"[-] Error reading PDF: {e}")
        return
    
    # If the file only has 1 page -> Print directly, no splitting needed
    if total_pages == 1:
        print("[!] 1-page file detected. Printing directly.")
        subprocess.run([SUMATRA_PATH, "-print-to", PRINTER_NAME, "-silent", pdf_path])
        os.remove(pdf_path)
        return

    writer_odd = PdfWriter()
    writer_even = PdfWriter()

    # Extract odd pages
    for i in range(0, total_pages, 2):
        writer_odd.add_page(reader.pages[i])

    # Extract even pages and reverse the order
    even_indices = list(range(1, total_pages, 2))
    even_indices.reverse()

    # Rotate even pages 180 degrees
    for i in even_indices:
        page = reader.pages[i]
        page.rotate(180)
        writer_even.add_page(page)

    odd_path = os.path.join(SPOOL_DIR, "temp_odd.pdf")
    even_path = os.path.join(SPOOL_DIR, "temp_even.pdf")

    with open(odd_path, "wb") as f:
        writer_odd.write(f)
    with open(even_path, "wb") as f:
        writer_even.write(f)

    # 1. Spool odd pages
    print("[+] Printing odd pages...")
    subprocess.run([SUMATRA_PATH, "-print-to", PRINTER_NAME, "-silent", odd_path])

    # 2. Show Windows native popup to wait for paper reload
    print("[!] Waiting for paper reload...")
    MB_OKCANCEL = 0x01
    MB_ICONINFORMATION = 0x40
    
    result = ctypes.windll.user32.MessageBoxW(
        0, 
        "Side 1 has finished printing.\nPlace the printed stack back into the input tray (do NOT flip or turn it), then click OK to print Side 2.\nClick Cancel to abort.", 
        "Auto Duplex Spooler", 
        MB_OKCANCEL | MB_ICONINFORMATION
    )

    # 3. Handle user input
    if result == 1: # OK button
        print("[+] Printing even pages...")
        subprocess.run([SUMATRA_PATH, "-print-to", PRINTER_NAME, "-silent", even_path])
    elif result == 2: # Cancel button
        print("[-] Side 2 printing aborted by user.")

    # 4. Clean up
    reader.stream.close()
    if os.path.exists(odd_path): os.remove(odd_path)
    if os.path.exists(even_path): os.remove(even_path)
    if os.path.exists(pdf_path): os.remove(pdf_path)
    print("[+] Job done!\n")

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            try:
                process_and_print(event.src_path)
            except Exception as e:
                print(f"[-] Thread processing error: {e}")

if __name__ == "__main__":
    if not os.path.exists(SPOOL_DIR):
        os.makedirs(SPOOL_DIR)
        
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, path=SPOOL_DIR, recursive=False)
    observer.start()
    
    print(f"[*] Auto Duplex Tool is running.")
    print(f"[*] Monitoring directory: {SPOOL_DIR}")
    print(f"[*] Target Printer: {PRINTER_NAME}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()