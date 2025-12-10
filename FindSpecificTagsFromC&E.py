import pandas as pd

excel_file = "/Users/seancourtney/Downloads/Berq/Papas Cause & Effect 10_09_25.xlsx"

# List of tags to search for
search_tags = [
    "FIT102", "FIT102_GAL_LT", "FIT102_GAL_TD", "FIT102_GAL_YD",
    "FIT102_GPS", "FIT102_OOR", "FIT102_OOR_TM", "FIT601_DS_O2_PM_H_SP",
    "GLT303_CL_STS", "HSN_COMM_LOSS", "LEL100_HHHH_HH_SP",
    "LIT201_FD_RQST_L_SP", "LIT201_LP_L_SP", "LIT201_LP_SP",
    "LIT301_LP_L_SP", "LIT301_LP_SP",
    "LIT301_MX301_STEP1_H_SP", "LIT301_MX301_STEP1_L_SP",
    "LIT301_MX301_STEP2_H_SP", "LIT301_MX301_STEP2_L_SP",
    "LIT301_MX301_STEP3_H_SP", "LIT301_MX301_STEP3_L_SP",
    "LIT301_MX301_STEP4_H_SP", "LIT301_MX301_STEP4_L_SP",
    "LIT301_MX301_STEP5_H_SP", "LIT301_MX301_STEP5_L_SP",
    "LIT301_MX301_STEP6_H_SP", "LIT301_MX301_STEP6_L_SP",
    "LIT301_MX301_STEP7_H_SP", "LIT301_MX301_STEP7_L_SP",
    "LIT302_LP_SP", "LIT401_LP_L_SP", "LIT401_LP_SP",
    "LIT601_H_FL_ST_H_SP", "LIT601_L_FL_SD_L_SP", "LIT601_UP_ST_H_SP",
    "P702_RN_STS", "TT301_LL_TD", "TT301_N_L_SP", "TT301_N_TD"
]

# Load column O by index (O = 14)
df = pd.read_excel(excel_file, sheet_name="C&E", header=0)

# Extract column O by index
col_O = df.iloc[:, 14].astype(str).str.strip()

# Find matches
matches = [tag for tag in search_tags if tag in col_O.values]

# Print results
print("Tags found in column O:\n")
for tag in matches:
    print("  -", tag)

print("\nTotal found:", len(matches))