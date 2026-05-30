logger = system.util.getLogger("CommLossTagInit")

parentFolder = "[default]CowPleasant_Tags/MemoryTags"
tagName = "CommLossTags 1"
tagPath = parentFolder + "/" + tagName

try:
    if not system.tag.exists(tagPath):
        tagConfig = {
            "name": tagName,
            "tagType": "AtomicTag",
            "valueSource": "memory",
            "dataType": "DataSet"
        }

        # "a" = abort if something already exists; safer than overwrite
        result = system.tag.configure(parentFolder, [tagConfig], "a")
        logger.info("Created dataset tag {0}. Result: {1}".format(tagPath, result))
    else:
        logger.info("Dataset tag already exists: {0}".format(tagPath))

    headers = ["tagPath", "documentation", "tagName"]

    data = [
        ["[default]CowPleasant_Tags/RACK1_COMM_LOSS", "PLC201 REMOTE RACK 1 LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "RACK1_COMM_LOSS"],
        ["[default]CowPleasant_Tags/PM_UP_COMM_LOSS", "UPGRADER POWER METER LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "PM_UP_COMM_LOSS"],
        ["[default]CowPleasant_Tags/BL_COMM_LOSS", "BOILER LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "BL_COMM_LOSS"],
        ["[default]CowPleasant_Tags/UP_COMM_LOSS", "UPGRADER LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "UP_COMM_LOSS"],
        ["[default]CowPleasant_Tags/FL_COMM_LOSS", "FLARE LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "FL_COMM_LOSS"],
        ["[default]CowPleasant_Tags/P201_COMM_LOSS", "DIGESTER SLUDGE FILL PUMP 1 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "P201_COMM_LOSS"],
        ["[default]CowPleasant_Tags/P202_COMM_LOSS", "DIGESTER SLUDGE FILL PUMP 2 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "P202_COMM_LOSS"],
        ["[default]CowPleasant_Tags/P301_COMM_LOSS", "DIGESTATE TRANSFER PUMP 1 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "P301_COMM_LOSS"],
        ["[default]CowPleasant_Tags/P302_COMM_LOSS", "DIGESTATE TRANSFER PUMP 2 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "P302_COMM_LOSS"],
        ["[default]CowPleasant_Tags/P401_COMM_LOSS", "DIGESTATE DISCHARGE PUMP 1 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "P401_COMM_LOSS"],
        ["[default]CowPleasant_Tags/P402_COMM_LOSS", "DIGESTATE DISCHARGE PUMP 2 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "P402_COMM_LOSS"],
        ["[default]CowPleasant_Tags/R401_COMM_LOSS", "SECONDARY DIGESTER SIDE MIXER 1 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "R401_COMM_LOSS"],
        ["[default]CowPleasant_Tags/R402_COMM_LOSS", "SECONDARY DIGESTER SIDE MIXER 2 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "R402_COMM_LOSS"],
        ["[default]CowPleasant_Tags/R403_COMM_LOSS", "SECONDARY DIGESTER SIDE MIXER 3 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "R403_COMM_LOSS"],
        ["[default]CowPleasant_Tags/Z201_COMM_LOSS", "PRETREAT GRINDER VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "Z201_COMM_LOSS"],
        ["[default]CowPleasant_Tags/V603_COMM_LOSS", "DESULPHUR INLET BLOWER 2 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "V603_COMM_LOSS"],
        ["[default]CowPleasant_Tags/R301_COMM_LOSS", "DIGESTER MIXER VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "R301_COMM_LOSS"],
        ["[default]CowPleasant_Tags/R401_COMM_LOSS", "DG2 MIXER 1 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "R401_COMM_LOSS"],
        ["[default]CowPleasant_Tags/R402_COMM_LOSS", "DG2 MIXER 2 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "R402_COMM_LOSS"],
        ["[default]CowPleasant_Tags/R403_COMM_LOSS", "DG2 MIXER 3 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "R403_COMM_LOSS"],
        ["[default]CowPleasant_Tags/V601_COMM_LOSS", "DESULPHUR INLET BLOWER 1 VFD COMMUNICAITON LOSS (0=NORMAL, 1=COMM LOSS)", "V601_COMM_LOSS"],
        ["[default]CowPleasant_Tags/PM_MSB1_COMM_LOSS", "MSB1 MAIN POWER METER LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "PM_MSB1_COMM_LOSS"],
        ["[default]CowPleasant_Tags/PM_DS_COMM_LOSS", "DESULPHUR POWER METER LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "PM_DS_COMM_LOSS"],
        ["[default]CowPleasant_Tags/PM_OG_COMM_LOSS", "O2 GENERATOR POWER METER LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "PM_OG_COMM_LOSS"],
        ["[default]CowPleasant_Tags/PM_SS_COMM_LOSS", "SAND SEPARATOR POWER METER LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "PM_SS_COMM_LOSS"],
        ["[default]CowPleasant_Tags/OG_COMM_LOSS", "O2 GENERATOR LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "OG_COMM_LOSS"],
        ["[default]CowPleasant_Tags/HSN_COMM_LOSS", "HISTORIAN LOSS OF COMMUNICATION (0=NORMAL, 1=COM LOSS)", "HSN_COMM_LOSS"]
    ]

    ds = system.dataset.toDataSet(headers, data)

    writeResult = system.tag.writeBlocking([tagPath], [ds])
    logger.info("Wrote dataset to {0}. Result: {1}".format(tagPath, writeResult))

except Exception as e:
    logger.error("Failed initializing CommLossTags 1: {0}".format(str(e)))