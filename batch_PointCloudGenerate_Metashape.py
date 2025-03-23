import os

dir_path = r'I:\yangmeikeng_deal_2023\2023-02-16\sample4\16-30\test\1good'
file_ls2 = os.listdir(dir_path)  
file_ls = [os.path.join(dir_path, file) for file in file_ls2] 
doc=Metashape.app.document
for i in range(0,len(file_ls)):
    files = os.listdir(file_ls[i])
    filelist=[]
    for file in files:
        if file.endswith('.JPG'):
            filelist.append(file)
    filelist = [os.path.join(file_ls[i], file) for file in filelist]

    if len(filelist)>7:
        filelist2 = filelist[0:len(filelist):5]
    else:
        filelist2 = list()
        filelist2.append(filelist[0])
        
    chunk = Metashape.app.document.addChunk()
    chunk.label = file_ls2[i]
    chunk.addPhotos(filelist)

    for camera in chunk.cameras:
        camera.reference.enabled = False

    chunk.crs = Metashape.CoordinateSystem()
        
    try:
        chunk.matchPhotos(downscale=2, generic_preselection=True, reference_preselection=False)
        
        chunk.alignCameras()
        
        chunk.buildDepthMaps(downscale=2, filter_mode=Metashape.AggressiveFiltering)

        chunk.buildDenseCloud()


        tempPointCloudPath = os.path.join(os.path.dirname(filelist2[0]),"pc.txt")
        chunk.exportPoints(tempPointCloudPath, format= Metashape.PointsFormat.PointsFormatXYZ, binary=False,save_normals=False,save_colors=False)

        f = open(tempPointCloudPath)
        pointcloud = []
        for line in f:
            point = list(map(lambda x: float(x), line.split()))
            pointcloud.append(point)
        f.close()

        name = {}
        for i in range(len(filelist2)):
            name[i] = os.path.splitext(os.path.basename(filelist2[i]))[0]


        imgCameras = chunk.cameras
        for i in range(len(imgCameras)):
            if imgCameras[i].label in name.values():
                camera = imgCameras[i]
                uvPath = os.path.join(os.path.dirname(filelist2[0]), camera.label+"_uv.txt")
                f = open(uvPath, 'w')
                for pindex in range(len(pointcloud)):
                    point = pointcloud[pindex]
                    uv = camera.project(point)
                    if uv is not None:
                        f.write(str(uv.x)+" "+str(uv.y)+"\n")
                    else:
                        f.write(str(0) + " " + str(0) + "\n")
                f.close()
    except KeyboardInterrupt:
        break
    except:
        continue
# PhotoScan.app.quit()