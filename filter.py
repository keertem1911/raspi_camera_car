# -*- coding: utf-8 -*-

import toolsw
import requests
import io
import matplotlib.pyplot as plt
import cv2
DETECTION_URL = "http://127.0.0.1:5000/v1/object-detection/yolov5s"
def filter_fn(img):
    '''
        :param img: A numpy array representing the input image
        :returns: A numpy array to send to the mjpg-streamer output plugin
    '''
    toolsw.put_time_to_image(img)
    '''buf = io.BytesIO()
    plt.imsave(buf, img, format='png')
    image_data = buf.getvalue()
    response = requests.post(DETECTION_URL, files={"image": image_data}).json()
    if len(response)>0:
        for obj in response:
            print(obj['xmin'])
            cv2.rectangle(img, (int(obj['xmin']), int(obj['ymin'])),
                              (int(obj['xmax']),int(obj['ymax'])), (255, 0, 0), 2)
    '''# cv2.imshow("jpg",img)
    # key= cv2.waitKey(0)
    return img


def init_filter():
    return filter_fn
# if __name__ == '__main__':
#     image_np = cv2.imread(r"E:\pycv2\yolov5-6.0\data\images\bus.jpg")
#     filter_fn(image_np)
#./mjpg_streamer -i "./input_uvc.so" -o "./output_http.so -w ./www -p 8080"
# ./mjpg_streamer -i "./input_opencv.so -filter cvfilter_py.so -fargs  /home/pi/camera/mjpg-streamer-master/mjpg-streamer-experimental/filter.py -r 320x240" -o "./output_http.so -w ./www -p 8080"
