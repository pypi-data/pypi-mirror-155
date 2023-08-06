#Für Generieren von Barcode benötigt
import os
import barcode
from barcode.writer import ImageWriter

def createBarcode(auftragsnummer="0",foldername=".//tmp//"):

    ######################################################
    #Ausgabe in Ordner
    ######################################################
    #Unterverzeichnis anlegen, falls noch nicht existent
    if not os.path.isdir(foldername):
        os.mkdir(foldername)
    ###########################################################
    
    ean = barcode.get('code128', auftragsnummer, writer=ImageWriter())
    filename = ean.save(os.path.join(foldername,str("BAR_"+auftragsnummer)))

