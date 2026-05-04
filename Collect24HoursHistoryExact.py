import system

# ============================================================
# LOGGER
# ============================================================
logger = system.util.getLogger("RollingHistoryCache")

def log(msg):
    logger.warn(msg)

# ============================================================
# CONFIG
# ============================================================
cacheTag   = "[default]Papas_Tags/MemoryTags/HistoryCache"
runningTag = "[default]Papas_Tags/MemoryTags/HistoryCacheRunning"

retainHours     = 24
historyProvider = "TAGHISTORIAN"

MAX_ROWS = 190000

# ============================================================
# TAG PATHS (INSERT YOUR TAGS HERE)
# ============================================================
tagPaths = [
    # "[default]Folder/Tag1",
    # "[default]Folder/Tag2",
]

# ============================================================
# START
# ============================================================
log("========== SCRIPT START ==========")

# Prevent overlap
running = system.tag.readBlocking([runningTag])[0].value
log("Running flag: %s" % running)

if running:
    log("Script already running, exiting")
    return

system.tag.writeBlocking([runningTag], [True])

try:
    # ============================================================
    # TIME RANGE (PREVIOUS FULL HOUR)
    # ============================================================
    now = system.date.now()

    # Round down to current hour
    thisHour = system.date.setTime(
        now,
        system.date.getHour24(now),
        0,
        0
    )

    # Previous hour window
    startTime = system.date.addHours(thisHour, -1)
    endTime   = thisHour

    # Rolling retention cutoff
    cutoff = system.date.addHours(endTime, -retainHours)

    log("Current time : %s" % now)
    log("This hour    : %s" % thisHour)
    log("Query start  : %s" % startTime)
    log("Query end    : %s" % endTime)
    log("Tag count    : %d" % len(tagPaths))

    if len(tagPaths) == 0:
        log("No tag paths defined. Exiting.")
        return

    # ============================================================
    # QUERY RAW HISTORY
    # ============================================================
    newData = system.tag.queryTagHistory(
        paths=tagPaths,
        startDate=startTime,
        endDate=endTime,
        returnSize=0,
        returnFormat="Tall",
        ignoreBadQuality=True,
        noInterpolation=True,
        includeBoundingValues=True,
        database=historyProvider
    )

    log("Raw rows returned: %d" % newData.getRowCount())

    # ============================================================
    # BUILD DOCUMENTATION MAP
    # ============================================================
    docMap = {}

    for p in tagPaths:
        try:
            cfg = system.tag.getConfiguration(p, False)
            docMap[p] = cfg[0].get("documentation", "") if cfg else ""
        except Exception as e:
            log("Config read failed for %s: %s" % (p, str(e)))
            docMap[p] = ""

    # ============================================================
    # MINUTE BUCKETING (LATEST VALUE PER MINUTE)
    # ============================================================
    bucketMap = {}

    for row in system.dataset.toPyDataSet(newData):

        rawPath = str(row["path"])

        if rawPath.startswith("["):
            fullPath = rawPath
        else:
            fullPath = "[default]" + rawPath

        tagName = rawPath.split("/")[-1]
        doc     = docMap.get(fullPath, "")

        ts = row["timestamp"]

        # Normalize to minute boundary
        millis = system.date.toMillis(ts)
        minuteMillis = (millis // 60000) * 60000
        minuteTs = system.date.fromMillis(minuteMillis)

        key = (rawPath, minuteMillis)

        existing = bucketMap.get(key)

        # Keep latest value within the minute
        if existing is None or ts > existing["timestamp"]:

            val = row["value"]

            try:
                if val is None:
                    val = None
                elif isinstance(val, float) and str(val) == "nan":
                    val = None
                else:
                    val = float(val)
            except:
                val = None

            try:
                quality = int(row["quality"]) if row["quality"] else 0
            except:
                quality = 0

            bucketMap[key] = {
                "path": rawPath,
                "tag": tagName,
                "timestamp": minuteTs,
                "value": val,
                "quality": quality,
                "documentation": doc
            }

    log("Rows after minute bucketing: %d" % len(bucketMap))

    # ============================================================
    # CONVERT TO DATASET
    # ============================================================
    headers = ["path", "tag", "timestamp", "value", "quality", "documentation"]

    newRows = []
    for v in bucketMap.values():
        newRows.append([
            v["path"],
            v["tag"],
            v["timestamp"],
            v["value"],
            v["quality"],
            v["documentation"]
        ])

    newData = system.dataset.toDataSet(headers, newRows)

    log("Rows this run (final): %d" % newData.getRowCount())

    # ============================================================
    # READ EXISTING CACHE
    # ============================================================
    existing = system.tag.readBlocking([cacheTag])[0].value

    if existing and existing.getRowCount() > 0:
        combined = system.dataset.appendDataset(existing, newData)
        log("Existing rows: %d" % existing.getRowCount())
    else:
        combined = newData
        log("No existing dataset")

    # ============================================================
    # TRIM TO LAST 24 HOURS
    # ============================================================
    headers = list(combined.getColumnNames())

    filtered = []
    for row in system.dataset.toPyDataSet(combined):
        if row["timestamp"] >= cutoff:
            filtered.append([row[h] for h in headers])

    log("Rows after time filter: %d" % len(filtered))

    # ============================================================
    # DEDUPE
    # ============================================================
    seen = set()
    deduped = []

    for row in filtered:
        key = (row[0], system.date.toMillis(row[2]))
        if key not in seen:
            seen.add(key)
            deduped.append(row)

    log("Rows after dedupe: %d" % len(deduped))

    # ============================================================
    # HARD CAP
    # ============================================================
    if len(deduped) > MAX_ROWS:
        log("Applying cap: %d" % MAX_ROWS)
        deduped = deduped[-MAX_ROWS:]

    finalData = system.dataset.toDataSet(headers, deduped)

    log("Final dataset rows: %d" % finalData.getRowCount())

    # ============================================================
    # WRITE
    # ============================================================
    system.tag.writeBlocking([cacheTag], [finalData])

    log("========== SCRIPT COMPLETE ==========")

except Exception as e:
    import traceback
    log("ERROR: %s" % str(e))
    log(traceback.format_exc())

finally:
    system.tag.writeBlocking([runningTag], [False])
    log("Running flag reset.")
