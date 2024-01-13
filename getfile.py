import json
import requests 

#Set mode to storage
storage = requests.get("http://192.168.1.8/SetMode?Storage")
storage_json = json.dumps(json.loads(storage.content), indent=2)
print("setting storage Mode")

#Get list of media files
response = requests.get("http://192.168.1.8/Storage?GetFilePage=0&type=Photo")
one_line_json = response.content.decode('utf-8')
pretty_json = json.dumps(json.loads(response.content), indent=2)
jsonObject = json.loads(pretty_json)

#print(f'Original: {one_line_json}')
print(f'{pretty_json}')

b = json.loads(pretty_json)
dist = b['fs'][0]['fid']


for item in jsonObject["fs"]: 
    # Updated data["sample_data"] as the array is 
    # being present as the value for sample_data
    filename = item["fid"]
    name = item["n"]
    url = "http://192.168.1.8/Storage?Download=" + filename
    data = requests.get("http://192.168.1.8/Storage?Download=" + filename)
    print ("Downloading: " + name)
    with open(name,'wb') as f:
      f.write(data.content)

#download Media 

off = requests.get("http://192.168.1.8/Misc?PowerOff")


