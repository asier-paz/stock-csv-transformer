import csv
import sys
from datetime import *

filename = ''
SESSIONS = []
FROM = None
UNTIL = None

def transform(diffPeriod):
	global SESSIONS, filename, FROM, UNTIL

	timestamps = []
	prices = []
	differences = []
	for i in range(len(SESSIONS)):
		session = SESSIONS[i]
		close = session['Close']
		timestamps.append(session['Date'].strftime("%Y-%m-%d %H:%M:%S"))
		prices.append(close)

		if i == 0:
			differences.append([''] * len(SESSIONS))
		else:
			diffs = [''] * len(SESSIONS)
			if diffPeriod != None:
				fromDiffIdx = i-diffPeriod-1 if i-diffPeriod-1 > 0 else 0
			else:
				fromDiffIdx = 0

			prevSessionsToDiff = SESSIONS[fromDiffIdx:i]
			c = 0
			for idiff in reversed(range(len(prevSessionsToDiff))):
				prevSession = prevSessionsToDiff[idiff]
				diffs[c] = close / prevSession['Close']
				c = c+1

			differences.append(diffs)

	print("Writing file now: {}".format(filename + '_converted.csv'))
	timestampsWritten = False
	closesWritten = False
	with open(filename + '_converted.csv', mode='w') as csv_file:
		writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		
		if not timestampsWritten:
			writer.writerow(timestamps)
			timestampsWritten = True
		if not closesWritten:
			writer.writerow(prices)
			closesWritten = True
		
		for x in range(len(prices)):
			ls = []
			for y in range(len(differences)):
				ls.append(differences[y][x])
			writer.writerow(ls)

def main():
	global SESSIONS, filename, FROM, UNTIL

	if len(sys.argv) < 2:
		print("You must provide the input CSV file")
		exit(0)

	if len(sys.argv) >= 4:
		try:
			FROM = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
		except ValueError as ve:
			print("If you want to specify a FROM date, you should input the date in the format YYYY-MM-DD")
			exit(-1)
		try:
			UNTIL = datetime.strptime(sys.argv[3], "%Y-%m-%d").date()
		except ValueError as ve:
			print("If you want to specify an UNTIL date, you should input the date in the format YYYY-MM-DD")
			exit(-1)
	
	try:
		filename = sys.argv[1]
		with open(filename, mode='r') as csv_file:
			print("Reading...")
			csv_reader = csv.DictReader(csv_file, delimiter=';')
			for session in csv_reader:
				date = session['Date']
				dt = date.split(' ')
				yr = dt[0][:4]
				mo = dt[0][4:6]
				da = dt[0][6:8]
				hh = dt[1][:2]
				mm = dt[1][2:4]
				ss = dt[1][4:6]
				d = datetime.strptime("{}-{}-{} {}:{}:{}".format(yr, mo, da, hh, mm, ss), "%Y-%m-%d %H:%M:%S")

				if FROM != None and d.date() < FROM:
					continue
				if UNTIL != None and d.date() > UNTIL:
					break

				SESSIONS.append({
					'Date': d,
					'Open': float(session['Open']),
					'High': float(session['High']),
					'Low': float(session['Low']),
					'Close': float(session['Close']),
					'Volume': int(session['Volume']),
				})
	except IOError as e:
		print("Error reading the file: {}".format(e))
		exit(-1)

	transform(sys.argv[4] if len(sys.argv) >= 5 else None)

if __name__ == "__main__":
	main()