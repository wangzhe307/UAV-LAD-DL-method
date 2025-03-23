#coding=utf-8
import os
import glob
def single_read_uav_pitchangle(uav_jpg_inpath):
    b = b"\x3c\x2f\x72\x64\x66\x3a\x44\x65\x73\x63\x72\x69\x70\x74\x69\x6f\x6e\x3e"
    a = b"\x3c\x72\x64\x66\x3a\x44\x65\x73\x63\x72\x69\x70\x74\x69\x6f\x6e\x20"
    img = open(uav_jpg_inpath,'rb')
    
    data = bytearray()
    flag = False
    for i in img.readlines():
        if a in i:
            flag = True
        if flag:
            data += i
        if b in i:
            break
    if len(data) > 0:
        data = str(data.decode('ascii'))
        #print(data)
        lines = list(filter(lambda x: 'drone-dji:' in x, data.split("\n")))
        for d in lines:
            d = d.strip()[10:]
            k, v = d.split("=")
            if k=="GimbalPitchDegree":
                PitchDegree = v.split('"')[1]

    return PitchDegree

if __name__ == '__main__':
    folder_dir=r'J:\paper\leaf_angle_paper\01_Manuscript return experiment\05_deal_video\02\1good'
    folder_list=os.listdir(folder_dir)
    print(folder_list)
    for i in range(0,len(folder_list)):
        folder_path=os.path.join(folder_dir,folder_list[i])
        jpg_list = glob.glob(os.path.join(folder_path, "*.jpg")) 
        jpg_inpath=jpg_list[0]
        txt_outpath=folder_path
        jpg_name = os.path.basename(jpg_inpath)
        path1=os.path.join(txt_outpath,jpg_name[:-4]+'_pitch.txt')
        f = open(path1, 'w')
        PitchDegree=single_read_uav_pitchangle(jpg_inpath)

        f.write(str(PitchDegree))
        f.close()