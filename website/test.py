import json

a_dictionary = {"gender": "Male"}

f = open('website/onboarding_stat.json', 'r+')
data = json.load(f)

#print(data['gender'])
data.update(a_dictionary)
f.seek(0)
json.dump(data, f)