import pikepdf # maybe pikepdf https://www.geeksforgeeks.org/how-to-crack-pdf-files-in-python/
import os

passwordList = [""]

def unlock(inputPath: str, outputPath: str = None, filename: str = None):
    for password in passwordList:
        try:
            
            # open PDF file and check each password
            with pikepdf.open("/home/matthew/Documents/programing/python/fuckMyNelson/users/user1/Chemistry 12U - Student Text PDF (Online)/14-12-2021_11h-42m-01s/tmp/1.pdf", password = password) as p:
                # If password is correct, break the loop
                print("[+] Password found:", password)
                break
                
        # If password will not match, it will raise PasswordError
        except pikepdf._qpdf.PasswordError as e:
            
            # if password is wrong, continue the loop
            continue


def merge(inputPdfPaths, outputPdfPath, name):
    pass

if __name__ == '__main__':
    unlock(inputPath="1")
    # merger = PdfFileMerger()
    # pathIn = "D://Programing//Python//programs//fuckMyNelson//users//user1//Chemistry 12U - Student Text PDF (Online)//13-12-2021_19h-29m-36s//tmp"
    # pathOut = "D://Programing//Python//programs//fuckMyNelson//users//user1//Chemistry 12U - Student Text PDF (Online)//13-12-2021_19h-29m-36s"
    # name = "Chemistry 12U - Student Text PDF (Online).pdf"
    # print()
    # for pdf in sorted(os.listdir(pathIn), key=lambda x: int(os.path.splitext(x)[0])):
    #     merger.append(os.path.join(pathIn,pdf))
    # merger.write(os.path.join(pathOut,name))
    # merger.close()