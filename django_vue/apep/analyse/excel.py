import os
import pandas as pd

class excel():
    def __init__(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
            
    def generateExcel(self,data):
        newData = []
        for i,data in enumerate(data):
            value = {
                'siren': data['siren'],
                'Code_naf': data['code_NAF'],
                'Raison_sociale': data['nom_entreprise'],
                'Effectif': data['effectif_moyen_entreprise'] if 'effectif_moyen_entreprise' in data else '0',
                'Apprentie': 0,
                'Assujetie': data['assujjetie_taxe'] if 'assujjetie_taxe' in data else 'non',
                'MS_TA': str(data['masse_salariale_TA'])+'€' if 'assujjetie_taxe' in data and 'masse_salariale_TA' in data  else '0.00€',
                'Assujetie_FPC': 'non',
                'MS_FPC': str(data['masse_salariale_TA'])+'€' if 'masse_salariale_TA' in data else '0.00€',
                'MS_CDD': str(data['masse_salariale_CDD'])+'€' if 'masse_salariale_CDD' in data else '0.00€',
            }
            newData.append(value)
        
        frame = pd.DataFrame(newData)
        #local
        # lienExcel = os.path.join(self.directory,".\excelGenerate\dsn.xlsx")
        #prod
        lienExcel = '/home/SDABOU/SILAE/django_vue/apep/excelGenerate/dsn.xlsx'
        # write =pd.ExcelWriter('excelGenerate/exported_json_data.xlsx', engine='openpyxl')
        write =pd.ExcelWriter(lienExcel, engine='openpyxl')
        frame.to_excel(write, sheet_name='DSN')
        workbook = write.book
        worksheet = write.sheets['DSN']
        
        worksheet.column_dimensions['B'].width = 12
        worksheet.column_dimensions['C'].width = 12
        worksheet.column_dimensions['D'].width = 20
        worksheet.column_dimensions['E'].width = 12
        worksheet.column_dimensions['F'].width = 12
        worksheet.column_dimensions['G'].width = 12
        worksheet.column_dimensions['H'].width = 12
        worksheet.column_dimensions['I'].width = 12
        worksheet.column_dimensions['J'].width = 12
        worksheet.column_dimensions['K'].width = 12

        print(type(worksheet))
        write.save()

        return lienExcel