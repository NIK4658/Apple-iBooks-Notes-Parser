# -*- coding: utf-8 -*-
import time
from PyPDF2 import PdfFileReader
from os import listdir
from os.path import isfile, join

ErrCounter = 0
author = None
Title = None
flag = None
pdf = None

def progress_bar(current, total, bar_length=20):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '-'
    padding = int(bar_length - len(arrow)) * ' '
    ending = '\n' if current == total else '\r'
    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)
    time.sleep(0.01)

def restoreAll():
    global flag
    global author
    global Title
    global ErrCounter
    flag = False
    author = False
    Title = False
    ErrCounter = 0

def writeLine(line, f):
    global ErrCounter
    try:
        f.write(''+ line + '\n')
    except:
        f.write('AN ERROR IS OCCURRED WHILE WRITING TO WRITE THIS LINE \n')
        ErrCounter += 1

def checkLast4Lines(page_num, line, lines):
    if(page_num==pdf.getNumPages() -1 and 
    (line == lines[lines.__len__() -1 ] or
     line == lines[lines.__len__() -2 ] or
     line == lines[lines.__len__() -3 ] or 
     line == lines[lines.__len__() -4 ])): 
        return True
    return False

def checkPrintAuthorANDTitle(page_num, line, f):
    global author
    global Title
    if(page_num == 0 and not Title):
        f.write('Title: '+ line + '\n')
        Title=True
        return False
    if(page_num == 0 and not author):
        f.write('Author: '+ line + '\n')
        author=True
        return False
    return True

def checkValidLine(line, lines):
    global flag
    if(line.split(' ').__len__() > 2 and line.split(' ')[2] == '2022'):
        return False
    if(line == ''):
        return False
    if(line == 'NOTE DA'):
        flag = True
        return False
    return True


def main(filename):
    global flag
    global pdf

    file_path = 'Input/'
    Paragraph = True
    ParagraphName = ''

    restoreAll()
    pdf = PdfFileReader(file_path+filename)

    with open('Output/' + filename.split('.')[0] + '.txt', 'w') as f:
        print('Total Pages: ' + str(pdf.numPages))
        for page_num in range(pdf.numPages):
            progress_bar(page_num+1, pdf.numPages)
            pageObj = pdf.getPage(page_num)
            try: 
                text = pageObj.extract_text()
            except:
                pass
            else:
                lines = text.split('\n')
                for line in lines:
                    if(not checkValidLine(line, lines)):
                        continue
                    if(flag == False):
                        continue
                    if(not checkPrintAuthorANDTitle(page_num, line, f)):
                        continue
                    if(checkLast4Lines(page_num, line, lines)):
                        continue

                    if(Paragraph):
                        linesplitted=line.split(',')
                        if(linesplitted.__len__() == 2 
                        and linesplitted[1].__len__() >= 3 
                        and linesplitted[1][0] + linesplitted[1][1] + linesplitted[1][2] == ' p.'):
                            line = linesplitted[0]

                        if(line == ParagraphName):
                            Paragraph = False
                            continue
                        else:
                            f.write('\n')
                            ParagraphName=line
                            lastSection = ParagraphName.split(',')
                            if(lastSection.__len__() == 2 and lastSection[1].split('.')[0] == ' p'):
                                Paragraph=False
                                writeLine(lastSection[0], f)
                                continue
                        Paragraph=False
                    else:
                        Paragraph=True
                    writeLine(line, f)
        f.close()

if __name__ == "__main__":
    fileskipped = 0
    onlyfiles = [f for f in listdir('Input/') if isfile(join('Input/', f))]
    if(onlyfiles.__len__() == 0):
        print('No files in Input folder')
        exit()
    print('-----------------------------------------------------')
    for file in onlyfiles:
        if(file.split('.')[1] != 'pdf'):
            fileskipped += 1
            continue
        print('Processing: ' + file)
        main(file)
        print('Issues: ' + str(ErrCounter))
        print('Completed: ' + file)
        print('-----------------------------------------------------')
    print('Done! ' + str(onlyfiles.__len__() - fileskipped) + ' files were processed.')