from curses import reset_shell_mode
import os, sys
from flask import Flask, render_template, request
"""
sys.path.insert(1, os.path.abspath('.'))
"""
from src.Archive import Archive
from src.Utilities import Utilities
import src.Constants  as Constants
from src import myConfig

from glob import glob
from io import BytesIO
from zipfile import ZipFile
from flask import send_file
from shutil import rmtree
app = Flask(__name__)

@app.route('/')
def index():
    return search()

def download():
    target = os.getcwd() + '/' + "extract"

    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for file in glob(os.path.join(target, '*')):
            zf.write(file, os.path.basename(file))
    stream.seek(0)
    # Remove folder after zipping
    rmtree(target)
    return send_file(
        stream,
        as_attachment=True,
        attachment_filename='archive.zip'
    )

@app.route("/search", methods=['GET', 'POST'])
def search():
     
    Utilities.checkCurrentArchive()
    extension = ""
    pathName = ""
    type = ""
    folderName = ""
    fileName = ""
    search = ""
    typeSearch = "simple"

    resources = []
    myArchive = Archive(myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME))
    
    extensions = myArchive.myDb.getAllExtensions()
    pathNames = myArchive.myDb.getAllPathNames()
    types = myArchive.myDb.getAllTypes()
    folderNames = myArchive.myDb.getAllFolderNames()
    fileNames = myArchive.myDb.getAllFileNames()
    try:
        if request.method == 'POST':
            # check if button btnExtract is pressed
            if request.form['btnExtract'] == 'Extract':
                metadataIds = request.form.getlist('metadataIds')
                #return metadataIds
                if len(metadataIds) >= 1:
                    metadatas = myArchive.myDb.getMetadatasByIds(metadataIds)
                    myArchive.extractResources(metadatas, os.getcwd()+"/extract")
                    return download()
            else:
                filters = dict()
                resources = []
    
                extension = request.form.get("selectExtension")
                pathName = request.form.get("selectPathName")
                type = request.form.get("selectType")
                folderName = request.form.get("selectFolderName")
                fileName = request.form.get("selectFileName")
                typeSearch = request.form['typeSearch']
                search = request.form['search']
                try:
                
                    # test valeur du radio button pour le type de recherche
                    match typeSearch:
                        case "fullText":
                            if search != "":
                                resources = myArchive.searchFullText(search)
                        case "simple":
                            if search != "":
                                filters = dict(x.split(':') for x in search.split(' '))
                            if extension != "":
                                filters["extension"] = extension
                            if pathName != "":
                                filters["pathName"] = pathName
                            if type != "":
                                filters["type"] = type
                            if folderName != "":
                                filters["folderName"] = folderName
                            if fileName != "":
                                filters["fileName"] = fileName
                            resources = myArchive.search(filters)
                            pass
                except Exception as e:
                    pass
                #myArchive.saveToExtract(resources)
        return render_template('search.html', 
        resources=resources, 
        extensions=extensions, 
        pathNames=pathNames, 
        types=types, 
        folderNames=folderNames, 
        fileNames=fileNames, 
        extension=extension, 
        pathName=pathName, 
        type=type, 
        folderName=folderName, 
        fileName=fileName,
        search=search,
        typeSearch=typeSearch
        )
    except Exception as e:
        return render_template('search.html', 
        resources=resources, 
        extensions=extensions, 
        pathNames=pathNames, 
        types=types, 
        folderNames=folderNames, 
        fileNames=fileNames, 
        extension=extension, 
        pathName=pathName, 
        type=type, 
        folderName=folderName, 
        fileName=fileName,
        search=search,
        typeSearch=typeSearch
        )


