import re

with open('./data.txt', 'r') as f, open('./result.txt', 'w+') as out:
    data = f.read()
   # result = list(re.findall(r'[а-яА-Я]+ | \n | \d*', data))
    result = re.sub(r'<.*>', '', data)
    out.write(result.strip())