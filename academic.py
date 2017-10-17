import requests
import xlsxwriter
import os

# generates excel files from the dictionaries
def xlsx_file(filename,listname):
	workbook = xlsxwriter.Workbook(os.path.join('excel_files', filename))
	worksheet = workbook.add_worksheet()
	row=0
	col=0

	for i in range(0,len(listname)):
	    row+=1
	    worksheet.write(row, col, i+1)
	    worksheet.write(row, col+1, listname[i])

	workbook.close()

# counts the number of papers in a particular year
def papers_in_a_year():
	parameters = {"vclass" : "http://vivoweb.org/ontology/core#ConferencePaper"}
	headers = {"Accept":"text/plain"}
	url = "https://vivo.ufl.edu/listrdf"
	r = requests.post(url, params = parameters, headers = headers)
	flag=0
	register=[]
	count=0

	for line in r.text.splitlines():
		paperUrl = line.split()[0].split("<")[1].split(">")[0] + "?format=rdfxml"
		rPaper = requests.get(paperUrl)

		for moreLines in rPaper.text.splitlines():

			if "vivo:dateTimeValue" in moreLines:
				dateTimeUrl = moreLines.split("\"")[1] + "?format=rdfxml"
				rDate = requests.get(dateTimeUrl)

				for moreLinesForDate in rDate.text.splitlines():

					if "vivo:dateTime" in moreLinesForDate and moreLinesForDate.split(">")[1].split("<")[0].split("-")[0] == "2010":
						print "Paper url : " + paperUrl.replace("individual","display").split("?")[0]
						register.append(paperUrl.replace("individual","display").split("?")[0])
						count=count+1
						flag=1
						break

			if flag==1:
				f=0
				break

	print "Total Number of Paper Published in 2010 %d is \n" % count	
	print register

	xlsx_file('register.xlsx',register)

def main():
	papers_in_a_year()

if __name__=='__main__':
	main()