# this is the program that will create the .script file to be used in the robot

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

with open('config.ini', 'r') as f:

    points = config['Points']
    cixfile = config['CIX']['file']
    speed_ms = config['GlobalSettings']['speed_ms']
    speed_rads = config['GlobalSettings']['speed_rads']
    accel_mss = config['GlobalSettings']['accel_mss']
    accel_radss = config['GlobalSettings']['accel_radss']
    blend_radius = config['GlobalSettings']['blend_radius']

    set_reference = config['Reference']['set_reference']
    ref_frame = config['Reference']['ref_frame']

    z_offset = config['ToolOffset']['urzdown']

ori = cixfile.replace('.CIX', '')  #removes .CIX from filename
with open(str(ori)+'.script', 'w') as f:
    f.write('def initialize():\n')
    f.write(f'   global speed_ms = {speed_ms}\n')
    f.write(f'   global speed_rads = {speed_rads}\n')       
    f.write(f'   global accel_mss = {accel_mss}\n')
    f.write(f'   global accel_radss = {accel_radss}\n')
    f.write(f'   global blend_radius = {blend_radius}\n')
    f.write('   set_tcp(p[0.000000, -0.077000, 0.150000, 0.000000, 0.000000, 0.000000])\n\n')

    f.write('def home():\n')
    f.write('   movej([-0.511159, -1.657892, -2.098940, -0.955557, 1.570796, -0.511159],accel_radss,speed_rads,0,blend_radius_m)\n\n')

    f.write('def '+str(ori)+'():\n')
    f.write(f'   set_reference(p{set_reference})\n')
    f.write(f'   ref_frame = p{ref_frame}\n')

    for key, value in config['Points'].items():
        x, y = value.split(',')
        x = float(x)/1000 
        y = float(y)/1000
        z1 = float(z_offset) + 0.05

        f.write(f'movel(pose_trans(ref_frame,p[{x}, {y}, {z1}, 3.1459265, 0.000000, 0.000000]\n')
        f.write(f'movel(pose_trans(ref_frame,p[{x}, {y}, {z_offset}, 3.1459265, 0.000000, 0.000000]\n')
        f.write(f'StartGlue()'+'\n')
        f.write(f'sleep(0.2500)'+ '\n')
        f.write(f'StopGlue()'+'\n')
        f.write(f'movel(pose_trans(ref_frame,p[{x}, {y}, {z1}, 3.1459265, 0.000000, 0.000000]\n')

    f.write('end')

    f.write ('def mainprog:\n')
    f.write ('   initialize()\n')
    f.write ('   home()\n')
    f.write ('   '+str(ori)+'()\n')
    f.write ('end')