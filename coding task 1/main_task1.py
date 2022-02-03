import json, unittest, datetime, string

with open("./data1_task1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data2_task1.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result_task1.json","r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1 (jsonObject):

    # IMPLEMENT: Conversion From Type 1
    #step1. copy location string
    location = jsonObject.get('location')
    #step2. remove the location element, we are going to update it
    jsonObject.pop('location')
    #step3. splitting the location into the several parts that are divided by "/"
    # remark: I imported String library to use rsplit method.
    listLocation = location.rsplit("/")
    #step4. now create a new dict inside of a jsonObject for the new method of displaying location
    jsonObject['location'] = {"country" : listLocation[0], "city" : listLocation[1],
    "area" : listLocation[2], "factory" : listLocation[3], "section": listLocation[4]}

    #step5. take the status and temperature for the "data" section
    status = jsonObject.get('operationStatus')
    temperature = jsonObject.get('temp')
    #step6. remove abovementioned elements
    jsonObject.pop('operationStatus')
    jsonObject.pop('temp')

    #step7. create new "data" section
    jsonObject['data'] = {'status': status, 'temperature' : temperature}


    return jsonObject


def convertFromFormat2 (jsonObject):

    # IMPLEMENT: Conversion From Type 2
    res={}
    #step1. as we can see almost everything needs change
    #therefore, lets copy what we need first
    #first of all, take the deviceID and devicetype
    deviceID = jsonObject['device'].get('id')
    deviceType = jsonObject['device'].get('type')
    res['deviceID'] = deviceID
    res['deviceType'] = deviceType
    #step2. change the timestamp to the one we need
    time = jsonObject.get('timestamp')
    date = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = str((date - datetime.datetime(1970, 1, 1)).total_seconds()*1000)
    timestamp = timestamp[:-2]
    timestamp = int(timestamp)
    res['timestamp'] = timestamp


    #step3. make one big section called location
    res['location'] = {'country' : jsonObject.get('country'),
    'city' : jsonObject.get('city'),
    'area' : jsonObject.get('area'),
    'factory' : jsonObject.get('factory'),
    'section' : jsonObject.get('section')}

    #step4. copy data thing to resulting dictionary
    res['data'] = jsonObject.get('data')

    return res


def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
