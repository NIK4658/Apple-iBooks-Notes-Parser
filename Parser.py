from asyncore import write
from PyPDF2 import PdfFileReader, PdfFileWriter 
from os import listdir
from os.path import isfile, join

file_path = None
pdf = None
flag = None
author = None
Title = None
Paragraph = None
ParagraphName = ''

def restoreAll():
    global flag
    global author
    global Title
    global Paragraph
    global ParagraphName
    global pdf
    global file_path

    file_path = 'Input/'
    pdf = None
    flag = False
    author = False
    Title = False
    Paragraph = True
    ParagraphName = ''

def writeLine(line, f):
    try:
        f.write(''+ line + '\n')
    except:
        f.write('AN ERROR IS OCCURRED WHILE WRITING TO WRITE THIS LINE \n')

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
    global author
    global Title
    global Paragraph
    global ParagraphName
    global pdf
    global file_path

    restoreAll()
    pdf = PdfFileReader(file_path+filename)

    with open('Output/' + filename.split('.')[0] + '.txt', 'w') as f:
        print('Total Pages: ' + str(pdf.numPages))
        for page_num in range(pdf.numPages):
            print('Page: {0}'.format(page_num))
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
                        if(linesplitted.__len__() == 2 and linesplitted[1].__len__() >= 3 and linesplitted[1][0]+linesplitted[1][1]+linesplitted[1][2] == ' p.'):
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
    onlyfiles = [f for f in listdir('Input/') if isfile(join('Input/', f))]
    if(onlyfiles.__len__() == 0):
        print('No files in Input folder')
        exit()
    for file in onlyfiles:
        print('Processing: ' + file)
        main(file)
        print('Completed: ' + file)
        print('-----------------------------------------------------')
    print('Done! ' + str(onlyfiles.__len__()) + ' files were processed.')