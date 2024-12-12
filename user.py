import requests
import pprint


class BaseRequest:
  def __init__(self, base_url):
    self.base_url= base_url

  def _request(self, url, request_type, data=None, expected_error=False):
    stop_flag = False
    while not stop_flag:
      if request_type =='GET':
        response = requests.get(url)
      elif request_type =='POST':
        response = requests.post(url, json=data)
      elif request_type =='PUT':
        response = requests.put(url, json=data)
      else:
        response = requests.delete(url)
      if not expected_error and response.status_code==200:
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
    response = self._request(url,'GET', expected_error=expected_error)
    return response.json()

  def post(self, endpoint, endpoint_id, body):
    url = f'{self.base_url}/{endpoint}/{endpoint_id}'
    response = self._request(url,'POST', data=body)
    return response.json()['message']

  def put(self, endpoint, endpoint_id, body):
    url = f'{self.base_url}/{endpoint}/{endpoint_id}'
    response = self._request(url,'PUT', data=body)
    return response        

  def delete(self, endpoint, endpoint_id):
    url = f'{self.base_url}/{endpoint}/{endpoint_id}'
    response = self._request(url,'DELETE')
    return response.json()['message']

BASE_URL_PETSTORE='https://petstore.swagger.io/v2'
base_request = BaseRequest(BASE_URL_PETSTORE)

user_data = {"id":1,"username":"someName","firstName":"someFirstName","lastName":"someLastName","email":"someEmail@.com","password":"somePassword","phone":"123456789","userStatus":1}
create_user = base_request.post('user','', user_data)

user_info = base_request.get('user','someName')
pprint.pprint(user_info)

update_data ={"id":1,"username":"someName","firstName":"someFirstNameNEW","lastName":"someLastName","email":"someEmail@.com","password":"somePassword","phone":"123456789","userStatus":1}
update_user = base_request.put('user','someName', update_data)

delete_status = base_request.delete('user','someName')
user_info = base_request.get('user', delete_status, expected_error=True)
