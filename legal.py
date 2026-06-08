import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
import PyPDF2
import os
import nltk

nltk.download('punkt')

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
        elif ext == ".pdf":
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
        else:
            messagebox.showerror("Unsupported File", "Only .txt or .pdf files are allowed.")
    except Exception as e:
        messagebox.showerror("Error", f"Error reading file: {e}")
    return text

def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

def upload_file():
    file_path = filedialog.askopenfilename(
        title="Choose a legal document",
        filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")]
    )
    if file_path:
        text = extract_text_from_file(file_path)
        if text:
            summary = summarize_text(text)
            show_summary(summary)

def show_summary(summary):
    summary_window = tk.Toplevel(root)
    summary_window.title("Summary")
    summary_window.geometry("800x500")
    summary_window.configure(bg="#f4f4f4")

    heading = tk.Label(summary_window, text="Document Summary", font=("Helvetica", 16, "bold"), bg="#f4f4f4", fg="#2e4053")
    heading.pack(pady=15)

    text_area = scrolledtext.ScrolledText(summary_window, wrap=tk.WORD, font=("Calibri", 12), bg="white", fg="#212121", relief=tk.FLAT, borderwidth=8)
    text_area.pack(expand=True, fill='both', padx=20, pady=10)
    text_area.insert(tk.END, summary)
    text_area.config(state='disabled')

root = tk.Tk()
root.title("Legal Document Summarizer")
root.geometry("600x300")
root.configure(bg="#e8f0fe")

title_label = tk.Label(root, text="📄 Legal Document Summarizer", font=("Helvetica", 18, "bold"), bg="#e8f0fe", fg="#1a237e")
title_label.pack(pady=25)

desc_label = tk.Label(root, text="Upload a legal document (.txt or .pdf) to generate a concise summary.", font=("Calibri", 12), bg="#e8f0fe", fg="#333333")
desc_label.pack()

upload_btn = tk.Button(root, text="Upload Document", command=upload_file, font=("Calibri", 13, "bold"),
                       bg="#3949ab", fg="white", padx=20, pady=10, relief=tk.RIDGE, borderwidth=2, activebackground="#5c6bc0")
upload_btn.pack(pady=30)

root.mainloop()
