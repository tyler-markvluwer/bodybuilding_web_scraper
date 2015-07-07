from bs4 import BeautifulSoup
import requests
from Exercise import Exercise

def strip_non_numbers(in_string, occurence=0):
	numbers = [int(char) for char in in_string if char.isdigit()]
	return numbers[occurence]

punctuation = ['.', ',', '!']

class JayCutlerWorkout(object):
	def __init__(self, url):
		r  = requests.get(url)
		data = r.text
		self.soup = BeautifulSoup(data, "html.parser")

		self.title = self._get_title()
		self.exercise_list = []
		self._get_exercise_info()

	def _get_title(self):
		for header in self.soup.find_all('div', class_='workout-header-blue'):
			return header.text

	def _get_exercise_info(self):
		for list_ in self.soup.find_all('ul', class_='defined'):
			for list_item in list_.find_all('a'):
				if not len(list_item.text):
					continue

				exercise_name = self._parse_name(list_item.text)
				exerse = Exercise(exercise_name)
				self.exercise_list.append(exerse)

			i = 0
			for desc in list_.find_all('span', class_='mpt-content content'):
				sets = self._parse_sets(desc.text)
				reps = self._parse_reps(desc.text)
				# print "sets: %s reps: %s" % (sets, reps)

				self.exercise_list[i].set_sets(sets)
				self.exercise_list[i].set_reps(reps)
				i += 1

		for exercise in self.exercise_list:
			print exercise.to_string()

	def _parse_name(self, in_string):
		return in_string.strip()
		
	def _parse_sets(self, in_string):
		in_string = ''.join([char for char in in_string if char not in punctuation])
		split_text = in_string.split(' ')
		try:
			set_index = split_text.index('sets')
		except:
			set_index = split_text.index('set')

		sets = strip_non_numbers(split_text[set_index - 1])
		return sets

	def _parse_reps(self, in_string):
		in_string = ''.join([char for char in in_string if char not in punctuation])
		split_text = in_string.split(' ')
		try:
			reps_index = split_text.index('rep')
		except:
			reps_index = split_text.index('reps')

		reps = split_text[reps_index - 1]
		return reps


	def to_json(self):
		
