import csv

def convertWebscraperToGephi(webscraperFile, webscraperFileFields, gephiNodesFileFields, gephiEdgesFileFields):
    gephiNodesFile, gephiEdgesFile= openGephiFiles()

    try:
        webScraperReader, gephiNodesWriter, gephiEdgesWriter= instantiateReadersAndWriters(webscraperFile, gephiNodesFile, gephiEdgesFile)

        writeGephiFilesHeaders(gephiNodesWriter, gephiEdgesWriter, gephiNodesFileFields, gephiEdgesFileFields)

        jumpFirstLineOfFile(webscraperFile)
        currentCitatedPatentNumber= None
        seen = {}
        nodeId, citatedId, citatorId = 0, 0, 0
        for row in webScraperReader:
            if row[webscraperFileFields['patent_number']] not in seen:
                nodeId+= 1;
                citatedId= nodeId;
                writeCitatedPatentNode(citatedId, gephiNodesWriter, row, webscraperFileFields)
                seen[row[webscraperFileFields['patent_number']]] = citatedId;
            if row[webscraperFileFields['citator_patent_number']] not in seen:
                nodeId+= 1;
                citatorId= nodeId;
                writeCitatorPatentNode(citatorId, gephiNodesWriter, row, webscraperFileFields)
                seen[row[webscraperFileFields['citator_patent_number']]] = citatorId;
            currentCitatedPatentNumber= row[webscraperFileFields['patent_number']]

            writeEdge(seen[row[webscraperFileFields['patent_number']]], seen[row[webscraperFileFields['citator_patent_number']]],
                gephiEdgesWriter, row, webscraperFileFields, currentCitatedPatentNumber)
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

def jumpFirstLineOfFile(file):
    file.readline();

def hasCitatedPatentChanged(row, webscraperFileFields, currentCitatedPatentNumber):
    if(row[webscraperFileFields['patent_number']] != currentCitatedPatentNumber):
        return True

    return False

def writeCitatedPatentNode(citatedId, gephiNodesWriter, row, webscraperFileFields):
    gephiNodesWriter.writerow((
        citatedId,
        row[webscraperFileFields['patent_number']],
        row[webscraperFileFields['patent_link']],
        row[webscraperFileFields['patent_link-href']],
        parsePatentDate(row[webscraperFileFields['patent_date']]),
        row[webscraperFileFields['patent_assignee']],
        row[webscraperFileFields['patent_abstract']]
    ))

def writeCitatorPatentNode(citatorId, gephiNodesWriter, row, webscraperFileFields):
    if(row[webscraperFileFields['citator_patent_number']]):
        gephiNodesWriter.writerow((
            citatorId,
            row[webscraperFileFields['citator_patent_number']],
            row[webscraperFileFields['citator_link']],
            row[webscraperFileFields['citator_link-href']],
            parsePatentDate(row[webscraperFileFields['citator_date']]),
            row[webscraperFileFields['citator_assignee']],
            row[webscraperFileFields['citator_abstract']]
        ))

def writeEdge(citatedId, citatorId, gephiEdgesWriter, row, webscraperFileFields, currentCitatedPatentNumber):
    if(row[webscraperFileFields['citator_patent_number']]):
        gephiEdgesWriter.writerow((
            citatorId,
            citatedId,
            'Directed',
            row[webscraperFileFields['citator_patent_number']],
            currentCitatedPatentNumber,
            parsePatentDate(row[webscraperFileFields['citator_date']])
        ))

def parsePatentDate(patentDateText):
    splited= patentDateText.split(', ')

    return splited[1];
