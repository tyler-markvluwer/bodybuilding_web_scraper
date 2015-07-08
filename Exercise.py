
class Exercise(object):
	def __init__(self, name, sets=None, reps=None, desc=None):
		self.name = name.encode('ascii', 'ignore')
		self.sets = sets
		self.reps = reps
		self.desc = desc

	def set_sets(self, sets):
		self.sets = sets

	def set_reps(self, reps):
		self.reps = reps

	def set_description(self, desc):
		i = 0
		for char in desc:
			if char.isdigit():
				index = i
				break

			i += 1

		try:
			desc = desc[:i] + ' ' + desc[i:]
		except:
			desc = desc

		self.desc = desc.encode('ascii', 'ignore')

	def to_string(self):
		return "\n{desc}\nname: {name} \nsets: {sets} \nreps: {reps}".format(
			desc=self.desc,
			name=self.name,
			sets=self.sets,
			reps=self.reps,
		)

	def split_range(self, range_string):
		if range_string:
			split = range_string.split('-')
			if len(split) > 1:
				min_ = int(split[0])
				max_ = int(split[1])

			else:
				min_ = int(split[0])
				max_ = int(split[0])
		else:
			min_ = None
			max_ = None

		return min_, max_

	def to_dict(self):
		reps_min, reps_max = self.split_range(self.reps)
		sets_min, sets_max = self.split_range(self.sets)

		return {
			'name': self.name,
			'sets': sets_max,
			'sets_min': sets_min,
			'sets_max': sets_max,
			"reps_min": reps_min,
			'reps_max': reps_max,
			'rest': 60,
			'desc': self.desc
		}
