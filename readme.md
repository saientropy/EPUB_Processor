# 256x256 eInk Reader Simulation

This project demonstrates how to load an ePub file, parse its textual content, and display it in a simulated **256×256** eInk display using a Tkinter GUI in Python. It includes:

- A GUI to select and open an ePub file.
- Automatic text extraction from the ePub.
- Pagination with a default of 20 words per “page” (configurable by the user).
- Simulated “Next” and “Previous” navigation buttons.
- A quick text widget that mimics a small display area (instead of real eInk).

In a real-world scenario, replace the simulation class (`EInkDisplaySim`) with calls to your hardware-based eInk driver.

---

## Features

- **Load ePub**: An “Open ePub” button opens a file dialog to let the user pick any `.epub` file.  
- **Text Extraction**: Extracts and cleans text from each chapter of the ePub, ignoring extraneous metadata.  
- **Pagination**: Splits the text into pages of 20 words by default, but can be changed via “Set Words/Page.”  
- **Navigation**: “Next” and “Previous” buttons let you move through the pages.  
- **Settings**: A dialog to adjust words-per-page on-the-fly.  
- **Simulation**: Uses a Tkinter `Text` widget as a stand-in for an actual eInk display.

Save the code as epub_eink_reader.py.

