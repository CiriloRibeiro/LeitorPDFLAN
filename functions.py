import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
import PyPDF2
import time
import re
import pandas as pd

CONTENT_KEYS = ['IL','Phase Delay', 'Delay Skew', 'RL', 'NEXT', 'ELFEXT']
IL_TITLE = 'Summary and Graphic: Insertion loss (IL)'
PD_TITLE = 'Summary and Graphic: Phase delay'
DS_TITLE = 'Summary and Graphic: Skew'
RL_TITLE = 'Summary and Graphic: Return Loss'
NEXT_TITLE = 'Summary and Graphic: Near End Crosstalk'
ELFEXT_TITLE = 'Summary and Graphic: Equal Level FEXT'
TITLES = [IL_TITLE,PD_TITLE,DS_TITLE,RL_TITLE,NEXT_TITLE,ELFEXT_TITLE]

INDEX_IL = ['IL Par 1', 'IL Par 2', 'IL Par 3', 'IL Par 4']
INDEX_RL = ['RL Par 1', 'RL Par 2', 'RL Par 3', 'RL Par 4']
INDEX_PD = ['PD Par 1', 'PD Par 2', 'PD Par 3', 'PD Par 4']
INDEX_DS = ['DS 1x2', 'DS 1x3', 'DS 1x4', 'DS 2x3', 'DS 2x4', 'DS 3x4']
INDEX_NEXT = ['NEXT 1x2', 'NEXT 1x3', 'NEXT 1x4', 'NEXT 2x3', 'NEXT 2x4', 'NEXT 3x4']
INDEX_ELFEXT = ['ELFEXT 1x2', 'ELFEXT 1x3', 'ELFEXT 1x4', 'ELFEXT 2x1', 'ELFEXT 2x3', 'ELFEXT 2x4', 'ELFEXT 3x1', 'ELFEXT 3x2', 'ELFEXT 3x4', 'ELFEXT 4x1', 'ELFEXT 4x2', 'ELFEXT 4x3']

pattern = "(?<=\]\\n)-?[0-9]{1,2}[,|.][0-9]*(?=\s\()"

#liberar extensão no windows explorer: abrir pasta -> Exibir -> Extensões de nomes de arquivos
def get_pdf_files(print_files = False):
    root = Tk()
    # Hide the main window of Tkinter
    #root.withdraw()
    # Open the folder dialog to select a directory
    folder_path = askdirectory()
    # Get the list of files and directories inside the selected folder
    contents = os.listdir(folder_path)
    # Filter the contents to include only files ending with ".pdf"
    pdf_files = [item for item in contents if item.endswith(".pdf") or item.endswith(".PDF")]
    if print_files:
        # Print the selected folder path
        print(f"Selected Folder:  {folder_path} \n")
        # Print the names of PDF files
        print("PDF Files:\n")
        for file_name in pdf_files:
            print(file_name)
        print("\n")
    root.destroy()
     
    folder_path =  os.path.abspath(folder_path) ##make sure the path works both on unix and windows systems
        
    return pdf_files, folder_path

def createLookups(CONTENT_KEYS, TITLES):
    lookups = dict(zip(CONTENT_KEYS,TITLES))
    return lookups


def pdfFileReader(pdf_file, lookups):
    try:
        with open(pdf_file, 'rb') as pdfFileObj:
            reader = PyPDF2.PdfReader(pdfFileObj)
            if "\\" in pdf_file:  # windows
                title = pdf_file.split('\\')[-1]
            else:
                title = pdf_file.split('/')[-1]
            pages = len(reader.pages)
            content = saveLANParam(reader, title, pages, lookups)
            return content
    except FileNotFoundError as e:
        print(f"File not found: {pdf_file}")
        print(e)
    except PermissionError as e:
        print(f"Permission denied for file: {pdf_file}")
        print(e)
    except Exception as e:
        print(f"An error occurred while opening the file: {pdf_file}")
        print(e)


def saveLANParam(reader, title, pages, lookups):
    content = {}
    keys_to_delete = []
    for page in range(pages):
        pageObj = reader.pages[page]
        pageText = pageObj.extract_text()
        #print(pageText)
        if page == 0 and (isLookupTitle(pageText,"ANEXT") or isLookupTitle(pageText,"AFEXT")):  
            return {}
        for key, value in lookups.items():
            if isLookupTitle(pageText, value):
                content[key] = pageText
                keys_to_delete.append(key)

        if keys_to_delete:
            for key in keys_to_delete:
                del lookups[key]
            keys_to_delete = []  # Reset the list for the next iteration
            #print(len(lookups))
            
        if lookups == {}:
            return content
            
    return content

def isLookupTitle(content, lookup):
    if lookup in content:
        #print(lookup)
        return True
    else:
        return False

def readPdfsFolder(files, folder):
    df_IL = pd.DataFrame(columns=INDEX_IL)
    df_PD = pd.DataFrame(columns=INDEX_PD)
    df_DS = pd.DataFrame(columns=INDEX_DS)
    df_RL = pd.DataFrame(columns=INDEX_RL)
    df_NEXT = pd.DataFrame(columns=INDEX_NEXT)
    df_ELFEXT = pd.DataFrame(columns=INDEX_ELFEXT)
    index_files = []
    for file in files:
        full_path = os.path.join(folder, file)
        lookups = createLookups(CONTENT_KEYS, TITLES)
        dictionary = pdfFileReader(full_path,lookups)
        if dictionary != {}:
            index_files.append(file)
            print(f'== Atual: {file}...Leitura {len(index_files)}/{len(files)}  ==')
            IL = getValues(dictionary['IL'], pattern, INDEX_IL)
            PhaseDelay = getValues(dictionary['Phase Delay'], pattern, INDEX_PD)
            DelaySkew = getValues(dictionary['Delay Skew'], pattern, INDEX_DS)
            RL = getValues(dictionary['RL'], pattern, INDEX_RL)
            NEXT = getValues(dictionary['NEXT'], pattern, INDEX_NEXT)
            ELFEXT = getValues(dictionary['ELFEXT'], pattern, INDEX_ELFEXT)
            df_IL = df_IL.append(IL, ignore_index=True)
            df_PD = df_PD.append(PhaseDelay, ignore_index=True)
            df_DS = df_DS.append(DelaySkew, ignore_index=True)
            df_RL = df_RL.append(RL, ignore_index=True)
            df_NEXT = df_NEXT.append(NEXT, ignore_index=True)
            df_ELFEXT = df_ELFEXT.append(ELFEXT, ignore_index=True)
            ####falta resolver como deixar o dataframe aninhado com todas as tabelas
            
    df = pd.concat([df_IL, df_PD, df_DS, df_RL, df_NEXT, df_ELFEXT], axis=1, join="inner")
    df['arquivo'] = index_files
    df = df.set_index('arquivo')
    return df
        
def getValues(filtered_dict, pattern, df_columns):
    param = re.findall(pattern, filtered_dict)
    param = [float(s.replace(",",".")) for s in param]
    data = pd.Series(param,index=df_columns)
    return data