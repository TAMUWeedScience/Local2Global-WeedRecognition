""" Written by Bholumram Gurjar (2022) """

from pathlib import Path
import numpy as np
import random
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageDraw

random.seed(0)

class_name_to_id_mapping = {"weed": 0
                            }
class_id_to_name_mapping = dict(zip(class_name_to_id_mapping.values(), class_name_to_id_mapping.keys()))


def plot_bounding_box(image, annotation_list):
    annotations = np.array(annotation_list)
    w, h = image.size

    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    transformed_annotations[:, [1, 3]] = annotations[:, [1, 3]] * w
    transformed_annotations[:, [2, 4]] = annotations[:, [2, 4]] * h
    transformed_annotations[:, 1] = transformed_annotations[:, 1] - (transformed_annotations[:, 3] / 2)
    transformed_annotations[:, 2] = transformed_annotations[:, 2] - (transformed_annotations[:, 4] / 2)
    transformed_annotations[:, 3] = transformed_annotations[:, 1] + transformed_annotations[:, 3]
    transformed_annotations[:, 4] = transformed_annotations[:, 2] + transformed_annotations[:, 4]

    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        plotted_image.rectangle(((x0, y0), (x1, y1)))

        plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))])

    plt.imshow(np.array(image))
    plt.show()



annotations = list(Path(r"C:\Users\gurja\workspace\Yolo_test\yolov5\Data_Conversion\Old_2021").glob("*.txt"))
# # Get any random annotation file

annotation_file = random.choice(annotations)
with open(annotation_file, "r") as file:
    annotation_list = file.read().split("\n")[:-1]
    annotation_list = [x.split(" ") for x in annotation_list]
    annotation_list = [[float(y) for y in x] for x in annotation_list]

# # Get the corresponding image file
image_file = annotation_file.with_suffix(".JPG")
assert os.path.exists(image_file)

# #Get the corresponding image file
# image_file = annotation_file.replace(annotations, images).replace("txt","JPG")
# assert os.path.exists(image_file)


# # Load the image
image = Image.open(image_file)
#Plot the Bounding Box
plot_bounding_box(image, annotation_list)

# Read images and annotations
# images = [os.path.join(r"C:\Users\gurja\workspace\Yolo_test\yolov5\Data_Conversion\annotations", x) for x in os.listdir(r"C:\Users\gurja\workspace\Yolo_test\yolov5\Data_Conversion\annotations")]
# annotations = [os.path.join(r"C:\Users\gurja\workspace\Yolo_test\yolov5\Data_Conversion\annotations", x) for x in os.listdir(r"C:\Users\gurja\workspace\Yolo_test\yolov5\Data_Conversion\annotations") if x[-3:] == "txt"]
#
# images.sort()
# annotations.sort()
# train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.2, random_state = 1)
# val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

