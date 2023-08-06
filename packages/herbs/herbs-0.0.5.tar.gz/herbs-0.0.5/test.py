from Archived.HERBS.herbs import *
run_herbs()

import imagecodecs
import tifffile
image_file_path = '/Users/jingyig/Work/Kavli/Data/HERBS_DATA/test_image_type/section_28.tif'

img_data = tifffile.imread(image_file_path)




p1 = np.array([[0, 0], [200, 0], [200, 100], [0, 100], [50, 25]])

p2 = np.array([[0, 80], [200, 80], [200, 0], [0, 0], [50, 60]])

p4 = p2.copy()
p4[:, 1] = 80 - p2[:, 1]

p3 = np.array([[0, 0], [200, 0], [200, 80], [0, 80], [50, 20]])

from skimage import io, transform
t = transform.ProjectiveTransform()
t.estimate(np.float32(p4), np.float32(p1))
# aaa = t.params
img_shape = a.shape
#
# t.estimate(np.float32(p3), np.float32(p1))
# bbb = t.params
img_hist_tempo = np.asanyarray(a)
img_warped = transform.warp(img_hist_tempo, t, output_shape=(img_shape[1], img_shape[0]), order=1, clip=False)


plt.subplot(1, 2, 1)
plt.imshow(a)
plt.subplot(1, 2, 2)
plt.imshow(img_warped)
plt.show()



import herbs
run_herbs()