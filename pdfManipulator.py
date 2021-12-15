import pikepdf # maybe pikepdf https://www.geeksforgeeks.org/how-to-crack-pdf-files-in-python/
import os, sys, concurrent.futures

def unlock(inputPdfPath: str, outputPdfPath: str = None):
    passwordList = [""]
    for password in passwordList:
        try:
            # open pdf file and check each password
            with pikepdf.open(inputPdfPath, password = password) as crackedPdf:
                # If opened save cracked pdf 
                fileOut = (outputPdfPath if outputPdfPath != None else os.path.join(os.path.dirname(inputPdfPath),os.path.splitext(os.path.basename(inputPdfPath))[0]+"Cracked"+os.path.splitext(os.path.basename(inputPdfPath))[1]))
                crackedPdf.save(fileOut)
                break
        except pikepdf._qpdf.PasswordError as err:
            continue

def multiUnlock(inputPdfPaths: list, outputPdfPath: str = None):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(unlock, inputPdfPath=pdf, outputPdfPath=os.path.join(outputPdfPath,os.path.basename(pdf))) for pdf in inputPdfPaths]

def mergePdfs(inputPdfPaths: str, outputPdfPath: str):
    mergePdf = pikepdf.Pdf.new()
    for pdfPath in inputPdfPaths:
        pdfPart = pikepdf.Pdf.open(pdfPath)
        mergePdf.pages.extend(pdfPart.pages)
        pdfPart.close()
    mergePdf.save(outputPdfPath)

if __name__ == '__main__':
    pathTmp = os.path.join(sys.path[0],"users","user1","Chemistry 12U - Student Text PDF (Online)","13-12-2021_19h-29m-36s","tmp")
    pathCracked = os.path.join(sys.path[0],"users","user1","Chemistry 12U - Student Text PDF (Online)","13-12-2021_19h-29m-36s","cracked")
    pathMerge = os.path.join(sys.path[0],"users","user1","Chemistry 12U - Student Text PDF (Online)","13-12-2021_19h-29m-36s","Chemistry 12U - Student Text PDF (Online)"+".pdf")
    # for pdf in os.listdir(pathTmp):
    #     unlock(inputPdfPath=os.path.join(pathTmp,pdf), outputPdfPath=os.path.join(pathCracked,pdf))
    # multiUnlock(inputPdfPaths = [os.path.join(pathTmp,pdf) for pdf in os.listdir(pathTmp)], outputPdfPath = pathCracked)    
    mergePdfs(inputPdfPaths = [os.path.join(pathTmp, file) for file in sorted(os.listdir(pathTmp), key=lambda x: int(os.path.splitext(x)[0]))], outputPdfPath = pathMerge)