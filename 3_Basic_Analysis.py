import pandas as pd
import numpy as np

df = pd.read_excel("bookies_full_with_profit_corrected_v3.xlsx")
df

#Removing commas and converting to numeric in order to do calculations on these columns 
num_cols = ['stake_final','profit_amount','loss_amount','refund_amount','odds']

for c in num_cols:
    if c in df.columns:
        df[c] = (df[c]
                 .astype(str)                    # convert e.g. "1,000,000" to string
                 .str.replace(',', '', regex=False)  # remove commas
                 .replace({'None':np.nan, 'nan':np.nan}) 
                 .replace({'':np.nan})
                 .pipe(pd.to_numeric, errors='coerce'))
# quick look
print(df[num_cols].head())


#Single-line overall summary
summary = {
    'total_bets': int(len(df)),
    'total_stake': int(df['stake_final'].sum(min_count=1)) if 'stake_final' in df.columns else None,
    'total_profit_amount': int(df['profit_amount'].sum(min_count=1)) if 'profit_amount' in df.columns else None,
    'total_loss_amount': int(df['loss_amount'].sum(min_count=1)) if 'loss_amount' in df.columns else None,
    'net_profit': int(df['profit_amount'].sum(min_count=1) - df['loss_amount'].sum(min_count=1)) if ('profit_amount' in df.columns and 'loss_amount' in df.columns) else None,
    'win_count': int((df['profit_amount']>0).sum()) if 'profit_amount' in df.columns else None,
    'loss_count': int((df['loss_amount']>0).sum()) if 'loss_amount' in df.columns else None,
    'refund_count': int((df['refund_amount']>0).sum()) if 'refund_amount' in df.columns else None,
    'win_rate': None
}
if summary['win_count'] is not None and summary['loss_count'] is not None and (summary['win_count']+summary['loss_count'])>0:
    summary['win_rate'] = round(summary['win_count']/(summary['win_count']+summary['loss_count']), 4)
print(summary)


#Converting numbers to formatted strings for display
def fmt(x):
    return f"{int(x):,}" if pd.notna(x) else "N/A"

# example usage after running snippet #1:
print("Total bets:", summary['total_bets'])
print("Total stake: $"+ fmt(summary['total_stake']))
print("Net profit: $"+ fmt(summary['net_profit']))
print("Win rate:", f"{summary['win_rate']:.2%}" if summary['win_rate'] is not None else "N/A")



#Top 10 games by total stake (which sports you bet most on)
by_game = df.groupby('game').agg(total_stake=('stake_final','sum'), bets=('bet_id','count')).sort_values('total_stake', ascending=False)
print(by_game.head(10))
by_game.head(10).to_excel('by_game_top10.xlsx')


#Top 10 games by net profit (who gave you wins/losses)
top_wins = df.sort_values('profit_amount', ascending=False).head(10)[['bet_id','game','name','stake_final','profit_amount','odds']]
top_losses = df.sort_values('loss_amount', ascending=False).head(10)[['bet_id','game','name','stake_final','loss_amount','odds']]
print("Top wins:\n", top_wins)
print("Top losses:\n", top_losses)
top_wins.to_excel('top_wins.xlsx', index=False)
top_losses.to_excel('top_losses.xlsx', index=False)
