import time
import json





# mutual recursion

def listParserAndCodeCreator( theList, rootCode = "", collectionOfCodes = list() ):


    if len(theList) == 0:
        return collectionOfCodes, rootCode


    for itemIdx in range(len(theList)):

        codeSoFar = rootCode
        if (not isinstance( theList[ itemIdx ], dict ) ) and (not isinstance( theList[ itemIdx ], list) ) and (not isinstance(theList[ itemIdx ], tuple) ):
            codeSoFar = codeSoFar + '[' + str(itemIdx) + ']'
            collectionOfCodes.append( codeSoFar )

        elif isinstance( theList[ itemIdx ], dict ):
            nestedDict = theList[ itemIdx ]
            codeSoFar = codeSoFar + '[' + str(itemIdx) +  ']'
            collectionOfCodes, codeSoFar = jsonParserAndCodeCreator( nestedDict, codeSoFar, collectionOfCodes )

        elif isinstance( theList[itemIdx], list ) or isinstance( theList[itemIdx], tuple ):
            nestedList = theList[itemIdx]
            codeSoFar = codeSoFar + '[' + str(itemIdx) + ']'
            collectionOfCodes, codeSoFar = listParserAndCodeCreator( nestedList, codeSoFar, collectionOfCodes )         

    return collectionOfCodes, codeSoFar



def jsonParserAndCodeCreator( theDict:dict, rootCode = "", collectionOfCodes = list() ):


    codeSoFar = rootCode
    for key in theDict:
    
        codeSoFar = rootCode
        if (not isinstance(theDict[key], dict ) ) and (not isinstance(theDict[key], list) ) and (not isinstance(theDict[key], tuple) ):
            codeSoFar = codeSoFar + '["' + str(key) +  '"]'
            collectionOfCodes.append( codeSoFar )

        elif isinstance( theDict[key], dict ):
            nestedDict = theDict[key]
            codeSoFar = codeSoFar + '["' + str(key) +  '"]'
            collectionOfCodes, codeSoFar = jsonParserAndCodeCreator( nestedDict, codeSoFar, collectionOfCodes )

        elif isinstance( theDict[key], list ) or isinstance( theDict[key], tuple ):
            nestedList = theDict[key]
            codeSoFar = codeSoFar + '["' + str(key) + '"]'
            collectionOfCodes, codeSoFar = listParserAndCodeCreator( nestedList, codeSoFar, collectionOfCodes )         


    return collectionOfCodes, codeSoFar








