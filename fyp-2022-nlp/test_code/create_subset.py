import pandas as pd

df_train_text = pd.read_csv('data/hate/train_text.txt', sep='\t', header=None)

# Take random sample of 100 rows
df_train_text_sample = df_train_text.sample(n=100)

# Output this sample to a new file
df_train_text_sample.to_csv('data/hate/train_text_sample.txt', sep='\t', header=None, index=False)