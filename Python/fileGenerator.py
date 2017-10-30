import time
from openpyxl import Workbook
from dataClasses import excelHeader


class fileGenerator:

    def __init__(self, inputData):

        self.data = inputData
        self.header = excelHeader()
        self.wb = Workbook()


    def writeDataToSheet(self, inputData, sheet, header):

        sheet.append(header)

        keys = inputData.keys()
        
        for key in keys:
            for row in inputData[key]:
                sheet.append(row)


    def writeDataToFile(self, fileType):

        #if fileType == 'INWARD':
        #    sheet = self.wb.worksheets[0]
        #elif fileType == 'OUTWARD':
        #    sheet = self.wb.worksheets[1]
       
        if fileType == 'INWARD':
            titleToReport = self.header.inwardSheetTitle.toReport
            titleToManual = self.header.inwardSheetTitle.toManual
            #filename = 'Inward_Remittance_' + time.strftime("%Y%m%d_%X", time.localtime()) + '.xlsx'
            filename = 'Inward_Remittance_' + time.strftime("%Y%m%d", time.localtime()) + '.xlsx'

            dataToReport = self.data.inwardData.dataToReport
            dataToManual = self.data.inwardData.dataToManual

        elif fileType == 'OUTWARD':
            titleToReport = self.header.outwardSheetTitle.toReport
            titleToManual = self.header.outwardSheetTitle.toManual
            filename = 'Outward_Remittance_' + time.strftime("%Y%m%d", time.localtime()) + '.xlsx'

            dataToReport = self.data.outwardData.dataToReport
            dataToManual = self.data.outwardData.dataToManual


        index = 0
        sheet = self.wb.worksheets[index]
        sheet.title = titleToReport 
        self.writeDataToSheet(dataToReport, sheet, self.header.inwardHeader)

        index += 1
        self.wb.create_sheet()
        sheet = self.wb.worksheets[index]
        sheet.title = titleToManual
        self.writeDataToSheet(dataToManual, sheet, self.header.inwardHeader)

        #filename = r'./%s' % filename
        print filename
        self.wb.save(r'./%s' % filename)


    def run(self):
        #self.writeDataToFile('INWARD')
        self.writeDataToFile('OUTWARD')
