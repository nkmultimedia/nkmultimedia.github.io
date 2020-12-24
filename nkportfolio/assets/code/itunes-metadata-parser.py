###################################################################################################
## PROGRAM TO READ AND PARSE AN ITUNES LIBRARY, GROUP BY A SELECTED FIELD (ALBUM, ARTIST, ETC),  ##
## AND STORE EACH GROUP IN A SEPERATE XML FILE (BASED ON REQUIRED FIELD)                         ##
##  ###########################################################################################  ##
##                                  Written in Python 2.7                                        ##
###################################################################################################

# import statements
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

##################################################################
# Method to read the given XML file (from fpath) and return the parsed XML tree
# NAME: getXML
# PARAMS: 
#       fpath - File path of iTunes Library XML file
# RETURNS: XML Tree read from the file path
##################################################################
def getXML(fpath):
    # Check if the given XML file exists
    if not os.path.exists(fpath):
        print "\n\nCan't find the iTunes Library. Please check the provided file name and path"
        return -1
    if not os.path.isfile(fpath):
        print "\n\nThe provided input is not a file. Please proived a proper file."
        return -1

    xmlString = ""
    print "Opening iTunes Library..."
    with open(fpath, 'r') as itunesLibFhand:
        print "Library opened!"
        # Ignore the first two lines of the XML file (Initial <XML> opening tag and <!DOCTYPE> tag)
        for i in [1,2]:
            itunesLibFhand.readline()
        print "Reading library..."
        # Read each line from XML and append to xmlString
        for line in itunesLibFhand:
            xmlString += line.strip()   # Remove trailing whitespaces
        print "Library reading complete!"

    print "Parsing XML... (this may take a while)"
    # CONVERTING XML STRING TO XML ELEMENT TREE
    itunesXML = ET.fromstring(xmlString)
    print "Parsing complete!"
    return itunesXML

##################################################################
# Method to extract iTunes Library Information (iTunes version, etc)
# NAME: getItunesInfo
# PARAMS:
#       itunesXML - iTunes Library XML Tree
# RETURNS: iTunes Library Information
##################################################################
def getItunesInfo(itunesXML):
    print "Extracting iTunes Library information..."
    # From itunesXML, copy all data except Playlists & Tracks
    itunesInfo = itunesXML[0][0:-4]
    if itunesInfo[-2].text == 'Tracks': # Remove extra 'Tracks' entry from itunesInfo
        itunesInfo = itunesInfo[0:-2]
    print "Extracted iTunes information!"
    return itunesInfo

##################################################################
# Method to append all fields from itunesInfo into the given XML element
# NAME: appendItunesInfo
# PARAMS: 
#       elem - XML element to store the iTunes Library information
#       itunesInfo - iTunes Library information
# RETURNS: XML element after appending itunes information
##################################################################
def appendItunesInfo(elem,itunesInfo):
    for item in itunesInfo:
        elem.append(item)
    return elem

##################################################################
# Method to extract an XML subtree containing all songs from the given iTunes library
# NAME: getTracks
# PARAMS: 
#       itunesXML - iTunes Library XML Tree
# RETURNS: XML subtree containing all songs in the given library
##################################################################
def getTracks(itunesXML):
    print "Getting Tracks..."
    # iTunes Library XML contains an array of key and value nodes
    # Loop through each node to locate the key named 'Tracks'
    for i in range(len(itunesXML[0])):
        if itunesXML[0][i].text != 'Tracks':
            continue
        # The 'Tracks' key node has been found
        # The node immediately after this one is the subtree that we are looking for
        tracks = itunesXML[0][i+1]
        break
    print "Done! Library has " + str(len(tracks)) + " tracks"
    return tracks

##################################################################
# Method to loop through the given tracks and extract all tracks that match the required category and target
# If the target is 'all', then all given tracks are grouped by the required category
# Ex 1: Extract all tracks from the album 'Thriller'
# Ex 2: Extract all tracks, grouped by albums
#
# NAME: getTracksByCategory
# PARAMS: 
#       tracks - XML tree of all songs
#       category - User's selected category (album, artist, genre, etc)
#       target - Specific target within category (specific album, etc) OR 'all' (select all entries present in the given category)
# RETURNS: JSON object containing the required tracks, grouped based on the given category 
#          (if target='all', then all songs are returned, grouped by the given category (ex: albums) )
##################################################################
def getTracksByCategory(tracks, category, target):
    print "Getting all tracks by " + category
    name = ""
    groups = {}                     # JSON object containing the required targets grouped by category 
    category = category.lower()     # selected category (ex: album)
    target = target.lower()         # selected target (ex: Thriller)
    # Loop through all tracks
    for track in tracks:
        # Loop through nodes (keys and values) within track
        for i in range(len(track)):
            if track[i].text and track[i].text.lower() == category:
                # Node corresponding to selected category (ex: album) has been found
                name = track[i+1].text # Name of category (name of album, ex: Thriller)
                if target != 'all': # If target is specific (ex: Thriller)
                    # Check if the found entry within our category (album) is the target we are looking for (ex: Thriller)
                    if name.lower() != target:
                        continue
                # If groups doesn't contain our target (ex: Thriller)
                if name not in groups:
                    # Add target (ex: Thriller) to groups{}
                    print "Found " + category + " " + name
                    groups[name] = []
                groups[name].append(track)

    print "Extracted all " + str(len(groups.items())) + " " + category + "! "
    return groups
    
##################################################################
# Method to sanitize the given string for use as an acceptable file name
# NAME: sanitize
# PARAMS: 
#       name - File name to sanitize
# RETURNS: Sanitized file name
##################################################################
def sanitize(name):
    for char in ['\\',':','/','?','%']:
        name = name.replace(char, '_')
    return name

##################################################################
# Method to construct the final XML tree and write it to a file
# NAME: createXML
# PARAMS: 
#       group - XML subtree containing all tracks within the selected group (ex: all songs in the album 'Thriller')
#       name - Name of the group (ex: 'Thriller')
#       itunesInfo - iTunes Library Information 
# RETURNS: NONE
##################################################################
def createXML(group, name, itunesInfo):
    print "Constructing new XML data for " + name + "..."

    # CREATE NEW XML ROOT NODE AND APPEND ITUNES LIBRARY INFORMATION
    root = ET.Element('plist')
    root.set('version', '1.0')
    root = appendItunesInfo(root, itunesInfo)

    # CREATE A NEW <KEY> AND <DICT> NODE TO STORE TRACKS
    rootkey = ET.SubElement(root,'key')
    rootkey.text = "Tracks"
    groupTracks = ET.SubElement(root,'dict')

    # ADD TRACKS TO XML TREE
    for i in range(len(group)):     # FOR EACH TRACK
        # APPEND TRACK
        keyElem = ET.Element('key')
        trackElem = group[i]
        keyElem.text = trackElem[1].text
        groupTracks.append(keyElem)
        groupTracks.append(trackElem)
    
    # FINALIZE XML TREE
    tree = ET.ElementTree(root)
    print "XML data constructed!"
    print "Creating file '" + name + ".xml'"
    # STRINGIFY AND RE-PARSE THE TREE TO CLONE THE OBJECT
    reparsed = minidom.parseString(ET.tostring(root)).toprettyxml(indent="\t")
    # SANITIZE FILE NAME BEFORE CREATING FILE
    name = sanitize(name)

    # WRITE THE FINAL XML FILE
    with open(name + ".xml", 'w') as fh:
        fh.write(reparsed.encode('utf-8'))
    print "File created!"


##################################################################
# Method containing the primary flow of the script               #
# NAME: main                                                     #
# PARAMS: NONE                                                   #
# RETURNS: NONE                                                  #
##################################################################
def main():
    fpath = "./iTunes Library.xml"
    categories = ["name", "artist", "album artist", "album", "genre", "kind", "year", "bit rate", "sample rate"]

    # INITIAL USER INPUT
    print "\nWelcome! This is a script to categorically extract information from your iTunes library\nPlease make sure that the file 'iTunes Library.xml' is in the same folder as this script\n"

    # GET CATEGORY TO EXTRACT
    while True:
        print "\nOn what category would you like to extract your data? (Album, Genre, Artist, etc)"
        category = raw_input()
        if category.lower() in categories:  # check if the user has entered a valid category
            break
        # Invalid input => give the user a list of valid categories
        print "That's not supported at the moment. Here are the possible options:"
        for item in categories:
            print item.capitalize()

    # GET SPECIFIC TARGET WITHIN SELECTED CATEGORY (EX, SPECIFIC ALBUM, SPECIFIC ARTIST, ETC)
    while True:
        print "\nPlease enter the " + category + " that you want to extract (Enter 'all' to extract all " + category + "s): "
        target = raw_input()
        if target:  # check if the user has entered a target
            break

    # READ AND PROCESS RAW ITUNES LIBRARY DATA
    print("")
    itunesXML = getXML(fpath)
    # itunesXML contains the iTunes XML Tree

    if itunesXML < 0:   # File not found
        print "\nSorry, the iTunes Library could not be found."
        return False

    # EXTRACT REQUIRED DATA
    # Get iTunes Info
    itunesInfo = getItunesInfo(itunesXML)
    # Get all tracks
    tracks = getTracks(itunesXML)
    # Extract the required tracks (based on target), and group by category (ex: group by albums)
    groupedData = getTracksByCategory(tracks, category, target)


    if target.lower() == 'all':     # Need to extract all groups to separate XML files
        # CREATE DIRECTORY FOR NEW FILES (EX: NEW DIRECTORY FOR ALBUMS)
        dirname = './' + category.lower().capitalize() + 's'
        if not os.path.exists(dirname):
            print "Creating new directory to store the files..."
            os.mkdir(dirname)
            print "Directory created!"
        os.chdir(dirname)   # Navigate into new directory

    # Loop through each group in groupedData, and extract each group to a separate XML file
    for group in groupedData.keys():
        # Create a new XML file for each group (ex: each album) present in groupedData
        createXML(groupedData[group], group, itunesInfo)
#############################
### CALLING MAIN FUNCTION ###
#############################
main()
print "\nScript completed successfully!"