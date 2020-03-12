#!/usr/bin/python3

import csv, sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="The file to process", required=True)
parser.add_argument("-i", "--sysid", help="System ID to apply changes to", required=True)
parser.add_argument("-a", "--apikey", help="API key to use", required=True)
parser.add_argument("-d", "--debug", action="store_true", help="Debugging output")
parser.add_argument("-s", "--start", type=int, help="Start date in yyyymmdd format")
parser.add_argument("-e", "--end", type=int, help="End date in yyyymmdd format")

args = parser.parse_args()

dailyTotals = defaultdict(dict)

with open(args.file) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line = 0
	for row in csv_reader:
		line += 1
		if row == []:
			continue

		try:
			rowid = row[0]
		except IndexError:
			print("Invalid csv on line %d: %s" % (line, row), file=sys.stderr)
			continue
		
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
				break
			continue


		elif rowid == "300":
			if args.debug:
				print("300: %s" % row, file=sys.stderr)
			rowtype = row[samples + 2]
			if rowtype != "A" and rowtype != "V":
				print("Unhandled 300 type on line %d: %s, %s" % (line, rowtype, row), file=sys.stderr)
			date = int(row[1])
			total = 0
			for sample in range(samples):
				total += int(float(row[2 + sample]) * 1000)
			dailyTotals[date][meter] = total

		elif rowid == "400":
			if args.debug:
				print("400: %s" % row, file=sys.stderr)
			pass

		elif rowid == "500":
			if args.debug:
				print("500: %s" % row, file=sys.stderr)
			pass

		elif rowid == "900":
			meter = ""
			date = ""
			continue

	print('Processed %d lines.' % (line), file=sys.stderr)

	for date in sorted(dailyTotals):
		if(args.start):
			if date < args.start:
				continue
		if(args.end):
			if date > args.end:
				continue
		try:
			exportwh = dailyTotals[date]['B1']
		except KeyError:
			exportwh = 0

		try:
			importwh = dailyTotals[date]['E1']
		except KeyError:
			importwh = 0

		# See https://pvoutput.org/help.html#api-addoutput for the positional parameters
		data = ("%s,,%d,,,,,,,%d,,,," % (date, exportwh, importwh))
		print(data)
