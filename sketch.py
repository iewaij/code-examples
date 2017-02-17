dict = {'a': 3, 'b': 2, 'c': 6}
print dict.items()
sorted_result = sorted(dict.items(), key = lambda x: x[1])
print sorted_result
