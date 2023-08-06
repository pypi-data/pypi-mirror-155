from habana_frameworks.mediapipe.media_types import ftype as ft

# INFO: Here we will give params and its default arguments order doesnt matter
# INFO: if any parameter is not set here it will be set to zero

image_decoder_params = {
    'output_format': 'rgb-i',
    'resize': [0, 0],  # for height,width
    'filter': ft.BI_LINEAR,
    'enable_random_crop': 0x0,
    'scale_min': 0,
    'scale_max': 0,
    'ratio_min': 0,
    'ratio_max': 0,
    'seed': 0}
