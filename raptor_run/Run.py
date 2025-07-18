import os,shutil
from copy import deepcopy
import os

def move_file(to_path,from_path='output/'):
    dir_files = os.listdir(from_path)
    if os.path.exists(to_path) is False:
        os.makedirs(to_path)
    for file in dir_files:
        file_path = os.path.join(from_path,file)
        if os.path.isfile(file_path):
            if os.path.exists(os.path.join(to_path,file)):
                os.remove(os.path.join(to_path,file))
            shutil.move(file_path, to_path)

GRMHD_DATA_DIR="/home/yuxin/Work/Work/EHT/raptor_run/MAD_a+15o16/a094-high"

CAM_SIZE = 46.2261
# CAM_SIZE=32
RESOLUTION = 100

# high resolution figure will be copied to result/data_save_dirname
HIGH_RESOLUTION = 8 * RESOLUTION

OUTPUT_DIR = "../raptor_output"

def Run(params_json,GRMHD_DATA_FILE,data_save_dirname):
    f = open('model.in','w')
    f.write(f'MBH		(Msun)	{params_json["MBH"]}')
    f.write(f'DISTANCE		(kpc) {params_json["DISTANCE"]}')
    f.write(f'M_UNIT		(g)	{params_json["M_UNIT"]}')
    f.write(f'R_LOW		(-)	{params_json["R_LOW"]}')
    f.write(f'R_HIGH		(-)	{params_json["R_HIGH"]}')
    f.write(f'INCLINATION	(deg)          {params_json["INCLINATION"]}')
    f.write(f'IMG_WIDTH	(pixels)	{params_json["IMG_WIDTH"]}')
    f.write(f'IMG_HEIGHT	(pixels)	{params_json["IMG_HEIGHT"]}')
    f.write(f'CAM_SIZE_X	(Rg)		{params_json["CAM_SIZE_X"]}')
    f.write(f'CAM_SIZE_Y	(Rg)		{params_json["CAM_SIZE_Y"]}')
    f.write(f'FREQS_PER_DEC	(-)		{params_json["FREQS_PER_DEC"]}')
    f.write(f'FREQ_MIN	(Hz)		{params_json["FREQ_MIN"]}')
    f.write(f'STEPSIZE	(-)		{params_json["STEPSIZE"]}')
    f.write(f'AXION_NORM  (-)    {params_json["AXION_NORM"]}')
    f.write(f'AXION_OMEGA  (-)    {params_json["AXION_OMEGA"]}')
    f.write(f'AXION_PHASE  (-)    {params_json["AXION_PHASE"]}')
    f.write(f'MAX_LEVEL	(-)		{params_json["MAX_LEVEL"]}')
    f.close()
    if params_json["AXION_NORM"]==0:
        if not os.path.exists(os.path.join(os.path.abspath(OUTPUT_DIR),data_save_dirname,"img_data_0.h5")):
            os.system(f'./RAPTOR model.in {GRMHD_DATA_FILE} 0 ')
            os.system(f'python plotter-example.py 0')
            move_file(os.path.join(os.path.abspath(OUTPUT_DIR),data_save_dirname))
    else:
        if not os.path.exists(os.path.join(os.path.abspath(OUTPUT_DIR),data_save_dirname,f"img_data_{params_json['AXION_PHASE']+1}.h5")):
            os.system(f'./RAPTOR model.in {GRMHD_DATA_FILE} {params_json["AXION_PHASE"]+1} ')
            os.system(f'python plotter-example.py {params_json["AXION_PHASE"]+1}')
            move_file(os.path.join(os.path.abspath(OUTPUT_DIR),data_save_dirname))
    os.remove("model.in")


PARAMS_JSON={
    "MBH": 6.2e9,
    "DISTANCE": 16800, 
    "M_UNIT": 3e+25,
    "R_LOW": 1,
    "R_HIGH": 1,
    "INCLINATION" : 163,
    "IMG_WIDTH": RESOLUTION,
    "IMG_HEIGHT": RESOLUTION,
    "CAM_SIZE_X": CAM_SIZE,
    "CAM_SIZE_Y": CAM_SIZE,
    "FREQS_PER_DEC": 1,
    "FREQ_MIN": 230.e9,
    "STEPSIZE": 0.005,
    "AXION_NORM": 0, # 0/0.1
    "AXION_OMEGA": 0.4, # default 0.4
    "AXION_PHASE": 0, # 0-15
    "MAX_LEVEL": 1,
}

if __name__=='__main__':


    GRMHD_DATA_FILES=[]
    rpaths=sorted(os.listdir(GRMHD_DATA_DIR))
    for rpath in rpaths:
        if os.path.isfile(os.path.join(GRMHD_DATA_DIR,rpath)):
            GRMHD_DATA_FILES.append(os.path.join(GRMHD_DATA_DIR,rpath))

    GRMHD_DATA_FILES=GRMHD_DATA_FILES[100:]
    # loop for grmhd time
    error_list=[]

    for axion_omega in [0.3,0.35,0.4,0.45]:
        for GRMHD_DATA_FILE in GRMHD_DATA_FILES:
            try:
                data_save_dirname=str(axion_omega)+"/"+os.path.basename(GRMHD_DATA_FILE)
                params_json=deepcopy(PARAMS_JSON)
                params_json["AXION_OMEGA"]=axion_omega
                Run(params_json,GRMHD_DATA_FILE,data_save_dirname)
                
                params_json["AXION_NORM"]=0.1
                
                for phase in range(16):
                    params_json["AXION_PHASE"]=phase
                    Run(params_json,GRMHD_DATA_FILE,data_save_dirname)
            except Exception as e:
                error_list.append(f"{e}")
                print(e)
        open(f"{axion_omega} done", "w").close()

    # loop for grmhd time (high resolution)
    for axion_omega in [0.3,0.35,0.4,0.45]:
        for GRMHD_DATA_FILE in GRMHD_DATA_FILES:
            try:
                data_save_dirname=str(axion_omega)+"/"+GRMHD_DATA_FILE+"_high_res"
                params_json=deepcopy(PARAMS_JSON)
                params_json["AXION_OMEGA"]=axion_omega
                params_json["IMG_WIDTH"]=HIGH_RESOLUTION
                params_json["IMG_HEIGHT"]=HIGH_RESOLUTION
                Run(params_json,GRMHD_DATA_FILE,data_save_dirname)
                
                params_json["AXION_NORM"]=0.1
                
                for phase in range(16):
                    params_json["AXION_PHASE"]=phase
                    Run(params_json,GRMHD_DATA_FILE,data_save_dirname)
            except Exception as e:
                error_list.append(f"{e}")
                print(e)
        open(f"{axion_omega} done", "w").close()

    errorlog = open("log_run_error.txt", 'w', encoding='utf-8')
    errorlog.write("\n".join(error_list))
    errorlog.close()
    os.rmdir("output")



