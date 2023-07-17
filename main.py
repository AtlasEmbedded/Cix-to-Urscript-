import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

BEGIN_CODE = 'BEGIN'
END_CODE = 'END'
MAINDATA = 'MAINDATA'
MACRO = 'MACRO'          #variables to be used in parsing the file
DRILL_ID = 'BV'
DIA = 'DIA'
DRILL_DIA = 8.0

directory = config['Directory']['Path']

def find_file(cixfile):
    for filename in os.listdir(directory):
        if filename == cixfile:
            print(f"File found: {cixfile}")

            config['CIX']['file'] = str(cixfile)
            with open ('config.ini', 'w') as configfile:
                config.write(configfile)
            return filename
    else:
        # If no file is found
        print("File not found")
        return 'file not found'
        
cixfile = config['CIX']['file']

def parseSection(cixfile):
    key = ''
    content = ''
    results = []
    with open (cixfile, 'r') as file:
        for line in (line.lstrip().rstrip() for line in file):
            if (line.startswith(BEGIN_CODE)):
                key = line[6:]
                content = []
            elif (line.startswith(END_CODE)):
                results.append([key, content])
            else:
                content.append(line)
    return results

def parseMaindata(maindata):
    for section in maindata:
        if (section[0] == MAINDATA):
            LPX = 0
            LPY = 0
            LPZ = 0
            for lineSplit in (line.split("=") for line in section[1]):
                if (lineSplit[0] == 'LPX'):
                    LPX = lineSplit[1]
                if (lineSplit[0] == 'LPY'):
                    LPY = lineSplit[1]
            for lineSplit in (line.split("=") for line in section[1]):
                if (lineSplit[0] == 'LPZ'):
                    LPZ = lineSplit[1]
                    URZdown = str(float(LPZ) / 1000)              # converts z to mm and is used for the UR script
                    URZup = str(float(LPZ) / 1000 + 0.1)          # takes the z value in mm and adds 0.1mm to it
                    config['ToolOffset']['URZdown'] = str(URZdown)
                    config['ToolOffset']['URZup'] = str(URZup)
                    config['WorkPiece']['LPX'] = str(LPX)
                    config['WorkPiece']['LPY'] = str(LPY)
                    config['WorkPiece']['LPZ'] = str(LPZ)
                    with open ('config.ini', 'w') as configfile:
                        config.write(configfile)
            return [URZdown, URZup, LPX, LPY, LPZ]

def parseDrill(drillData):
    result = []
    for section in drillData:
        if (section[0] == MACRO):
            if (section[1][0].split("=")[1] == DRILL_ID):
                found = False
                drill_x = 0
                drill_y = 0
                for line in (line.split(',') for line in section[1][1:]):
                    if (len(line) == 3 and line[1].split('=')[1] == 'X'):
                        drill_x = float(line[2].split('=')[1])
                    if (len(line) == 3 and line[1].split('=')[1] == 'Y'):
                        drill_y = float(line[2].split('=')[1])
                    if (len(line) == 3 and line[1].split('=')[1] == DIA and float(line[2].split('=')[1]) == DRILL_DIA):
                        found = True
                if (found):
                    result.append([drill_x, drill_y])
    return result

def WriteConfig():
    for i, lst in enumerate(parseDrill(parseSection(cixfile))):
        key = f'Point{i + 1}'
        value = ','.join(map(str, lst))                                     # writes the points to the config file
        config.set('Points', key, value)

        config['GlobalSettings']['speed_ms'] = '0.3'
        config['GlobalSettings']['speed_rads'] = '0.75'
        config['GlobalSettings']['accel_mss'] = '3'
        config['GlobalSettings']['accel_radss'] = '1.2'
        config['GlobalSettings']['blend_radius'] = '0.001'


        with open ('config.ini', 'w') as configfile:
            config.write(configfile)


