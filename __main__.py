from functions import *
import pandas as pd

def main():
	lista, folder = get_pdf_files()

	df = readPdfsFolder(lista,folder)
	with pd.ExcelWriter('output.xlsx') as writer:
		df.to_excel(writer, sheet_name='Output')

if __name__ == '__main__':
	main()