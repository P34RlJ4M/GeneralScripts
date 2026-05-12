# ============================================================
# ULTRA LOW MEMORY WIDE DATASET BUILDER
#
# PURPOSE:
#   Build a WIDE historian dataset:
#
#       timestamp | Tag1 | Tag2 | Tag3
#
# STRATEGY:
#
#   FOR EACH HOUR:
#
#       Query EACH TAG individually
#       at 1-minute resolution
#
#       Store ONLY that hour in memory
#
#       Build ONE WIDE dataset
#
#       Append ONE TIME to dataset tag
#
# BENEFITS:
#
#   - Very low memory usage
#   - Very small historian queries
#   - Avoids timeout issues
#   - Avoids giant datasets in memory
#   - Tags stay grouped by timestamp
#
# IMPORTANT:
#
#   Dataset tag MUST already exist:
#
#       [default]New Folder/DStag
#
# ============================================================

import system

# ============================================================
# LOGGER
# ============================================================
logger = system.util.getLogger(
    "UltraLowMemoryWideBuilder"
)

def log(msg):

    logger.warn(msg)

    print msg

log("====================================================")
log("SCRIPT START")
log("====================================================")

try:

    # ========================================================
    # CONFIG
    # ========================================================
    historyProvider = "IgnitionSplitter"

    datasetTag = "[default]New Folder/DStag"

    #
    # 1-minute intervals
    #
    minutesPerHour = 60

    # ========================================================
    # TIME RANGE
    # ========================================================
    startDate = system.date.parse(
        "2026-04-01 00:00:00",
        "yyyy-MM-dd HH:mm:ss"
    )

    endDate = system.date.parse(
        "2026-05-01 00:00:00",
        "yyyy-MM-dd HH:mm:ss"
    )

    log("Start Date      : %s" % startDate)
    log("End Date        : %s" % endDate)
    log("Dataset Tag     : %s" % datasetTag)
    log("History Provider: %s" % historyProvider)

    # ========================================================
    # TAG PATHS
    # ========================================================
    paths = [
        "[default]Gas Analyzers/AIT_11703/SCP_ANALOG_01/Output",
        "[default]Gas Analyzers/GC_BTU",
        "[default]Gas Analyzers/GC_CH4",
        "[default]Injection Site/INJ_REAL_DATA/KM_BTU_MB",
        "[default]Injection Site/INJ_REAL_DATA/KM_CH4_MB",
        "[default]Injection Site/INJ_REAL_DATA/KM_FG_FLOW_MB",
        "[default]Injection Site/INJ_REAL_DATA/KM_INJ_FLOW_MB",
        "[default]PEI Flare/Analogs/FLARE_GHS_FLOW_RATE",
        "[default]PEI Flare/Analogs/FLARE_METHANE_LVL",
        "[default]Quadrogen/READ_QUAD_PLC_REAL/Inlet Flowmeter - Total Flow",
        "[default]Quadrogen/READ_QUAD_PLC_REAL/Product Gas Flow",
        "[default]Raw Tags/AMI_ANALOG/SCP_OUT",
        "[default]Raw Tags/Analogs/AIT_10514/SCP_OUT",
        "[default]Raw Tags/Analogs/AIT_10515/SCP_01/Output",
        "[default]Raw Tags/Analogs/AIT_11701/SCP_OUT",
        "[default]Raw Tags/Analogs/AIT_11702/SCP_OUT",
        "[default]Raw Tags/Analogs/AIT_11703/SCP_OUT",
        "[default]Raw Tags/Analogs/AIT_11704/SCP_OUT",
        "[default]Raw Tags/Analogs/AIT_11705/SCP_01/Output",
        "[default]Raw Tags/Analogs/FIT_10203/SCP_OUT",
        "[default]Raw Tags/Analogs/FIT_10417/SCP_OUT",
        "[default]Raw Tags/Analogs/FIT_10421/SCP_OUT",
        "[default]Raw Tags/Analogs/FIT_10423/SCP_OUT",
        "[default]Raw Tags/Analogs/FIT_10518/SCP_OUT",
        "[default]Raw Tags/Analogs/FIT_10607/SCP_OUT",
        "[default]Raw Tags/Analogs/FIT_11101/SCP_OUT",
        "[default]Raw Tags/Analogs/FIT_11103/SCP_OUT",
        "[default]Raw Tags/Analogs/FIT_11103_1/SCP_OUT",
        "[default]Raw Tags/Analogs/FIT_11201/SCP_OUT",
        "[default]Gas Analyzers/Raw Gas/Raw GC BTU",
        "[default]Gas Analyzers/Raw Gas/Raw GC CH4",
        "[default]PLANET /DIG-GAS-1/Scaled_Value",
        "[default]PLANET /DIG-GAS-2/Scaled_Value",
        "[default]PLANET /DIG-GAS-3/Scaled_Value",
        "[default]PLANET /LIT-10705-1/Scaled_Value",
        "[default]PLANET /LIT-10705-2/Scaled_Value",
        "[default]PLANET /LIT-10705-3/Scaled_Value",
        "[default]RIO-1/AIT-10514/Scaled_Value",
        "[default]RIO-1/FIT-10203/Scaled_Value",
        "[default]RIO-1/FIT-10417/Scaled_Value",
        "[default]RIO-1/FIT-10421/Scaled_Value",
        "[default]RIO-1/FIT-10423/Scaled_Value",
        "[default]RIO-1/FIT-10518/Scaled_Value",
        "[default]RIO-1/FIT-10607/Scaled_Value",
        "[default]RIO-1/FIT-11201/Scaled_Value"
    ]

    log("Configured paths: %d" % len(paths))

    # ========================================================
    # VERIFY DATASET TAG EXISTS
    # ========================================================
    if not system.tag.exists(datasetTag):

        raise Exception(
            "Dataset tag does not exist: %s"
            % datasetTag
        )

    # ========================================================
    # VERIFY TAGS
    # ========================================================
    validPaths = []

    log("Verifying tags...")

    for path in paths:

        try:

            if system.tag.exists(path):

                validPaths.append(path)

                log("VALID TAG   : %s" % path)

            else:

                log("INVALID TAG : %s" % path)

        except Exception as e:

            log("ERROR checking tag: %s" % path)

            log(str(e))

    if len(validPaths) == 0:

        raise Exception(
            "No valid tags found."
        )

    log("Valid tags: %d" % len(validPaths))

    # ========================================================
    # BUILD HEADERS
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

    log("Column count: %d" % len(headers))

    # ========================================================
    # INITIALIZE TYPED EMPTY DATASET
    # ========================================================
    log("Initializing dataset tag...")

    typedRow = []

    #
    # TIMESTAMP COLUMN
    #
    typedRow.append(
        system.date.now()
    )

    #
    # VALUE COLUMNS
    #
    for i in range(len(columnNames)):

        typedRow.append(float(0))

    #
    # TEMP DATASET
    #
    tempDS = system.dataset.toDataSet(
        headers,
        [typedRow]
    )

    #
    # REMOVE DUMMY ROW
    #
    emptyDS = system.dataset.deleteRow(
        tempDS,
        0
    )

    #
    # WRITE EMPTY DATASET
    #
    system.tag.writeBlocking(
        [datasetTag],
        [emptyDS]
    )

    log("Dataset tag initialized.")

    # ========================================================
    # PROCESS HOURS
    # ========================================================
    currentHourStart = startDate

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

        #
        # SMALL IN-MEMORY STRUCTURE
        #
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

                log("Starting historian query...")

                #
                # ONE TAG
                # ONE HOUR
                #
                data = system.tag.queryTagHistory(

                    paths=[path],

                    startDate=currentHourStart,
                    endDate=currentHourEnd,

                    #
                    # 1-MINUTE RESOLUTION
                    #
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

                log("Historian query complete.")
                log("Rows returned : %d" % data.getRowCount())
                log("Duration (ms) : %d" % durationMS)

                if data.getRowCount() == 0:

                    log("No rows returned.")

                    continue

                # ================================================
                # COLUMN NAME
                # ================================================
                columnName = path.replace(
                    "[default]",
                    ""
                ).strip("/")

                # ================================================
                # PROCESS ROWS
                # ================================================
                pyData = system.dataset.toPyDataSet(
                    data
                )

                rowCounter = 0

                for row in pyData:

                    rowCounter += 1

                    ts = row["timestamp"]

                    val = row["value"]

                    tsMillis = system.date.toMillis(
                        ts
                    )

                    #
                    # CREATE TIMESTAMP BUCKET
                    #
                    if tsMillis not in masterMap:

                        masterMap[tsMillis] = {
                            "timestamp": ts
                        }

                    #
                    # STORE VALUE
                    #
                    masterMap[tsMillis][columnName] = val

                log("Processed rows: %d" % rowCounter)

                #
                # MEMORY CLEANUP
                #
                data = None

                pyData = None

            except Exception as e:

                log("================================================")
                log("TAG FAILED")
                log(path)
                log("================================================")

                log(str(e))

                import traceback

                log(traceback.format_exc())

        # ====================================================
        # BUILD ONE-HOUR DATASET
        # ====================================================
        log("Building one-hour dataset...")

        rows = []

        sortedKeys = sorted(
            masterMap.keys(),
            reverse=True
        )

        for tsMillis in sortedKeys:

            rowMap = masterMap[tsMillis]

            rowData = []

            #
            # TIMESTAMP
            #
            rowData.append(
                rowMap.get("timestamp")
            )

            #
            # TAG COLUMNS
            #
            for col in columnNames:

                rowData.append(
                    rowMap.get(col, None)
                )

            rows.append(rowData)

        hourDS = system.dataset.toDataSet(
            headers,
            rows
        )

        log(
            "One-hour dataset rows   : %d"
            % hourDS.getRowCount()
        )

        log(
            "One-hour dataset columns: %d"
            % hourDS.getColumnCount()
        )

        # ====================================================
        # READ EXISTING DATASET TAG
        # ====================================================
        log("Reading existing dataset tag...")

        existingDS = system.tag.readBlocking(
            [datasetTag]
        )[0].value

        existingRows = 0

        if existingDS:

            existingRows = existingDS.getRowCount()

        log(
            "Existing dataset rows: %d"
            % existingRows
        )

        # ====================================================
        # FIRST WRITE VS APPEND
        # ====================================================
        if existingRows == 0:

            log("First dataset write detected.")

            combinedDS = hourDS

        else:

            log("Appending dataset...")

            combinedDS = system.dataset.appendDataset(
                existingDS,
                hourDS
            )

        log(
            "Combined dataset rows: %d"
            % combinedDS.getRowCount()
        )

        # ====================================================
        # WRITE DATASET TAG
        # ====================================================
        log("Writing dataset to tag...")

        writeResult = system.tag.writeBlocking(
            [datasetTag],
            [combinedDS]
        )

        log(
            "Write result: %s"
            % str(writeResult[0])
        )

        # ====================================================
        # MEMORY CLEANUP
        # ====================================================
        log("Performing memory cleanup...")

        masterMap = None
        rows = None
        hourDS = None
        existingDS = None
        combinedDS = None

        log("Memory cleanup complete.")

        # ====================================================
        # NEXT HOUR
        # ====================================================
        currentHourStart = currentHourEnd

    # ========================================================
    # FINAL DATASET INFO
    # ========================================================
    log("====================================================")
    log("FINAL DATASET INFO")
    log("====================================================")

    finalDS = system.tag.readBlocking(
        [datasetTag]
    )[0].value

    if finalDS:

        log(
            "Final dataset rows   : %d"
            % finalDS.getRowCount()
        )

        log(
            "Final dataset columns: %d"
            % finalDS.getColumnCount()
        )

    # ========================================================
    # COMPLETE
    # ========================================================
    log("====================================================")
    log("SCRIPT COMPLETE")
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