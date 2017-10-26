import time
from openpyxl import Workbook

class File_Generator:

    def __init__(self, inputDataToReport, inputDataToManual):

        self.inputDataToReport = inputDataToReport
        self.inputDataToManual = inputDataToManual
        self.wb = Workbook()


    def writeDataToSheet(self, inputData, sheet, header):

        sheet.append(header)

        keys = inputData.keys()
        
        for key in keys:
            for row in inputData[key]:
                sheet.append(row)


    def writeDataToFile(self, fileType):

        if fileType == 'INWARD':
            sheet = self.wb.worksheets[0]
        elif fileType == 'OUTWARD':
            sheet = self.wb.worksheets[1]
       
        if fileType == 'INWARD':
            header = ['Transaction Value Date(663)', 'Ref. NO.', 'From(662)', 'AMOUNT', 'Currency(664)', 'Customer', 'Rate', 'SEK', 'Origanisation Number/ID', 'Personal Number', 'Address', 'Tax Code'] 
            titleToReport = 'Inward Remittance Report'
            titleToManual = 'Inward Remittance Manually Confirm'
            #filename = 'Inward_Remittance_' + time.strftime("%Y%m%d_%X", time.localtime()) + '.xlsx'
            filename = 'Inward_Remittance_' + time.strftime("%Y%m%d", time.localtime()) + '.xlsx'

        elif FILETYPE == 'OUTWARD':
            header = ['CP03_BEN_CUS_NO', 'CP03_EXTN_REF_NO', 'CP03_PAY_CURR', 'CP03_PAY_AMT', 'FROM_CON'] 
            titleToReport = 'Outward Remittance Report'
            titleToManual = 'Outward Remittance Manually Confirm'
            filename = 'Outward_Remittance_' + time.strftime("%Y%m%d_%X", time.localtime()) + '.xlsx'



        index = 0
        sheet = self.wb.worksheets[index]
        sheet.title = titleToReport 
        self.writeDataToSheet(self.inputDataToReport, sheet, header)

        index += 1
        self.wb.create_sheet()
        sheet = self.wb.worksheets[index]
        sheet.title = titleToManual
        self.writeDataToSheet(self.inputDataToManual, sheet, header)

        #filename = r'./%s' % filename
        print filename
        self.wb.save(r'./%s' % filename)


    def run(self):
        self.writeDataToFile('INWARD')
