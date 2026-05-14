import system
import time

# ============================================================
# LOGGER
# ============================================================
logger = system.util.getLogger(
    "ActivePipelineUpdater"
)

def log(msg):

    logger.warn(str(msg))
    print str(msg)

# ============================================================
# CONFIG
# ============================================================
base_folder = "[default]CowPleasant_Tags"

#
# Leave blank to CLEAR the activePipeline
#
new_pipeline = ""

# ============================================================
# TAG LIST
# ============================================================
tagPaths = [
    "OAS102_OOR",
    "AT601_OOR",
    "AT6011_OOR",
    "AT6021_OOR",
    "FIT201_OOR",
    "FIT401_OOR",
    "FIT603_OOR",
    "FIT604_OOR",
    "AT602_CH4_LL",
    "AT602_CO2_HH",
    "AT602_O2_HH",
    "LT301_LL",
    "PIT201_L",
    "PIT202_H",
    "PIT203_H",
    "PIT301_H",
    "PIT302_H",
    "PIT401_H",
    "PIT402_H",
    "PT801_LL",
    "PT801_HH",
    "PT801_OOR",
    "TT201_H",
    "TT202_H",
    "TT203_OOR",
    "TT204_OOR",
    "TT302_H",
    "TT303_H",
    "TT304_OOR",
    "TT305_OOR",
    "TT401_LL",
    "TT402_H",
    "TT403_H",
    "TT404_OOR",
    "TT405_OOR",
    "TT701_OOR",
    "TT702_OOR",
    "TT703_OOR",
    "TT704_OOR",
    "TT705_OOR",
    "TT706_OOR",
    "TT707_OOR",
    "TT708_OOR",
    "P201_SPD_L",
    "P201_AMP_HH",
    "P201_VFD_FLT",
    "P202_SPD_L",
    "P202_AMP_HH",
    "P202_VFD_FLT",
    "P301_SPD_L",
    "P301_AMP_HH",
    "P301_VFD_FLT",
    "P302_SPD_L",
    "P302_AMP_HH",
    "P302_VFD_FLT",
    "P401_SPD_L",
    "P401_AMP_HH",
    "P401_VFD_FLT",
    "P402_SPD_L",
    "P402_AMP_HH",
    "P402_VFD_FLT",
    "R401_AMP_HH",
    "R401_VFD_FLT",
    "R402_AMP_HH",
    "R402_VFD_FLT",
    "R403_AMP_HH",
    "R403_VFD_FLT",
    "V603_AMP_HH",
    "V603_VFD_FLT",
    "Z201_AMP_HH",
    "Z201_AMP_HH_SD",
    "Z201_VFD_FLT",
    "UP_0RHM10AN001_ALM",
    "UP_0RHA10AN001_ALM",
    "UP_0NDD10AC001_ALM",
    "UP_0RHA91AA101_ALM",
    "UP_0RKC10AA101_ALM",
    "UP_0RHH10AA103_ALM",
    "UP_0RHM10AA101_ALM",
    "UP_0RKC15AA101_ALM",
    "UP_0RHS20AT001",
    "UP_GN_WRN",
    "UP_NOT_RDY",
    "FL_GN_ALM",
    "FL_B2112_GN_ALM",
    "RACK1_COMM_LOSS",
    "HSN_COMM_LOSS",
    "PM_MSB1_COMM_LOSS",
    "PM_UP_COMM_LOSS",
    "PM_DS_COMM_LOSS",
    "PM_OG_COMM_LOSS",
    "PM_SS_COMM_LOSS",
    "OG_COMM_LOSS",
    "BL_COMM_LOSS",
    "UP_COMM_LOSS",
    "FL_COMM_LOSS",
    "P201_COMM_LOSS",
    "P202_COMM_LOSS",
    "P301_COMM_LOSS",
    "P302_COMM_LOSS",
    "P401_COMM_LOSS",
    "P402_COMM_LOSS",
    "R301_COMM_LOSS",
    "R401_COMM_LOSS",
    "R402_COMM_LOSS",
    "R403_COMM_LOSS",
    "Z201_COMM_LOSS",
    "V601_COMM_LOSS",
    "V603_COMM_LOSS",
    "P701_FLT",
    "P702_FLT",
    "P703_FLT",
    "P704_FLT",
    "P501_FLT",
    "R201_FLT",
    "V901_FLT",
    "V902_FLT",
    "FV101_OP_FLT",
    "FV101_CL_FLT",
    "FV203_OP_FLT",
    "FV203_CL_FLT",
    "FV214_OP_FLT",
    "FV214_CL_FLT",
    "FV216_OP_FLT",
    "FV216_CL_FLT",
    "FV303_OP_FLT",
    "FV303_CL_FLT",
    "FV310_OP_FLT",
    "FV310_CL_FLT",
    "FV312_OP_FLT",
    "FV312_CL_FLT",
    "FV314_OP_FLT",
    "FV314_CL_FLT",
    "FV403_OP_FLT",
    "FV403_CL_FLT",
    "FV414_OP_FLT",
    "FV414_CL_FLT"
]

# ============================================================
# UPDATE ALARM PIPELINES
# ============================================================
def update_pipeline(tag_name):

    try:

        # ====================================================
        # BUILD FULL TAG PATH
        # ====================================================
        tag_path = (
            base_folder +
            "/" +
            str(tag_name)
        )

        log("------------------------------------------------")
        log("Checking tag:")
        log(tag_path)

        # ====================================================
        # VERIFY TAG EXISTS
        # ====================================================
        if not system.tag.exists(tag_path):

            return False, "TAG NOT FOUND"

        # ====================================================
        # READ CONFIGURATION
        # ====================================================
        config = system.tag.getConfiguration(
            tag_path,
            False
        )

        if not config:

            return False, "NO CONFIGURATION"

        tagConfig = config[0]

        # ====================================================
        # CHECK ALARMS
        # ====================================================
        alarms = tagConfig.get(
            "alarms",
            []
        )

        if len(alarms) == 0:

            return False, "NO ALARMS"

        log("Alarm count: %d" % len(alarms))

        # ====================================================
        # UPDATE ACTIVE PIPELINES
        # ====================================================
        updatedCount = 0

        for alarm in alarms:

            try:

                alarmName = alarm.get(
                    "name",
                    "UnnamedAlarm"
                )

                oldPipeline = alarm.get(
                    "activePipeline",
                    ""
                )

                log(
                    "Alarm: %s"
                    % alarmName
                )

                log(
                    "Old Pipeline: %s"
                    % oldPipeline
                )

                # ============================================
                # CLEAR ACTIVE PIPELINE
                # ============================================
                alarm["activePipeline"] = new_pipeline

                log(
                    "New Pipeline: BLANK"
                )

                updatedCount += 1

            except Exception as e:

                log("FAILED TO UPDATE ALARM")
                log(str(e))

        # ====================================================
        # SAVE CONFIGURATION
        # ====================================================
        result = system.tag.configure(

            basePath=base_folder,

            tags=[tagConfig],

            collisionPolicy="o"
        )

        log("CONFIGURE RESULT:")
        log(str(result))

        return True, (
            "UPDATED %d ALARM(S)"
            % updatedCount
        )

    except Exception as e:

        import traceback

        log("EXCEPTION:")
        log(str(e))
        log(traceback.format_exc())

        return False, str(e)

# ============================================================
# START
# ============================================================
log("====================================================")
log("STARTING ACTIVE PIPELINE CLEAR")
log("====================================================")

log("Target tag count: %d" % len(tagPaths))

successCount = 0
failCount = 0

# ============================================================
# PROCESS TAGS
# ============================================================
for tagName in tagPaths:

    success, msg = update_pipeline(
        tagName
    )

    if success:

        log("SUCCESS: %s" % msg)

        successCount += 1

    else:

        log("FAILED: %s" % msg)

        failCount += 1

    #
    # Small delay for gateway breathing room
    #
    time.sleep(0.25)

# ============================================================
# SUMMARY
# ============================================================
log("")
log("====================================================")
log("UPDATE COMPLETE")
log("====================================================")

log("Successful Updates : %d" % successCount)
log("Failed Updates     : %d" % failCount)
log("Total Processed    : %d" % len(tagPaths))
