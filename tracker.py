# TRACK STATS

class Tracker:
	def __init__(self):
		self.att_count = 0
		self.email_count = 0
		self.regulars = 0
		self.reappears = 0
		self.unidentified = 0

	def print(self):
		print()
		print(f'Downloaded {self.att_count} attachments from {self.email_count} emails')
		print()
		print(f'{self.regulars} Regulars')
		print(f'{self.reappears} Reappears')
		print(f'{self.unidentified} Unidentified')
		print()