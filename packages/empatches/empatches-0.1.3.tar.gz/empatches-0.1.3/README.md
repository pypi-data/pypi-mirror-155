
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
 [![Generic badge](https://img.shields.io/badge/Version-0.1.3-<COLOR>.svg)](https://shields.io/) [![Downloads](https://pepy.tech/badge/empatches)](https://pepy.tech/project/empatches)

# Extract and Merge Image Patches (EMPatches)

Extract and Merge image patches for easy, fast and self-contained digital image processing and deep learning model training.

* **Extract** patches
* **Merge** the extracted patches to obtain the original image back.

### *Update 0.1.2*
* Script updated for handeling floating point precision arrays.

## Dependencies

```
python >= 3.6
numpy 
math
```

## Usage

### Extracting Patches
```python
from empatches import EMPatches
import imgviz # just for plotting

# get image either RGB or Grayscale
img = cv2.imread('../penguin.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# load module
emp = EMPatches()
img_patches, indices = emp.extract_patches(img, patchsize=128, overlap=0.2)

# displaying 1st 10 image patches
tiled= imgviz.tile(list(map(np.uint8, img_patches[0:10])),border=(255,0,0))
plt.figure()
plt.imshow(tiled)
```

![alt text](https://github.com/Mr-TalhaIlyas/EMPatches/raw/main/screens/patch.png)

### Image Processing
Now we can perform our operation on each patch independently and after we are done we can merge them back together.

```python
'''
pseudo code
'''
# do some processing, just store the patches in the list in same order
img_patches_processed = some_processing_func(img_patches)
# or run your deep learning model on patches independently and then merge the predictions
img_patches_processed = model.predict(img_patches)
```

### Merging Patches
After processing the patches if you can merge all of them back in original form as follows,
```python
merged_img = emp.merge_patches(img_patches_processed, indices)
# display
plt.figure()
plt.imshow(merged_img.astype(np.uint8))
```
![alt text](https://github.com/Mr-TalhaIlyas/EMPatches/raw/main/screens/merged.png)


## More Examples

For further details and more examples visit my [github](https://github.com/Mr-TalhaIlyas/EMPatches)
