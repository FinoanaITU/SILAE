import os
import numpy as np
import pandas as pd
import zipfile
import re
class FileAnalyse():
    def __init__(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
    
    def getFileContent(self,file='', dico=False):
        path_to_dico = os.path.join(self.directory,"data",'dico.txt')
        allData = []
        dataTab = open(path_to_dico)  if dico else  file.read().decode('unicode-escape').splitlines() 
        for line in dataTab:
            data = None
            tabLine = line.replace('\n', '').split(',')
            if  len(tabLine) > 1 and tabLine[0] != " ":
                data = [tabLine[0],tabLine[1].replace("'",'')]
            elif len(tabLine[0]) >= 100 :
                data=['S20.G01.00.002',self.findNomEntrepriseByReg(tabLine[0])]
            allData.append(data) if data != None else None
        
        return np.array(allData)

    def compareFileAndDoc(self,type='',zipFile_Data='',file_data=''):
        dico_list = self.getFileContent(dico=True)
        file_list = zipFile_Data if type =="zip" else file_data
        data = {}
        taxeApprentissage = False 
        for d,dico_code in enumerate(dico_list):
            for f,line_file in enumerate(file_list):
                if dico_code[0] == line_file[0]:
                    #filtrer masse salariale by code taxe pour Taxe apprentissage
                    if line_file[0] == "S21.G00.44.001" and line_file[1] == "001":
                        ms = float(file_list[f+1][1])
                        # data['masse_salariale_TA'] = int(round(ms))
                        data = self.calculeTA(data,dico_code, line_file, ms)
                        taxeApprentissage = True

                    #pour masse salariale CDD/ formation continue
                    if line_file[0] == "S21.G00.44.001" and line_file[1] == "013":
                        ms = int(round(float(file_list[f+1][1])))
                        data['masse_salariale_CDD'] = ms
                        # data = self.calculeTA(data,dico_code, line_file, ms)

                    #pour masse salariale formation professionel
                    if line_file[0] == "S21.G00.44.001" and line_file[1] == "007":
                        ms = int(round(float(file_list[f+1][1])))
                        if taxeApprentissage == False:
                            data = self.calculeTA(data,dico_code, line_file, ms)
                        data['masse_salariale_CFP'] = ms
                    elif line_file[0] != "S21.G00.44.001" and line_file[0] != "S21.G00.44.002":
                        # data.append({dico_code[1]:line_file[1]})
                        data[dico_code[1]] = line_file[1]
        return data

    def extractZipFile(self,file_name):
        path_to_file = os.path.join(self.directory,"data",file_name)
        return zipfile.ZipFile(path_to_file)

    def dataByzip(self,file):
        # zip = self.extractZipFile(file_name)
        zip = zipfile.ZipFile(file)
        finalData = []
        for name in zip.namelist():
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

    def isZipFileUpload(self,nameFile):
        reg = r"\.zip"
        match = re.search(reg,nameFile)
        if match != None:
            return True
        else: 
            return False

    def calculeTA(self,data,dico_code, line_file, ms):
        data[dico_code[1]] = line_file[1] 
        calcul = lambda valeur,pourcentage: int(round((valeur*pourcentage)/100))
        taxe = calcul(ms,0.68)
        data['Taxe_apprentissage'] = taxe
        data['solde_ecole'] = calcul(taxe,13)
        data['opco'] = calcul(taxe,87)
        data['masse_salariale_TA'] = round(ms)

        return data

# def main():
#     # print(FileAnalyse.getFileContent('dico.txt'),'--------------------')
#     # print(FileAnalyse().getFileContent('DSN_CL0071_202011_53877903400031!_NE_01.edi'))

#     # data = FileAnalyse().compareFileAndDoc('autre','','almas_85122637300013_1912_11_RG.txt')
#     # print(data)
#     FileAnalyse().dataByzip('Complet.zip')

# if __name__ == "__main__":
#     main()