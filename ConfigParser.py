import json

class ConfigParser():

	def __init__(self, configSource):
		self.config = configSource
		json_file = open(configSource).read()

		self.data = json.loads(json_file)

	def host(self):
		return self.data["host"]

	def user(self):
		return self.data["user"]

	def password(self):
		return self.data["password"]

	def port(self):
		return self.data["port"]