from pprint import pprint

import requests
import json
import hashlib


url = "https://suitecrmdemo.dtbc.eu/service/v4/rest.php"
payload = {
    "method": "login",
    "input_type": "JSON",
    "response_type": "JSON",
    "rest_data": json.dumps({
        "user_auth": {
            "user_name": "Demo",
            # "password": "Demo"
            "password": hashlib.md5("Demo".encode()).hexdigest()
        },
        "application_name": "RestTest",
        "name_value_list": []
    })
}
response = requests.post(url, data=payload, verify=False)

if response.status_code == 200:
    session_id = json.loads(response.text)["id"]
    print("Session ID:", session_id)
else:
    print("Failed to get session ID")

pprint(response.json())

payload = {
    'method': 'get_entry_list',
    'input_type': 'JSON',
    'response_type': 'JSON',
    'rest_data': json.dumps({
        'session': session_id,
        'module_name': 'Leads',
        'query': '',
        'order_by': '',
        'offset': '0',
        'select_fields': [],
        'link_name_to_fields_array': [],
        'max_results': '1000',
        'deleted': '0'
    })
}
response_l = requests.post(url, data=payload)

if response.status_code == 200:
    print(200)
    # leads_data = json.loads(response.text)['entry_list']
    # for lead in leads_data:
    #     print(lead)
else:
    print('Failed to fetch leads')


# pprint(response.json())
result = response_l.json() ## ???
with open("data.json", "w") as f:
    f.write(json.dumps(result))
    f.close()
