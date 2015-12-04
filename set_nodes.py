import json

filename = "latest.json"

with open(filename, 'r') as f:
	data = json.load(f)

strs = {}

for ip in data['nodes']:
	ver = data['nodes'][ip][1]
	if ver in strs:
		strs[ver] += 1
	else:
		strs[ver] = 1

# sort dictionary by frequency
import operator
strs = sorted(strs.items(), key=operator.itemgetter(1), reverse=True)

# print
for i in strs:
	print(i[1],'\t', i[0])
