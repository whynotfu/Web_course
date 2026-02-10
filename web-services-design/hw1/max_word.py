import re

with open("example.txt", encoding="utf-8") as f:
    text = f.read()

words = re.findall(r"[A-Za-zА-Яа-яЁё]+", text)

max_len = max(len(word) for word in words)

for word in words:
    if len(word) == max_len:
        print(word)
