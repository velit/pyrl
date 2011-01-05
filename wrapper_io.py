class Wrapper():
	_inst = None

	def __getattr__(self, name):
		return getattr(Wrapper._inst, name)

	def __setattr__(self, name, value):
		return setattr(Wrapper._inst, name, value)

	def __delattr__(self, name):
		return delattr(Wrapper._inst, name, value)
