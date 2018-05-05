import csv

def convertWebscraperToGephi(webscraperFile, webscraperFileFields, gephiNodesFileFields, gephiEdgesFileFields):
    gephiNodesFile, gephiEdgesFile= openGephiFiles()

    try:
        webScraperReader, gephiNodesWriter, gephiEdgesWriter= instantiateReadersAndWriters(webscraperFile, gephiNodesFile, gephiEdgesFile)

        writeGephiFilesHeaders(gephiNodesWriter, gephiEdgesWriter, gephiNodesFileFields, gephiEdgesFileFields)

        currentCitatedPatentNumber= None;
        for row in webScraperReader:
            if(hasCitatedPatentChanged(row, webscraperFileFields, currentCitatedPatentNumber)):
                writeCitatedPatentNode(gephiNodesWriter, row, webscraperFileFields);

            writeCitatorPatentNode(gephiNodesWriter, row, webscraperFileFields)
            currentCitatedPatentNumber= row[webscraperFileFields['patent_number']]
            writeEdge(gephiEdgesWriter, row, webscraperFileFields, currentCitatedPatentNumber)

    finally:
        closeAllFiles(webscraperFile, gephiNodesFile, gephiEdgesFile)

def openGephiFiles():
    gephiNodesFile= open('nodes.csv', 'w', newline='')
    gephiEdgesFile= open('edges.csv', 'w', newline='')

    return gephiNodesFile, gephiEdgesFile

def closeAllFiles(webscraperFile, gephiNodesFile, gephiEdgesFile):
    webscraperFile.close()
    gephiNodesFile.close()
    gephiEdgesFile.close()

def instantiateReadersAndWriters(webscraperFile, gephiNodesFile, gephiEdgesFile):
    webScraperReader= csv.reader(webscraperFile)
    gephiNodesWriter= csv.writer(gephiNodesFile)
    gephiEdgesWriter= csv.writer(gephiEdgesFile)

    return webScraperReader, gephiNodesWriter, gephiEdgesWriter

def writeGephiFilesHeaders(gephiNodesWriter, gephiEdgesWriter, gephiNodesFileFields, gephiEdgesFileFields):
    gephiNodesWriter.writerow(gephiNodesFileFields)
    gephiEdgesWriter.writerow(gephiEdgesFileFields)

def hasCitatedPatentChanged(row, webscraperFileFields, currentCitatedPatentNumber):
    if(row[webscraperFileFields['patent_number']] != currentCitatedPatentNumber):
        return True

    return False

def writeCitatedPatentNode(gephiNodesWriter, row, webscraperFileFields):
    gephiNodesWriter.writerow((
        '',
        row[webscraperFileFields['patent_number']],
        row[webscraperFileFields['patent_link']],
        row[webscraperFileFields['patent_link-href']],
        row[webscraperFileFields['patent_date']],
        row[webscraperFileFields['patent_assignee']],
        row[webscraperFileFields['patent_abstract']]
    ))

def writeCitatorPatentNode(gephiNodesWriter, row, webscraperFileFields):
    if(row[webscraperFileFields['citator_patent_number']]):
        gephiNodesWriter.writerow((
            '',
            row[webscraperFileFields['citator_patent_number']],
            row[webscraperFileFields['citator_link']],
            row[webscraperFileFields['citator_link-href']],
            row[webscraperFileFields['citator_date']],
            '',
            ''
        ))

def writeEdge(gephiEdgesWriter, row, webscraperFileFields, currentCitatedPatentNumber):
    if(row[webscraperFileFields['citator_patent_number']]):
        gephiEdgesWriter.writerow((
            '',
            '',
            'Directed',
            row[webscraperFileFields['citator_patent_number']],
            currentCitatedPatentNumber
        ))
