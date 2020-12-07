import torch

# Functions to load and pre-process the images:
from skimage.io import imread
from skimage import img_as_ubyte
from .sigver.sigver.preprocessing.normalize import (
    normalize_image, resize_image,
    crop_center, preprocess_signature)

# Functions to load the CNN model
from .sigver.sigver.featurelearning.models import SigNet

# Functions for plotting:
import matplotlib.pyplot as plt
# %matplotlib inline
plt.rcParams['image.cmap'] = 'Greys'

#
# PRE-PROCESSING
#

def load_signature(path):
  return img_as_ubyte(imread(path, as_gray=True))

original = load_signature('sigver/data/some_signature.png')

#
# Manually normalizing the image following the steps provided in the paper.
# These steps are also implemented in preprocess.normalize.preprocess_signature
#
normalized = 255 - normalize_image(original, (952, 1360))
resized = resize_image(normalized, (170, 242))
cropped = crop_center(resized, (150,220))

# #
# # Visualizing the intermediate steps
# #
# f, ax = plt.subplots(4,1, figsize=(6,15))
# ax[0].imshow(original, cmap='Greys_r')
# ax[1].imshow(normalized)
# ax[2].imshow(resized)
# ax[3].imshow(cropped)

# ax[0].set_title('Original')
# ax[1].set_title('Background removed/centered')
# ax[2].set_title('Resized')
# ax[3].set_title('Cropped center of the image')

# 
# If GPU is available, use it:
# 
device = torch.device('cpu')
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device: {}'.format(device))

# 
# Load the model
# 
state_dict, _, _ = torch.load('sigver/models/signet.pth')
base_model = SigNet().to(device).eval()
base_model.load_state_dict(state_dict)

def test():
  # 
  # Processing multiple images and obtaining feature vectors
  # 
  user1_sigs = [load_signature('sigver/data/test/real{}.png'.format(i)) for i in  [1,2,3,4]]
  user2_sigs = [load_signature('sigver/data/test/fake{}.png'.format(i)) for i in  [1,2]]

  canvas_size = (952, 1360)

  processed_user1_sigs = torch.tensor([preprocess_signature(sig, canvas_size) for sig in user1_sigs])
  processed_user2_sigs = torch.tensor([preprocess_signature(sig, canvas_size) for sig in user2_sigs])

  # #
  # # Shows pre-processed samples of the two users
  # #
  # f, ax = plt.subplots(2,2, figsize=(10,6))
  # ax[0,0].imshow(processed_user1_sigs[0])
  # ax[0,1].imshow(processed_user1_sigs[1])

  # ax[1,0].imshow(processed_user2_sigs[0])
  # ax[1,1].imshow(processed_user2_sigs[1])

  #
  # Inputs need to have 4 dimensions (batch x channels x height x width), and also be between [0, 1]
  #
  processed_user1_sigs = processed_user1_sigs.view(-1, 1, 150, 220).float().div(255)
  processed_user2_sigs = processed_user2_sigs.view(-1, 1, 150, 220).float().div(255)

  # 
  # Obtain the features. Note that you can process multiple images at the same time
  # 
  with torch.no_grad():
    user1_features = base_model(processed_user1_sigs.to(device))
    user2_features = base_model(processed_user2_sigs.to(device))


  #  ----
  #  ----

  #
  # Inspecting the learned features
  #

  print(user1_features.shape)
  print(user2_features.shape)


  print('Euclidean distance between signatures from the same user')
  print(torch.norm(user1_features[0] - user1_features[1]))
  print(torch.norm(user1_features[0] - user1_features[2]))
  print(torch.norm(user1_features[0] - user1_features[3]))
  # print(torch.norm(user2_features[0] - user2_features[1]))


  print('Euclidean distance between signatures from the difference user')
  print(torch.norm(user1_features[0] - user2_features[0]))
  print(torch.norm(user1_features[0] - user2_features[1]))

  print(torch.norm(user1_features[1] - user2_features[0]))
  print(torch.norm(user1_features[1] - user2_features[1]))


  print('Euclidean distance between signatures from different users')
  dists = [torch.norm(u1 - u2).item() for u1 in user1_features for u2 in user2_features]
  print(dists)

  return dists



def get_distance(user_id, filename):
  # 
  # Processing multiple images and obtaining feature vectors
  # 
  user1_sigs = [load_signature('sigver/data/test/real{}.png'.format(i)) for i in  [1,2,3,4]]
  uploaded_sigs = [load_signature(filename)]

  canvas_size = (952, 1360)

  print(uploaded_sigs)

  processed_user1_sigs = torch.tensor([preprocess_signature(sig, canvas_size) for sig in user1_sigs])
  uploaded_sigs = torch.tensor([preprocess_signature(sig, canvas_size) for sig in uploaded_sigs])

  # #
  # # Shows pre-processed samples of the two users
  # #
  # f, ax = plt.subplots(2,2, figsize=(10,6))
  # ax[0,0].imshow(processed_user1_sigs[0])
  # ax[0,1].imshow(processed_user1_sigs[1])

  # ax[1,0].imshow(uploaded_sigs[0])
  # ax[1,1].imshow(uploaded_sigs[1])

  #
  # Inputs need to have 4 dimensions (batch x channels x height x width), and also be between [0, 1]
  #
  processed_user1_sigs = processed_user1_sigs.view(-1, 1, 150, 220).float().div(255)
  uploaded_sigs = uploaded_sigs.view(-1, 1, 150, 220).float().div(255)

  # 
  # Obtain the features. Note that you can process multiple images at the same time
  # 
  with torch.no_grad():
    user_features = base_model(processed_user1_sigs.to(device))
    uploaded_features = base_model(uploaded_sigs.to(device))


  #  ----
  #  ----

  #
  # Inspecting the learned features
  #

  print(user_features.shape)
  print(uploaded_features.shape)

  # print('Euclidean distance between signatures from the same user')
  # print(torch.norm(user_features[0] - user_features[1]))
  # print(torch.norm(user_features[0] - user_features[2]))
  # print(torch.norm(user_features[0] - user_features[3]))
  # # print(torch.norm(uploaded_features[0] - uploaded_features[1]))


  # print('Euclidean distance between signatures from the difference user')
  # print(torch.norm(user_features[0] - uploaded_features[0]))
  # print(torch.norm(user_features[0] - uploaded_features[1]))

  # print(torch.norm(user_features[1] - uploaded_features[0]))
  # print(torch.norm(user_features[1] - uploaded_features[1]))


  print('Euclidean distance between signatures from different users')
  dists = [torch.norm(u1 - u2).item() for u1 in user_features for u2 in uploaded_features]
  print(dists)

  return {
    'dists': dists,
    'file': filename
  }

def analyse(SIGNATURE_IMAGES_PATH, filename):
  # 
  # Processing multiple images and obtaining feature vectors
  # 
  user1_sigs = [load_signature(PATH) for PATH in SIGNATURE_IMAGES_PATH]
  uploaded_sigs = [load_signature(filename)]

  # print(uploaded_sigs)
  canvas_size = (952, 1360)

  processed_user1_sigs = torch.tensor([preprocess_signature(sig, canvas_size) for sig in user1_sigs])
  uploaded_sigs = torch.tensor([preprocess_signature(sig, canvas_size) for sig in uploaded_sigs])

  #
  # Inputs need to have 4 dimensions (batch x channels x height x width), and also be between [0, 1]
  #
  processed_user1_sigs = processed_user1_sigs.view(-1, 1, 150, 220).float().div(255)
  uploaded_sigs = uploaded_sigs.view(-1, 1, 150, 220).float().div(255)

  # 
  # Obtain the features. Note that you can process multiple images at the same time
  # 
  with torch.no_grad():
    user_features = base_model(processed_user1_sigs.to(device))
    uploaded_features = base_model(uploaded_sigs.to(device))


  #  ----
  #  ----

  #
  # Inspecting the learned features
  #

  print(user_features.shape)
  print(uploaded_features.shape)

  print('Euclidean distance between signatures from different users')
  dists = [torch.norm(u1 - u2).item() for u1 in user_features for u2 in uploaded_features]
  print(dists)

  return {
    'dists': dists,
    'file': filename
  }