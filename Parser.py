from PyPDF2 import PdfFileReader, PdfFileWriter 

file_path = 'Summary2.pdf'
pdf = PdfFileReader(file_path)
flag = False
author = False
Title = False
Paragraph = True
ParagraphName = ''

with open('NotesFile.txt', 'w') as f:
    for page_num in range(pdf.numPages):
        print('Page: {0}'.format(page_num))
        pageObj = pdf.getPage(page_num);
        try: 
            text = pageObj.extract_text()
            print(''.center(100, '-'))
        except:
            print('Error')
            pass
        else:
            lines = text.split('\n')
            for line in lines:
                if (line == lines[0] or line == lines[1]):
                    pass
                if (line.split(' ').__len__() > 2):
                    if(line.split(' ')[2] == '2022'):
                        continue
                if(line == ''):
                    continue
                if(line == 'NOTE DA'):
                    flag = True
                    continue
                if(flag == False):
                    print('pass')
                    continue
                print('print')
                if(page_num==0 and not Title):
                    f.write('Title: '+ line + '\n')
                    Title=True
                    continue
                if(page_num==0 and not author):
                    f.write('Author: '+ line + '\n')
                    author=True
                    continue
                if(page_num==pdf.getNumPages()-1 and (line == lines[lines.__len__()-1] or line == lines[lines.__len__()-2] or line == lines[lines.__len__()-3] or line == lines[lines.__len__()-4])): 
                    continue
                if(Paragraph):
                    if(line == ParagraphName):
                        Paragraph = False
                        continue
                    else:
                        f.write('\n')
                        ParagraphName=line
                        lastSection = ParagraphName.split(',')
                        if(lastSection.__len__() == 2 and lastSection[1].split('.')[0] == ' p'):
                            Paragraph=False
                            f.write(''+ lastSection[0] + '\n')
                            continue
                    Paragraph=False
                else:
                    Paragraph=True
                try:
                    f.write(''+ line + '\n')
                except:
                    f.write('AN ERROR IS OCCURRED WHILE WRITING TO WRITE THIS LINE \n')
    f.close()