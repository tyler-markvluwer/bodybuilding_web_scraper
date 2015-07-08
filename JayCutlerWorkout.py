from bs4 import BeautifulSoup
import requests
from Exercise import Exercise
import json

def strip_non_numbers(in_string, occurence=0):
	print in_string
	numbers = [int(char) for char in in_string if char.isdigit()]
	return numbers[occurence]

punctuation = ['.', ',', '!']

class JayCutlerWorkout(object):
	def __init__(self, url, day):

		r  = requests.get(url)
		data = r.text
		self.soup = BeautifulSoup(data, "html.parser")

		self.day = day
		self.title = self._get_title().encode('ascii', 'ignore')
		self.exercise_list = []
		self._get_exercise_info()

	def _get_title(self):
		for header in self.soup.find_all('div', class_='workout-header-blue'):
			return header.text

		return "Day {day}: Rest".format(day=self.day)

	def _get_exercise_info(self):
		exercise_box = self.soup.find(id='meal-plan-table')

		try:
			list_ = exercise_box.find('ul')
		except:
			# Most likely a rest day. Can't get info!
			return

		for list_item in list_.find_all('a'):
			if not len(list_item.text):
				continue

			exercise_name = self._parse_name(list_item.text)
			exerse = Exercise(exercise_name)
			self.exercise_list.append(exerse)

		i = 0
		for desc in list_.find_all('span', class_='mpt-content content'):
			self.exercise_list[i].set_description(desc.text.strip())

			sets = self._parse_sets(self.exercise_list[i].desc)
			reps = self._parse_reps(desc.text)
			# print "sets: %s reps: %s" % (sets, reps)

			self.exercise_list[i].set_sets(sets)
			self.exercise_list[i].set_reps(reps)

			i += 1

	def _parse_name(self, in_string):
		return in_string.strip()
		
	def _parse_sets(self, in_string):
		split_string = in_string.split(' ')
		for split in split_string:
			if split[0].isdigit():
				return split

		return None

		# try:
		# 	set_index = split_text.index('sets')
		# except:
		# 	set_index = split_text.index('set')

		# sets = strip_non_numbers(split_text[set_index - 1])
		# return sets

	def _parse_reps(self, in_string):
		in_string = ''.join([char for char in in_string if char not in punctuation])
		split_text = in_string.split(' ')
		try:
			reps_index = split_text.index('rep')
		except:
			try:
				reps_index = split_text.index('reps')
			except:
				return None

		reps = split_text[reps_index - 1]
		return reps

	def to_dict(self):
		exercises = [exc.to_dict() for exc in self.exercise_list]
		
		return {
			'workout_name': self.title,
			'exercises': exercises
		}

	def to_json(self, fp):
		to_dict = self.to_dict()

		with open(fp, 'w') as outfile:
			json.dump(to_dict, outfile, indent=4, separators=(',', ': '), ensure_ascii=False)

	def to_coffee(self, fp):
		to_dict = self.to_dict()

		file_contents = "day{day_num} = {file_contents}\n\nmodule.exports = day{day_num}".format(
			day_num=self.day,
			file_contents=str(to_dict).encode('ascii', 'ignore'),
		)

		with open(fp, 'w') as outfile:
			outfile.write(file_contents)



