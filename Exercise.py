
class Exercise(object):
	def __init__(self, name, sets=None, reps=None):
		self.name = name
		self.sets = sets
		self.reps = reps

	def set_sets(self, sets):
		self.sets = sets

	def set_reps(self, reps):
		self.reps = reps

	def to_string(self):
		return "\nname: {name} \nsets: {sets} \nreps: {reps}".format(
			name=self.name,
			sets=self.sets,
			reps=self.reps,
		)
