class Model:
	unique_id = 0
	models = {}

	def __init__(self, **kwargs):
		self.values = kwargs
		self.unique_id = Model.createNewModel()

	def addValue(self, valueDict: dict):
		self.values[valueDict['name']] = valueDict

	@classmethod
	def createNewModel(cls, model):
		cls.unique_id += 1
		cls.models[cls.unique_id] = model

		return cls.unique_id