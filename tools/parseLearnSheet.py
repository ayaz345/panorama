import csv
import requests

CSV_FILE = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTlH08v-dqtGl49T0Eslb56o-Y-xp6kOwhEo4Bwx387AxbpGHFw7AUBeBQMQdwEBI9g4gBBnGmUZ5EW/pub?output=csv'

learnDataMap = {}
reader = csv.DictReader(requests.get(CSV_FILE).text.splitlines())
for row in reader:
	if row['Shippable'] != 'TRUE':
		continue
	if row['Mode'] in learnDataMap:
		learnDataMap[row['Mode']].append(row)
	else:
		learnDataMap[row['Mode']] = [row]

with open( '../data/learn.vdf', 'w' ) as output:
	output.write( '"Learn"\n' )
	output.write( '{\n' )
	for mode, modeData in sorted(learnDataMap.items()):
		output.write(f'\t"{mode}"\n')
		output.write('\t{\n')
		for card_index, data in enumerate(modeData, start=1):
			output.write(f'\t\t"{mode}{card_index}"\n')
			output.write( '\t\t{\n' )
			for key, value in data.items():
				if key == 'Shippable':
					continue
				output.write( '\t\t\t"{}"\t"{}"\n'.format(key, str(value).replace('"', '\'')) )
			output.write( '\t\t}\n' )
		output.write('\t}\n')
	output.write('}')