import pandas as pd

papers_path = input().strip()
links_path = input().strip()


papers = pd.read_csv(papers_path, sep=';', dtype={'id': str})
papers.columns = ['id', 'title', 'author']
papers['title'] = papers['title'].str.strip()
papers['author'] = papers['author'].str.strip()


links = pd.read_csv(links_path, sep=';', dtype=str)
links.columns = ['paper_id', 'reference']
links['reference'] = links['reference'].str.strip()


citations = links.groupby('reference').size().reset_index(name='cites')


merged = papers.merge(citations, left_on='title', right_on='reference', how='left')
merged['cites'] = merged['cites'].fillna(0).astype(int)


author_avg = merged.groupby('author', as_index=False)['cites'].mean()
author_avg.columns = ['author', 'avg']


top3 = author_avg.sort_values('avg', ascending=False).head(3)
for _, row in top3.iterrows():
    print(f"{row['author']} {row['avg']:.3f}")