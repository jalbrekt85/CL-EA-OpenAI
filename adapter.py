from bridge import Bridge
import json
import config
import binascii
from preprompt import pre_prompt

class Adapter:

    def __init__(self, input):
        self.base_url = "https://api.openai.com/v1/engines/davinci/completions"
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.set_params()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def set_params(self):
        self.prompt = self.request_data.get("prompt")

    def create_request(self):
        print(pre_prompt + self.prompt)
        try:
            headers={
    "Authorization": f"Bearer {config.API_KEY}",
    "Content-Type": 'application/json'
  }
            json={
                "prompt": pre_prompt + self.prompt,
                "max_tokens": 40,
                "temperature": 0.5,
                "top_p": 1,
                "n": 1,
                "stop": ["#"]
            }
            response = self.bridge.request(self.base_url, json=json, headers=headers)
            data = response.json()['choices'][0]['text']
            if ':' in data:
                data = data.split(':')[1][1:]
            hex_data = binascii.hexlify(data.encode('utf8'))
            bytes_data = '0x' + str(hex_data)[2:-1]
            self.result = bytes_data
            self.result_success(bytes_data)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, data):
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'result': self.result,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
