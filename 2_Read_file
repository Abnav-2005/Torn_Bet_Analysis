import pandas as pd
df = pd.read_csv("bookies_clean1.csv")
df

#Make a new column Sl. no at the beginning which starts from 1 and not 0
df.insert(0, "Sl. no", range(1, len(df) + 1))
df.to_excel("bookies_clean1.xlsx", index=False)

df

df = pd.read_excel("bookies_full_with_profit_corrected_v3.xlsx")
df

cols = ["stake_final", "profit_amount", "loss_amount", "refund_amount"]
 



