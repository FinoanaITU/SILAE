import os
import numpy as np
import pandas as pd
import zipfile
import re

from pandas.core.construction import is_empty_data
class FileAnalyse():
    def __init__(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
    
    def getFileContent(self,file='', dico=False):
        path_to_dico = os.path.join(self.directory,"data",'dico.txt')
        allData = []
        # dataTab = open(path_to_dico)  if dico else  file.read().decode('unicode-escape').splitlines() 
        dataTab = open(path_to_dico)  if dico else  self.readFile(file.read()) 
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
                        data['assujjetie_taxe'] = 'oui'

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
                        data['masse_salariale_FPC'] = ms
                    elif line_file[0] != "S21.G00.44.001" and line_file[0] != "S21.G00.44.002":
                        # data.append({dico_code[1]:line_file[1]})
                        data[dico_code[1]] = line_file[1]
        #calcule OPCO
        data = self.getDataOPCOxlsx(data)
        self.calculeOPCO(data,data['masse_salariale_TA'] if 'masse_salariale_TA' in data else 0 ,data['masse_salariale_CDD'] if 'masse_salariale_CDD' in data else 0 ,data['effectif_moyen_entreprise'] if 'effectif_moyen_entreprise' in data else 0 )
        data ['pdfCreate'] = False
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
            # dataTab = zip.read(name).decode('utf-8').splitlines()
            dataTab = self.readFile(zip.read(name))
            for lineData in dataTab:
                if len(lineData) <= 100 and re.search(r'\\',lineData) == None :
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
        return matches.group(0) if matches != None else ''

    def isZipFileUpload(self,nameFile):
        reg = r"\.zip"
        match = re.search(reg,nameFile)
        if match != None:
            return True
        else: 
            return False

    def calculeTA(self,data,dico_code, line_file, ms):
        data[dico_code[1]] = line_file[1] 
        calcul = lambda valeur,pourcentage: (valeur*pourcentage)/100
        taxe = calcul(ms,0.68)
        data['Taxe_apprentissage'] = round(taxe)
        data['solde_ecole'] = round(calcul(taxe,13))
        data['opco'] = round(calcul(taxe,87))
        data['masse_salariale_TA'] = round(ms)

        return data

    def calculeOPCO(self, data, ms_continue, ms_cdd, nbr_salarie):
        contribution = lambda masse,pourcentage: round((masse*pourcentage)/100, 2)
        if(int(nbr_salarie) <= 11):
            data['contribution_legale'] = contribution(ms_continue,0.55)
            data['contribution_cdd'] = contribution(ms_cdd,1)
            self.acompteCUFPA(data,ms_continue,0,0)
        else:
            data['contribution_legale'] = contribution(ms_continue,1)
            data['contribution_cdd'] = contribution(ms_cdd,1)
            self.acompteCUFPA(data,ms_continue,1,0)

        return data
    
    def acompteCUFPA(self, data, ms_continue, pourcentage_form_continue, masse_alsace):
        contributions_formation = lambda masse,pourcentage: round((((masse*pourcentage)/100)*60)/100, 2)
        ta_metropole = lambda masse: round((((((masse*0.68)/100)*87)/100)*60)/100, 2)
        ta_alsace = lambda masse_alsace: round((((masse_alsace*0.44)/100)*60)/100, 2)

        data['contributions_formation'] = contributions_formation(ms_continue,pourcentage_form_continue)
        data['ta_metropole'] = ta_metropole(ms_continue)
        data['ta_alsace'] = ta_alsace(masse_alsace)

        return data


    def readFile(self, fileString):
        dataTab = []
        try:
            dataTab = fileString.decode('unicode-escape').splitlines()
        except UnicodeDecodeError:
            dataTab = fileString.decode('utf-8').splitlines()
        finally:
            return dataTab

    def getDataOPCOxlsx(self, data):
        path_to_file = os.path.join(self.directory,"data",'BaseOPCO.xlsx')
        # data = pd.read_excel(path_to_file, engine='openpyxl')
        allFile = pd.ExcelFile(path_to_file, engine='openpyxl')
        # opcoList = ['AFDAS','OPCO SANTE', 'OPCO ENT PROX', 'OPCO MOBILITES','OPCO 2I', 'OPCOMMERCE', 'AKTO','CONSTRUCTYS', 'COHESION SOCIALE','OCAPIAT','ATLAS']
        index_col =['branche', 'idcc', 'brochure', 'opca','opco','address']
        feuille = pd.read_excel(allFile)
        feuille.columns = index_col
        idcc = int(data['IDCC']) if 'IDCC' in data else 0
        # ligneOp = feuille[feuille.idcc == idcc]
        ligneOp = feuille[feuille.idcc == idcc]
        if ligneOp.empty == False:
            activiter  = str(ligneOp.branche).replace("'", ' ').replace("é",'e').replace('è','e').replace('Name: branche, dtype: object','')
            # print(self.formatActiviter(activiter))
            address = str(ligneOp.address).replace('Name: address, dtype: object','').replace('\n','')
            print(self.removeNumber(activiter))
            data['activite'] = self.removeNumber(self.formatActiviter(activiter))+'...'
            data['nom_opco'] = self.removeNumber(str(ligneOp.opco).replace('Name: opco, dtype: object','').replace('\n',''))
            data['address_opco'] = address[3:]
        print(ligneOp)
        # for i,opcoName in enumerate(opcoList):
        #     feuille = pd.read_excel(allFile, opcoName)
        #     feuille.columns = index_col 
        #     idcc = int(data['IDCC']) if 'IDCC' in data else 0
        #     ligneOp = feuille[feuille.idcc == idcc]
        #     if ligneOp.empty == False:
        #         self.formatActiviter(str(ligneOp.branche))
        #         activiter  = str(ligneOp.branche).replace("'", ' ').replace("é",'e').replace('è','e').replace('\n','').replace('Name: branche, dtype: object','')
        #         data['activite'] = activiter
        #         data['nom_opco'] = opcoName
        #     # else:
        #     #     print(idcc)
        #     #     print(opcoName)
        #     #     print('--------------------')
        return data

    def removeNumber(self, str):
        # i=0
        return re.sub(r"\d+", '', str)
        #    
    def formatActiviter(self, activiter):
        return re.sub('[^0-9a-zA-Z]+', ' ', activiter)
        
def main():
    # print(FileAnalyse.getFileContent('dico.txt'),'--------------------')
    # print(FileAnalyse().getFileContent('DSN_CL0071_202011_53877903400031!_NE_01.edi'))

    # data = FileAnalyse().compareFileAndDoc('autre','','almas_85122637300013_1912_11_RG.txt')
    # print(data)
    FileAnalyse().getDataOPCOxlsx()

if __name__ == "__main__":
    main()