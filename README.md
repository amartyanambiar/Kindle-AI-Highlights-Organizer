# Kindle AI Highlights Organizer

Necessity is the mother of all invention! Since there was no free service to do this, I built it myself. Simple, but very helpful.

This tool mainly solves two problems:

- Organizes your entire Kindle clippings file into multiple text files (one per book) for easy separation and access.
- Summarizes your highlights using AI - because fragmented highlights and personal notes without the book open are hard to understand, but AI makes them coherent and meaningful.

## What does it do?

- Splits your exported `My Clippings.txt` into separate files for each book.
- Merges highlights and notes by location.
- Lets you summarize your highlights using AI (Mistral 7B on Ollama) for easy review in Apple Notes or any other note-taking apps.

## How to use

1. **Organize your clippings**

   - Make sure your `My Clippings.txt` is in this folder.
   - Run:
     ```sh
     python organize_clippings.py
     ```
   - This creates an `organized_clippings` folder with one file per book.

2. **Summarize with AI (optional)**
   - Make sure Ollama is running with the Mistral 7B model. (feel free to use any other model you prefer, just change the `model` in the code)
   - Run:
     ```sh
     python summarize_clippings.py
     ```
   - Summaries will be saved in the `summaries` folder.

## Examples

This repository includes a few example files in the `organized_clippings` and `summaries` folders. The highlights and notes might not make complete sense to you (as they were my highlights & reading notes), but they demonstrate how well the AI summarization works to transform fragmented highlights into coherent, understandable summaries.

---

## If you have time to contribute:

- Make the summarizer model-agnostic (easy to use with any LLM or API)
- Add a beautiful UI for even easier use.
- Improve the summarization prompt to handle more complex highlights & notes.
- Maybe even a browser extension???

With these, you'll have an awesome product, people charge a lot for this kind of thing!
