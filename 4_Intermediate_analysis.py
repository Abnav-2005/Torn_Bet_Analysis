"""
Purpose:

To understand which odds ranges (low odds vs high odds) produced the best betting performance.

What I did:

I divided odds into meaningful “buckets”:

<1.5, 1.5–2.0, 2.0–2.5, 2.5–3.0, 3.0–5.0, 5.0+

For each bucket, we calculated:

Total Profit (sum of money won)

Total Loss (sum of money lost)

Total Stake (money risked)

Number of Bets

Then I computed:

net = total_profit - total_loss
ROI % = (net / total_stake) × 100

Why this is useful:

This shows which odds ranges are profitable or unprofitable.

For example:

Low odds may win more often but have low payouts.

High odds may give higher profit but lose more frequently.

This analysis lets you identify the sweet spot where risk and reward balance best.

Deliverables:

Table of odds buckets with profit, loss, ROI, stake, count

Exported as: odds_bucket_roi.xlsx

"""
bins = [0,1.5,2.0,2.5,3.0,5.0,100]
labels = ['<1.5','1.5-2.0','2.0-2.5','2.5-3.0','3.0-5.0','5.0+']
df['odds_bucket'] = pd.cut(df['odds'], bins=bins, labels=labels, include_lowest=True)
agg = df.groupby('odds_bucket').agg(total_profit=('profit_amount','sum'), total_loss=('loss_amount','sum'), total_stake=('stake_final','sum'), count=('bet_id','count'))
agg['net'] = agg['total_profit'].fillna(0) - agg['total_loss'].fillna(0)
agg['ROI_pct'] = (agg['net'] / agg['total_stake']) * 100
print(agg.sort_values('count', ascending=False))
agg.to_excel('odds_bucket_roi.xlsx')
















"""
Purpose:

To find out which teams/events I bet on the most, and whether those bets were profitable or not.

What we did:

Grouped data by both:

pick (team/selection)

game (sport category)

For each combination, we calculated:

Total number of bets

Total profit

Total loss

Net = profit − loss

Why this is useful:

This analysis gives insights into:

Which teams I bet on most often

Which picks were consistently profitable

Which picks were costing me money

How my betting preferences affect my results

It helps identify profitable patterns and risky trends.

Deliverables:

Top 20 picks by frequency

Top 50 saved to top_picks.xlsx

"""

top_picks = df.groupby(['pick','game']).agg(count=('bet_id','count'), profit=('profit_amount','sum'), loss=('loss_amount','sum'))
top_picks['net'] = top_picks['profit'].fillna(0) - top_picks['loss'].fillna(0)
print(top_picks.sort_values('count', ascending=False).head(20))
top_picks.sort_values('count', ascending=False).head(50).to_excel('top_picks.xlsx')












"""
Purpose:

To analyze how different bet sizes perform and how often each stake size is used.

What we did:

We divided stake amounts into 5 tiers:

Tier	Range	Meaning
tiny	0–1M	Very small bets
small	1M–10M	Low-risk bets
medium	10M–50M	Moderate bets
large	50M–200M	High stakes
whale	200M–1T	Very large bets

Then for each tier, we calculated:

Number of bets

Net profit (profit − loss)

Why this is useful:

Shows how your betting behavior changes with stake size, such as:

Do large stakes perform worse than small stakes?

Are medium stakes your most profitable?

Do whale bets cause huge variance?

This is excellent for understanding risk management and bet sizing strategy.

Deliverables:

Stake tier summary

Saved as stake_tier_stats.xlsx

"""

bins = [0, 1_000_000, 10_000_000, 50_000_000, 200_000_000, 10**12]
labels = ['tiny (0–1M)','small (1M–10M)','medium (10M–50M)','large (50M–200M)','whale (200M–1T)']
df['stake_tier'] = pd.cut(df['stake_final'], bins=bins, labels=labels)
tier_stats = df.groupby('stake_tier').agg(bets=('bet_id','count'), net=('profit_amount','sum'))
print(tier_stats)
tier_stats.to_excel('stake_tier_stats.xlsx')
















"""
Purpose:

To check whether any numeric variables in the dataset move together or influence each other.

What we analyzed:
Column	Meaning
stake_final	money risked
profit_amount	money won
loss_amount	money lost
refund_amount	refunded stake
odds	betting odds taken

We used df.corr() to compute pairwise correlations.

Interpretation of correlation values:
Value	Meaning
+1.0	perfectly increases together
0	no relationship
-1.0	perfectly inverse relationship
Why this is useful:

The correlation matrix helps answer:

Do higher stakes lead to higher profits?

Are higher odds linked to bigger profit swings?

Are loss amounts strongly linked to stake size?

Are profit and loss inversely related (they should be)?

This provides a statistical summary of relationships in your dataset.

Deliverables:

Correlation matrix

Saved as numeric_corr.xlsx

"""

numcols = ['stake_final','profit_amount','loss_amount','refund_amount','odds']
numcols = [c for c in numcols if c in df.columns]
corr = df[numcols].corr()
print(corr)
corr.to_excel('numeric_corr.xlsx')
