import model

class User(model.Model):
	def __init__(self):
		super().__init__()

		self.addValue({
			'name': 'Username',
			'type': str,
			'none': False
		})

		self.addValue({
			'name': 'Password',
			'type': str,
			'none': False,
			'secret': True
		})

		self.addValue({
			'name': 'Posts',
			'type': dict,
			'none': True,
			'default': {}
		})

class Post(model.Model):
	def __init__(self):
		super().__init__()

		self.addValue({
			'name': 'Name',
			'type': str,
			'none': False
		})

		self.addValue({
			'name': 'Author',
			'type': dict,
			'none': False
		})

		self.addValue({
			'name': 'Body',
			'type': str,
			'none': False
		})

		self.addValue({
			'name': 'Comments',
			'type': [],
			'none': True
		})

class Comment(model.Model):
	def __init__(self):
		super().__init__()

		self.addValue({
			'name': 'Name',
			'type': str,
			'none': False
		})

		self.addValue({
			'name': 'Author',
			'type': str,
			'none': False
		})

		self.addValue({
			'name': 'Body',
			'type': str,
			'none': False
		})