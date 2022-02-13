'''
# displays a listing of stars brighter than Magnitude 3,
# which are currently between 5 hours East and 5 hours West
#   to be used for MOUNT ALIGNMENT

#[com dot hotmail @ rlw1138] -- 2020-APR-15
'''
import sys
# import libraries -- note Class DateTime is distinct from Modeule datetime
# CLASSES
from datetime import datetime as DateTime, timedelta as TimeDelta, date as Date
# MODULES
import datetime

DeBuG = False

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

#     ALIGNMENT STARS DATA FILE

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

# save alternate datasets in a '.py' file in the 'data' folder
import importlib
AlignStarData = 'data.bright_align_stars' # for the N-Star Align
ALIGNSTARDATA = importlib.import_module(AlignStarData)
#print('CONFIG(star data: '+str(len(ALIGNSTARDATA.stars))+ ' rows)')

HMS = '%H:%M:%S'

PRINT_HEADER = True
STARCOUNT = len(ALIGNSTARDATA.stars)
OUTPUT_TEXT = ''

# figure out where 06:00 and 18:59 are located in the data
early_Cutoff = late_Cutoff = ''
num = 0
for star in ALIGNSTARDATA.stars:
    num += 1
    if early_Cutoff == '' and star[3] > '05:59:59':
        early_Cutoff = num
    if late_Cutoff == '' and star[3] >= '18:59:59':
        late_Cutoff = num - 1
if DeBuG: print('early: %s -- late: %s' % (str(early_Cutoff), str(late_Cutoff) ) )


def header():
    '''column titles for align_stars list'''
    txt = '{0:>4}) {1:^8}{2:^15}{3:^11} {4:^11}{5}   {6}\n'
    separator = ' - - | - - - | - - - - - - -| - - - - - | - - - - - - - - - - - - -'
    buf = separator + '\n'
    buf += txt.format( 'num', 'bayer', 'name', 'r/a', 'dec', 'Vmag', 'offset' )
    buf += separator + '\n'
    return buf


def scan_late(LST, maxlat, minlat):
    '''scans stars[] for align stars after late_cutoff time
    if LST < 6 scan R/A's 19:00 thru 23:59'''
    valid_stars = list()
    num = 0
    for star in ALIGNSTARDATA.stars:
        num += 1
        if num < late_Cutoff: continue
        valid_stars.append( test_star(LST, maxlat, minlat, num, star, type=2) )
    return valid_stars


def scan_normal(LST, maxlat, minlat):
    ''' if LST >= 06:00 and <= 18:00 just scan thru stars[] data start-to-finish '''
    valid_stars = list()
    num = 0
    for star in ALIGNSTARDATA.stars:
        num += 1
        valid_stars.append( test_star(LST, maxlat, minlat, num, star, type=0) )
    return valid_stars


def scan_early(LST, maxlat, minlat):
    '''scans stars[] for align stars before early_cutoff time
    if LST > 18 scan R/A's 00:00 thru 04:59 '''
    valid_stars = list()
    num = 0
    for star in ALIGNSTARDATA.stars:
        num += 1
        if num > early_Cutoff: continue
        valid_stars.append( test_star(LST, maxlat, minlat, num, star, type=1) )
    return valid_stars


def test_star(LST, maxlat, minlat, num, star, type):
    ''' find stars where Dec is within 75 degrees of our latitude '''
    de = star[4]
    iDec = de.split('*') # degrees only
    iDec = int(iDec[0])

    if maxlat > iDec and iDec > minlat:
        ''' find stars within +/- 5 hours of our longitude (LST)'''
        # Five hours of R/A is equivalent to 75 degrees of DEC
        ra = star[3]
        RA = ra.split(':')
        minute = int(RA[1])
        RA = int(RA[0])

        if type == 0:
            tdelta = LST - RA

        elif type == 1 and LST > 18:
            tdelta = (LST-24) - RA
#            tdelta = ((RA+24) - LST)*-1

        elif type == 2 and LST < 6:
            tdelta = LST - (RA-24)
#            tdelta = (RA - (LST+24))*-1

        # Five hours of R/A
        if abs(tdelta) <= 5:
            name1 = star[0]
            name2 = star[1]
            mag = round(star[2])
            if mag < 1:
                mag = '-' + str(abs(mag))
            if name2.startswith('Polaris'):
                offset = 'Pole Star'
            elif tdelta <= -1:
                offset = str(abs(tdelta)) + ' hour W'
            elif tdelta >=  1:
                offset = str(abs(tdelta)) + ' hour E'
            else:
                offset = 'near meridian'

            txt = '{0:>4}) {1:<8}{2:<15}{3:>11} {4:>11} {5:>2} ~ {6}\n'
            #print(txt.format( str(num), name1, name2, ra, de, mag, offset ))
            global OUTPUT_TEXT
            OUTPUT_TEXT += txt.format( num, name1, name2, ra, de, mag, offset )
            return str(num)


# START HERE


def align_stars( lst='', lat='', heading=None):
    """generates a list of stars within 75* of current location at the current time"""
    global OUTPUT_TEXT
    all_valid_stars = list()


    # get OnStep's Local Sidereal Time [ie: R/A of Zenith]
    if DeBuG is False: strLST = lst
    if heading: OUTPUT_TEXT += '\n        Local Sidereal Time: ' + strLST + ' - (r/a of your zenith)\n\n'
    LST = DateTime.strptime(strLST, HMS)

    # for current 'site', get latitude [declination of Zenith],
    # set Min and Max degrees to no more than 75 degrees difference
    # (to allow for obstructions on the horizon)
    #

    lat = lat.split('*') # degrees only
    lat = int(lat[0])
    maxlat = lat + 75
    if maxlat > 90: maxlat = 90
    minlat = lat - 75
    if minlat < -90: minlat = -90
    if DeBuG:
        print('lat: %s  --  max: %s  --  min: %s' %(lat, str(maxlat), str(minlat)))
        #sys.exit('stopping')
    #
    # The Bright Stars data file is ordered by R/A from 00:00 to 23:59
    #   so the "visible stars" listing displays in order from East to West:
    #
    # if the Local Sidereal Time is between 06:00 and 18:59, we can just
    #   scan through the whole list beginning-to-end
    #
    # if the LST is before 06:00 we first need to scan the last 5 hours
    #   of the list and then come back and scan from the beginning
    #
    # if the LST is after 18:59 we need the scan the whole list (skipping
    #   over the first 5 hours) and then come back and scan the first 5 hours
    #

    LST = strLST.split(':')
    LST = int(LST[0])
    tmp=""

    if heading: tmp = header()
    OUTPUT_TEXT += tmp

    if LST < 6:
        # need to scan last 5 hrs of list first
        all_valid_stars.extend( scan_late(LST, maxlat, minlat) )
        all_valid_stars.extend( scan_normal(LST, maxlat, minlat) )

    elif LST > 18:
        all_valid_stars.extend( scan_normal(LST, maxlat, minlat) )
        # need to scan first 5 hrs of list
        all_valid_stars.extend( scan_early(LST, maxlat, minlat) )

    else:
        all_valid_stars.extend( scan_normal(LST, maxlat, minlat) )

    if heading: tmp = header()
    OUTPUT_TEXT += tmp

    #pager(OUTPUT_TEXT)
    return OUTPUT_TEXT
    #return all_valid_stars

if __name__ == "__main__":
    align_stars()
