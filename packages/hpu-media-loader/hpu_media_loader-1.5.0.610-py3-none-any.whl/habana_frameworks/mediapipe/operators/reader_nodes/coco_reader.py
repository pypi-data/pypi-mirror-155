from habana_frameworks.mediapipe.operators.media_nodes import MediaReaderNode
from habana_frameworks.mediapipe.media_types import dtype as dt
from habana_frameworks.mediapipe.media_types import readerOutType as ro
from habana_frameworks.mediapipe.backend.nodes import opnode_tensor_info
import os
import json
import time
import numpy
import time
import argparse
import numpy as np


# Implement a datareader for COCO dataset
class coco_reader(MediaReaderNode):
    """
    Class defining coco reader node.

    """

    def __init__(self, name, guid, device, inputs, params, cparams, out_info):
        """
        Constructor method.

        :params name: node name.
        :params guid: guid of node.
        :params guid: device on which this node should execute.
        :params params: node specific params.
        :params cparams: backend params.
        :params out_info: node output information
        """
        super().__init__(name, guid, device, inputs, params, cparams, out_info)
        self.annfile = params['annfile']
        self.root = params['root']
        self.slice_index = int(params['slice_index'])
        self.num_slices = int(params['num_slices'])
        self.ids_dtype = dt.UINT64
        self.sizes_dtype = dt.UINT32
        self.boxes_dtype = dt.FLOAT32
        self.labels_dtype = dt.UINT32
        self.indices_dtype = dt.UINT32
        self.np_images_shape = np.array([self.batch_size], dtype=np.uint32)
        self.np_ids_shape = np.array([self.batch_size], dtype=np.uint32)
        self.np_sizes_shape = np.array([self.batch_size, 2], dtype=np.uint32)
        self.np_boxes_shape = np.array(
            [0, 4], dtype=np.uint32)  # this is variable output
        self.np_labels_shape = np.array(
            [0], dtype=np.uint32)  # this is variable output
        self.np_indices_shape = np.array(
            [self.batch_size + 1], dtype=np.uint32)
        if params['seed'] == None:
            self.seed = int(time.time())
        else:
            self.seed = params['seed']
        self.shuffle = params['shuffle']
        self.largest = os.path.join(self.root, '000000479400.jpg')

        with open(self.annfile) as fp:
            self.data = json.load(fp)

        self.images = {}
        self.label_map = {}

        # 0 stand for the background
        cnt = 0
        for cat in self.data["categories"]:
            cnt += 1
            self.label_map[cat["id"]] = cnt

        # read image attribute
        for img in self.data["images"]:
            img_id = img["id"]
            img_name = img["file_name"]
            img_size = (img["height"], img["width"])
            # print(img_name)
            if img_id in self.images:
                raise Exception("dulpicated image record")
            self.images[img_id] = (img_name, img_size, [])

        # read bboxes
        for bboxes in self.data["annotations"]:
            img_id = bboxes["image_id"]
            category_id = bboxes["category_id"]
            bbox = bboxes["bbox"]
            bbox_label = self.label_map[bboxes["category_id"]]
            self.images[img_id][2].append((bbox, bbox_label))

        # remove images without bbox
        for k, v in list(self.images.items()):
            if len(v[2]) == 0:
                # print("empty image: {}".format(k))
                self.images.pop(k)

    def get_largest_file(self):
        """
        Method to get largest media in the dataset.

        returns: largest media element in the dataset.
        """
        return self.largest

    def get_media_output_type(self):
        """
        Method to specify type of media output produced by the reader.

        returns: type of media output which is produced by this reader.
        """
        return ro.FILE_LIST

    def __len__(self):
        """
        Method to get dataset length.

        returns: length of dataset in units of batch_size.
        """
        return self.len

    def __iter__(self):
        """
        Method to initialize iterator.

        """
        if(self.shuffle == True):
            self.seed += 1
            rng = numpy.random.default_rng(self.seed)
            rng.shuffle(self.keys)
        self.current_index = int(self.slice_index * self.len * self.batch_size)
        return self

    def __next__(self):
        """
        Method to get one batch of dataset ouput from iterator.

        """
        last_index = self.current_index + self.batch_size
        if last_index > (self.batch_size * self.len):
            raise StopIteration

        images = []
        ids = np.zeros(shape=self.np_ids_shape, dtype=self.ids_dtype)
        sizes = np.zeros(shape=self.np_sizes_shape, dtype=self.sizes_dtype)
        indices = np.zeros(shape=self.np_indices_shape,
                           dtype=self.indices_dtype)
        boxes = []
        labels = []
        i = 0
        for index in range(self.current_index, last_index):
            image_id = self.keys[index]
            image = self.images[image_id]
            file_name = image[0]
            htot, wtot = image[1]
            image_path = os.path.join(self.root, file_name)

            images.append(image_path)
            ids[i] = image_id
            sizes[i] = [htot, wtot]
            indices[i+1] = indices[i] + len(image[2])
            i = i + 1

            for (l, t, w, h), bbox_label in image[2]:
                r = l + w
                b = t + h
                box = [l / wtot, t / htot, r / wtot, b / htot]
                boxes.append(box)
                labels.append(bbox_label)

        self.current_index = last_index

        images = np.array(images)
        boxes = np.array(boxes, dtype=self.boxes_dtype)
        boxes = np.array(boxes, dtype=self.boxes_dtype)
        labels = np.array(labels, dtype=self.labels_dtype)
        return images, ids, sizes, boxes, labels, indices

    def gen_output_info(self):
        """
        Method to generate output type information.

        :returns : output tensor information of type "opnode_tensor_info".
        """
        out_info = []
        o = opnode_tensor_info(dt.NDT, self.np_images_shape[::-1], "")
        out_info.append(o)
        o = opnode_tensor_info(self.ids_dtype, self.np_ids_shape[::-1], "")
        out_info.append(o)
        o = opnode_tensor_info(self.sizes_dtype, self.np_sizes_shape[::-1], "")
        out_info.append(o)
        o = opnode_tensor_info(self.boxes_dtype, self.np_boxes_shape[::-1], "")
        out_info.append(o)
        o = opnode_tensor_info(
            self.labels_dtype, self.np_labels_shape[::-1], "")
        out_info.append(o)
        o = opnode_tensor_info(
            self.indices_dtype, self.np_indices_shape[::-1], "")
        out_info.append(o)
        return out_info

    def set_params(self, params):
        """
        Setter method to set mediapipe specific params.

        :params params: mediapipe params of type "opnode_params".
        """
        self.batch_size = params.batch_size
        self.np_images_shape = np.array([self.batch_size], dtype=np.uint32)
        self.np_ids_shape = np.array([self.batch_size], dtype=np.uint32)
        self.np_sizes_shape = np.array([self.batch_size, 2], dtype=np.uint32)
        self.np_boxes_shape = np.array(
            [0, 4], dtype=np.uint32)  # this is variable output
        self.np_labels_shape = np.array(
            [0], dtype=np.uint32)  # this is variable output
        self.np_indices_shape = np.array(
            [self.batch_size + 1], dtype=np.uint32)
        num_images = len(self.images)
        self.len = int((num_images / self.num_slices) // self.batch_size)
        self.keys = numpy.fromiter(self.images.keys(), dtype=int)


'''
TEST CODE
'''


def main(root, annfile, batch_size=1, shuffle=True, index=0):
    dl = CocoReader(root=root, annfile=annfile, shuffle=shuffle)
    dl.set_batch_size = batch_size
    batch = 0
    for images, metadata in dl:
        if (index == batch):
            print("FILE: ", images)
            '''
            print("IDS: ", metadata.ids)
            print("SIZES: ", metadata.sizes)
            print("INDICES: ", metadata.indices)
            print("BOXES: ", metadata.boxes)
            print("LABELS: ", metadata.labels)
            '''
            break

        batch += 1


if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Display Coco Dataset batch")

    parse.add_argument('-b', '--batch', action='store',
                       dest='batch_size', help="Batch size")
    parse.add_argument('-d', '--dir', action='store',
                       dest='dir', help="COCO Dataset Path")
    parse.add_argument('-a', '--annf', action='store',
                       dest='ann', help="path of annotation file")
    parse.add_argument('-s', '--shuffle', action='store',
                       dest='shuffle', help="1 to enable shuffle")
    parse.add_argument('-i', '--index', action='store',
                       dest='index', help="batch index to print")

    args = parse.parse_args()
    if args.batch_size is None:
        batch_size = 4
    else:
        batch_size = int(args.batch_size)

    if args.dir is None:
        root = r'/software/data/pytorch/coco/train2017'
    else:
        root = str(args.dir)

    if args.ann is None:
        #annf = r'/software/users/gjaiswal/annotations/instances_train2017.json'
        annf = r'H:\mobaxterm\home\instances_train2017.json'
    else:
        annf = str(args.ann)

    if args.shuffle is None:
        shuff = False
    else:
        shuff = bool(int(args.shuffle))

    if args.index is None:
        index = 0
    else:
        index = index(args.index)
    main(root=root, annfile=annf, batch_size=batch_size, shuffle=shuff, index=index)
