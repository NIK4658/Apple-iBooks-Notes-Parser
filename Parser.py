# -*- coding: utf-8 -*-
import time
from PyPDF2 import PdfFileReader
from os import listdir
from os.path import isfile, join

# Global variables
ErrCounter = 0
author = None
Title = None
flag = None
pdf = None

# Print progress bar status, this is only for the user to see, nothing less than graphics
def progress_bar(current, total, bar_length=20):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '-'
    padding = int(bar_length - len(arrow)) * ' '
    ending = '\n' if current == total else '\r'
    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)
    # This sleep is ONLY FOR GRAPHICS PURPOSE, can be disabled or turnedo to 0 if full performance is needed
    time.sleep(0.01)

# Check Numper of PDF files in the directory
def getNumPDF(onlyfiles):
    nPDF = 0
    for file in onlyfiles:
        if(file.split('.')[1] == 'pdf'):
            nPDF += 1   
    return nPDF

# Reset the global variables
def restoreAll():
    global flag
    global author
    global Title
    global ErrCounter
    flag = False
    author = False
    Title = False
    ErrCounter = 0

# Write the line to the .txt file, if the writing fails, increase the error counter and write an error line in the .txt file
def writeLine(line, f):
    global ErrCounter
    try:
        f.write(''+ line + '\n')
    except:
        f.write('AN ERROR IS OCCURRED WHILE WRITING TO WRITE THIS LINE \n')
        ErrCounter += 1

# Check if the line is one of the last 4 lines of the pdf, if so, skip to the next line
def checkLast4Lines(page_num, line, lines):
    if(page_num==pdf.getNumPages() -1 and 
    (line == lines[lines.__len__() -1 ] or
     line == lines[lines.__len__() -2 ] or
     line == lines[lines.__len__() -3 ] or 
     line == lines[lines.__len__() -4 ])): 
        return True
    return False

# Check if the line is the book title OR the author
def checkPrintAuthorANDTitle(page_num, line, f):
    global author
    global Title
    # If the line is the book title, write it to the .txt file
    if(page_num == 0 and not Title):
        f.write('Title: '+ line + '\n')
        Title=True
        return True
    # If the line is the author, write it to the .txt file
    if(page_num == 0 and not author):
        f.write('Author: '+ line + '\n')
        author=True
        return True
    return False

# Check if the line is a valid line
def checkValidLine(line, lines):
    global flag
    # Exclude the lines that are dates
    if(line.split(' ').__len__() > 2 and line.split(' ')[2] == '2022'):
        return False
    # Exclude the lines that are empty
    if(line == ''):
        return False
    # Exclude the lines above the start of the highlighted text
    if(line == 'NOTE DA'):
        flag = True
        return False
    return True

# Main function
def main(filename):
    global flag
    global pdf
    file_path = 'Input/'
    Paragraph = True
    ParagraphName = ''
    restoreAll()
    pdf = PdfFileReader(file_path+filename)
    # Create a new .txt file to write to, called as the filename of the pdf file analyzed
    with open('Output/' + filename.split('.')[0] + '.txt', 'w') as f:
        print('Total Pages: ' + str(pdf.numPages))
        # Loop through each page of the pdf
        for page_num in range(pdf.numPages):
            # Print progress bar status (this is only for the user to see, nothing less than graphics)
            progress_bar(page_num+1, pdf.numPages)
            pageObj = pdf.getPage(page_num)
            # Extract the text from the page
            try: 
                text = pageObj.extract_text()
            except:
                pass
            else:
                # Split the text into lines
                lines = text.split('\n')
                # Loop through each line
                for line in lines:
                    # If the line is NOT a valid line, skip to the next line
                    if(not checkValidLine(line, lines)):
                        continue
                    # If the program has NOT reached the start of the highlighted text, skip to the next line 
                    if(flag == False):
                        continue
                    # If the line is the book title OR the author, write that to the .txt file
                    if(checkPrintAuthorANDTitle(page_num, line, f)):
                        continue
                    # If the line is one of the last 4 lines of the pdf, skip to the next line
                    if(checkLast4Lines(page_num, line, lines)):
                        continue
                    # If the line is a paragraph TITLE, check if is the first time that the program has seen it
                    if(Paragraph):
                        # Avoid writing the same paragraph title twice or more
                        linesplitted=line.split(',')
                        if(linesplitted.__len__() == 2 
                        and linesplitted[1].__len__() >= 3 
                        and linesplitted[1][0] + linesplitted[1][1] + linesplitted[1][2] == ' p.'):
                            line = linesplitted[0]
                        # If the program has NOT seen the paragraph title yet, write it to the .txt file
                        if(line == ParagraphName):
                            # Paragraph already found, skip to the next line
                            Paragraph = False
                            continue
                        else:
                            # Write the paragraph title to the .txt file
                            f.write('\n')
                            ParagraphName=line
                            lastSection = ParagraphName.split(',')
                            # If the paragraph title is associated with a page, write only the paragraph title
                            if(lastSection.__len__() >= 2 and lastSection[lastSection.__len__()-1].split('.')[0] == ' p'):
                                line = lastSection[0]
                                for index in range(1, lastSection.__len__()-1):
                                    line = line + ',' + lastSection[index]
                        Paragraph=False
                    else:
                        # Write the line to the .txt file
                        Paragraph=True
                    writeLine(line, f)
        # After the loop is done, close the .txt file
        f.close()

#Main Program
if __name__ == "__main__":
    fileskipped = 0
    # Get all files in the Input folder
    onlyfiles = [f for f in listdir('Input/') if isfile(join('Input/', f))]
    if(getNumPDF(onlyfiles) == 0):
        print('No PDF files in Input folder')
        exit()
    print('-----------------------------------------------------')
    # For each file in the Input folder, check if it is a pdf file, and if so, run the main function
    for file in onlyfiles:
        if(file.split('.')[1] != 'pdf'):
            fileskipped += 1
            continue
        print('Processing: ' + file)
        # Run the main function
        main(file)
        print('Issues: ' + str(ErrCounter))
        print('Completed: ' + file)
        print('-----------------------------------------------------')
    # Once all files have been processed, print the number of files processed (total files minus files skipped)
    print('Done! ' + str(getNumPDF(onlyfiles)) + ' files were processed.')