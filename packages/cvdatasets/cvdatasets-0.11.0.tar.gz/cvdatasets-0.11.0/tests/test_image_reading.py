#!/usr/bin/env python
if __name__ != '__main__': raise Exception("Do not import me!")

import gc
import cv2
import logging
import numpy as np
import tempfile

from PIL import Image
from cvargparse import Arg
from cvargparse import BaseParser
from humanfriendly import format_size
from imageio import imread
from imageio import imwrite
from tqdm import trange

def read_pil(path, mode="RGB", close=False):
	im = Image.open(path, mode="r").convert(mode)

	arr = np.asarray(im, dtype=np.uint8)

	if close:
		im.close()

	return arr

def read_imageio(path, mode="RGB", close=False):
	return imread(path, pilmode=mode)

def read_opencv(path, mode="RGB", close=False):
	mode = dict(
		RGB=cv2.IMREAD_COLOR,
		L=cv2.IMREAD_GRAYSCALE,
	).get(mode)
	return cv2.imread(path, mode)

def gc_collect(verbose=False):
	if not verbose:
		gc.collect()
		return

	objs = {id(obj): str(obj) for obj in gc.get_objects()}
	gc.collect()
	remaining = {id(obj) for obj in gc.get_objects()}

	for i, info in objs.items():
		if i in remaining:
			continue
		print(i, info)


def main(args):

	shape = tuple(args.resolution) + (args.channels,)
	im = np.random.randint(0, 256, size=shape, dtype=np.uint8)

	logging.info(f"Created an image with shape {im.shape} and {format_size(im.nbytes, binary=True)}")

	with tempfile.NamedTemporaryFile(suffix=".jpg") as f:
		logging.info(f"Storing image to {f.name}")
		imwrite(f.name, im)

		readers = dict(
			pil=read_pil,
			imageio=read_imageio,
			opencv=read_opencv,
		)
		logging.info(f"Using {args.read} reading")
		reader = readers.get(args.read)

		for i in trange(args.n_iterations):

			im1 = reader(f.name, close=args.close_image)
			mse = np.sqrt(np.mean((im1/255 - im/255) ** 2))
			assert mse < 1, \
				"Created and read image are not equal!"

			if args.garbage_collect:
				gc_collect()


def parse_args():
	parser = BaseParser()

	parser.add_args([
		Arg("--resolution", "-r", nargs=2, type=int, default=(6000, 4000)),
		Arg("--channels", "-c", type=int, default=3),

		Arg("--n_iterations", "-n", type=int, default=100),
		Arg("--garbage_collect", "-gc", action="store_true"),
		Arg("--close_image", "-ci", action="store_true"),

		Arg("--read", choices=["pil", "imageio", "opencv"], default="pil")
	])

	return parser.parse_args()

def check_objects(phase: str, info: dict):
	if phase == "start": return

	collected = info["collected"]
	logging.info(f"{collected} collected objects")

gc.callbacks.append(check_objects)

main(parse_args())
