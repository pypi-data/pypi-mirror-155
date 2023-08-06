import json

class Response:

   def __init__(self, params):
      """
      Initialize a Response object
      """
      self.error = params.get('error', True)
      self.success = params.get('success', False)
      self.message = params.get('message', '')
      self.data = params.get('data', None)

   def to_json(self):
      """
      Returns the object in JSON format
      """

      return json.dumps(self.__dict__)
