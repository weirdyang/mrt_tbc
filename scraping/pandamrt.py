import pandas as pd
import re

df = pd.read_csv('smrt_singapore_output.tsv', sep='\t', header='infer', encoding='utf-8')
df = df[df['full_text'].str.contains('fault')]
df = df[~df['full_text'].str.contains('update')]
df.to_csv('faults_smrt.tsv', sep='\t', header=True, encoding='utf-8')
print(df)
df = pd.read_csv('faults_smrt.tsv', sep='\t', header='infer', encoding='utf-8')
texts = df['full_text'].tolist()
faults = []
for name in texts:
    match = re.findall(r'#(\b\w+\b)', name)
    faults.extend(match)
with open('stations.txt', 'w+', encoding='utf-8') as f:
    for name in faults:
        f.write('{}\n'.format(name))
