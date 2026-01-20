import system

logger = system.util.getLogger("FaultDurationTransform")

# Always return a dataset, even if empty
emptyDataset = system.dataset.toDataSet(
    ["Fault Name", "Duration (s)", "Duration (H:MM:SS)"],
    []
)

try:
    # -----------------------------
    # Validate input
    # -----------------------------
    if value is None or str(value).strip() == "":
        logger.error("UDT path is null or empty")
        return emptyDataset

    basePath = str(value).strip()
    faultsFolder = basePath + "/Faults"

    logger.info("Browsing folder: {}".format(faultsFolder))

    # -----------------------------
    # Browse Fault tags
    # -----------------------------
    faultTags = system.tag.browse(faultsFolder).getResults()

    faultPaths = []
    faultNames = []

    for tag in faultTags:
        if not tag['hasChildren']:
            tagName = tag['name']
            # Include Fault0, Fault1, etc. (exclude plain "Fault")
            if tagName.startswith("Fault") and tagName != "Fault":
                if len(tagName) > 5 and tagName[5:].isdigit():
                    fullPath = faultsFolder + "/" + tagName
                    faultPaths.append(fullPath)
                    faultNames.append(tagName)

    if not faultPaths:
        logger.warn("No fault tags found in: {}".format(faultsFolder))
        return emptyDataset

    logger.info("Found {} fault tags: {}".format(len(faultPaths), faultNames))

    # -----------------------------
    # Time window (adjustable)
    # -----------------------------
    endTime = system.date.now()
    startTime = system.date.addHours(endTime, -1)

    # -----------------------------
    # Query raw history
    # -----------------------------
    rawHistory = system.tag.queryTagHistory(
        paths=faultPaths,
        startDate=startTime,
        endDate=endTime,
        returnSize=-1,
        returnFormat="Tall"
    )

    logger.info("Raw history returned {} rows".format(rawHistory.rowCount))

    # -----------------------------
    # Initialize duration map
    # -----------------------------
    tagDurations = {}
    for tagName in faultNames:
        tagDurations[tagName] = 0  # whole seconds

    # Group history by tag
    tagData = {}
    for row in range(rawHistory.rowCount):
        path = rawHistory.getValueAt(row, "path")
        ts = rawHistory.getValueAt(row, "timestamp")
        val = rawHistory.getValueAt(row, "value")

        tagName = path.split("/")[-1]
        if tagName not in tagData:
            tagData[tagName] = []
        tagData[tagName].append((ts, val))

    # -----------------------------
    # Calculate ON durations
    # -----------------------------
    for tagName, dataPoints in tagData.items():
        totalDurationMs = 0
        lastValue = None
        lastTimestamp = None

        for ts, val in dataPoints:
            if lastTimestamp is not None and lastValue == 1:
                totalDurationMs += ts.getTime() - lastTimestamp.getTime()

            lastValue = val
            lastTimestamp = ts

        # If still ON at end of range
        if lastValue == 1 and lastTimestamp is not None:
            totalDurationMs += endTime.getTime() - lastTimestamp.getTime()

        tagDurations[tagName] = int(totalDurationMs / 1000)  # convert to whole seconds


    # -----------------------------
    # Format as H:MM:SS
    # -----------------------------
    def format_hh_mm_ss(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return "{}:{:02d}:{:02d}".format(hours, minutes, secs)


    # -----------------------------
    # Build dataset
    # -----------------------------
    rows = []
    for tagName in faultNames:
        durationSec = int(tagDurations.get(tagName, 0))
        formatted = format_hh_mm_ss(durationSec)
        rows.append([tagName, durationSec, formatted])

    logger.info("Returning dataset with {} rows".format(len(rows)))

    return system.dataset.toDataSet(
        ["Fault Name", "Duration (s)", "Duration (H:MM:SS)"],
        rows
    )

except Exception as e:
    logger.error("Fault duration transform failed: {}".format(str(e)))
    try:
        import traceback

        logger.error(traceback.format_exc())
    except:
        pass

    return emptyDataset