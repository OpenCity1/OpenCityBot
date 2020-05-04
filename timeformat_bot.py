import datetime


def get_date_from_short_form_and_unix_time(short_time="0M", hrs=5, mins=30):
	today_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=hrs, minutes=mins), "UTC"))
	cond1 = ("M" if "M" == short_time[1:] else "Y" if "Y" == short_time[1:] else "D" if "D" == short_time[1:] else "H" if "H" == short_time[1:] else "MO" if "MO" == short_time[
	                                                                                                                                                                 1:] else "S") if short_time[
	                                                                                                                                                                                  1:] in [
		                                                                                                                                                                                  'M',
		                                                                                                                                                                                  'D',
		                                                                                                                                                                                  'Y',
		                                                                                                                                                                                  'H',
		                                                                                                                                                                                  'MO',
		                                                                                                                                                                                  'S'] else (
		"m" if "m" == short_time[1:] else "y" if "y" == short_time[1:] else "d" if "d" == short_time[1:] else "h" if "h" == short_time[1:] else "mo" if "mo" == short_time[
		                                                                                                                                                        1:] else "s")
	cond2 = (2592000 if "M" == short_time[1:] else 31556952 if "Y" == short_time[1:] else 86400 if "D" == short_time[1:] else 3600 if "H" == short_time[
	                                                                                                                                         1:] else 60 if "MO" == short_time[
	                                                                                                                                                                1:] else 1) if short_time[
	                                                                                                                                                                               1:] in [
		                                                                                                                                                                               'M',
		                                                                                                                                                                               'D',
		                                                                                                                                                                               'Y',
		                                                                                                                                                                               'H',
		                                                                                                                                                                               'H',
		                                                                                                                                                                               'MO',
		                                                                                                                                                                               'S'] else (
		2592000 if "m" == short_time[1:] else 31556952 if "y" == short_time[1:] else 86400 if "d" == short_time[1:] else 3600 if "h" == short_time[
		                                                                                                                                1:] else 60 if "mo" == short_time[
		                                                                                                                                                       1:] else 1)
	seconds = int(short_time.strip(cond1)) * int(cond2)
	after_time = datetime.timedelta(seconds=seconds)
	total_time = today_time + after_time
	format_time = total_time.strftime("%a, %#d %B %Y %#I:%M %p")
	auto_time = datetime.datetime(year=total_time.year, month=total_time.month, day=total_time.day, hour=total_time.hour, minute=total_time.minute, second=total_time.second)
	return auto_time, format_time, auto_time.timestamp()
