# Imports
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np
import pickle
from sklearn.cluster import KMeans
import os, shutil, glob, os.path
from PIL import Image as pil_image
image.LOAD_TRUNCATED_IMAGES = True 
model = VGG16(weights='imagenet', include_top=False)

# Variables
imdir = './splited' # DIR containing images
targetdir = "./clustered" # DIR to copy clustered images to
number_clusters = 9

# Loop over files and get features
filelist = glob.glob(os.path.join(imdir, '*.png'))
filelist.sort()
featurelist = []
for i, imagepath in enumerate(filelist):
    try:
        print("    Status: %s / %s" %(i, len(filelist)), end="\r")
        img = image.load_img(imagepath, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        features = np.array(model.predict(img_data))
        featurelist.append(features.flatten())
    except Exception as e:
        print(e)
        continue

print("done")
# Clustering
kmeans = KMeans(n_clusters=number_clusters, random_state=0).fit(np.array(featurelist))
with open("model.pkl", "wb") as f:
    pickle.dump(kmeans, f)

print("done kmeans")
# Copy images renamed by cluster 
# Check if target dir exists
try:
    print('targetdir %s'%targetdir)
    os.makedirs(targetdir)
except OSError:
    print("mkdir error")
    pass
# Copy with cluster name
print("\n")
for i, m in enumerate(kmeans.labels_):
    try:
        print("    Copy: %s / %s" %(i, len(kmeans.labels_)), end="\r")
        shutil.copy(filelist[i], targetdir + "/" + str(m) + "_" + str(i) + ".png")
    except Exception as e:
        print(e)
        continue
