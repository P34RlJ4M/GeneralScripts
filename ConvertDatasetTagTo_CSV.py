import system

logger = system.util.getLogger("DatasetFormatter")

# ============================================================
# CONFIG
# ============================================================
tagPath = "[default]Papas_Tags/MemoryTags/HistoryCache"
exportFolder = r"C:\Users\Public\Documents\MyExports"

location = "Papas"  # replace or parameterize

logger.warn("=== SCRIPT START ===")

try:
    # ============================================================
    # READ DATASET
    # ============================================================
    result = system.tag.readBlocking([tagPath])[0]

    if result.value is None:
        logger.warn("Dataset is empty.")
        return

    ds = result.value

    logger.warn("Rows read: %d" % ds.getRowCount())

    # ============================================================
    # BUILD PIVOT STRUCTURE
    # ============================================================
    dataMap = {}  # {timestamp: {tag: value}}
    tagSet = set()

    for row in system.dataset.toPyDataSet(ds):

        ts = row["timestamp"]
        tag = row["tag"]
        val = row["value"]

        tagSet.add(tag)

        # Clean value
        try:
            if val is None:
                val = None
            elif isinstance(val, float) and str(val) == "nan":
                val = None
            else:
                val = float(val)
        except:
            val = None

        if ts not in dataMap:
            dataMap[ts] = {}

        dataMap[ts][tag] = val

    logger.warn("Unique timestamps: %d" % len(dataMap))
    logger.warn("Unique tags: %d" % len(tagSet))

    # ============================================================
    # SORT TAGS + DATES
    # ============================================================
    tagList = sorted(list(tagSet))
    dateList = sorted(list(dataMap.keys()))  # ASCENDING

    # ============================================================
    # BUILD FINAL DATASET
    # ============================================================
    headers = ["Date"] + tagList
    rows = []

    for ts in dateList:
        rowVals = [ts]

        tagValues = dataMap[ts]

        for tag in tagList:
            rowVals.append(tagValues.get(tag, None))

        rows.append(rowVals)

    logger.warn("Final rows: %d" % len(rows))
    logger.warn("Final columns: %d" % len(headers))

    newDS = system.dataset.toDataSet(headers, rows)

    # ============================================================
    # FORMAT DATE
    # ============================================================
    try:
        newDS = system.dataset.formatDates(newDS, "yyyy-MM-dd HH:mm:ss")
    except:
        logger.warn("Date formatting skipped")

    # ============================================================
    # BUILD FILE NAME
    # ============================================================
    dateStr = system.date.format(system.date.now(), "yyyyMMdd")
    fileName = "%s_%s.csv" % (location, dateStr)

    filePath = exportFolder + "\\" + fileName

    logger.warn("Export path: %s" % filePath)

    # ============================================================
    # EXPORT CSV
    # ============================================================
    csv = system.dataset.toCSV(newDS)

    system.file.writeFile(filePath, csv)

    logger.warn("File written successfully.")
    logger.warn("=== SCRIPT COMPLETE ===")

except Exception as e:
    import traceback

    logger.error("SCRIPT FAILED: %s" % str(e))
    logger.error(traceback.format_exc())
