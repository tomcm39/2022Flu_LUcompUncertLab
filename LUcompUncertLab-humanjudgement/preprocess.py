#mcandrew

import sys
from metaculus_client import metaculus_client
from interfaceForServer import interfaceForServer

if __name__ == "__main__":
    interface = interfaceForServer()
    
    metac = metaculus_client("../../../../metaculusloginInfoFlu.text")
    metac.sendRequest2Server() # ping the server
   
    #questions = [9483, 9482, 9481, 9480, 9479, 9478, 9334, 9340, 9331, 9328, 9324, 9337, 9339, 9341, 9342,9338,9336,9335,9333]
    questions = interface.collectAllQuestionIds()
    
    for q in questions:
        sys.stdout.write('\rDownloading data from Q {:04d}\r'.format(q))
        sys.stdout.flush()

        metac.collectQdata(q) # collect json data for this specific question
        if metac.data["type"]=="discussion":
            continue

        if metac.hasDist() == False: # skip question with textual answers only
            continue
        metac.constructPDF()  # contstuct community, unweighted consensus PDF

        if len(metac.dens)==0:
            continue
        interface.extractCommunityPrediction(metac)

     # compute and store prob dens functions
    interface.communityPredictions2DF()
    interface.out()

    # compute quantiles
    interface.computeAllQuantiles()
    interface.mergeQuantilesAndPredictions()
    interface.out(quants=True)
