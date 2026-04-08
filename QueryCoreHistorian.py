import system

logger = system.util.getLogger("HistoryExport")

# ============================================================
# CONFIG
# ============================================================
start_date = system.date.parse("2026-03-01 00:01:00", "yyyy-MM-dd HH:mm:ss")
end_date   = system.date.parse("2026-03-31 23:59:00", "yyyy-MM-dd HH:mm:ss")

output_path = r"C:\myExports\myExport.csv"

paths = [
    "[default]Quadrogen/READ_QUAD_PLC_REAL/Inlet Flowmeter - Total Flow",
    "[default]Gas Analyzers/Raw Gas/Raw GC BTU/Scaled_Value",
    "[default]Gas Analyzers/Raw Gas/Raw GC CH4/Scaled_Value",
    "[default]Quadrogen/READ_QUAD_PLC_REAL/Product Gas Flow",
    "[default]Gas Analyzers/GC_BTU",
    "[default]Gas Analyzers/GC_CH4",
    "[default]PEI Flare/Analogs/FLARE_GHS_FLOW_RATE",
    "[default]Injection Site/INJ_REAL_DATA/KM_BTU_MB",
    "[default]Injection Site/INJ_REAL_DATA/KM_CH4_MB",
    "[default]Injection Site/INJ_REAL_DATA/KM_INJ_FLOW_MB",
    "[default]Injection Site/KM_INJ_VOL_MMBTU_LT"
]

# ============================================================
# SETTINGS
# ============================================================
chunk_hours = 24   # adjust (12, 6, etc. if still heavy)
first_write = True

current_start = start_date

logger.info("Starting export...")

while current_start < end_date:

    current_end = system.date.addHours(current_start, chunk_hours)
    if current_end > end_date:
        current_end = end_date

    logger.info("Querying from %s to %s" % (current_start, current_end))

    try:
        data = system.tag.queryTagHistory(
            paths=paths,
            startDate=current_start,
            endDate=current_end,
            returnSize=0,                # ← CRITICAL (natural sampling)
            aggregationMode="Average",
            returnFormat="Wide"
        )

        if data.getRowCount() == 0:
            logger.info("No data in this chunk.")
        else:
            csv = system.dataset.toCSV(data, first_write)

            # Append instead of overwrite
            system.file.writeFile(output_path, csv, not first_write)

            first_write = False

    except Exception as e:
        logger.error("Chunk failed: %s" % str(e))

    current_start = current_end

logger.info("Export complete.")
system.perspective.print("Export complete.")