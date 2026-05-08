# ============================================================
# IGNITION SCRIPT CONSOLE
# CHECK TAG EXISTENCE + HISTORY CONFIGURATION
# ============================================================
#
# PURPOSE:
# This script checks a list of tags to determine:
#
#   1. Does the tag exist?
#   2. Is history enabled?
#
# The script prints detailed results to the Script Console.
#
# ============================================================
# HOW TO USE
# ============================================================
#
# 1. Paste this script into the Ignition Script Console
#
# 2. Replace the placeholder tagPaths list with your tags
#
# 3. Run the script
#
# ============================================================

import system

# ============================================================
# LOGGER
# ============================================================

logger = system.util.getLogger("HistoryCheck")

def log(msg):
    logger.warn(msg)

log("=== SCRIPT START ===")

# ============================================================
# PLACEHOLDER TAG LIST
# ============================================================
#
# REPLACE THIS WITH YOUR TAGS
#
# Example:
#
# tagPaths = [
#     "[default]Folder/Tag1",
#     "[default]Folder/Tag2"
# ]
#
# ============================================================

tagPaths = [
    "[default]CowPleasant_Tags/AT601",
    "[default]CowPleasant_Tags/AT6011",
    "[default]CowPleasant_Tags/AT6021",
    "[default]CowPleasant_Tags/AT901_H2S",
    "[default]CowPleasant_Tags/AT901_LEL",
    "[default]CowPleasant_Tags/AT902_H2S",
    "[default]CowPleasant_Tags/AT902_LEL",
    "[default]CowPleasant_Tags/AT904_LEL",
    "[default]CowPleasant_Tags/FIT201",
    "[default]CowPleasant_Tags/FIT201_GAL_TD",
    "[default]CowPleasant_Tags/FIT201_GAL_YD",
    "[default]CowPleasant_Tags/FIT401",
    "[default]CowPleasant_Tags/FIT401_GAL_TD",
    "[default]CowPleasant_Tags/FIT401_GAL_YD",
    "[default]CowPleasant_Tags/FIT601",
    "[default]CowPleasant_Tags/FIT601_CH4",
    "[default]CowPleasant_Tags/FIT601_MSCF_TD",
    "[default]CowPleasant_Tags/FIT601_MSCF_YD",
    "[default]CowPleasant_Tags/FIT601_MMBTU_TD",
    "[default]CowPleasant_Tags/FIT601_MMBTU_YD",
    "[default]CowPleasant_Tags/FIT602",
    "[default]CowPleasant_Tags/FIT602_CH4",
    "[default]CowPleasant_Tags/FIT602_MSCF_TD",
    "[default]CowPleasant_Tags/FIT602_MSCF_YD",
    "[default]CowPleasant_Tags/FIT602_MMBTU_TD",
    "[default]CowPleasant_Tags/FIT602_MMBTU_YD",
    "[default]CowPleasant_Tags/FIT603",
    "[default]CowPleasant_Tags/FIT603_CH4",
    "[default]CowPleasant_Tags/FIT603_MSCF_TD",
    "[default]CowPleasant_Tags/FIT603_MSCF_YD",
    "[default]CowPleasant_Tags/FIT603_MMBTU_TD",
    "[default]CowPleasant_Tags/FIT603_MMBTU_YD",
    "[default]CowPleasant_Tags/FIT604",
    "[default]CowPleasant_Tags/FIT604_CH4",
    "[default]CowPleasant_Tags/FIT604_MSCF_TD",
    "[default]CowPleasant_Tags/FIT604_MSCF_YD",
    "[default]CowPleasant_Tags/FIT604_MMBTU_TD",
    "[default]CowPleasant_Tags/FIT604_MMBTU_YD",
    "[default]CowPleasant_Tags/AT602_CH4",
    "[default]CowPleasant_Tags/AT602_CO2",
    "[default]CowPleasant_Tags/AT602_O2",
    "[default]CowPleasant_Tags/AT602_H2S",
    "[default]CowPleasant_Tags/LIT201",
    "[default]CowPleasant_Tags/LIT201_VOL_GAL",
    "[default]CowPleasant_Tags/LIT301",
    "[default]CowPleasant_Tags/LIT301_VOL_GAL",
    "[default]CowPleasant_Tags/LIT401",
    "[default]CowPleasant_Tags/LIT401_VOL_GAL",
    "[default]CowPleasant_Tags/LIT601",
    "[default]CowPleasant_Tags/LT301",
    "[default]CowPleasant_Tags/TT301",
    "[default]CowPleasant_Tags/TT401",
    "[default]CowPleasant_Tags/GHT603_PR_OP_STS",
    "[default]CowPleasant_Tags/GLT603_VR_OP_STS",
    "[default]CowPleasant_Tags/P501_RN_TM",
    "[default]CowPleasant_Tags/R201_RN_TM",
    "[default]CowPleasant_Tags/V901_RN_TM",
    "[default]CowPleasant_Tags/V902_RN_TM",
    "[default]CowPleasant_Tags/P701_RN_TM",
    "[default]CowPleasant_Tags/P702_RN_TM",
    "[default]CowPleasant_Tags/P703_RN_TM",
    "[default]CowPleasant_Tags/P704_RN_TM",
    "[default]CowPleasant_Tags/P201_RN_TM",
    "[default]CowPleasant_Tags/P202_RN_TM",
    "[default]CowPleasant_Tags/P301_RN_TM",
    "[default]CowPleasant_Tags/P302_RN_TM",
    "[default]CowPleasant_Tags/P401_RN_TM",
    "[default]CowPleasant_Tags/P402_RN_TM",
    "[default]CowPleasant_Tags/R301_RN_TM",
    "[default]CowPleasant_Tags/R401_RN_TM",
    "[default]CowPleasant_Tags/R402_RN_TM",
    "[default]CowPleasant_Tags/R403_RN_TM",
    "[default]CowPleasant_Tags/V601_RN_TM",
    "[default]CowPleasant_Tags/V603_RN_TM",
    "[default]CowPleasant_Tags/Z201_RN_TM",
    "[default]CowPleasant_Tags/PM_MSB1_KWH",
    "[default]CowPleasant_Tags/PM_UP_KWH",
    "[default]CowPleasant_Tags/PM_DS_KWH",
    "[default]CowPleasant_Tags/PM_OG_KWH",
    "[default]CowPleasant_Tags/PM_TL_KWH",
    "[default]CowPleasant_Tags/BL_FR_RT",
    "[default]CowPleasant_Tags/BL_PMP_SPD",
    "[default]CowPleasant_Tags/BL_RN_TM",
    "[default]CowPleasant_Tags/UP_0UCA10CQ002",
    "[default]CowPleasant_Tags/UP_0RHA10CF001",
    "[default]CowPleasant_Tags/UP_0RHA10CF001_MSCF_TD",
    "[default]CowPleasant_Tags/UP_0RHA10CF001_MSCF_YD",
    "[default]CowPleasant_Tags/UP_0RHA10CF001_MMBTU_TD",
    "[default]CowPleasant_Tags/UP_0RHA10CF001_MMBTU_YD",
    "[default]CowPleasant_Tags/UP_0RHH15DQ001_CH4",
    "[default]CowPleasant_Tags/UP_0RHH15DQ001_CO2",
    "[default]CowPleasant_Tags/UP_0RHH15DQ001_O2",
    "[default]CowPleasant_Tags/UP_0RHH15DQ001_H2S",
    "[default]CowPleasant_Tags/UP_0RHH15DQ001_H2S_1",
    "[default]CowPleasant_Tags/UP_0RHH15DQ001_H2S_2",
    "[default]CowPleasant_Tags/UP_NOR_OUT_FLW",
    "[default]CowPleasant_Tags/UP_0RHH10DQ001_CH4",
    "[default]CowPleasant_Tags/UP_0RHH10DQ001_CO2",
    "[default]CowPleasant_Tags/UP_0RHH10DQ001_O2",
    "[default]CowPleasant_Tags/UP_0RHH10DQ001_H2S",
    "[default]CowPleasant_Tags/UP_WB",
    "[default]CowPleasant_Tags/UP_WB_AVE",
    "[default]CowPleasant_Tags/UP_0RHH10DQ002_CH4",
    "[default]CowPleasant_Tags/UP_0RHH10DQ002_HHV",
    "[default]CowPleasant_Tags/UP_0RHH10DQ002_CO2",
    "[default]CowPleasant_Tags/UP_0RHH10DQ002_O2",
    "[default]CowPleasant_Tags/UP_0RHH10DQ002_O2_PPM",
    "[default]CowPleasant_Tags/UP_0RHH10DQ002_H2S",
    "[default]CowPleasant_Tags/UP_0RHH10DQ002_N2",
    "[default]CowPleasant_Tags/UP_0RHH16DQ001_O2",
    "[default]CowPleasant_Tags/UP_INJ_VOL_LT",
    "[default]CowPleasant_Tags/UP_INJ_VOL_YD",
    "[default]CowPleasant_Tags/UP_RM_CO2",
    "[default]CowPleasant_Tags/UP_0ULF10CQ002",
    "[default]CowPleasant_Tags/UP_0RHH10CF001",
    "[default]CowPleasant_Tags/UP_0RHH10CF002",
    "[default]CowPleasant_Tags/UP_0RHH10CF002_MSCF_TD",
    "[default]CowPleasant_Tags/UP_0RHH10CF002_MSCF_YD",
    "[default]CowPleasant_Tags/UP_0RHH10CF002_MMBTU_TD",
    "[default]CowPleasant_Tags/UP_0RHH10CF002_MMBTU_YD",
    "[default]CowPleasant_Tags/UP_ORHH20DQ001_CH4",
    "[default]CowPleasant_Tags/UP_STATE",
    "[default]CowPleasant_Tags/DS_FIC7011_SCFM",
    "[default]CowPleasant_Tags/DS_FIC6021_SCFM",
    "[default]CowPleasant_Tags/DS_LCA1031_IN",
    "[default]CowPleasant_Tags/DS_LCA1032_IN",
    "[default]CowPleasant_Tags/DS_GA1_CH4",
    "[default]CowPleasant_Tags/DS_GA1_O2",
    "[default]CowPleasant_Tags/DS_GA1_CO2",
    "[default]CowPleasant_Tags/DS_GA1_H2S",
    "[default]CowPleasant_Tags/DS_GA2_CH4",
    "[default]CowPleasant_Tags/DS_GA2_O2",
    "[default]CowPleasant_Tags/DS_GA2_CO2",
    "[default]CowPleasant_Tags/DS_GA2_H2S",
    "[default]CowPleasant_Tags/TL_DISP1_FILL_PSI",
    "[default]CowPleasant_Tags/TL_DISP2_FILL_PSI",
    "[default]CowPleasant_Tags/TL_DISP1_FL_STS",
    "[default]CowPleasant_Tags/TL_DISP2_FL_STS",
    "[default]CowPleasant_Tags/TL_DIS1_FL_V_OP_STS",
    "[default]CowPleasant_Tags/TL_DIS2_FL_V_OP_STS"
]

# ============================================================
# VALIDATION
# ============================================================

if len(tagPaths) == 0:
    log("No tag paths supplied.")
    print ""
    print "No tag paths supplied."
    print ""
    raise Exception("tagPaths list is empty")

log("Tag count: %d" % len(tagPaths))

# ============================================================
# RESULT STORAGE
# ============================================================

existingHistoryEnabled = []
existingHistoryDisabled = []
missingTags = []

# ============================================================
# PROCESS TAGS
# ============================================================

for tagPath in tagPaths:

    log("Checking tag: %s" % tagPath)

    try:

        # ====================================================
        # CHECK TAG EXISTS
        # ====================================================

        browse = system.tag.exists(tagPath)

        if not browse:

            log("MISSING TAG: %s" % tagPath)

            missingTags.append(tagPath)

            continue

        # ====================================================
        # GET TAG CONFIGURATION
        # ====================================================

        cfg = system.tag.getConfiguration(tagPath, False)

        if not cfg or len(cfg) == 0:

            log("FAILED TO READ CONFIG: %s" % tagPath)

            existingHistoryDisabled.append(tagPath)

            continue

        cfg = cfg[0]

        # ====================================================
        # CHECK HISTORY
        # ====================================================

        historyEnabled = cfg.get("historyEnabled", False)

        if historyEnabled:

            provider = cfg.get("historyProvider", "UNKNOWN")

            sampleMode = cfg.get("sampleMode", "UNKNOWN")

            try:
                sampleRate = cfg.get("historySampleRate", "UNKNOWN")
            except:
                sampleRate = "UNKNOWN"

            existingHistoryEnabled.append({
                "path": tagPath,
                "provider": provider,
                "sampleMode": sampleMode,
                "sampleRate": sampleRate
            })

            log(
                "HISTORY ENABLED | Provider=%s | SampleMode=%s | SampleRate=%s | %s"
                % (provider, sampleMode, sampleRate, tagPath)
            )

        else:

            existingHistoryDisabled.append(tagPath)

            log("HISTORY DISABLED: %s" % tagPath)

    except Exception as e:

        log("ERROR PROCESSING TAG: %s" % tagPath)
        log(str(e))

# ============================================================
# PRINT RESULTS
# ============================================================

print ""
print "===================================================="
print "TAGS WITH HISTORY ENABLED"
print "===================================================="
print ""

if len(existingHistoryEnabled) == 0:

    print "NONE"

else:

    for item in existingHistoryEnabled:

        print "Tag Path     : %s" % item["path"]
        print "Provider     : %s" % item["provider"]
        print "Sample Mode  : %s" % item["sampleMode"]
        print "Sample Rate  : %s" % item["sampleRate"]
        print ""

# ============================================================

print ""
print "===================================================="
print "TAGS WITH HISTORY DISABLED"
print "===================================================="
print ""

if len(existingHistoryDisabled) == 0:

    print "NONE"

else:

    for tagPath in existingHistoryDisabled:

        print tagPath

# ============================================================

print ""
print "===================================================="
print "MISSING TAGS"
print "===================================================="
print ""

if len(missingTags) == 0:

    print "NONE"

else:

    for tagPath in missingTags:

        print tagPath

# ============================================================
# SUMMARY
# ============================================================

print ""
print "===================================================="
print "SUMMARY"
print "===================================================="
print ""

print "Total Tags Checked      : %d" % len(tagPaths)
print "History Enabled         : %d" % len(existingHistoryEnabled)
print "History Disabled        : %d" % len(existingHistoryDisabled)
print "Missing Tags            : %d" % len(missingTags)

print ""
print "=== SCRIPT COMPLETE ==="
print ""

log("=== SCRIPT COMPLETE ===")