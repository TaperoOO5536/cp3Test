import requests
import pprint


class BaseRequest:
  def __init__(self, base_url):
    self.base_url = base_url


  def _request(self, url, request_type, data=None, expected_error=False):
    stop_flag = False
    while not stop_flag:
      if request_type == 'GET':
          response = requests.get(url)
      elif request_type == 'POST':
          response = requests.post(url, json=data)
      elif request_type == 'PUT':
          response = requests.put(url, json=data)    
      else:
          response = requests.delete(url)

      if not expected_error and response.status_code == 200:
        stop_flag = True
      elif expected_error:
        stop_flag = True

    # log part
    pprint.pprint(f'{request_type} example')
    pprint.pprint(response.url)
    pprint.pprint(response.status_code)
    pprint.pprint(response.reason)
    pprint.pprint(response.text)
    pprint.pprint(response.json())
    pprint.pprint('**********')
    return response

  def get(self, endpoint, endpoint_id, expected_error=False):
    url = f'{self.base_url}/{endpoint}/{endpoint_id}'
    response = self._request(url, 'GET', expected_error=expected_error)
    return response.json()

  def post(self, endpoint, endpoint_id, body):
    url = f'{self.base_url}/{endpoint}/{endpoint_id}'
    response = self._request(url, 'POST', data=body)
    return response.json()
    
  def delete(self, endpoint, endpoint_id):
    url = f'{self.base_url}/{endpoint}/{endpoint_id}'
    response = self._request(url, 'DELETE')
    return response.json()


BASE_URL_PETSTORE = 'https://petstore.swagger.io/v2'
base_request = BaseRequest(BASE_URL_PETSTORE)

store_data = {
    "id": 1,
    "petId": 1,
    "quantity": 1,
    "shipDate": "2024-11-11T10:00:00.000Z",
    "status": "placed",
    "complete": True
}
create_store = base_request.post('store/order', '', store_data)
pprint.pprint(create_store)

store_info = base_request.get('store/order', 1)
pprint.pprint(store_info)


delete_status = base_request.delete('store/order', 1)
store_info = base_request.get('store/order', delete_status, expected_error=True)
pprint.pprint(store_info)