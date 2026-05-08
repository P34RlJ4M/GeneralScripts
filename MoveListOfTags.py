# ============================================================
# IGNITION SCRIPT CONSOLE
# MOVE TAGS TO BADTAGS FOLDER
# ============================================================
#
# PURPOSE:
# Move tags into:
#
#   [default]CowPleasant_Tags/BadTags
#
# NOTES:
# - Tags are MOVED, not copied
# - Original tag names are preserved
# - Missing tags are logged
# - Detailed logging included
# - Compatible with Ignition Jython 2.7
#
# ============================================================

import system

# ============================================================
# LOGGER
# ============================================================

logger = system.util.getLogger("MoveBadTags")

def log(msg):
    logger.warn(msg)

log("=== SCRIPT START ===")

# ============================================================
# DESTINATION FOLDER
# ============================================================

destinationFolder = "[default]CowPleasant_Tags/BadTags"

# ============================================================
# TAGS TO MOVE
# ============================================================

tagPaths = [

    "[default]CowPleasant_Tags/FIT601_DS_O2_PM_H_SP",
    "[default]CowPleasant_Tags/FIT604_SCF_LT",
    "[default]CowPleasant_Tags/HSN_COMM_LOSS",
    "[default]CowPleasant_Tags/LIT201_FD_RQST_L_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP1_H_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP1_L_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP2_H_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP2_L_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP3_H_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP3_L_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP4_H_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP4_L_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP5_H_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP5_L_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP6_H_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP6_L_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP7_H_SP",
    "[default]CowPleasant_Tags/LIT301_MX301_STEP7_L_SP",
    "[default]CowPleasant_Tags/LIT401_LP_L_SP",
    "[default]CowPleasant_Tags/LIT401_TG_H_SP",
    "[default]CowPleasant_Tags/LIT601_H_FL_ST_H_SP",
    "[default]CowPleasant_Tags/LIT601_HH_HH_SP",
    "[default]CowPleasant_Tags/LIT601_L_FL_SD_L_SP",
    "[default]CowPleasant_Tags/LIT601_L_L_SP",
    "[default]CowPleasant_Tags/LIT601_LL_LL_SP",
    "[default]CowPleasant_Tags/LIT601_UP_ST_H_SP",
    "[default]CowPleasant_Tags/LT301_LL_LL_SP",
    "[default]CowPleasant_Tags/OG_",
    "[default]CowPleasant_Tags/OG_COMM_LOSS",
    "[default]CowPleasant_Tags/OG_PT3_PM_H_SP",
    "[default]CowPleasant_Tags/P201_AMP_HH_HH_SP",
    "[default]CowPleasant_Tags/P201_SPD_L_L_SP",
    "[default]CowPleasant_Tags/P202_AMP_HH_HH_SP",
    "[default]CowPleasant_Tags/P202_SPD_L_L_SP",
    "[default]CowPleasant_Tags/P301_AMP_HH_HH_SP",
    "[default]CowPleasant_Tags/P301_SPD_L_L_SP",
    "[default]CowPleasant_Tags/P302_AMP_HH_HH_SP",
    "[default]CowPleasant_Tags/P302_SPD_L_L_SP",
    "[default]CowPleasant_Tags/P401_AMP_HH_HH_SP",
    "[default]CowPleasant_Tags/P401_SPD_L_L_SP",
    "[default]CowPleasant_Tags/P402_AMP_HH_HH_SP",
    "[default]CowPleasant_Tags/P402_SPD_L_L_SP",
    "[default]CowPleasant_Tags/PIT201_L_L_SP",
    "[default]CowPleasant_Tags/PIT201_LL_LL_SP",
    "[default]CowPleasant_Tags/PIT202_H_H_SP",
    "[default]CowPleasant_Tags/PIT202_HH_HH_SP",
    "[default]CowPleasant_Tags/PIT203_H_H_SP",
    "[default]CowPleasant_Tags/PIT203_HH_HH_SP",
    "[default]CowPleasant_Tags/PIT301_H_H_SP",
    "[default]CowPleasant_Tags/PIT301_HH_HH_SP",
    "[default]CowPleasant_Tags/PIT302_H_H_SP",
    "[default]CowPleasant_Tags/PIT302_HH_HH_SP",
    "[default]CowPleasant_Tags/PIT401_H_H_SP",
    "[default]CowPleasant_Tags/PIT401_HH_HH_SP",
    "[default]CowPleasant_Tags/PIT402_H_H_SP",
    "[default]CowPleasant_Tags/PIT402_HH_HH_SP",
    "[default]CowPleasant_Tags/PM_SS_COMM_LOSS",
    "[default]CowPleasant_Tags/PT601_H_H_SP",
    "[default]CowPleasant_Tags/PT601_HH_HH_SP",
    "[default]CowPleasant_Tags/PT601_L_L_SP",
    "[default]CowPleasant_Tags/PT601_LL_LL_SP",
    "[default]CowPleasant_Tags/PT602_H_H_SP",
    "[default]CowPleasant_Tags/PT602_HH_HH_SP",
    "[default]CowPleasant_Tags/PT602_L_L_SP",
    "[default]CowPleasant_Tags/PT602_LL_LL_SP",
    "[default]CowPleasant_Tags/PT801_HH_HH_SP",
    "[default]CowPleasant_Tags/PT801_LL_LL_SP",
    "[default]CowPleasant_Tags/PT901_LL_LL_SP",
    "[default]CowPleasant_Tags/PT902_HH_HH_SP",
    "[default]CowPleasant_Tags/PT902_LL_LL_SP",
    "[default]CowPleasant_Tags/R301_AMP_HH_HH_SP",
    "[default]CowPleasant_Tags/R401_AMP_HH_HH_SP",
    "[default]CowPleasant_Tags/R402_AMP_HH_HH_SP",
    "[default]CowPleasant_Tags/UP_0NDA10CT001",
    "[default]CowPleasant_Tags/UP_0NDB11CT001",
    "[default]CowPleasant_Tags/UP_0UCA10CT001",
    "[default]CowPleasant_Tags/UP_0ULF10CT001",
    "[default]CowPleasant_Tags/UP_0ULF10CT002"

]

# ============================================================
# CREATE DESTINATION FOLDER IF NEEDED
# ============================================================

try:

    system.tag.configure(
        "[default]CowPleasant_Tags",
        [{
            "name": "BadTags",
            "tagType": "Folder"
        }],
        "m"
    )

    log("Verified BadTags folder exists")

except Exception as e:

    log("Failed to verify/create BadTags folder")
    log(str(e))

# ============================================================
# MOVE TAGS
# ============================================================

movedCount = 0
missingCount = 0
failedCount = 0

for sourcePath in tagPaths:

    try:

        # ====================================================
        # VERIFY TAG EXISTS
        # ====================================================

        if not system.tag.exists(sourcePath):

            log("MISSING: %s" % sourcePath)

            missingCount += 1
            continue

        # ====================================================
        # MOVE TAG
        # ====================================================

        system.tag.move(
            [sourcePath],
            destinationFolder
        )

        log("MOVED: %s" % sourcePath)

        movedCount += 1

    except Exception as e:

        log("FAILED: %s" % sourcePath)
        log(str(e))

        failedCount += 1

# ============================================================
# SUMMARY
# ============================================================

print ""
print "=================================================="
print "MOVE TAG SUMMARY"
print "=================================================="
print ""

print "Moved Tags   : %d" % movedCount
print "Missing Tags : %d" % missingCount
print "Failed Tags  : %d" % failedCount

print ""
print "=== SCRIPT COMPLETE ==="

log("Moved Tags   : %d" % movedCount)
log("Missing Tags : %d" % missingCount)
log("Failed Tags  : %d" % failedCount)

log("=== SCRIPT COMPLETE ===")