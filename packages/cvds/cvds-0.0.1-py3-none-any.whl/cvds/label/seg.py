import os.path as osp
import glob
import numpy as np
import typing
from PIL import Image


class SegLabel:
    def __init__(self, 
                 dataset_dir: str,
                 num_classes: int,
                 ext: str = "png",
                 ignore: int = 255) -> None:
        """ A class about state label's information in segmentation.

        Args:
            dataset_dir (str): Directory path of labels.
            num_classes (int): Number of classes.
            ext (str, optional): The image extension. Defaults to "png".
            ignore (int, optional): Ignored category index. Defaults to 255.

        Raises:
            FileNotFoundError: Directory path of labels is not exists.
        """
        if not osp.exists(dataset_dir):
            raise FileNotFoundError("{} is not find.".format(dataset_dir))
        self.path_list = glob.glob(osp.join(dataset_dir, ("*." + ext)))
        self.num_classes = num_classes
        self.shape = np.asarray(Image.open(self.path_list[0])).shape
        self.ignore = ignore
        self._init_calc()

    def __len__(self) -> int:
        return len(self.path_list)

    def _init_calc(self) -> None:
        self.area: typing.Dict[str, float] = dict()
        self.sample: typing.Dict[str, int] = dict()
        self.class_index: typing.Dict[tuple, typing.List[str]] = dict()
        for cls in range(self.num_classes):
            self.area[str(cls)] = 0
            self.sample[str(cls)] = 0
        for lab_path in self.path_list:
            lab_path = osp.normpath(lab_path)
            lab = np.asarray(Image.open(lab_path))
            classes = np.unique(lab).tolist()
            if self.ignore in classes:
                classes.remove(self.ignore)
            for cls in classes:
                self.sample[str(cls)] += 1
            classes = tuple(classes)
            if classes not in self.class_index.keys():
                self.class_index[classes] = [lab_path]
            else:
                self.class_index[classes].append(lab_path)
            for cls in range(self.num_classes):
                self.area[str(cls)] += np.sum(lab == cls)
        all_area = self.__len__() * self.shape[0] * self.shape[1]
        for cls in range(self.num_classes):
            self.area[str(cls)] = self.area[str(cls)] / all_area * 100

    def index(self, classes: typing.List[int]) -> typing.List[str]:
        """ Find image path with this classes.

        Args:
            classes (typing.List[int]): The index of classes.

        Returns:
            typing.List[str]: These images path.
        """
        cid = tuple(classes)
        if cid in self.class_index.keys():
            return self.class_index[cid]
        else:
            return []
