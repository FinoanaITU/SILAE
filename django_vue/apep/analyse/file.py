import os
import numpy as np
import pandas as pd
import zipfile
import re
class FileAnalyse():
    def __init__(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
    
    def getFileContent(self,file_name):
        path_to_file = os.path.join(self.directory,"data",file_name )
        allData = []
        for line in open(path_to_file):
            tabLine = line.replace('\n', '').split(',')
            if  len(tabLine) > 1 :
                data = [tabLine[0],tabLine[1].replace("'",'')]
            else:
                data=['S20.G01.00.002',self.findNomEntrepriseByReg(tabLine[0])]
            allData.append(data)
        
        return np.array(allData)

    def compareFileAndDoc(self,type,zipFile_Data,file_name=''):
        dico_list = self.getFileContent('dico.txt')
        file_list = zipFile_Data if type =="zip" else self.getFileContent(file_name)
        data = [] 
        for d,dico_code in enumerate(dico_list):
            for f,line_file in enumerate(file_list):
                if dico_code[0] == line_file[0]:
                    # print({dico_code[1]:line_file[1]})
                    data.append({dico_code[1]:line_file[1]})
        return data

    def extractZipFile(self,file_name):
        path_to_file = os.path.join(self.directory,"data",file_name)
        return zipfile.ZipFile(path_to_file)

    def dataByzip(self,file_name):
        zip = self.extractZipFile(file_name)
        finalData = []
        for name in zip.namelist():
            print(name)
            allData = []
            dataTab = zip.read(name).decode('unicode-escape').splitlines()
            for lineData in dataTab:
                if len(lineData) <= 100 :
                    value = lineData.split(',')
                    allData.append([value[0],value[1].replace("'",'')])
                else:
                    nomEntreprise = self.findNomEntrepriseByReg(lineData)
                    allData.append(['S20.G01.00.002', nomEntreprise])
            finalData.append(self.compareFileAndDoc('zip',allData))
            # print(finalData)
        return finalData

    def findNomEntrepriseByReg(self,text):
        regex = r"(?<=\+11=)(.*)(?=\+12)"
        matches = re.search(regex,text)
        return matches.group(0)


# def main():
#     # print(FileAnalyse.getFileContent('dico.txt'),'--------------------')
#     # print(FileAnalyse().getFileContent('DSN_CL0071_202011_53877903400031!_NE_01.edi'))

#     # data = FileAnalyse().compareFileAndDoc('autre','','almas_85122637300013_1912_11_RG.txt')
#     # print(data)
#     FileAnalyse().dataByzip('Complet.zip')

# if __name__ == "__main__":
#     main()