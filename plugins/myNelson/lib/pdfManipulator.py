import pikepdf, os, concurrent.futures

def unlock(inputPdfPath: str, outputPdfPath: str = None, passwordList: list[str] = [""]):
    """Takes a input pdf file and a output pdf file if end location is different from the input location or if the name has changed\n
    Usage example:\n
        pdfIn = "pdf1.pdf"\n
        pdfOut = "pdf2.pdf"\n
        passwordList = [""]\n
        unlock(inputPdfPath=pdfIn, outputPdfPath=pdfOut, passwordList=passwordList)\n"""
    # check to see if input pathfile is correct
    if os.path.isfile(inputPdfPath) == False:
        print("Input filepath  does not exist: "+inputPdfPath)
        raise
    for password in passwordList:
        try:
            # open pdf file and check each password to see if it correct
            with pikepdf.open(inputPdfPath, password = password) as crackedPdf:
                # gens cracked pdfs name 
                fileOut = (outputPdfPath if outputPdfPath != None else os.path.join(os.path.dirname(inputPdfPath),os.path.splitext(os.path.basename(inputPdfPath))[0]+"Cracked"+os.path.splitext(os.path.basename(inputPdfPath))[1]))
                # checks if the fileOut already exist if it does then add number increment to the file name
                if os.path.isfile(fileOut) == True:
                    fileNum = 1
                    while os.path.isfile(os.path.join(os.path.dirname(fileOut), os.path.splitext(os.path.basename(fileOut))[0]+"("+str(fileNum)+")"+os.path.splitext(os.path.basename(fileOut))[1])):
                        fileNum += 1
                    fileOut = os.path.join(os.path.dirname(fileOut), os.path.splitext(os.path.basename(fileOut))[0]+"("+str(fileNum)+")"+os.path.splitext(os.path.basename(fileOut))[1])
                crackedPdf.save(fileOut)
                break
        except pikepdf._qpdf.PasswordError as err:
            continue

def multiUnlock(inputPdfPaths: list, outputPdfPath: str = None, passwordList: list[str] = [""]):
    """Takes input pdf files in as a list and the pdf file in to a output directory name is the same as another adds numaric to the name\n
    Usage example:\n
        pdfsIn = ["pdf1.pdf", "pdf2.pdf"]\n
        dirOut = "/dirOut/"\n
        passwordList = [""]\n
        multiUnlock(inputPdfPath=pdfIn, outputPdfPath=dirOut, passwordList=passwordList)\n"""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(unlock, inputPdfPath=pdf, outputPdfPath=os.path.join(outputPdfPath,os.path.basename(pdf)), passwordList=passwordList) for pdf in inputPdfPaths]

def mergePdfs(inputPdfPaths: str, outputPdfFilepath: str):
    """Takes input pdf files in as a list and merges the pdfs in the order of the list then outputs pdf to desired location\n
    Usage example:\n
        pdfsIn = ["pdf1.pdf", "pdf2.pdf"]\n
        pdfout = "ComboPdf.pdf"\n
        mergePdfs(inputPdfPaths = pdfsIn, outputPdfFilepath = pdfout)\n"""
    mergePdf = pikepdf.Pdf.new()
    for pdfPath in inputPdfPaths:
        pdfPart = pikepdf.Pdf.open(pdfPath)
        mergePdf.pages.extend(pdfPart.pages)
        pdfPart.close()
    mergePdf.save(outputPdfFilepath)

if __name__ == '__main__':
    import sys
    pathTmp = os.path.join(sys.path[0],"users","Matthew Zelenka","Chemistry 12U - Student Text PDF (Online)","14-12-2021_11h-42m-01s","tmp")
    pathCracked = os.path.join(sys.path[0],"users","Matthew Zelenka","Chemistry 12U - Student Text PDF (Online)","14-12-2021_11h-42m-01s","cracked")
    filepathMerge = os.path.join(sys.path[0],"users","Matthew Zelenka","Chemistry 12U - Student Text PDF (Online)","14-12-2021_11h-42m-01s","Chemistry 12U - Student Text PDF (Online)"+".pdf")
    # for pdf in os.listdir(pathTmp):
    #     unlock(inputPdfPath=os.path.join(pathTmp,pdf), outputPdfPath=os.path.join(pathCracked,pdf))
    # multiUnlock(inputPdfPaths = [os.path.join(pathTmp,pdf) for pdf in os.listdir(pathTmp)], outputPdfPath = pathCracked)    
    mergePdfs(inputPdfPaths = [os.path.join(pathTmp, file) for file in sorted(os.listdir(pathTmp), key=lambda x: int(os.path.splitext(x)[0]))], outputPdfFilepath = filepathMerge)
    pass