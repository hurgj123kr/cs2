import os
import glob
path = "./AI_05_허성호"
black = glob.glob(path+"/black"+'/*')
picture = glob.glob(path+"/picture"+'/*')
home_alone = glob.glob("./home_alone"+"/*")

def rename(images):

    if "black" in images[0]:
        for x,y in enumerate(images):
            os.rename(y, os.path.join(path+"/black", "black_" +"{0:03d}.jpg".format(x)))
        black = glob.glob(path+"/black"+"/*")
        print("black {}번째 이미지까지 성공".format(x+1))
    
    elif "picture" in images[0]:
        for x,y in enumerate(images):
            os.rename(y, os.path.join(path+"/picture", "picture_" +"{0:03d}.jpg".format(x)))
        black = glob.glob(path+"/picture"+"/*")
        print("picture {}번째 이미지까지 성공".format(x+1))
    
    elif "home_alone" in images[0]:
        for x,y in enumerate(images):
            os.rename(y, os.path.join("./home_alone", "home_alone_" +"{0:03d}.jpg".format(x)))
        home_alone = glob.glob("./home_alone"+"/*")
        print("home_alone {}번째 이미지까지 성공".format(x+1))
    

#rename(home_alone)
#rename(picture) 이미지 정렬완료.
