# need install some libraries
# the main library --- Pillow
# install page of Pillow : http://pillow-cn.readthedocs.org/zh_CN/latest/installation.html
import base64
from PIL import Image
import os

# make thumb image
def make_thumb(image):
	# thumb image
	width, height = image.size
	size = 300
	# make rect image
	if width > height:
		delta = (width - height) / 2
		box = (delta, 0, delta+height, height)
		region = image.crop(box)
	elif height > width:
		delta = (height - width) / 2
		box = (0, delta, width, delta+width)
		region = image.crop(box)
	else:
		region = image

	thumb = region.resize((size, size), Image.ANTIALIAS)
	thumb = circle(thumb)
	return thumb

#make the cricle of image
def circle(ima):
    size = ima.size
    
    r2 = min(size[0], size[1])
    if size[0] != size[1]:
        ima = ima.resize((r2, r2), Image.ANTIALIAS)
    imb = Image.new('RGBA', (r2, r2),(255,255,255,0))
    pima = ima.load()
    pimb = imb.load()
    r = float(r2/2) 
    for i in range(r2):
        for j in range(r2):
            lx = abs(i-r+0.5) 
            ly = abs(j-r+0.5)
            l  = pow(lx,2) + pow(ly,2)
            if l <= pow(r, 2):
                pimb[i,j] = pima[i,j]
    return imb


# image merge function
def image_merge(image_bg, image_photo, image_barcode):

	if not os.path.exists(image_bg):
		return None
	if not os.path.exists(image_photo):
		return None
	if not os.path.exists(image_barcode):
		return None

	img_bg = Image.open(image_bg)
	img_ph = Image.open(image_photo)
	img_bc = Image.open(image_barcode)

	#merge the photo and bg
	#

	img_ph = make_thumb(img_ph)

	x0 = 0
	y0 = 0
	width = img_ph.size[0]
	height = img_ph.size[1]

	print("photo", width, height)

	#the merge area of bg and photo
	box = (x0, y0, width, height)

	region = img_ph.crop(box)

	#paste the select area of image_photo
	img_bg.paste(region, box)

	#merge the barcode and bg

	img_bc = make_thumb(img_bc)

	x0 = 0
	y0 = 0
	width = img_bc.size[0]
	height = img_bc.size[1]

	print("barcode", width, height)

	#the merge area of bg and barcode
	box = (x0, y0, width, height)
	region = img_bc.crop(box)

	#paste the select area of image_barcode
	img_bg.paste(region, box)

	print("bg",img_bg.size)

	img_bg.save('merge.jpg')

	return image_bg


if __name__ == '__main__':
	image_merge('bg.jpg', 'photo.jpeg', 'barcode.jpeg')
