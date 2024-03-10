import pandas as pd  

lst = []
i = 0
with open('data/hate/train_text_sample.txt', "r", encoding="utf-8") as in_file:
    for line in in_file.readlines():
        print(line)
        lst.append(input('label: '))
        if i == 2:
            break
        i =+ 1


df = pd.DataFrame(lst)
df.to_csv('labels.csv', index=False)

