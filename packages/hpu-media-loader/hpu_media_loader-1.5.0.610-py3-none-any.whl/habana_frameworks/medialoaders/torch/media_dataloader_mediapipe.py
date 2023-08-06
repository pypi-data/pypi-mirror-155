from habana_frameworks.mediapipe.mediapipe import MediaPipe  # NOQA
from habana_frameworks.mediapipe import fn  # NOQA
from habana_frameworks.mediapipe.media_types import imgtype as it  # NOQA
from habana_frameworks.mediapipe.media_types import dtype as dt  # NOQA
from habana_frameworks.mediapipe.media_types import ftype as ft  # NOQA
from habana_frameworks.mediapipe.media_types import layout as lt  # NOQA
from habana_frameworks.mediapipe.operators.cpu_nodes.cpu_nodes import media_function  # NOQA

import os
import time
import sys

import torch
import torch.utils.data
import torchvision
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
import numpy as np
import copy
import math
#from datetime import datetime
from PIL import Image
#from collections.abc import Sequence
from enum import Enum


class Crop_Type(Enum):
    """
    Enum class defining crop-resize type.

    """
    Crop_Only = 0
    ResizedCrop = 1
    Crop_Resize = 2
    Resize_Crop = 3


class random_flip_func(media_function):
    """
    Class to randomly generate input for RandomFlip media node.

    """

    def __init__(self, params):
        """
        Constructor method.

        :params params: random_flip_func specific params.
                        shape: output shape
                        dtype: output data type
                        seed: seed to be used
        """
        self.np_shape = params['shape'][::-1]
        self.np_dtype = params['dtype']
        self.seed = params['seed']
        self.rng = np.random.default_rng(self.seed)

    def __call__(self):
        """
        Callable class method.

        :returns : randomly generated binary output per image.
        """
        a = self.rng.choice([0, 1], p=[0.5, 0.5], size=self.np_shape)
        a = np.array(a, dtype=self.np_dtype)
        return a


class random_resized_crop_func(media_function):
    """
    Class to generate random crop parameters.

    """

    def __init__(self, params):
        """
        Constructor method.

        :params params: random_resized_crop_func specific params
                        shape: output shape.
                        dtype: output data type.
                        seed: seed to be used.
                        priv_params: private params for random_resized_crop_func
                                     resizewidth: resize output width.
                                     resizeheight: resize output height.
                                     scale: lower and upper bounds for the random area of the crop, before resizing.
                                     ratio: lower and upper bounds for the random aspect ratio of the crop, before resizing.
        """
        self.np_shape = params['shape'][::-1]
        self.np_dtype = params['dtype']
        self.batch_size = self.np_shape[0]
        self.priv_params = params['priv_params']
        self.resizeWidth = self.priv_params['resizewidth']
        self.resizeHeight = self.priv_params['resizeheight']
        self.scale = self.priv_params['scale']
        self.ratio = self.priv_params['ratio']
        self.seed = params['seed']
        self.rng = np.random.default_rng(self.seed)

    def __call__(self, filelist):
        """
        Callable class method.

        :params filelist: batch of files.
        :returns : random crop parameters for filelist.
        """
        a = np.zeros(shape=self.np_shape, dtype=self.np_dtype)
        for i in range(self.batch_size):
            a[i] = self.random_window_calculator(filelist[i])
        # print("RandomResizedCrop: ", a)
        return a

    def random_window_calculator(self, filename):
        """
        Method to generate crop params for a file.

        :params filename: file for which crop params are to be generated.
        :returns : random crop parameters for specified file.
        """
        clp_value = 48
        clp_value_two_stage = 76
        width, height = Image.open(filename).size
        #print("Image is ",width,height)
        area = width*height
        # print(area)

        scale = np.array([self.scale[0], self.scale[1]]
                         )  # np.array([0.08,1.0])
        ratio = np.array([self.ratio[0], self.ratio[1]]
                         )  # np.array([3./4.,4./3.])

        # log_ratio = torch.log(torch.tensor(ratio))
        log_ratio = np.log(ratio)
        for _ in range(10):
            #target_area = area * torch.empty(1).uniform_(scale[0], scale[1]).item()
            target_area = area * self.rng.uniform(scale[0], scale[1])
            # aspect_ratio = torch.exp(
            #    torch.empty(1).uniform_(log_ratio[0], log_ratio[1])
            # ).item()
            aspect_ratio = math.exp(
                self.rng.uniform(log_ratio[0], log_ratio[1]))

            w = int(round(math.sqrt(target_area * aspect_ratio)))
            h = int(round(math.sqrt(target_area / aspect_ratio)))

            w = max(w, clp_value)
            h = max(h, clp_value)
            if((w < self.resizeWidth and h > self.resizeHeight) or (w > self.resizeWidth and h < self.resizeHeight)):
                w = max(w, clp_value_two_stage)
                h = max(h, clp_value_two_stage)
            w = min(w, width)
            h = min(h, height)

            if 0 < w <= width and 0 < h <= height:
                #i = torch.randint(0, height - h + 1, size=(1,)).item()
                #j = torch.randint(0, width - w + 1, size=(1,)).item()
                i = self.rng.integers(0, width - w + 1)
                j = self.rng.integers(0, height - h + 1)
                return [i/width, j/height, w/width, h/height]

        # Fallback to central crop
        in_ratio = float(width) / float(height)
        if in_ratio < min(ratio):
            w = width
            h = int(round(w / min(ratio)))
        elif in_ratio > max(ratio):
            h = height
            w = int(round(h * max(ratio)))
        else:  # whole image
            w = width
            h = height
        w = max(w, clp_value)
        h = max(h, clp_value)
        if((w < self.resizeWidth and h > self.resizeHeight) or (w > self.resizeWidth and h < self.resizeHeight)):
            w = max(w, clp_value_two_stage)
            h = max(h, clp_value_two_stage)
        w = min(w, width)
        h = min(h, height)

        i = (width - w) // 2
        j = (height - h) // 2
        # return i, j, h, w
        return [i/width, j/height, w/width, h/height]


class center_crop_func(media_function):
    """
    Class to generate center crop parameters.

    """

    def __init__(self, params):
        """
        Constructor method.

        :params params: center_crop_func specific params.
                        shape: output shape
                        dtype: output data type
                        priv_params: private params for center_crop_func
                                     cropWidth: crop output width
                                     cropHeight: crop output height
        """
        self.np_shape = params['shape'][::-1]
        self.np_dtype = params['dtype']
        self.batch_size = self.np_shape[0]
        self.priv_params = params['priv_params']
        self.cropWidth = self.priv_params['cropWidth']
        self.cropHeight = self.priv_params['cropHeight']

    def __call__(self, filelist):
        """
        Callable class method.

        :params filelist: batch of files.
        :returns : center crop parameters for filelist.
        """
        a = np.zeros(shape=self.np_shape, dtype=self.np_dtype)
        i = 0
        for filename in filelist:
            width, height = Image.open(filename).size
            # print("Image is ",filename, width,height)
            if width > self.cropWidth:
                crop_x = (width - self.cropWidth) // 2
                crop_x_ratio = crop_x / width
                crop_w_ratio = self.cropWidth / width
            else:
                crop_x_ratio = 0
                crop_w_ratio = 1

            if height > self.cropHeight:
                crop_y = (height - self.cropHeight) // 2
                crop_y_ratio = crop_y / height
                crop_h_ratio = self.cropHeight / height
            else:
                crop_y_ratio = 0
                crop_h_ratio = 1
            a[i] = [crop_x_ratio, crop_y_ratio, crop_w_ratio, crop_h_ratio]
            i += 1
        # print("CenterCrop: ", a)
        return a


class HPUMediaPipe(MediaPipe):
    """
    Class defining resnet media pipe.

    """
    instance_count = 0

    def __init__(self, a_torch_transforms, a_root, a_batch_size, a_shuffle=False, a_drop_last=True, a_prefetch_count=1, a_num_instances=1, a_instance_id=0, a_device=None):
        """
        Constructor method.

        :params a_torch_transforms: torchvision transforms to be applied on mediapipe.
        :params a_root: path from which to load the images.
        :params a_batch_size: mediapipe output batch size.
        :params a_shuffle: whether images have to be shuffled.
        :params a_drop_last: whether to drop the last incomplete batch or round up.
        :params a_prefetch_count: queue depth for media processing. <1/2/3>
        :params a_num_instances: number of devices.
        :params a_instance_id: instance id of current device.
        :params a_device: media device to run mediapipe on. <hpu/hpu:0>
        """
        self.super_init = False
        self.root = a_root
        batchSize = a_batch_size
        self.shuffle = a_shuffle
        self.drop_last = a_drop_last

        if not isinstance(a_torch_transforms, transforms.Compose):
            raise ValueError(
                "torch_transforms should be of type torchvision.transforms")
        self.transforms = a_torch_transforms.transforms
        self.transform_to_ignore = []
        self.crop_transform_index = None
        self.resize_transform_index = None
        self.cmn_transform_index = None

        num_crop = 0
        num_resize = 0
        num_cmn = 0
        crop_width = None
        crop_height = None
        resize_width = None
        resize_height = None

        self.crop_type = None
        resize_crop_handled = True
        self.crop_width = None
        self.crop_height = None
        self.need_crop_op = False
        self.decode_width = None
        self.decode_height = None
        self.media_output_dtype = 'uint8'

        transform_count = 0
        for t in self.transforms:
            if isinstance(t, transforms.RandomResizedCrop):
                if num_crop == 0 and num_resize == 0:
                    print("transform RandomResizedCrop: Random Crop,Resize w:h ",
                          t.size[1], t.size[0], " scale: ", t.scale, " ratio: ", t.ratio, " interpolation: ", t.interpolation)
                    num_crop += 1
                    num_resize += 1
                else:
                    raise ValueError(
                        "Unsupported 2nd crop/resize transform: " + str(type(t)))
                resize_height = t.size[0]
                resize_width = t.size[1]
                if (resize_width % 16 != 0) or (resize_height % 8 != 0):
                    raise ValueError(
                        "Unsupported w:h for transform: " + str(type(t)))
                self.crop_type = Crop_Type.ResizedCrop
                self.transform_to_ignore.append(transform_count)
                self.crop_transform_index = transform_count
                self.resize_transform_index = transform_count

            elif isinstance(t, transforms.CenterCrop):
                if num_crop == 0:
                    print("transform CenterCrop: w:h ", t.size[1], t.size[0])
                    num_crop += 1
                else:
                    raise ValueError(
                        "Unsupported 2nd Crop transform: " + str(type(t)))

                crop_height = t.size[0]
                crop_width = t.size[1]

                if num_resize == 0:
                    self.crop_type = Crop_Type.Crop_Only
                    self.transform_to_ignore.append(transform_count)
                else:
                    self.crop_type = Crop_Type.Resize_Crop
                    if num_cmn == 0:
                        resize_crop_handled = False
                    else:
                        resize_crop_handled = True

                self.crop_transform_index = transform_count

            elif isinstance(t, transforms.Resize):
                check_maxsize = False
                if num_resize == 0:
                    if isinstance(t.size, int):
                        resize_height = t.size
                        resize_width = t.size
                        check_maxsize = True
                    elif (isinstance(t.size, tuple) or (isinstance(t.size, list))) and len(t.size) == 1:
                        resize_height = t.size[0]
                        resize_width = t.size[0]
                        check_maxsize = True
                    elif (isinstance(t.size, tuple) or (isinstance(t.size, list))) and len(t.size) == 2:
                        resize_height = t.size[0]
                        resize_width = t.size[1]
                    else:
                        raise ValueError(
                            "Unsupported size: transforms.Resize ")
                    print("transform Resize: w:h ", resize_width, resize_height, " interpolation: ",
                          t.interpolation, " max_size: ", t.max_size)  # t.antialias ignored

                    num_resize += 1

                    if (resize_width % 16 != 0) or (resize_height % 8 != 0):
                        raise ValueError(
                            "Unsupported w:h for transform: " + str(type(t)))

                    # resize_height will be same as resize_width
                    if (check_maxsize == True) and (t.max_size != None) and (resize_width > t.max_size):
                        raise ValueError(
                            "max_size must be greater than resize width/height for transform: " + str(type(t)))

                else:
                    raise ValueError(
                        "Unsupported 2nd resize transform: " + str(type(t)))

                # Update crop type to Crop_Resize
                if (num_crop == 1) and (self.crop_type == Crop_Type.Crop_Only):
                    self.crop_type = Crop_Type.Crop_Resize

                self.transform_to_ignore.append(transform_count)
                self.resize_transform_index = transform_count

            elif isinstance(t, transforms.Normalize):
                if num_cmn == 0:
                    print("transform Normalize: mean:std",
                          t.mean, t.std)  # t.inplace ignored

                    if ((not isinstance(t.mean, list)) and (not isinstance(t.mean, tuple))) or (len(t.mean) != 3):
                        raise ValueError(
                            "Unsupported mean for Normalize transform")

                    if ((not isinstance(t.std, list)) and (not isinstance(t.std, tuple))) or (len(t.std) != 3):
                        raise ValueError(
                            "Unsupported std for Normalize transform")

                    if t.mean != [0.485, 0.456, 0.406] and t.mean != (0.485, 0.456, 0.406):
                        print(
                            "transform Normalize mean is different than default mean")

                    if t.std != [0.229, 0.224, 0.225] and t.std != (0.229, 0.224, 0.225):
                        print("transform Normalize std is different than default std")
                    num_cmn += 1
                else:
                    raise ValueError(
                        "Unsupported 2nd Normalize transform: " + str(type(t)))

                if resize_crop_handled == False:
                    resize_crop_handled = True

                # cmn to be added as last node in media graph
                self.transform_to_ignore.append(transform_count)
                self.cmn_transform_index = transform_count

            elif isinstance(t, transforms.RandomHorizontalFlip):
                if t.p == 0.5:
                    print("transform RandomHorizontalFlip: probability ", t.p)
                else:
                    raise ValueError(
                        "Unsupported probability for transform: " + str(type(t)))  # TODO

            elif isinstance(t, transforms.RandomVerticalFlip):
                if t.p == 0.5:
                    print("transform RandomVerticalFlip: probability ", t.p)
                else:
                    raise ValueError(
                        "Unsupported probability for transform: " + str(type(t)))  # TODO

            elif isinstance(t, transforms.ToTensor):
                print("transform ToTensor")
                self.media_output_dtype = 'float32'  # TODO
                self.transform_to_ignore.append(transform_count)

            else:
                raise ValueError("Unsupported transform: " + str(type(t)))

            transform_count += 1

        if (num_cmn == 0) and (self.media_output_dtype == 'float32'):
            raise ValueError("Unsupported output data type float32")  # TODO

        if num_resize == 1:
            self.decode_width = resize_width
            self.decode_height = resize_height
        elif num_resize == 0:
            if self.crop_type == Crop_Type.Crop_Only:
                if (crop_width % 16 != 0) or (crop_height % 8 != 0):
                    raise ValueError(
                        "Unsupported w:h for transform: transforms.CenterCrop")
                self.decode_width = crop_width
                self.decode_height = crop_height
                print("No resize found, using crop resolution of ",
                      self.decode_width, "x", self.decode_height)
            else:
                raise ValueError("No resize/crop found")
                #self.decode_width = default_output_size
                #self.decode_height = default_output_size
        else:
            raise ValueError("Unsupported resize count")

        if num_crop == 1:
            if self.crop_type == Crop_Type.Resize_Crop:
                self.enable_crop = False
                if (resize_width < crop_width) or (resize_height < crop_height):
                    print(" resize width:height ", resize_width, resize_height,
                          "crop width:height ", crop_width, crop_height)
                    raise ValueError(
                        "Unsupported crop width/height > resize width/height")
            else:
                self.enable_crop = True
                if (self.crop_type == Crop_Type.Crop_Only) or (self.crop_type == Crop_Type.Crop_Resize):
                    self.crop_width = crop_width
                    self.crop_height = crop_height

        else:
            if num_crop != 0:
                raise ValueError("Unsupported crop count")
            self.enable_crop = False

        if resize_crop_handled == False:
            self.need_crop_op = True

        # np.random.seed(int(time.time()))  # TODO
        # np.random.seed(1000)

        self.num_instances = a_num_instances
        self.instance_id = a_instance_id

        print("MediaDataloader num instances {} instance id {}".format(
            self.num_instances, self.instance_id))

        HPUMediaPipe.instance_count += 1
        self.pipename = "{}:{}".format(
            self.__class__.__name__, HPUMediaPipe.instance_count)
        self.pipename = str(self.pipename)

        self.super_init = True
        super().__init__(device=a_device, batch_size=batchSize,
                         prefetch_depth=a_prefetch_count, pipename=self.pipename)

    def __del__(self):
        """
        Destructor method.

        """
        if self.super_init == True:
            super().__del__()

    def definegraph(self):
        """
        Method defines the media graph based on transforms.

        :returns : output images, labels
        """
        # seed_mediapipe = 1000 #TODO: Update
        seed_mediapipe = int(time.time_ns() % (2**31 - 1))

        # try to print the seed for distributed
        try:
            print("MediaDataloader {}/{} seed : {}".format(self.instance_id,
                  self.num_instances, seed_mediapipe), force=True)
        except TypeError:
            print("MediaDataloader seed : {}".format(seed_mediapipe))

        crop_func = None
        enable_decoder_random_crop = False
        batchSize = self.getBatchSize()

        if self.enable_crop == True:
            if self.crop_type == Crop_Type.ResizedCrop:

                # random_crop_params = {}
                # random_crop_params['resizewidth'] = self.decode_width
                # random_crop_params['resizeheight'] = self.decode_height
                # random_crop_params['scale'] = self.transforms[self.crop_transform_index].scale
                # random_crop_params['ratio'] = self.transforms[self.crop_transform_index].ratio
                # crop_func = random_resized_crop_func
                enable_decoder_random_crop = True
                crop_func = None
                print("Decode ResizedCrop w:h",
                      self.decode_width, self.decode_height)

            elif (self.crop_type == Crop_Type.Crop_Only) or (self.crop_type == Crop_Type.Crop_Resize):
                random_crop_params = {}
                random_crop_params['cropWidth'] = self.crop_width
                random_crop_params['cropHeight'] = self.crop_height
                crop_func = center_crop_func

                print("Decode w:h ", self.decode_width, self.decode_height,
                      "Center Crop w:h: ", self.crop_width, self.crop_height)

            else:
                assert False, "Error: wrong crop type"
        else:
            # No Crop or crop_type = Crop_Type.Resize_Crop
            print("Decode w:h ", self.decode_width,
                  self.decode_height, " , Crop disabled")
            crop_func = None

        #crop_func = None
        if self.resize_transform_index == None:
            assert self.crop_type == Crop_Type.Crop_Only, "No resize transform available"
            res_pp_filter = ft.BI_LINEAR  # 3
        else:
            if self.transforms[self.resize_transform_index].interpolation == InterpolationMode.BILINEAR:
                res_pp_filter = ft.BI_LINEAR  # 3
            elif self.transforms[self.resize_transform_index].interpolation == InterpolationMode.NEAREST:
                res_pp_filter = ft.NEAREST  # 2
            elif self.transforms[self.resize_transform_index].interpolation == InterpolationMode.BICUBIC:
                res_pp_filter = ft.BICUBIC  # 4
            elif self.transforms[self.resize_transform_index].interpolation == InterpolationMode.BOX:
                res_pp_filter = ft.BOX  # 6
            elif self.transforms[self.resize_transform_index].interpolation == InterpolationMode.LANCZOS:
                res_pp_filter = ft.LANCZOS  # 1
            elif self.transforms[self.resize_transform_index].interpolation == InterpolationMode.HAMMING:
                print(
                    "Warning: InterpolationMode.HAMMING not supported, using InterpolationMode.BILINEAR")
                res_pp_filter = ft.BI_LINEAR
            else:
                assert False, "Error: Unsupported InterpolationMode"

        # if crop_func == None:
        #    print("Decode w:h ", self.decode_width, self.decode_height, " with Crop Disabled")
        print("MediaDataloader shuffle is ", self.shuffle)
        print("MediaDataloader output type is ", self.media_output_dtype)

        self.input = fn.ReadImageDatasetFromDir(
            dir=self.root, format="JPEG", seed=seed_mediapipe, shuffle=self.shuffle, drop_remainder=self.drop_last, label_dtype=dt.UINT32, num_slices=self.num_instances, slice_index=self.instance_id)  # TODO: check label_dtype
        jpegs, data = self.input()

        def_output_image_size = [self.decode_width, self.decode_height]
        if enable_decoder_random_crop == True:
            # crop_type = Crop_Type.ResizedCrop

            self.decode = fn.ImageDecoder(output_format=it.RGB_P, resize=def_output_image_size, filter=res_pp_filter, enable_random_crop=0xDEADBEEF,
                                          scale_min=self.transforms[self.crop_transform_index].scale[0], scale_max=self.transforms[self.crop_transform_index].scale[1], ratio_min=self.transforms[self.crop_transform_index].ratio[0], ratio_max=self.transforms[self.crop_transform_index].ratio[1], seed=seed_mediapipe)
            images = self.decode(jpegs)
        else:
            self.decode = fn.ImageDecoder(
                output_format=it.RGB_P, resize=def_output_image_size, filter=res_pp_filter)

            if crop_func is not None:
                # crop_func is center_crop_func or random_resized_crop_func
                self.random_crop = fn.MediaFunc(func=crop_func, dtype=dt.FLOAT32, shape=[
                                                4, batchSize], priv_params=random_crop_params, seed=seed_mediapipe)
                crop_val = self.random_crop(jpegs)
                images = self.decode(jpegs, crop_val)
            else:
                images = self.decode(jpegs)

        width = def_output_image_size[0]
        height = def_output_image_size[1]
        crop_cmn = False
        transform_count = 0
        for t in self.transforms:
            if transform_count in self.transform_to_ignore:
                #print("ignored transform ", str(type(t)))
                pass
            else:
                if isinstance(t, transforms.CenterCrop):
                    assert self.crop_type == Crop_Type.Resize_Crop, "Wrong Crop Type"
                    height = t.size[0]
                    width = t.size[1]
                    cmn_pos_offset = 0.5
                    if self.need_crop_op == True:
                        self.crop_op = fn.Crop(
                            crop_w=width, crop_h=height, crop_pos_x=cmn_pos_offset, crop_pos_y=cmn_pos_offset, crop_d=0)
                        images = self.crop_op(images)
                    else:
                        crop_cmn = True

                elif isinstance(t, transforms.RandomHorizontalFlip):
                    self.random_flip_input = fn.MediaFunc(
                        func=random_flip_func, shape=[batchSize], dtype=dt.UINT8, seed=seed_mediapipe)
                    self.random_flip = fn.RandomFlip(horizontal=1)
                    flip = self.random_flip_input()
                    images = self.random_flip(images, flip)
                elif isinstance(t, transforms.RandomVerticalFlip):
                    # random_flip_fn = rng_for_flip_function
                    self.random_flip_input = fn.MediaFunc(
                        func=random_flip_func, shape=[batchSize], dtype=dt.UINT8, seed=seed_mediapipe)
                    self.random_flip = fn.RandomFlip(vertical=1)
                    flip = self.random_flip_input()
                    images = self.random_flip(images, flip)

                # elif isinstance(t, transforms.ToTensor):
                #    pass
                else:
                    assert False, "Error: Unsupported transform" + str(type(t))
            transform_count += 1

        if self.cmn_transform_index != None:
            # transforms.Normalize
            t = self.transforms[self.cmn_transform_index]
            #normalize_mean = np.array([(0.485 * 255), (0.456 * 255), (0.406 * 255)], dtype=np.float32)
            #normalize_std = np.array([1 / (0.229 * 255), 1 / (0.224 * 255), 1 / (0.225 * 255)], dtype=np.float32)
            normalize_mean = np.array(
                [t.mean[0] * 255, t.mean[1] * 255, t.mean[2] * 255], dtype=np.float32)
            normalize_std = np.array(
                [1 / (t.std[0] * 255), 1 / (t.std[1] * 255), 1 / (t.std[2] * 255)], dtype=np.float32)
            normalize_scale = 0.03125

            # Define Constant tensors
            self.norm_mean = fn.MediaConst(data=normalize_mean, shape=[
                1, 1, 3], dtype=dt.FLOAT32)
            self.norm_std = fn.MediaConst(data=normalize_std, shape=[
                1, 1, 3], dtype=dt.FLOAT32)
            if crop_cmn == True:
                if self.media_output_dtype == 'uint8':
                    self.cmn = fn.CropMirrorNorm(crop_w=width, crop_h=height, crop_pos_x=cmn_pos_offset,
                                                 crop_pos_y=cmn_pos_offset, crop_d=0, output_scale=normalize_scale, output_zerop=128, dtype=dt.UINT8)
                elif self.media_output_dtype == 'float32':
                    self.cmn = fn.CropMirrorNorm(crop_w=width, crop_h=height, crop_pos_x=cmn_pos_offset,
                                                 crop_pos_y=cmn_pos_offset, crop_d=0, dtype=dt.FLOAT32)
                else:
                    assert False, "Data type not supported by Normalize"
                crop_cmn = False
            else:
                if self.media_output_dtype == 'uint8':
                    self.cmn = fn.CropMirrorNorm(
                        crop_w=width, crop_h=height, crop_d=0, output_scale=normalize_scale, output_zerop=128, dtype=dt.UINT8)
                elif self.media_output_dtype == 'float32':
                    self.cmn = fn.CropMirrorNorm(
                        crop_w=width, crop_h=height, crop_d=0, dtype=dt.FLOAT32)
                else:
                    assert False, "Data type not supported by Normalize"
            mean = self.norm_mean()
            std = self.norm_std()
            images = self.cmn(images, mean, std)

        #self.transpose = fn.Transpose(permutation=[2, 0, 1, 3], tensorDim=4)
        #images = self.transpose(images)
        #self.shape = [self.batchsize, 3, height, width]

        self.setOutputShape(batch_size=batchSize, channel=3,
                            height=height, width=width, layout=lt.NCHW)
        return images, data
