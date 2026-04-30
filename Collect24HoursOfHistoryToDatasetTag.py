import system

logger = system.util.getLogger("RollingHistoryCache")


def log(msg):
    logger.warn(msg)


# ============================================================
# CONFIG
# ============================================================
cacheTag = "[default]Papas_Tags/MemoryTags/HistoryCache"
runningTag = "[default]Papas_Tags/MemoryTags/HistoryCacheRunning"

queryHours = 1
retainHours = 24
historyProvider = "TAGHISTORIAN"

MAX_ROWS = 190000

tagPaths = [
    "[default]Papas_Tags/FIT601",
    "[default]Papas_Tags/FIT601_CH4",
    "[default]Papas_Tags/FIT602",
    "[default]Papas_Tags/FIT602_CH4",
    "[default]Papas_Tags/FIT603",
    "[default]Papas_Tags/FIT603_CH4",
    "[default]Papas_Tags/FIT603_MSCF_TD",
    "[default]Papas_Tags/FIT603_MSCF_YD",
    "[default]Papas_Tags/FIT603_MMBTU_TD",
    "[default]Papas_Tags/FIT603_MMBTU_YD",
    "[default]Papas_Tags/LIT301_VOL_GAL",
    "[default]Papas_Tags/LIT301",
    "[default]Papas_Tags/LIT401",
    "[default]Papas_Tags/LIT401_VOL_GAL",
    "[default]Papas_Tags/LIT601",
    "[default]Papas_Tags/TT301",
    "[default]Papas_Tags/TT401",
    "[default]Papas_Tags/OG_AT3",
    "[default]Papas_Tags/AT602_CH4",
    "[default]Papas_Tags/AT602_CO2",
    "[default]Papas_Tags/AT602_O2",
    "[default]Papas_Tags/AT602_H2S",
    "[default]Papas_Tags/FM1002",
    "[default]Papas_Tags/FM1002_MSCF_TD",
    "[default]Papas_Tags/FM1002_MSCF_YD",
    "[default]Papas_Tags/FIT103",
    "[default]Papas_Tags/FIT103_GAL_TD",
    "[default]Papas_Tags/FIT103_GAL_YD",
    "[default]Papas_Tags/H2S100",
    "[default]Papas_Tags/LT507",
    "[default]Papas_Tags/PIT1002",
    "[default]Papas_Tags/AT902_H2S",
    "[default]Papas_Tags/FIT101",
    "[default]Papas_Tags/FIT101_GAL_TD",
    "[default]Papas_Tags/FIT101_GAL_YD",
    "[default]Papas_Tags/FIT201",
    "[default]Papas_Tags/FIT201_GAL_TD",
    "[default]Papas_Tags/FIT201_GAL_YD",
    "[default]Papas_Tags/FIT201_GAL_CY",
    "[default]Papas_Tags/FIT401",
    "[default]Papas_Tags/FIT401_GAL_TD",
    "[default]Papas_Tags/FIT401_GAL_YD",
    "[default]Papas_Tags/LIT201",
    "[default]Papas_Tags/LIT201_VOL_GAL",
    "[default]Papas_Tags/P502_RN_TM",
    "[default]Papas_Tags/P701_RN_TM",
    "[default]Papas_Tags/P704_RN_TM",
    "[default]Papas_Tags/V901_RN_TM",
    "[default]Papas_Tags/V902_RN_TM",
    "[default]Papas_Tags/P703_RN_TM",
    "[default]Papas_Tags/R505_RN_TM",
    "[default]Papas_Tags/P505_RN_TM",
    "[default]Papas_Tags/P501_RN_TM",
    "[default]Papas_Tags/P201_RN_TM",
    "[default]Papas_Tags/P202_RN_TM",
    "[default]Papas_Tags/P301_RN_TM",
    "[default]Papas_Tags/P302_RN_TM",
    "[default]Papas_Tags/P401_RN_TM",
    "[default]Papas_Tags/P402_RN_TM",
    "[default]Papas_Tags/R201_RN_TM",
    "[default]Papas_Tags/R401_RN_TM",
    "[default]Papas_Tags/R402_RN_TM",
    "[default]Papas_Tags/Z201_RN_TM",
    "[default]Papas_Tags/V603_RN_TM",
    "[default]Papas_Tags/R301_RN_TM",
    "[default]Papas_Tags/V601_RN_TM",
    "[default]Papas_Tags/PM_MM_KWH",
    "[default]Papas_Tags/PM_DG_KWH",
    "[default]Papas_Tags/PM_UP_KWH",
    "[default]Papas_Tags/MM_LT102",
    "[default]Papas_Tags/MM_LT506",
    "[default]Papas_Tags/MM_LT508",
    "[default]Papas_Tags/MM_LT509",
    "[default]Papas_Tags/DS_FIC7011_SCFM",
    "[default]Papas_Tags/DS_FIC6021_SCFM",
    "[default]Papas_Tags/DS_GA1_CH4",
    "[default]Papas_Tags/DS_GA1_O2",
    "[default]Papas_Tags/DS_GA1_CO2",
    "[default]Papas_Tags/DS_GA1_H2S",
    "[default]Papas_Tags/DS_GA2_CH4",
    "[default]Papas_Tags/DS_GA2_O2",
    "[default]Papas_Tags/DS_GA2_CO2",
    "[default]Papas_Tags/DS_GA2_H2S",
    "[default]Papas_Tags/UP_0RHH15DQ001_CH4",
    "[default]Papas_Tags/UP_0RHH15DQ001_CO2",
    "[default]Papas_Tags/UP_0RHH15DQ001_O2",
    "[default]Papas_Tags/UP_0RHH15DQ001_H2S",
    "[default]Papas_Tags/UP_0RHH15DQ001_H2S_1",
    "[default]Papas_Tags/UP_0RHH15DQ001_H2S_2",
    "[default]Papas_Tags/UP_0RHH10DQ001_CH4",
    "[default]Papas_Tags/UP_0RHH10DQ001_CO2",
    "[default]Papas_Tags/UP_0RHH10DQ001_O2",
    "[default]Papas_Tags/UP_0RHH10DQ001_H2S",
    "[default]Papas_Tags/UP_WB",
    "[default]Papas_Tags/UP_WB_AVE",
    "[default]Papas_Tags/UP_0RHH10DQ002_CH4",
    "[default]Papas_Tags/UP_0RHH10DQ002_HHV",
    "[default]Papas_Tags/UP_0RHH10DQ002_CO2",
    "[default]Papas_Tags/UP_0RHH10DQ002_O2",
    "[default]Papas_Tags/UP_0RHH10DQ002_O2_PPM",
    "[default]Papas_Tags/UP_0RHH10DQ002_H2S",
    "[default]Papas_Tags/UP_0RHH10DQ002_N2",
    "[default]Papas_Tags/UP_0RHH20DQ001_CH4",
    "[default]Papas_Tags/UP_INJ_VOL_LT",
    "[default]Papas_Tags/UP_INJ_VOL_YD",
    "[default]Papas_Tags/UP_0RHA10CF001",
    "[default]Papas_Tags/UP_0RHA10CF001_MSCF_TD",
    "[default]Papas_Tags/UP_0RHA10CF001_MSCF_YD",
    "[default]Papas_Tags/UP_0RHA10CF001_MMBTU_TD",
    "[default]Papas_Tags/UP_0RHA10CF001_MMBTU_YD",
    "[default]Papas_Tags/UP_0RHH10CF001",
    "[default]Papas_Tags/UP_0RHH10CF002",
    "[default]Papas_Tags/UP_0RHH10CF002_MSCF_TD",
    "[default]Papas_Tags/UP_0RHH10CF002_MSCF_YD",
    "[default]Papas_Tags/UP_0RHH10CF002_MMBTU_TD",
    "[default]Papas_Tags/UP_0RHH10CF002_MMBTU_YD",
    "[default]Papas_Tags/FL_FLW_SCFM",
    "[default]Papas_Tags/FL_VOL_SCF",
    "[default]Papas_Tags/FL_RN_TM",
    "[default]Papas_Tags/FL_B2112_RN_TM",
    "[default]Papas_Tags/BL_FR_RT",
    "[default]Papas_Tags/AT902_LEL",
    "[default]Papas_Tags/AT901_LEL",
    "[default]Papas_Tags/AT903",
    "[default]Papas_Tags/AT601",
    "[default]Papas_Tags/GD102",
    "[default]Papas_Tags/UP_RM_CH4",
    "[default]Papas_Tags/LEL100"
]

# ============================================================
# START
# ============================================================
log("=== SCRIPT START ===")

# Prevent overlap
if system.tag.readBlocking([runningTag])[0].value:
    log("Script already running, exiting")
    return

system.tag.writeBlocking([runningTag], [True])

try:
    # ============================================================
    # TIME RANGE
    # ============================================================
    endTime = system.date.now()
    startTime = system.date.addHours(endTime, -queryHours)
    cutoff = system.date.addHours(endTime, -retainHours)

    log("Query range: %s -> %s" % (startTime, endTime))
    log("Tag count: %d" % len(tagPaths))

    # ============================================================
    # QUERY RAW HISTORY (FIX APPLIED HERE)
    # ============================================================
    newData = system.tag.queryTagHistory(
        paths=tagPaths,
        startDate=startTime,
        endDate=endTime,
        returnSize=0,
        returnFormat="Tall",
        ignoreBadQuality=True,
        noInterpolation=True,
        includeBoundingValues=True,  # 🔥 FIX FOR MIDNIGHT GAP
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
        except:
            docMap[p] = ""

    # ============================================================
    # FORCE 1 ROW PER TAG PER MINUTE
    # ============================================================
    bucketMap = {}

    for row in system.dataset.toPyDataSet(newData):

        rawPath = str(row["path"])

        if rawPath.startswith("["):
            fullPath = rawPath
        else:
            fullPath = "[default]" + rawPath

        tagName = rawPath.split("/")[-1]
        doc = docMap.get(fullPath, "")

        ts = row["timestamp"]

        # Minute bucket
        millis = system.date.toMillis(ts)
        minuteMillis = (millis // 60000) * 60000
        minuteTs = system.date.fromMillis(minuteMillis)

        key = (rawPath, minuteMillis)

        existing = bucketMap.get(key)

        # Keep latest value in that minute
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

    log("=== SCRIPT COMPLETE ===")

except Exception as e:
    import traceback

    log("ERROR: %s" % str(e))
    log(traceback.format_exc())

finally:
    system.tag.writeBlocking([runningTag], [False])