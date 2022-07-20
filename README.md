# AppleBooks-Notes-Parser 📚
## This Python script is used to export all the **notes in a book** as a **text file**. 
### These are contained within a PDF file. 
**In the PDF file**, each Note shows above it the title of the paragraph in which it is contained, this leads to a lot of **confusion** in addition to the useless **waste of space.** \
This script **groups the notes** according to the **title** of the paragraph they belong to.
___

## **FEATURES:**
- Extracts the **title and author** of the Book and inserts these two information into the **first two lines** of the text file.
- It's able to manage and process **multiple PDF files at the same time**.
- It includes a **graphical loading** bar to show the user the current status of the transcript while the script is running.
- Ignore any **non-PDF** files inside the Input folder.
- In case of **transcription errors**, this script notes the number of errors **per file** and then informs the user.


## **USAGE:**
 1. Insert all the **PDF** files you want to process into the **Input** folder. 
 2. **Run the script**.
 3. All created .txt files can be found in the **Output** folder.

---

## **PDF REQUIREMENTS:**
 - Each line must be an **alternation** of TitleParagraph - Note.
 - Each TitleParagraph/Note must remain on a **single line** and not break through dividing into several lines.



