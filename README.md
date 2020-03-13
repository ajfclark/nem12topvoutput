# NEM12toPVoutput

usage: nem12topvoutput.py [-h] -f FILE -i SYSID -a APIKEY [-d] [-s START]
						  [-e END] -ip IMPORTPEAK -er EXPORT

## Required switches:
### -f FILE, --file FILE
The NEM12 csv file to process

### -i SYSID, --sysid SYSID
System ID to apply changes to

### -a APIKEY, --apikey APIKEY
API key to use

### -ip IMPORTPEAK, --importpeak IMPORTPEAK
Import peak register (E1)

### -er EXPORT, --export EXPORT
Export register (B1)

## Optional switches:
### -s START, --start START
Start date in yyyymmdd format

### -e END, --end END
End date in yyyymmdd format

### -d, --debug
Debugging output
