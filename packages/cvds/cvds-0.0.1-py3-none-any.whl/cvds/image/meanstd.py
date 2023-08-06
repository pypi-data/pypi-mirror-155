import os.path as osp
import glob
import numpy as np
import typing
from PIL import Image


def calc_mean_std(dataset_dir: str, 
                  ext: str = "jpg",
                  channels: int = 3) -> typing.Dict[str, np.ndarray]:
    """ Using to calculate mean/std about images in a directory.

    Args:
        dataset_dir (str): Directory path of images.
        ext (str, optional): The image extension. Defaults to "jpg".
        channels (int, optional): Number of image channels. Defaults to 3.

    Raises:
        FileNotFoundError: Directory path of images is not exists.

    Returns:
        typing.Dict[str, np.ndarray]: The dict about mean/std.
    """
    if not osp.exists(dataset_dir):
        raise FileNotFoundError("{} is not find.".format(dataset_dir))
    img_path_list = glob.glob(osp.join(dataset_dir, ("*." + ext)))
    lens = len(img_path_list)
    means = np.zeros((1, channels), dtype="float32")
    stds = np.zeros((1, channels), dtype="float32")
    # first calc means
    for img_path in img_path_list:
        img = np.asarray(Image.open(img_path)) / 255.
        for c in range(channels):
            means[0, c] += np.mean(img[:, :, c])
    means /= lens
    # secend calc stds
    for img_path in img_path_list:
        img = np.asarray(Image.open(img_path)) / 255.
        for c in range(channels):
            stds[0, c] += np.mean((img[:, :, c] - means[0, c]) ** 2)
    stds = (stds / lens) ** 0.5
    return {"mean": means, "std": stds}
