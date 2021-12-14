from PyPDF2 import PdfFileMerger # maybe pikepdf https://www.geeksforgeeks.org/how-to-crack-pdf-files-in-python/
import os

if __name__ == '__main__':
    merger = PdfFileMerger()
    pathIn = "D://Programing//Python//programs//fuckMyNelson//users//user1//Chemistry 12U - Student Text PDF (Online)//13-12-2021_19h-29m-36s//tmp"
    pathOut = "D://Programing//Python//programs//fuckMyNelson//users//user1//Chemistry 12U - Student Text PDF (Online)//13-12-2021_19h-29m-36s"
    name = "Chemistry 12U - Student Text PDF (Online).pdf"
    print()
    for pdf in sorted(os.listdir(pathIn), key=lambda x: int(os.path.splitext(x)[0])):
        merger.append(os.path.join(pathIn,pdf))
    merger.write(os.path.join(pathOut,name))
    merger.close()