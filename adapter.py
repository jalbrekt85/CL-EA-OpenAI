from bridge import Bridge
import json
import config

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
        try:
            headers={
    "Authorization": f"Bearer {config.API_KEY}",
    "Content-Type": 'application/json'
  }
            json={
    "prompt": self.prompt,
    "max_tokens": 150,
}
            response = self.bridge.request(self.base_url, json=json, headers=headers)
            data = response.json()['choices'][0]['text']
            self.result = data
            self.result_success(data)
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
