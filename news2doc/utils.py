import datetime

class ESTTimeZone(datetime.tzinfo):
    def utcoffset(self, dt):
      return datetime.timedelta(hours=+8)

    def dst(self, dt):
        return datetime.timedelta(0)

def yesterday():
	now = datetime.datetime.now()
	yesterday = now - datetime.timedelta(days=1)
	return yesterday
