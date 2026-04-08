import system

logger = system.util.getLogger("RawHistoryExport")

# ============================================================
# CONFIG
# ============================================================
start_date = system.date.parse("2026-03-01 00:01:00", "yyyy-MM-dd HH:mm:ss")
end_date   = system.date.parse("2026-03-31 23:59:00", "yyyy-MM-dd HH:mm:ss")

output_path = r"C:\myExports\myExport.csv"

paths = [
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:Quadrogen/READ_QUAD_PLC_REAL/Inlet Flowmeter - Total Flow",
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:Gas Analyzers/Raw Gas/Raw GC BTU/Scaled_Value",
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:Gas Analyzers/Raw Gas/Raw GC CH4/Scaled_Value",
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:Quadrogen/READ_QUAD_PLC_REAL/Product Gas Flow",
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:Gas Analyzers/GC_BTU",
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:Gas Analyzers/GC_CH4",
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:PEI Flare/Analogs/FLARE_GHS_FLOW_RATE",
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:Injection Site/INJ_REAL_DATA/KM_BTU_MB",
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:Injection Site/INJ_REAL_DATA/KM_CH4_MB",
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:Injection Site/INJ_REAL_DATA/KM_INJ_FLOW_MB",
    "histprov:Historian:/sys:ignition-scada-1:/prov:default:/tag:Injection Site/KM_INJ_VOL_MMBTU_LT"
]

# ============================================================
# SETTINGS
# ============================================================
chunk_hours = 12   # raw data = heavy → keep this small
first_write = True

current_start = start_date

logger.info("Starting RAW export in chunks...")

# ============================================================
# HEADER CLEANER
# ============================================================
def clean_header(col_name):
    if ":/tag:" in col_name:
        tag_part = col_name.split(":/tag:")[-1]
        return tag_part.split("/")[-1]
    return col_name

# ============================================================
# MAIN LOOP
# ============================================================
total_rows = 0

while current_start < end_date:

    current_end = system.date.addHours(current_start, chunk_hours)
    if current_end > end_date:
        current_end = end_date

    logger.info("Querying: %s → %s" % (current_start, current_end))

    try:
        results = system.historian.queryRawPoints(
            paths=paths,
            startTime=current_start,
            endTime=current_end,
            returnSize=-1  # OK now because chunked
        )

        row_count = results.rowCount
        col_count = results.columnCount

        if row_count == 0:
            logger.info("No data in this chunk.")
            current_start = current_end
            continue

        # Build headers ONCE
        if first_write:
            headers = [clean_header(results.getColumnName(i)) for i in range(col_count)]
            header_line = ",".join(headers) + "\n"
            system.file.writeFile(output_path, header_line, False)
            first_write = False

        # Build rows for THIS chunk only
        lines = []

        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                val = results.getValueAt(row, col)
                row_data.append('"' + str(val) + '"')
            lines.append(",".join(row_data))

        chunk_csv = "\n".join(lines) + "\n"

        # Append chunk
        system.file.writeFile(output_path, chunk_csv, True)

        total_rows += row_count
        logger.info("Chunk complete: %s rows" % row_count)

    except Exception as e:
        logger.error("Chunk FAILED: %s" % str(e))

    current_start = current_end

logger.info("Export complete. Total rows: %s" % total_rows)
system.perspective.print("Export complete. Rows: " + str(total_rows))