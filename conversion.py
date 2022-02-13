'''
 converts times from h:m:s to float, and float to h:m:s

 ALSO converts data elements to JSON and saves to a file in the ./data folder


#[com dot hotmail @ rlw1138] -- 2020-APR-15
'''
DeBuG = False

import math


def str_to_int(user_input, error_flag=1):
    """
    tries to convert an input string into integer number, round-toward-zero

    """
    try:
        val = int(user_input)
        #"Input is an integer"
        error_flag -= 1
    except ValueError:
        try:
            val = float(user_input)
            #"Input is a float"
            val = int(val) #round down to integer
            error_flag -= 1
        except ValueError:
            # nope, still not a number!
            val=''
            error_flag += 1 #bump up the error flag
    return val, error_flag


def dms_To_float(dms):
    '''
    convert sexagesimal string to float
       format [s]DD:MM
              [s]DD:MM.9999
              [s]DD:MM:SS
              [s]DD:MM:SS.9999
        Sign s is assumed positive if missing
        DD may be indicated with a trailing
          degree symbol or asterisk in place
          of the leftmost colon
    '''
    import re
    d = m = s = 0
    times = re.split('[*°\':"]+', dms)
    if dms == times: return False # there were no separators!
    L = len(times)
    if L > 0 : d = int(times[0])
    if L > 1 :
        if times[1] == '' or times[1] is None:
            m = 0
        else:
            m = float(times[1])
    if L > 2 :
        if times[2] == '' or times[2] is None:
            s = 0
        else:
            s = float(times[2])
    if L > 3 : return False # something has gone very wrong
    if (d < 0 or d > 90 or m < 0 or m > 59.9999 or s < 0 or s > 59.9999): return False
    f = d + m/60.0 + s/360.0
    return f


def hms_To_float(hms):
    '''
    convert sexagesimal string to float
       format HH:MM
              HH:MM.9999
              HH:MM:SS
              HH:MM:SS.9999
    '''
    h = m = s = 0
    times = hms.split(':')
    if hms == times: return False # there were no ':'
    L = len(times)
    if L > 0 : h = int(times[0])
    if L > 1 :
        if times[1] == '' or times[1] is None:
            m = 0
        else:
            m = float(times[1])
    if L > 2 :
        if times[2] == '' or times[2] is None:
            s = 0
        else:
            s = float(times[2])
    if L > 3 : return False # something has gone very wrong
    if (h < 0 or h > 23 or m < 0 or m > 59.9999 or s < 0 or s > 59.9999): return False
    f = h + m/60.0 + s/360.0
    return f


def float_To_hms(f, p):
    '''
    convert float to sexagesimal string ( sHH:MM:SS.ssss )

    '''
    DeBuG = False
    h1 = m1 = f1 = s1 = sd = 0.0
    # round to 0.00005 second or 0.5 second, depending on precision
    if p == 'PRECISION_HIGHEST':
        f1 = abs(f) + 0.0000000139
    else: # PRECISION_HIGH
        f1 = abs(f) + 0.000139
    h1 = math.floor(f1)                    # hours from the integer part
    m1 = (f1 - h1) * 60.0                # minutes from the decimal part x 60 minutes
    s1 = (m1 - math.floor(m1)) * 60.0    # seconds from the remainder of the minutes x 60
    if p == 'PRECISION_HIGHEST':
        sd = (s1 - math.floor(s1)) * 10000.0
        s = "{}{:02d}:{:02d}:{:02d}.{:04d}"
    elif p == 'PRECISION_HIGH':
        s = "{}{:02d}:{:02d}:{:02d}"
    elif p == 'PRECISION_LOW':
        s1 = s1 / 6.0
        s = "{}{:02d}:{:02d}.{:1d}"
    # set sign and return result string
    if (f < 0.0 and (sd != 0 or s1 != 0 or m1 != 0 or h1 != 0)):
        sign = "-"
    else:
        sign = "+"
    if DeBuG:
        print('   s ' + str(s))
        print('sign ' + str(sign))
        print('  h1 ' + str(h1))
        print('  m1 ' + str(m1))
        print('  s1 ' + str(s1))
        print('  sd ' + str(sd))
    if p == 'PRECISION_HIGHEST':
        string = s.format(sign, int(h1), int(m1), int(s1), int(sd))
    else:
        string = s.format(sign, int(h1), int(m1), int(s1))
    return string


def validate_dms(dms):
    '''
    validate sexagesimal string
       format [s]DD:MM
              [s]DD:MM.9999
              [s]DD:MM:SS
              [s]DD:MM:SS.9999
        Sign s is assumed positive if missing
        DD may be indicated with a trailing
          degree symbol or asterisk in place
          of the leftmost colon

        Imperfections are corrected before returning
        Float or String. The correction may simply be
        replacing the bad value with zeroes.

        Completely fubar input returns False

    '''
    import re
    d = m = s = 0
    times = re.split('[*°\':"]+', dms)
    if dms == times: return False # there were no separators!
    L = len(times)
    if L > 0 :
        try:
            d = int(times[0])
        except ValueError:
            return False
        if ( d < -90 or d > 90 ): return False
    if L > 1 :
        if times[1] == '' or times[1] is None:
            m = 0
        else:
            try:
                m = float(times[1])
                if m == int(m): m = int(m)
                if (m<0 or m>59.9999 ): return False
            except ValueError:
                m = str(m)
    if L > 2 :
        if times[2] == '' or times[2] is None:
            s = 0
        else:
            try:
                s = float(times[2])
                if s == int(s): s=int(s)
                if (s<0 or s>59.9999 ): return False
            except ValueError:
                s = str(s)
    if L > 3 : return False # something has gone very wrong
    ## print('d{}d m{}m s{}s'.format(d, m, s))
    if '.' in str(m) or '.' in str(s) : # found a decimal place
        f = d + m/60.0 + s/360.0
        return f # return the floating-point representation
    else: # neither M nor S has decimals
        M = str(m).zfill(2) # force to two digits
        S = str(s).zfill(2) # force to two digits
        V = '{}*{}:{}'.format(d,M,S)
        return V


def validate_hms(hms):
    '''
    convert sexagesimal string to float
       format HH:MM
              HH:MM.9999
              HH:MM:SS
              HH:MM:SS.9999

        Imperfections are corrected before returning
        Float or String. The correction may simply be
        replacing the bad value with zeroes.

        Completely fubar input returns False


    '''
    h = m = s = 0
    times = hms.split(":")
    if hms == times: return False # there were no separators!
    L = len(times)
    if L > 0 :
        try:
            h = int(times[0])
        except ValueError:
            return False
        if (h<0 or h>23): return False
    if L > 1 :
        if times[1] == '' or times[1] is None:
            m = 0
        else:
            try:
                m = float(times[1])
                if m == int(m): m = int(m)
                if (m<0 or m>59.9999 ): return False
            except ValueError:
                m = str(m)
    if L > 2 :
        if times[2] == '' or times[2] is None:
            s = 0
        else:
            try:
                s = float(times[2])
                if s == int(s): s=int(s)
                if (s<0 or s>59.9999 ): return False
            except ValueError:
                s = str(s)
    if L > 3 : return False # something has gone very wrong
    ## print('h{}h m{}m s{}s'.format(h, m, s))
    if '.' in str(m) or '.' in str(s) : # found a decimal place
        f = h + m/60.0 + s/360.0
        return f # return the floating-point representation
    else: # neither M nor S has decimals
        M = str(m).zfill(2) # force to two digits
        S = str(s).zfill(2) # force to two digits
        V = '{}:{}:{}'.format(h,M,S)
        return V











import json

def conversion_test():
    """test stuff"""
    print('\n\n')

    data = { "x": 12153535.232321, "y": 35234531.232322 }

    #this over-writes the file each time it's called
    file = open('./app/data/OnStep_json-dump.json', 'w+')

    json.dump(data, file)
    print('test data dumped to file: {}'.format( file.name ))
    print()

    #Reading back from a file
    file = open('./app/data/OnStep_json-dump.json', 'r')
    print('test data read from file: {}'.format( file.name ))
    print(json.load(file))
    print()

    file.close()
    '''
Note Unlike pickle and marshal, JSON is not a framed protocol, so trying to serialize multiple objects with repeated calls to dump() using the same filepointer will result in an invalid JSON file.
    '''
    more_data = { "object": "Alkaid" }

    #  NOTE NEW FILENAME
    file = open('./app/data/OnStep_object.json', 'w')

    json.dump(more_data, file)
    print('test data dumped to file: {}'.format( file.name ))
    print()

    #Reading back from file
    file = open('./app/data/OnStep_object.json', 'r')
    print('test data read from file: {}'.format( file.name ))
    print(json.load(file))
    print()

    file.close()


    #If you want to get a simple string back instead of dumping it to a file, you can use json.dumps() instead:

    print('json.dumps output: {}"'.format( json.dumps({ "x": 12153535.232321, "y": 35234531.232322 }) ))
    print()


if __name__ == "__main__":
    conversion_test()
