import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from ebooklib import epub
from bs4 import BeautifulSoup

# -----------------------------------------------------
# 1) Helper Functions to Extract and Paginate Text
# -----------------------------------------------------
def extract_text_from_epub(epub_file_path):
    """
    Extracts all textual content from an ePub file,
    returning a list of words.
    """
    book = epub.read_epub(epub_file_path)
    all_words = []

    for item in book.get_items():
        # Check if this item is HTML/xHTML content
        if item.get_type() == epub.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            text_content = soup.get_text(separator=' ')
            
            # Quick cleaning
            text_content = text_content.replace('\n', ' ').strip()
            words_in_chapter = text_content.split()
            all_words.extend(words_in_chapter)

    return all_words

def paginate_words(words, words_per_page=20):
    """
    Splits the list of words into "pages" each containing
    up to words_per_page words.
    Returns a list of lists.
    """
    pages = []
    total_words = len(words)
    idx = 0
    while idx < total_words:
        chunk = words[idx : idx + words_per_page]
        pages.append(chunk)
        idx += words_per_page
    return pages

# -----------------------------------------------------
# 2) A Simulated eInk Display Class
# -----------------------------------------------------
class EInkDisplaySim:
    """
    This class simulates an eInk display using
    a Tkinter Text widget for demonstration.
    In real usage, you would replace this class
    with your actual eInk display driver code.
    """
    def __init__(self, text_widget):
        self.text_widget = text_widget
    
    def clear(self):
        """Clears the simulated display."""
        self.text_widget.delete('1.0', tk.END)
    
    def draw_text(self, text):
        """
        Draw the given text in the Text widget.
        """
        self.text_widget.insert(tk.END, text)
    
    def refresh(self):
        """
        In a real eInk display, you'd trigger
        the actual hardware refresh here.
        For simulation, we can just do nothing
        or forcibly update the GUI.
        """
        self.text_widget.update()

# -----------------------------------------------------
# 3) The Main GUI Application
# -----------------------------------------------------
class EPubReaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("256x256 eInk Reader (Simulation)")

        # Default settings
        self.words_per_page = 20
        self.pages = []  # List of pages (each page is a list of words)
        self.current_page_idx = 0

        # -------------------------------------------------
        # Layout: top frame for buttons, main frame for "display"
        # -------------------------------------------------
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Button: Open ePub
        btn_open = tk.Button(top_frame, text="Open ePub", command=self.open_epub)
        btn_open.pack(side=tk.LEFT, padx=5)

        # Button: Prev Page
        btn_prev = tk.Button(top_frame, text="Previous", command=self.prev_page)
        btn_prev.pack(side=tk.LEFT, padx=5)

        # Button: Next Page
        btn_next = tk.Button(top_frame, text="Next", command=self.next_page)
        btn_next.pack(side=tk.LEFT, padx=5)

        # Button: Set Words/Page
        btn_set_wpp = tk.Button(top_frame, text="Set Words/Page", command=self.set_words_per_page)
        btn_set_wpp.pack(side=tk.LEFT, padx=5)

        # Button: Exit
        btn_exit = tk.Button(top_frame, text="Exit", command=self.root.quit)
        btn_exit.pack(side=tk.RIGHT, padx=5)

        # -------------------------------------------------
        # Create a text widget to simulate eInk 256x256
        # We'll enforce a fixed size to mimic a small display area.
        # -------------------------------------------------
        self.display_frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_widget = tk.Text(self.display_frame, width=40, height=16,
                                   wrap=tk.WORD, font=('Arial', 12))
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Our simulated eInk display instance
        self.eink_display = EInkDisplaySim(self.text_widget)

    # -------------------------------------------------
    # GUI Handlers
    # -------------------------------------------------
    def open_epub(self):
        """
        Opens a file dialog for the user to select an ePub,
        extracts the text, paginates, and displays page 1.
        """
        file_path = filedialog.askopenfilename(
            title="Open ePub File",
            filetypes=[("ePub Files", "*.epub"), ("All Files", "*.*")]
        )
        if not file_path:
            return  # User cancelled

        try:
            all_words = extract_text_from_epub(file_path)
            self.pages = paginate_words(all_words, self.words_per_page)
            self.current_page_idx = 0
            
            if not self.pages:
                messagebox.showwarning("Warning", "No textual content found in this ePub.")
                return
            
            self.render_current_page()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open/parse ePub:\n{e}")

    def next_page(self):
        """Navigates to the next page if possible."""
        if not self.pages:
            return  # No pages loaded
        if self.current_page_idx < len(self.pages) - 1:
            self.current_page_idx += 1
            self.render_current_page()
        else:
            messagebox.showinfo("Info", "You are on the last page.")

    def prev_page(self):
        """Navigates to the previous page if possible."""
        if not self.pages:
            return
        if self.current_page_idx > 0:
            self.current_page_idx -= 1
            self.render_current_page()
        else:
            messagebox.showinfo("Info", "You are on the first page.")

    def set_words_per_page(self):
        """
        Asks the user for a new words-per-page setting,
        re-paginates, and resets to page 0.
        """
        if not self.pages:
            messagebox.showinfo("Info", "Open an ePub first before setting words/page.")
            return

        new_wpp = simpledialog.askinteger(
            "Words per Page",
            "Enter the number of words per page:",
            initialvalue=self.words_per_page,
            minvalue=1, maxvalue=9999
        )

        if new_wpp is None:
            return  # user cancelled
        # Re-paginate
        # Flatten current pages back to a single word list:
        all_words = [word for page in self.pages for word in page]
        self.words_per_page = new_wpp
        self.pages = paginate_words(all_words, self.words_per_page)
        self.current_page_idx = 0
        self.render_current_page()

    # -------------------------------------------------
    # Display logic
    # -------------------------------------------------
    def render_current_page(self):
        """
        Render the current page's words to the eInk display simulation.
        """
        if not self.pages:
            return

        # Clear the simulated display
        self.eink_display.clear()

        # Prepare text to render
        page_words = self.pages[self.current_page_idx]
        text_to_display = " ".join(page_words)

        # Draw text
        self.eink_display.draw_text(text_to_display)

        # Trigger refresh (simulated)
        self.eink_display.refresh()

# -----------------------------------------------------
# 4) Main Entry Point
# -----------------------------------------------------
def main():
    root = tk.Tk()
    app = EPubReaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
