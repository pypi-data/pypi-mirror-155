import numpy as np
from typing import Tuple, List
from PIL import Image


class ImageSegmentationAnnotation:
    """
    Represents the annotations for a single image in an image-segmentation
    data-set. Consists of an array of indices into a table of labels.
    """

    BYTE_PLACE_MULTIPLIER = np.array([list(1 << i for i in reversed(range(8)))], np.uint8)

    def __init__(self, labels: List[str], size: Tuple[int, int]):
        self._labels = list(labels)
        self._size = size
        self._indices: np.ndarray = np.zeros((size[1], size[0]), np.uint16)
        self._indices.flags.writeable = False

        self._is_negative: bool = True
        self._requires_negative_check: bool = False

    @property
    def labels(self) -> List[str]:
        return list(self._labels)

    @labels.setter
    def labels(self, value: List[str]):
        if len(value) < self.max_index:
            raise Exception("Not enough labels provided for current state of indices: %d < %d" % ((len(value), self.max_index)))

        self._labels = list(value)

    @property
    def size(self) -> Tuple[int, int]:
        return self._size

    @property
    def num_labels(self) -> int:
        return len(self._labels)

    @property
    def indices(self) -> np.ndarray:
        return self._indices

    @indices.setter
    def indices(self, value: np.ndarray):
        # Make sure the array is of the correct shape/type
        if value.shape != self._indices.shape:
            raise Exception("Can't change shape of index array: current=%s, supplied=%d" % (str(self._indices.shape), str(value.shape)))
        elif value.dtype != np.uint16:
            raise Exception("Can't change type of index array, must be np.uint16")

        # Make sure there are enough labels for the indices
        if np.max(value) > len(self._labels):
            unique = [str(x) for x in list(np.unique(value))]
            raise Exception("Not enough labels for this array: %d < %d (unique values: %s)" % (len(self._labels), np.max(value), ",".join(unique)))

        self._indices = value
        self._indices.flags.writeable = False
        self._label_images = None

    @property
    def label_images(self):
        """
        Decompresses the annotation layers.

        :return: the dictionary with the layers, key is name of layer
        :rtype: dict
        """
        label_images = dict()
        # Process each label separately
        for label_index, label in enumerate(self.labels, 1):
            # Rows are packed into bytes, so the length must be a multiple of 8
            row_pad = (8 - self.size[0]) % 8
            # Select the pixels which match this label
            selector_array: np.ndarray = (self.indices == label_index)
            # If no pixels match this label, no need to create an image
            if not selector_array.any():
                continue
            # Pad the rows
            selector_array = np.pad(selector_array, ((0, 0), (0, row_pad)))
            # Striate the pixels, 8 to a row (includes packing bits)
            selector_array.resize((selector_array.size // 8, 8), refcheck=False)
            # Multiply each applicable bit by its position value in the byte
            selector_array = selector_array * self.BYTE_PLACE_MULTIPLIER
            # Reduce the individual pixels to a byte per group of 8
            selector_array = np.sum(selector_array, 1, np.uint8, keepdims=True)
            # Create the 1-bit image for the label
            annotation = Image.frombytes("1", self.size, selector_array.tostring())
            # Append the image and its label to the list
            label_images[label] = annotation

        return label_images

    @property
    def max_index(self) -> int:
        return np.max(self._indices)

    @property
    def is_negative(self):
        if self._requires_negative_check:
            self._is_negative = np.sum(self._indices) == 0
            self._requires_negative_check = False

        return self._is_negative
