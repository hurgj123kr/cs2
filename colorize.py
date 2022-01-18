import os
import numpy as np
import cv2

models_path = "./models"

kernel_path = models_path + "/pts_in_hull.npy"
CAFFE_MODEL = models_path + "/colorization_release_v2.caffemodel"
DEPLOY_FILE = models_path + "/colorization_deploy_v2.prototxt"

# 클러스터를 중앙값으로 불러옴.
pts_in_hull = np.load(kernel_path)
pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1).astype(np.float32)

# 모델 불러오기
net = cv2.dnn.readNetFromCaffe(DEPLOY_FILE,CAFFE_MODEL)#dnn은 cv2모듈이며 이미 학습한 모델을 사용하기위해서 이용.

#모델 layer 설정.
net.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull]

#dnn module에 없는값을 추가해줌. 있어야하는값을.
net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full((1, 313), 2.606, np.float32)]


def main(filepath):
    image_path = filepath
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image_input = image.copy()
    # convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    
    image_rgb = image.copy()
    
    # normalize input
    image_rgb = (image_rgb / 255.).astype(np.float32)
    
    # convert RGB to LAB
    image_lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2Lab)
    # only L channel to be used
    image_l = image_lab[:, :, 0] #L부분만 사용하는데 L은 색의 명도를 나타내고 0에가까울수록 흑색에 가깝게 해줌.
    
    input_image = cv2.resize(image_l, (224, 224))
    input_image -= 50 # subtract 50 for mean-centering

    net.setInput(cv2.dnn.blobFromImage(input_image))
    
    prediction = net.forward()[0,:,:,:].transpose((1, 2, 0))

    #resize to image shape
    prediction_resize = cv2.resize(prediction, (image.shape[1], image.shape[0]))

    #concatenate image L
    prediction_lab = np.concatenate([image_l[:,:, np.newaxis], prediction_resize], axis=2)

    #LAB to RGB
    prediction_rgb = cv2.cvtColor(prediction_lab, cv2.COLOR_Lab2RGB)
    prediction_rgb = np.clip(prediction_rgb, 0,1) * 255
    prediction_rgb = prediction_rgb.astype(np.uint8)#8진수로 표현.

    filename, ext = os.path.splitext(image_path)
    input_filename = '%s_input%s' % (filename, ext)
    output_filename = '%s_output%s' % (filename, ext)

    pred_rgb_output = cv2.cvtColor(prediction_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(input_filename, image_input)
    cv2.imwrite(output_filename, pred_rgb_output)
    return input_filename, output_filename

if __name__ == "__main__":
    main()