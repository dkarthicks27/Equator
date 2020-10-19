array = 'hi hello hi hi hi perform'.split()
# print([tokens[i:i+shingleLength] for i in range(len(tokens) - shingleLength + 1)])

seen = set()
array1 = []
for i in array:
    if i not in seen:
        seen.add(i)
        array1.append(i)



print(array1)
print(seen)