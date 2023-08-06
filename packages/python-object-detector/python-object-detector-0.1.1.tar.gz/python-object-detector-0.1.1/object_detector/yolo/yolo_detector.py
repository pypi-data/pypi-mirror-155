import json
import cv2
import time
import numpy as np
from object_detector.settings import DATA_PATH


YOLO_LABELS_PATH = DATA_PATH.joinpath("coco.names")
YOLO_WEIGHTS_PATH = DATA_PATH.joinpath("yolov2-tiny.weights")
YOLO_CONFIG_PATH = DATA_PATH.joinpath("yolov2-tiny.cfg")
YOLO_COLORS_PATH = DATA_PATH.joinpath("yolo_colors.txt")


# load the COCO class labels our YOLO model was trained on
LABELS = open(YOLO_LABELS_PATH).read().strip().split("\n")
# initialize a list of colors to represent each possible class label
# np.random.seed(42)
# COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
COLORS = np.loadtxt(YOLO_COLORS_PATH, dtype='uint8')


# derive the paths to the YOLO weights and model configuration
weights_path = str(YOLO_WEIGHTS_PATH)
config_path = str(YOLO_CONFIG_PATH)
# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
print("Yolo layers {}.".format(ln))
print("Output layer index: {}.".format(net.getUnconnectedOutLayers()))
print("Output layer name: {}.".format(ln[32]))
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]


def get_image_height(image: np.ndarray):
    return image.shape[0]


def get_image_width(image: np.ndarray):
    return image.shape[1]


def yolo(image: np.ndarray, min_confidence=0.5, threshold=0.3):
    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(
        image, 1 / 255.0, (416, 416), swapRB=True, crop=False
    )
    net.setInput(blob)
    start = time.time()
    layer_outputs = net.forward(ln)
    end = time.time()
    # show timing information on YOLO
    # print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    class_ids = []

    # loop over each of the layer outputs
    for output in layer_outputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > min_confidence:  # 50% confidence
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                res_y = get_image_height(image)
                res_x = get_image_width(image)
                # print(detection[0:4])
                # print(np.array([W, H, W, H]))
                box = detection[0:4] * np.array([res_x, res_y, res_x, res_y])
                (centerX, centerY, width, height) = box.astype("int")
                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, threshold)

    detected_objects = []

    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            # draw a bounding box rectangle and label on the image
            color = [int(c) for c in COLORS[class_ids[i]]]
            # cv2.rectangle(image._mat, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[class_ids[i]], confidences[i])
            # cv2.putText(image._mat, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            obj = dict(
                name=LABELS[class_ids[i]],
                confidence=confidences[i],
                xmin=x,
                ymin=y,
                xmax=x + w,
                ymax=y + h,
            )
            detected_objects.append(obj)

    return json.dumps(detected_objects)
