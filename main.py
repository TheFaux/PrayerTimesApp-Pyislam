from pyIslam.praytimes import PrayerConf, Prayer
from datetime import date, timedelta, datetime

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import GLib as glib


Date = date.today()
Data = {
	'longitude':46.7152,
	'latitude':24.6537,
	'timezone':+3#,
	#angle_ref: ,
	#asr_madhab: ,
	#enable_summer_time:
}

prayers = ['fajr', 'sherook', 'dohr', 'asr', 'maghreb', 'ishaa']

prayersEng = ['Fajr', 'Shrouk', 'Zuhr', 'Asr', 'Maghrib', 'Isha']
prayersAra = ['الفجر', 'الشروق', 'الظهر', 'العصر', 'المغرب', 'العشاء']

prayerNames = prayersAra


def set_now():
	#return "now" var with offset from "Date" var
	return datetime.now().replace(day=Date.day, month=Date.month, year=Date.year)


def set_prayers(prayers):
	#return list of prayertimes
	return [eval('pt.' + prayer + '_time()') for prayer in prayers]


def remainder(prayer_time):
	now = datetime.now()#real current time needed for remainder cauclation
	prayer_datetime = datetime.combine(set_now(), prayer_time)#offset "now" var needed for next-day prayer cauclation

	#calculate positive delta
	invert = now > prayer_datetime
	if invert :
		delta = now - prayer_datetime
	else:
		delta = prayer_datetime - now

	delta -= timedelta(days=delta.days, microseconds=delta.microseconds)#remove microseconds & ±1 days
	return delta


#get prayer times
pc = PrayerConf(**Data)
pt = Prayer(pc, Date)
prayerTimes = set_prayers(prayers)


def time_passed():
	now = set_now()#offset "now" var for compatibility with +day uptime
	#true ishaa prayer has already passed
	return now > datetime.combine(now, prayerTimes[-1])

def load_next():
	#advance to next day

	#grant access to global vars
	global pc, pt, prayerTimes, Date

	#advance day & update vars
	Date = Date + timedelta(days=1)
	pc = PrayerConf(**Data)
	pt = Prayer(pc, Date)
	prayerTimes = set_prayers(prayers)

#prerun day advancement
if time_passed():load_next()


class Main:
	def __init__(self):

		#grab glade file
		gladeFile = "main.glade"
		self.builder = gtk.Builder()
		self.builder.add_from_file(gladeFile)


		#initialize window
		window = self.builder.get_object("Main")
		window.connect("destroy", gtk.main_quit)#implement quit on X button
		window.show()


		#compile prayer name objects list from glade & set names from "prayerNames"
		self.prayerNameObjs = [self.builder.get_object(prayer + "Name") for prayer in prayersEng]
		for indx,obj in enumerate(self.prayerNameObjs): obj.set_text(prayerNames[indx])

		#compile prayer time objects list from glade
		self.TimeObjects = [self.builder.get_object(prayer) for prayer in prayersEng]

		self.getRemainders()

		#grab prayer remainder time & name objects from glade
		self.nextPrayerObj = self.builder.get_object("NP")
		self.nextPrayerRemainderObj = self.builder.get_object("NPR")

		#compile prayer remainder buttons objects list from glade
		self.prayerButtons = [self.builder.get_object(prayer + 'Button') for prayer in prayersEng]
		#implement switching between remainder/time for prayers in time field on click
		for button in self.prayerButtons: button.connect("button-press-event", self.showRemainder)


		self.ButtonDict = dict(zip(self.prayerButtons, self.TimeObjects))



	def setTimes(self):
		for i,obj in enumerate(self.TimeObjects):
			obj.set_text(str(prayerTimes[i]))

	def getRemainders(self):
		now = datetime.now()
		self.prayerRemainders = [remainder(prayer_time) for prayer_time in prayerTimes]
		self.prayerRemainders = ["{}{}".format({True:"+", False:"-"}[now > datetime.combine(now, prayer_time).replace(day=Date.day, month=Date.month, year=Date.year)], str(prayer_remainder)) for prayer_remainder,prayer_time in zip(self.prayerRemainders, prayerTimes)]

	def setRemainders(self):
		self.getRemainders()
		return True#enables repetition with glib.timeout_add_seconds

	def showRemainder(self, widget, event):
		field = self.ButtonDict[widget]
		indx = self.TimeObjects.index(field)
		time = prayerTimes[indx]
		remainder = self.prayerRemainders[indx]

		if '+' in field.get_text() or '-' in field.get_text():
			field.set_text(str(time))
		else:
			field.set_markup("<b>{}</b>".format(remainder))

	def setNextPrayer(self):
		if '+' in self.prayerRemainders[-1]:self.overflow()
		for i,remainder in enumerate(self.prayerRemainders):
			if '-' in remainder:
				self.nextPrayerObj.set_text(prayerNames[i])
				self.nextPrayerRemainderObj.set_markup("<b>{}</b>".format(remainder))
				break
		return True

	def overflow(self):
		load_next()
		self.setTimes()



if __name__ == '__main__':
	main = Main()
	main.setTimes()
	glib.timeout_add_seconds(1, main.setRemainders)#repeat function every 1 second
	glib.timeout_add_seconds(1, main.setNextPrayer)
	gtk.main()
