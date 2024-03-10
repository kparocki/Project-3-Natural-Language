import pandas as pd

# Read in the sample file
df_train_text_sample = pd.read_csv('data/hate/train_text_sample.txt', sep='\t', header=None)

# Read in the original file
df_train_text = pd.read_csv('data/hate/train_text.txt', sep='\t', header=None)
# Read in the original label
df_train_label = pd.read_csv('data/hate/train_labels.txt', sep='\t', header=None)

# Combine the two datasets into one with header
df_train = pd.concat([df_train_text, df_train_label], axis=1)
# Rename columns
df_train.columns = ['text', 'label']


# Map the labels from the original file to the sample file
final_df = pd.DataFrame(columns=['text', 'label'])

# Loop over each row in the sample file and lookup label
for index, row in df_train_text_sample.iterrows():
    # Get the text
    text = row[0]

    # Lookup label in original file
    label = df_train[df_train['text'] == text]['label'].values[0]

    # Add to final dataframe
    final_df = final_df.append({'text': text, 'label': label}, ignore_index=True)

    # Save checkpoint to file
    final_df.to_csv('data/hate/train_text_sample_with_labels.csv', sep='\t', index=False)