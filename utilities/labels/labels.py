# -*- coding: utf-8 -*-

import numpy as np
import shapely.geometry as geometry
import utm
import overpy
import time
import math

import cv2
import random
import os.path

#Variable definitions for main function
srcFilePath    = 'C:/temp'
srcPictureName = 'T35WMN_20190829T100031_TCI.jpg'
gtFileName     = 'label_gt.txt'
repeatCount    = 50

#Overpy query for power:substation and coordinate area
overKey   = 'power'
overValue = 'substation'
query = """
[timeout:99999];
(
  node[""" + overKey + """=""" + overValue + """](64.8214388312971, 24.8120825440702, 65.8214035188828, 27.20571148892141);
  way[""" + overKey + """=""" + overValue + """](64.8214388312971, 24.8120825440702, 65.8214035188828, 27.20571148892141);
);
out;
"""

#coordinates for utm coordinate conversion
points = np.array([
        [
          65.80591820047655, 24.8120825440702
        ],
        [
          65.8214035188828, 27.213549565024742
        ],
        [
          64.8362407624999, 27.20571148892141
        ],
        [
          64.8214388312971, 24.892314281559564 # origo 0,0
        ],
        [
          65.80591820047655, 24.8120825440702
        ]
      ]);
    
#Overpy query for labelling houses
#overKey   = 'building'
#overValue = 'house'
#houseQuery = """
#[timeout:99999];
#(
#  node[""" + overKey + """=""" + overValue + """](64.8214388312971, 24.8120825440702, 65.8214035188828, 27.20571148892141);
#  way[""" + overKey + """=""" + overValue + """](64.8214388312971, 24.8120825440702, 65.8214035188828, 27.20571148892141);
#);
#out;
#""";


def cropPictures(imagePath, imageName, tgtName, origoX = 0, origoY = 0, xinc = 640, yinc = 400):

    Img = cv2.imread(imagePath + "/" + imageName) 
    Img2 = Img[origoY:origoY+yinc, origoX:origoX+xinc,:]
    cv2.imwrite(imagePath + "/" + tgtName, Img2)
    
    return;


def prepareCrop(x_coordinate, y_coordinate):

    y = 10980-int(y_coordinate/10)
    x = int(x_coordinate/10)
    
    xrand = random.randrange(x-550, x-100)
    if xrand > 10980-640:
        xrand = 10980-640
    elif xrand < 0:
        xrand = 0

    yrand = random.randrange(y-350, y-80)
    if yrand > 10980-400:
        yrand = 10980-400
    elif yrand < 0:
        yrand = 0

    return xrand, yrand


def cropCroordinates(origX, origY, cropX, cropY):
    
    origX_ = int(origX/10)
    origY_ = int(origY/10)
    
    cropY_ = 10980 - cropY
    diffX = origX_ - cropX
    diffY = cropY_ - origY_
    
    return diffX, diffY


def convertCoordinates(query, points):

    api = overpy.Overpass(url="http://overpass-api.de/api/interpreter")
    response = api.query(query);
    lss = [];

    for i, way in enumerate(response.ways):
        ls_coords = []
        try:
            time.sleep(2);
            nodes = way.get_nodes(resolve_missing=True);
        except:
            try:
                time.sleep(3);
                nodes = way.get_nodes(resolve_missing=True);   
            except:
                try:
                    time.sleep(4);
                    nodes = way.get_nodes(resolve_missing=True);
                except:
                    time.sleep(5);
                    nodes = way.get_nodes(resolve_missing=True);   
        finally:
            for node in nodes:
                ls_coords.append((node.lon,node.lat));
        
            lss.append(geometry.LineString(ls_coords).bounds);
    
            
    x_len = 6400
    y_len = 4000
    ret_list = []

    o_x, o_y, _, _ = utm.from_latlon(points[3][0], points[3][1]);
    
    for ls in lss:
        x1, y1, _, _ = utm.from_latlon(ls[1], ls[0]);
        x2, y2, _, _ = utm.from_latlon(ls[3], ls[2]);
        w = int(x2-x1);
        h = int(y2-y1);
        
        cx = int(x1 - o_x + w/2)
        cy = int(y1 - o_y + h/2)

        filey = int(cy / y_len)
        filex = int(cx / x_len)

        ret_list.append((filex,filey,cx,cy,w,h))
    
    return ret_list;


def writeGTfile(labels, filename, labelDesc):
    
    try:
        f = open(filename, "w+")
    
        for item in labels:
            f.write("%s,1\n" % (item[0]))
            f.write("%s,%s,%s,%s,%s\n" % (item[1], item[2], item[3], item[4], labelDesc))
    except:
        print("GT file error")    
    finally:
        f.close()

    return;

def main(folder, srcFile, tgtFile, repeatCtnr):

    assert os.path.exists(folder), "Path not found: %s" % (folder)
    assert os.path.exists(folder + "/" + srcFile), "File not found: %s" % (folder + "/" + srcFile)

    labels = []
    cntr = 0

    clss_list = convertCoordinates(query, points);
    
    for idx in range(0, repeatCtnr):
        for cls in clss_list:
            xvalue, yvalue = prepareCrop(cls[2], cls[3])
            tgtName = "Pic_" + str(idx) + "__" + str(cls[1]) + "_" + str(cls[0]) + "_" + str(cntr) + ".jpg"
            cropPictures(folder, srcFile, tgtName, xvalue, yvalue, 640, 400)
            croppedX, croppedY = cropCroordinates(cls[2], cls[3], xvalue, yvalue)
            labels.append((tgtName, croppedX, croppedY, math.ceil(cls[4]/10), math.ceil(cls[5]/10)))
            cntr += 1
    
    writeGTfile(labels, folder + "/" + tgtFile, overValue)


main(srcFilePath, srcPictureName, gtFileName, repeatCount);


