import datetime


def get_date_from_short_form_and_unix_time(hrs=5, mins=30):
	total_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=hrs, minutes=mins), "IST"))
	format_time = total_time.strftime("%a, %#d %B %Y %#I:%M %p")
	auto_time = datetime.datetime(year=total_time.year, month=total_time.month, day=total_time.day, hour=total_time.hour, minute=total_time.minute, second=total_time.second)
	return auto_time, format_time, auto_time.timestamp()
