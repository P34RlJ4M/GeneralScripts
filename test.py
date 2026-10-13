loggerName = 'Melt Deck Project'
functionName = 'EvaluateResults'
startTime = system.date.now()
result = True
try:
    import time

    time.sleep(2)
    udtPaths = {
        '1': '[default]Melt_Deck/Line_1',
        '2': '[default]Melt_Deck/Line_2',
        '3': '[default]Melt_Deck/Line_3',
        '4': '[default]Melt_Deck/Line_4',
        '5': '[default]Melt_Deck/Line_5'
    }

    ## Query Local DB for Latest Spectrometer Result
    queryOk = False
    query = 'SELECT * FROM spectrometerresults ORDER BY id DESC LIMIT 1'
    latestRecord = system.db.runQuery(query=query, database='Ignition Prod', tx='')
    latestRecord = utility.datasetToDict(latestRecord)
    if not utility.isNullOrEmpty(latestRecord) and len(latestRecord) == 1:
        latestFurnace = latestRecord['furnace']
        latestUdtTagPath = udtPaths[str(latestFurnace)]
        latestRecipe = latestRecord['recipe']
        latestSource = latestRecord['source']
        queryOk = True

    else:
        msg = 'Error: Latest Record Retrieval from Database Failed..'

    ## Filters out Spectrometer Results that are not for the Furnace
    sourceOk = False
    if queryOk:
        if str(latestSource).lower() == 'furnace':
            sourceOk = True

        else:
            msg = 'Error: Latest Spectrometer Result was not a Furnace Source..'

    ## Validates Recipe from Spectrometer Result matches Expected
    recipeOk = False
    if sourceOk:
        if str(latestRecipe).lower() == '85 brass' or str(latestRecipe).lower() == 'no lead':
            recipeOk = True

        else:
            msg = 'Error: Latest Spectrometer Result used an Unknown Recipe..'

    # Calculates Required Additions (Charges)
    additionCheckOk = False
    if recipeOk:
        if str(latestRecipe).lower() == '85 brass':
            print
            'this is a lead furnace check'

            latestTin = latestRecord['tin']
            tinAdditions = 0.0
            latestPhos = latestRecord['phosphorus']
            phosAdditions = 0.0
            latestZinc = latestRecord['zinc']
            zincAdditions = 0.0
            latestCopper = latestRecord['copperbalance']
            zincFromCopperAdditions = 0.0
            finalZincAdditions = 0.0
            latestNickel = latestRecord['nickel']
            latestCuNi = latestCopper + latestNickel
            copperAdditions = 0.0

            tinLookups = [
                {'low': 0.00, 'high': 4.00, 'additions': -1},
                {'low': 4.00, 'high': 4.05, 'additions': 20},
                {'low': 4.05, 'high': 4.10, 'additions': 16},
                {'low': 4.10, 'high': 4.13, 'additions': 10},
                {'low': 4.13, 'high': 4.16, 'additions': 8},
                {'low': 4.16, 'high': 100, 'additions': 0}
            ]
            for i in tinLookups:
                low = i['low']
                high = i['high']
                additions = i['additions']
                if latestTin >= low and latestTin < high:
                    tinAdditions = float(additions)
                    print
                    'needs TIN additions = ' + str(tinAdditions)
                    break

            phosLookups = [
                {'low': 0.000, 'high': 0.005, 'additions': 6},
                {'low': 0.005, 'high': 0.007, 'additions': 4},
                {'low': 0.007, 'high': 0.009, 'additions': 2},
                {'low': 0.009, 'high': 100, 'additions': 0}
            ]
            for i in phosLookups:
                low = i['low']
                high = i['high']
                additions = i['additions']
                if latestPhos >= low and latestPhos < high:
                    phosAdditions = float(additions)
                    print
                    'needs PHOS additions = ' + str(phosAdditions)
                    break

            zincLookups = [
                {'low': 0.00, 'high': 4.00, 'additions': -1},
                {'low': 4.00, 'high': 4.68, 'additions': 'calc'},
                {'low': 4.68, 'high': 4.73, 'additions': 44},
                {'low': 4.73, 'high': 4.78, 'additions': 38},
                {'low': 4.78, 'high': 4.83, 'additions': 33},
                {'low': 4.83, 'high': 4.88, 'additions': 27},
                {'low': 4.88, 'high': 4.93, 'additions': 22},
                {'low': 4.93, 'high': 4.98, 'additions': 17},
                {'low': 4.98, 'high': 5.05, 'additions': 11},
                {'low': 5.05, 'high': 100, 'additions': 0}
            ]
            for i in zincLookups:
                low = i['low']
                high = i['high']
                additions = i['additions']
                if latestZinc >= low and latestZinc < high:
                    if str(additions) == 'calc':
                        additions = ((5.10 - float(latestZinc)) * 110)

                    zincAdditions = float(additions)
                    print
                    'needs ZINC additions = ' + str(zincAdditions)
                    break

            copperLookups = [
                {'low': 0.00, 'high': 85.75, 'additions': 0},
                {'low': 85.75, 'high': 85.80, 'additions': 11},
                {'low': 85.80, 'high': 85.85, 'additions': 17},
                {'low': 85.85, 'high': 85.90, 'additions': 22},
                {'low': 85.90, 'high': 85.95, 'additions': 28},
                {'low': 85.95, 'high': 86.00, 'additions': 33},
                {'low': 86.00, 'high': 100, 'additions': -1}
            ]

            for i in copperLookups:
                low = i['low']
                high = i['high']
                additions = i['additions']
                if latestCopper >= low and latestCopper < high:
                    zincFromCopperAdditions = float(additions)
                    if zincAdditions == -1:
                        finalZincAdditions = -1

                    else:
                        if zincAdditions == 0:
                            finalZincAdditions = zincFromCopperAdditions

                        elif zincAdditions >= zincFromCopperAdditions:
                            finalZincAdditions = zincAdditions

                        elif zincAdditions < zincFromCopperAdditions:
                            finalZincAdditions = zincFromCopperAdditions

                    print
                    'copper needs zinc additions = ' + str(zincFromCopperAdditions)
                    print
                    'final adjusted zinc additions = ' + str(finalZincAdditions)
                    break

            cuNiLookups = [
                {'low': 0.00, 'high': 84.00, 'additions': -1},
                {'low': 84.00, 'high': 84.10, 'additions': 22},
                {'low': 84.10, 'high': 84.20, 'additions': 12},
                {'low': 84.20, 'high': 100, 'additions': 0}
            ]
            for i in cuNiLookups:
                low = i['low']
                high = i['high']
                additions = i['additions']
                if latestCuNi >= low and latestCuNi < high:
                    copperAdditions = float(additions)
                    print
                    'needs copper additions = ' + str(copperAdditions)
                    break

            additionCheckOk = True

        else:
            additionCheckOk = True
            print 'this is a no lead furnace check'

    ## Writes Calcualted Additions to Furnace UDT Tag
    writeOk = False
    if additionCheckOk:
        writePaths = [
            latestUdtTagPath + '/1_Data/CopperAdditions',
            latestUdtTagPath + '/1_Data/PhosAdditions',
            latestUdtTagPath + '/1_Data/TinAdditions',
            latestUdtTagPath + '/1_Data/ZincAdditions'
        ]
        writeVals = [
            copperAdditions,
            phosAdditions,
            tinAdditions,
            finalZincAdditions
        ]
        writeRes = system.tag.writeBlocking(writePaths, writeVals, timeout=3000)
        for res in writeRes:
            if str(res) == 'good':
                writeOk = True

            else:
                writeOk = False
                msg = 'Error: Failed to Write Additions to UDT Tag..'
                break

    # Finalize Script Execution
    if writeOk:
        result = True
        msg = 'Successfully processed Spectrometer Results.. (Cu = ' + str(copperAdditions) + ', P = ' + str(
            phosAdditions) + ', Sn = ' + str(tinAdditions) + ', Zn = ' + str(finalZincAdditions) + ')'

except Exception as e:
    msg = utility.formatErrorMessage(e)

writePath = event.getTagPath()
writeRes = system.tag.writeBlocking([str(writePath)], [0])
endTime = system.date.now()
delta = system.date.millisBetween(startTime, endTime)
utility.insertLogEntry(loggerName=loggerName, functionName=functionName, result=result, message=msg,
                       executionTime=delta)

