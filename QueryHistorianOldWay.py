import system

# ============================================================
# TIME RANGE
# ============================================================
endTime = system.date.now()
startTime = system.date.addDays(endTime, -50)

# ============================================================
# TAG PATHS
# ============================================================
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
# QUERY HISTORY
# ============================================================
data = system.tag.queryTagHistory(
    paths=paths,
    startDate=startTime,
    endDate=endTime,
    returnSize=72000,
    aggregationMode="Average",
    returnFormat="Wide",
    database="Americus-RNG-Splitter"
)

# ============================================================
# EXPORT TO CSV
# ============================================================
csv = system.dataset.toCSV(data)

system.file.writeFile(r"C:\myExports\myExport.csv", csv)