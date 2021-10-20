# py .\autoxmlconfig.py -i "JS|goatData.js|goatLesson.js|js\jquery\" -i "JAR|WEB-INF\lib\"

configxml = "config.xml"

import os
import glob
from pathlib import Path
import xml.etree.ElementTree as ElementTree
from xml.dom import minidom
from optparse import OptionParser

def get_files(extensions):
    all_files = []
    for ext in extensions:
        all_files.extend(Path('.').glob(ext))
    return all_files

parser = OptionParser()
parser.add_option("-i", "--include", help="List of pipe '|' separated folders and or files. This option will search recursively in the folders provided for all files and any direct files specified and exclude everything else. Use only relative paths. Specify the extention of the files as the first element in the list. For folders, make sure to include the double trailing backslash '\\\\'. This option can be used multiple times. Eg. -i \"JS|path\\to\\folder\\\\|path\\to\\file.js\" -i \"JAVA|path\\to\\other\\folder\\\\|path\\to\\other\\file.java\"", action='append')
(toincludeoptions, args) = parser.parse_args()
parser.print_help()
try:
    configuration = ElementTree.Element('Configuration')
    configuration.set('thirdParty','true')
    targets = ElementTree.SubElement(configuration, 'Targets')
    target = ElementTree.SubElement(targets, 'Target')
    target.set('path','')
    print("\r\n")
    print("===============================================================================")
    print("================================ autoxmlconfig ================================")
    print("===============================================================================")
    print("Found the following JS files to match the include options:")
    print("\r\n")

    presentfoldertemp = os.path.dirname(os.path.realpath(__file__)).split("\\")
    presentfolder = presentfoldertemp[len(presentfoldertemp)-1]

    for toincludetemp in toincludeoptions.include:
        toinclude_data = toincludetemp.split("|")
        extensions_data = set()
        extensions_data.add('**/*.' + str(toinclude_data[0]).lower())
        files = get_files(extensions_data)
        for file in files:
            found = 0
            for toinclude in toinclude_data[1:]:
                
                #print(toinclude[-1])
                #this is a folder so let's check all files in current folder matching extension
                if toinclude[-1] == "\\":
                        #iterate trough all files that match extension in folder
                    if str(toinclude) in str(file) and str(file).split(".")[-1] == str(toinclude_data[0]).lower():  
                        print(presentfolder + "\\" + str(file))
                        found = 1

                #this is a file
                else:
                    if str(file).split("\\")[-1] == str(toinclude):  
                        print(presentfolder + "\\" + str(file))
                        found = 1
                            
            if found == 0:
                exclude = ElementTree.SubElement(target, 'Exclude')
                exclude.text = presentfolder + "\\" + str(file)


    xmlstr = minidom.parseString(ElementTree.tostring(configuration)).toprettyxml(indent="   ")
    with open(configxml, "w") as f:
        f.write(xmlstr)

    print("\r\n")
    print("===============================================================================")
    print("Everything else will be excluded.")
    print("\r\n" + "Written: " + configxml)
    print("\r\n")
    print("\r\n" + "For folders, make sure to include the double trailing backslash '\\\\'.")
    print("\r\n")

except Exception as e: print(e)
    

