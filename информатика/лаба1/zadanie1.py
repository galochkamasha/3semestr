import pandas as pd

games_path = input().strip()
rates_path = input().strip()


games = pd.read_csv(games_path, sep=';', dtype={'id': str})
games.columns = ['id', 'name', 'company']
games['id'] = games['id'].str.strip()


rates = pd.read_csv(rates_path, sep=';', dtype={'id': str})
rates.columns = ['id', 'mark']
rates['id'] = rates['id'].str.strip()
rates['mark'] = rates['mark'].astype(float)


avg_scores = rates.groupby('id', as_index=False)['mark'].mean()
avg_scores.columns = ['id', 'avg']

merged = games.merge(avg_scores, on='id', how='inner')


top3 = merged.sort_values('avg', ascending=False).head(3)
for _, row in top3.iterrows():
    print(f"{row['name']} {row['avg']:.3f}")


high = merged[merged['avg'] > 8.0]
studio_counts = high.groupby('company').size().reset_index(name='count')
studio_counts = studio_counts.sort_values(
    by=['count', 'company'], ascending=[False, True]
)

best = studio_counts.iloc[0]
print(f"{best['company']} {best['count']}")