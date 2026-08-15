books = []
for i in range(5):
    title = input("Enter book title: ")
    books.append(title)
longest = max(books, key=len)
shortest = min(books, key=len)
print("Longest title:", longest)
print("Shortest title:", shortest)
word = input("Enter word to search: ")
for title in books:
    if word.lower() in title.lower().split():
        print("Word found in:", title)
for title in books:
    print(title, "->", len(title.split()), "words")
books.sort()
print("Final list:")
for title in books:
    print(title)
    