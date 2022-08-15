from statsmodels.tsa.stattools import grangercausalitytests
import pandas as pd

df = pd.read_csv('StockData/main_ds.csv')

max_lag = 7  # 1 week
thresh = 0.05
p_vals = {}
companies = [
    "CBAT_Bat",
    "ENS_Bat",
    "TIA_Bat",
    "ALB_Min",
    "LAC_Min",
    "SQM_Min",
]


def print_signif(p_val, thresh):
    p_val = round(p_val, 4)
    if (p_val <= thresh):
        print("\n ***** SIGNIFICANT! *****")
        print(f"p_val: {p_val} <= thresh {thresh}")
    print()


def is_significant(p_val, thresh):
    if (p_val <= thresh):
        return True
    return False


def get_p_value(result):
    return result.get(max_lag)[0].get("ssr_ftest")[1]


def format_matrix(p_vals):
    matrix_str = '{:10}'.format(" ")
    for row in p_vals:
        matrix_str +=  '{:10}'.format(str(row))
    matrix_str += '\n'
    for row in p_vals:
        matrix_str += '{:10}'.format(str(row))
        for val in p_vals[row]:
            matrix_str += '{:10}'.format(str(val))
        matrix_str += "\n"
    return matrix_str


# Perform forward and reverse GC testing
for cause in companies:
    effect_p_vals = []
    for effect in companies:
        print("\n" + cause + " -> " + effect)
        result = grangercausalitytests(df[[cause, effect]], maxlag=[max_lag])
        p_val = get_p_value(result)
        effect_p_vals.append(round(p_val, 4))
    p_vals[cause] = effect_p_vals


print("\n\n"+format_matrix(p_vals))

print(f"P vals below the {thresh} significant threshold:\n")
print(f"{'{:11}'.format('Cause')} {'{:10}'.format('Effect')} {'{:8}'.format('P Val')}")

keys_list = list(p_vals)
for idx_row, row in enumerate(p_vals):
    for idx_col, val in enumerate(p_vals[row]):
        if is_significant(val, thresh):
            print(f"{'{:8}'.format(row)} -> {keys_list[idx_col]} {'{:8}'.format(val)}")
