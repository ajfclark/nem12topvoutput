# NEM12toPVoutput

This is a quick utility to take teh import and export kWh figures from a NEM12 file and feed them in to PVOutput for dates that already have generation figures present.

NEM12 specification used: https://www.aemo.com.au/-/media/Files/Electricity/NEM/Retail_and_Metering/Metering-Procedures/2018/MDFF-Specification-NEM12--NEM13-v106.pdf

## Usage:

`nem12topvoutput.py [-h] -f FILE -i SYSID -a APIKEY -ip IMPORTPEAK -er EXPORT [-d] [-s START] [-e END]`

## Required switches:
* `-f FILE, --file FILE`: The NEM12 csv file to process
* `-i SYSID, --sysid SYSID`: System ID to apply changes to
* `-a APIKEY, --apikey APIKEY`: API key to use
* `-ip IMPORTPEAK, --importpeak IMPORTPEAK`: Import peak register name in the NEM12 file, e.g. E1
* `-er EXPORT, --export EXPORT`: Export register name, e.g. B1

## Optional switches:
* `-s START, --start START`: Start date in yyyymmdd format
* `-e END, --end END`: End date in yyyymmdd format
* `-d, --debug`: Debugging output

## Example:
I've downloaded my NEM12 file from Powercor on the 2020-03-13 and want to load in all the data in the file from the 2020-03-10 onwards:
```
$ ./nem12topvoutput.py -f 20180313_20200313_POWERCOR_DETAILED.csv -s 20200310 -ip E1 -er B1 -a [apikey] -i 61698
Processed 8 lines.
20200310: <Response [200]>
20200311: <Response [200]>
```
