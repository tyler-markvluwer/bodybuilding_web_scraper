from JayCutlerWorkout import JayCutlerWorkout
import json

# for i in range(35, 56):
# 	print "day: {day}".format(day=i)
# 	url = "http://www.bodybuilding.com/fun/living-large-jay-cutlers-8-week-mass-building-trainer-day-{day}.html".format(day=i)

# 	JayCutlerWorkout(url)

FOLDER_NAME = 'workouts'
MAX_DAYS = 57

for i in xrange(34, MAX_DAYS):
	print "day: {day}".format(day=i)

	url = "http://www.bodybuilding.com/fun/living-large-jay-cutlers-8-week-mass-building-trainer-day-{day}.html".format(day=i)
	jay_workout = JayCutlerWorkout(url, i)

	fp = '{direc}/day{day_num}.coffee'.format(
		direc=FOLDER_NAME,
		day_num=i,
	)

	jay_workout.to_coffee(fp)
