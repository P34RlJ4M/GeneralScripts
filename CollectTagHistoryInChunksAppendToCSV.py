### First create a message handler gateway script, name it RunHistoryExport.

###Put the script below inside of the message handler
#
# Put this script on a button to run the script and message handler, change the project
# if name:
#     system.util.sendMessage(
#         project="Americus-RNG",
#         messageHandler="RunHistoryExport"
#     )








import system
import os

# ============================================================
# LOGGER
# ============================================================
logger = system.util.getLogger("GatewayHistoryCSVExport")

def log(msg):
    logger.warn(str(msg))

log("====================================================")
log("SCRIPT START")
log("====================================================")

try:

    # ========================================================
    # CONFIG
    # ========================================================
    historyProvider = "IgnitionSplitter"

    exportFolder = r"C:\myExports"
    exportFile   = exportFolder + r"\AprilHistory_GatewayExport.csv"

    minutesPerHour = 60

    startDate = system.date.parse(
        "2026-04-01 00:00:00",
        "yyyy-MM-dd HH:mm:ss"
    )

    endDate = system.date.parse(
        "2026-05-01 00:00:00",
        "yyyy-MM-dd HH:mm:ss"
    )

    # ========================================================
    # TAG PATHS
    # ========================================================
    paths = [

        # INSERT TAGS HERE

    ]

    log("Configured Tags: %d" % len(paths))

    # ========================================================
    # CREATE EXPORT FOLDER
    # ========================================================
    if not os.path.exists(exportFolder):

        os.makedirs(exportFolder)

        log("Created export folder.")

    # ========================================================
    # DELETE OLD FILE
    # ========================================================
    if os.path.exists(exportFile):

        os.remove(exportFile)

        log("Deleted old export file.")

    # ========================================================
    # VERIFY TAGS
    # ========================================================
    validPaths = []

    for path in paths:

        try:

            if system.tag.exists(path):

                validPaths.append(path)

                log("VALID TAG: %s" % path)

            else:

                log("INVALID TAG: %s" % path)

        except Exception as e:

            log(str(e))

    if len(validPaths) == 0:

        raise Exception("No valid tags found.")

    # ========================================================
    # CSV HEADERS
    # ========================================================
    headers = ["timestamp"]

    columnNames = []

    for path in validPaths:

        col = path.replace(
            "[default]",
            ""
        ).strip("/")

        columnNames.append(col)

        headers.append(col)

    # ========================================================
    # PROCESS HOURS
    # ========================================================
    currentHourStart = startDate

    firstWrite = True

    hourCounter = 0

    while currentHourStart < endDate:

        hourCounter += 1

        currentHourEnd = system.date.addHours(
            currentHourStart,
            1
        )

        log("====================================================")
        log("HOUR #%d" % hourCounter)
        log("%s -> %s" % (
            currentHourStart,
            currentHourEnd
        ))
        log("====================================================")

        masterMap = {}

        # ====================================================
        # PROCESS TAGS
        # ====================================================
        tagCounter = 0

        for path in validPaths:

            tagCounter += 1

            log("----------------------------------------------------")
            log("TAG %d OF %d" % (
                tagCounter,
                len(validPaths)
            ))
            log(path)
            log("----------------------------------------------------")

            try:

                queryStart = system.date.now()

                data = system.tag.queryTagHistory(

                    paths=[path],

                    startDate=currentHourStart,
                    endDate=currentHourEnd,

                    returnSize=minutesPerHour,

                    aggregationMode="LastValue",

                    returnFormat="Tall",

                    noInterpolation=True,

                    ignoreBadQuality=True,

                    database=historyProvider
                )

                queryEnd = system.date.now()

                durationMS = system.date.millisBetween(
                    queryStart,
                    queryEnd
                )

                log("Rows returned : %d" % data.getRowCount())
                log("Duration (ms) : %d" % durationMS)

                columnName = path.replace(
                    "[default]",
                    ""
                ).strip("/")

                for row in system.dataset.toPyDataSet(data):

                    ts = row["timestamp"]

                    val = row["value"]

                    tsMillis = system.date.toMillis(ts)

                    if tsMillis not in masterMap:

                        masterMap[tsMillis] = {
                            "timestamp": ts
                        }

                    masterMap[tsMillis][columnName] = val

                data = None

            except Exception as e:

                log("TAG FAILED")
                log(path)
                log(str(e))

        # ====================================================
        # BUILD DATASET
        # ====================================================
        rows = []

        sortedKeys = sorted(
            masterMap.keys(),
            reverse=True
        )

        for tsMillis in sortedKeys:

            rowMap = masterMap[tsMillis]

            rowData = []

            rowData.append(
                rowMap.get("timestamp")
            )

            for col in columnNames:

                rowData.append(
                    rowMap.get(col, None)
                )

            rows.append(rowData)

        hourDS = system.dataset.toDataSet(
            headers,
            rows
        )

        log("Hour dataset rows: %d" % hourDS.getRowCount())

        # ====================================================
        # CSV
        # ====================================================
        csvChunk = system.dataset.toCSV(
            hourDS,
            showHeaders=firstWrite
        )

        system.file.writeFile(
            exportFile,
            csvChunk,
            not firstWrite
        )

        firstWrite = False

        log("CSV chunk written.")

        # ====================================================
        # CLEANUP
        # ====================================================
        masterMap = None
        rows = None
        hourDS = None
        csvChunk = None

        currentHourStart = currentHourEnd

    log("====================================================")
    log("EXPORT COMPLETE")
    log("====================================================")

except Exception as e:

    log("====================================================")
    log("SCRIPT FAILED")
    log("====================================================")

    log(str(e))

    import traceback

    log(traceback.format_exc())

log("====================================================")
log("SCRIPT END")
log("====================================================")