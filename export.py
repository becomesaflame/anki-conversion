# Pull images for an Anki text export into a folder

import argparse
import re
import os
import shutil


mediaDir = '~/.local/share/Anki2/User 1/collection.media' 

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('filename', help="Name of Anki text export file")
  parser.add_argument('export_location', help="Name of folder to export images to")
  return parser.parse_args()


def pullImages(inFile):
  '''
  Read in inFile
  Find all image source strings
  Return a list of image source strings
  '''
  with open(inFile) as f:
    fileRaw = f.read()

  pattern = re.compile('src="".+?"')
  images = []

  for match in re.finditer(pattern, fileRaw): 
    images.append(match.group()[6:-1]) 

  return images

def storeImages(images, folder):
  '''
  Get each image in the list of images and store it in the specified
  folder
  '''

  # Create directory
  try:
    os.mkdir(folder) 
  except OSError as exception: 
    # TODO check if folder is empty and continue if it is
    raise

  # Copy images into directory
  for img in images:
    fullPath = os.path.expanduser(os.path.join(mediaDir, img))
    if (os.path.isfile(fullPath)): 
      shutil.copy(fullPath, folder)
    else:
      print("Error: file " + fullPath + " not found.") 


if __name__ == '__main__':
  args = parseArgs()
  images = pullImages(args.filename) 
  storeImages(images, args.export_location) 

