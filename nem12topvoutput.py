#!/usr/bin/python3

import csv, sys, argparse, requests
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="The file to process", required=True)
parser.add_argument("-i", "--sysid", help="System ID to apply changes to", required=True)
parser.add_argument("-a", "--apikey", help="API key to use", required=True)
parser.add_argument("-d", "--debug", action="store_true", help="Debugging output")
parser.add_argument("-s", "--start", type=int, help="Start date in yyyymmdd format")
parser.add_argument("-e", "--end", type=int, help="End date in yyyymmdd format")
parser.add_argument("-ip", "--importpeak", help="Import peak register", required=True)
parser.add_argument("-er", "--export", help="Export register", required=True)

args = parser.parse_args()

dailyTotals = defaultdict(dict)

with open(args.file) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line = 0
	processed = 0
	for row in csv_reader:
		line += 1

		if row == []:
			continue

		try:
			rowid = row[0]
		except IndexError:
			print("Invalid csv on line %d: %s" % (line, row), file=sys.stderr)
			break
		
		if rowid == "200":
			if args.debug:
				print("200: %s" % row, file=sys.stderr)
			meter = row[3]
			interval = row[8]
			if interval == "30":
				samples = 48 
			elif interval == "15":
				samples = 96
			else:
				print("Invalid interval on line %d: %s, %s" % (line, interval, row), file=sys.stderr)
				sys.exit(1)
				break
			processed += 1
			continue

		elif rowid == "300":
			date = int(row[1])
			if (args.start and date < args.start) or (args.end and date > args.end):
				skip = True
				continue
			else:
				skip = False
	
			if args.debug:
				print("300: %s" % row, file=sys.stderr)

			rowtype = row[samples + 2]
			if rowtype != "A" and rowtype != "V":
				print("Unhandled 300 type on line %d: %s, %s" % (line, rowtype, row), file=sys.stderr)
				sys.exit(1)
				break

			total = 0
			for sample in range(samples):
				total += int(float(row[2 + sample]) * 1000)
			dailyTotals[date][meter] = total
			processed += 1
			continue

		elif rowid == "400" and not skip:
			if args.debug:
				print("400: %s" % row, file=sys.stderr)
			processed += 1
			continue

		elif rowid == "500" and not skip:
			if args.debug:
				print("500: %s" % row, file=sys.stderr)
			processed += 1
			continue

		elif rowid == "900":
			if args.debug:
				print("900: %s" % row, file=sys.stderr)
			meter = ""
			date = ""
			processed += 1
			continue

	print('Processed %d lines.' % (processed), file=sys.stderr)

	for date in sorted(dailyTotals):
		try:
			exportwh = dailyTotals[date][args.export]
		except KeyError:
			exportwh = 0

		try:
			importwh = dailyTotals[date][args.importpeak]
		except KeyError:
			importwh = 0

		# See https://pvoutput.org/help.html#api-addoutput for the positional parameters
		response = requests.post("https://pvoutput.org/service/r2/addoutput.jsp", 
			params={"data" : "%s,,%d,,,,,,,%d,,,," % (date, exportwh, importwh)},
			headers={"X-Pvoutput-Apikey" : args.apikey, "X-Pvoutput-SystemId" : args.sysid}
		)
		print(response)
