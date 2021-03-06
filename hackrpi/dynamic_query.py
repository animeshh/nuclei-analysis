import os
import itertools
import numpy as np
from PIL import Image, ImageDraw
from scipy import misc
from skimage.draw import polygon

#Cluster based on filters
#fileNum = '01'
#curDir = os.path.dirname(os.path.realpath("__file__"))
#parDir = os.path.abspath(os.path.join(curDir, os.pardir))  #abspath(curDir/..)
#dataDir = parDir + '/data/path-image-1' + str(fileNum) + '.tif/'
#ftPath = dataDir + 'path-image-1' + str(fileNum) + '.seg.000000.000000.csv'
# Load path-image from .jpg
#imgPath = dataDir + 'path-image-1' + str(fileNum) + '.000000.000000.jpg'
# Load polygons co-ordinates from .txt
#txtPath = dataDir + 'path-image-1' + str(fileNum) + '.seg.000000.000000.txt'
#txt = open(txtPath, 'r')


def pairwise(iterable):
    #"s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return itertools.izip(a, a)

# Obtain text file given image file and data directory
def getTextPath(imgPath, dataDir):
    import os

    res = ''
    for ind,elem in enumerate(imgPath.split('.')):
        res += elem
        if ind == 1:
            res += '.seg'
        res += '.'
    txtPath = dataDir + '/' + res + 'txt'

    txt = open(txtPath, 'r')
    return txt

def drawPoly(polyIdList, txt, imgPath, dataDir):
    count = 1
    #print dataDir,'/',imgPath,'.jpg'
    #im = Image.open(dataDir + '/' + imgPath + '.jpg')
    #imArray = np.asarray(im)
    #maskIm = Image.new("RGB", (imArray.shape[1], imArray.shape[0]), "Black")
    #draw = ImageDraw.Draw(maskIm)
    #draw.rectangle([0,0,400,400], fill="green")
    
    #print imArray
    imgArray = np.zeros((4096, 4096), dtype=np.uint8)
    for line in txt:
        if count in polyIdList:
            poly = line.split('\t')
            poly = poly[51:]
            poly = poly[0]
            poly = poly.replace(';', ',')
                       
            mypoly = []
            polyList = poly.split(',')
            while '' in polyList:
               polyList.remove('')
            if '\n' in polyList:
               polyList.remove('\n')
            for i, num in enumerate(polyList):
               polyList[i] = int(float(polyList[i]))

            # Draw a line from every co-ordinate with thickness of 1 px
            for x, y in pairwise(polyList):
               mypoly.append((x/2, y))

            P = np.array(mypoly)
            # Extract x and y co-ordinates
            x = P[:, 0]
            y = P[:, 1]
            rr, cc = polygon(y, x)
            imgArray[rr, cc] = 200
            #draw.line((0, 0) + (count,count), fill=128)
            #draw.line((0, im.size[1], im.size[0], 0), fill=128)
            #draw.polygon(mypoly, outline=1, fill=128)
            #draw.polygon([(count, count+1), (count-1, count+1), (count-1, count), (count, count+1)], outline=1, fill=128)
            #ImageDraw.Draw(im).polygon(mypoly, outline=(0,0,0,128), fill=(255,255,0,128))
            #ImageDraw.Draw(maskIm).polygon(mypoly, outline=(0,0,0,128), fill=(255,255,0,128))
            #print mypoly
            #del draw
        count+=1
    
    #im.save(dataDir + '/' + imgPath + ".uiQueryPolyMark.jpg")
    #maskIm.save(dataDir + '/' + imgPath + ".uiQueryPolyMark.jpg")
    misc.imsave(dataDir + '/' + imgPath + ".uiQueryPolyMark.jpg", imgArray)


def filteredCluster(paraList, imgPath, dataDir):

    ftPath = dataDir + '/' + imgPath + '.csv' 
    fp = open(ftPath, 'r')
    fName = dataDir + '/' + imgPath + '.filter.csv' 
    fw = open(fName,'w')
    featureIndexList = []
    polyId = []
    data = fp.readlines()
    
    #print paraList
    for i, para in enumerate(paraList):
        if(para != None):
            #print para
            featureIndexList.append(i)
    #print "Selected features: ",featureIndexList
    for line in data:
        value = line.split()
        #print value
        area = float(value[1])
        perimeter = float(value[2])
        compactness = float(value[3])
        assym = float(value[4])
        BoundaryIndex = float(value[5])
        contrast = float(value[6])
        energy = float(value[7])
        homogeneity = float(value[8])
        correlation = float(value[9])
        dissimilarity = float(value[10])
        asm = float(value[11])
        
        feature = ""
        for i,index in enumerate(featureIndexList):
            para = paraList[index]
            #print para
            if (float(value[index+1])>=para[0]) and (float(value[index+1]) <= para[1]):
                feature += str(float(value[index+1])) + " "
                #print "check here"            
            else:
                #print "Fail: ", para[0], para[1], value[index+1]
                feature = ""
                break
        
        if(feature != ""):
            #print "found"
            fw.write(feature + "\n")
            polyId.append(int(value[0]))
        else:
            pass
            #print("not found")
        
    #filteredCluster(0)
    fw.close()
    txt = getTextPath(imgPath, dataDir)
    drawPoly(polyId, txt, imgPath, dataDir)
    from kmean_cluster import start_kmeans
    from plot_dbscan import start_dbscan
    start_kmeans(fName, dataDir + '/' + imgPath + ".kmeans.png", featureIndexList)
    start_dbscan(fName, dataDir + '/' + imgPath + ".dbscan.png", featureIndexList)

#for testing
#paraList = [[0,100],[0,100],[0,100],[0,100],None,None,None,None,None,None,None,None]
#filteredCluster(paraList)
