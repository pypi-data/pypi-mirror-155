# datastate

Dataset statistical calculation.

## How to use

```python
from cvds import calc_mean_std, SegLabel

# calculate mean and std from image dataset
msd = calc_mean_std("dataset/image")
print(msd)
"""
output:
{'mean': array([[0.4923597 , 0.4912278 , 0.44912583]], dtype=float32), 'std': array([[0.2124527 , 0.20088832, 0.22155836]], dtype=float32)}
"""

# check label's information
lab_infor = SegLabel("dataset/label", num_classes=4)
print(lab.area)  # area of each category
print(lab.sample)  # number of samples per category
print(lab.index([0, 1, 2, 3]))  # list of path with index category
"""
output:
{'0': 18.079630533854164, '1': 42.78903537326389, '2': 18.866475423177086, '3': 20.26485866970486}
{'0': 5, '1': 8, '2': 4, '3': 6}
['dataset\\label\\45.png', 'dataset\\label\\47.png']
"""
```

## TODO

- [x] calc neam and std (population).

- [x] calc area of each category in segmentation task.

- [ ] calc number of samples per category in classification task.

- [ ] calc anchor size and etc in detection task.

- [ ] add other state calc about dataset.
