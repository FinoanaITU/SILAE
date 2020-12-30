import os
import numpy as np
import pandas as pd

class FileAnalyse:
    
    def getFileContent(file_name):
        directory = os.path.dirname(os.path.dirname(__file__))
        path_to_file = os.path.join(directory,"../data",file_name )
        allData = []
        for line in open(path_to_file):
            tabLine = line.replace('\n', '').split(',')
            data = [
                tabLine[0],
                tabLine[1].replace("'",'')
            ]
            allData.append(data)
        
        # return np.array(allData)
        data_np=np.array(allData)
        print(data_np)

        # data_pd = pd.DataFrame(data_np)
        # print(data_pd)

    def compareFileAndDoc(file_name):
        dico_list = FileAnalyse.getFileContent('dico.txt')
        file_list = FileAnalyse.getFileContent(file_name)
        

def main():
    FileAnalyse.getFileContent('DADSU-19_CABESTAN.txt')

if __name__ == "__main__":
    main()