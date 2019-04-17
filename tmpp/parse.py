import json
import xmltodict
 
with open("gateway.xml", 'r') as f:
    xmlString = f.read()
 
print("XML input (sample.xml):")
print(xmlString)
     
jsonString = json.dumps(xmltodict.parse(xmlString))
actualJson = json.loads(jsonString)

print(actualJson)
print(type(actualJson))

print(actualJson['application']['gateways'])
print("\nJSON output(output.json):")

with open("output.json", 'w') as f:
    f.write(jsonString)