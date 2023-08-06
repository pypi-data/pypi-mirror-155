import re

text1 = r'(abc) daf (abc)'
text2 = r'env:aa="D:\.venv"'

old_name='.venv'

mat = re.sub(r'\(' + 'abc' + r'\)', '(123)', text1)

mat = re.search(r'[a-zA-Z]:\\.*\\' + old_name + r'([\n"])', text2)

mat = re.search(r'[a-zA-Z]:\\' + old_name + r'([\n"])', text2)

print(mat.group())
