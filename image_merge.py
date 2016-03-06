# need install some libraries
# the main library --- Pillow
# install page of Pillow : http://pillow-cn.readthedocs.org/zh_CN/latest/installation.html
import base64
from PIL import Image
import os
import urllib2
import cStringIO

photo_width = 176
photo_height = 160

barcode_width = 173
barcode_height = 140


# image merge function
def image_merge(image_bg, photo_url, barcode_url):

	if not os.path.exists(image_bg):
		return None
	# if not os.path.exists(image_photo):
	# 	return None
	# if not os.path.exists(image_barcode):
	# 	return None
	# open the image file 
	img_bg = Image.open(image_bg)

	img_ph = image_load(photo_url)

	img_bc = image_load(barcode_url)

	if not img_ph or not img_bc:
		return None

	bg_width, bg_height = img_bg.size

	# merge the photo with bg
	merge_photo(img_ph, img_bg, 263, 263, photo_width)

	# merge barcode with bg
	merge_barcode(img_bc, img_bg, 290, 953, barcode_width)

	# img_bg.save('merge.jpg')

	return img_bg

# load file based on the url
def image_load(url):
	file = cStringIO.StringIO(urllib2.urlopen(url).read())
	img = Image.open(file)
	return img


#merge photo
def merge_photo(photo, bg, x, y, size):

	width,height = photo.size

	if width > height:
		delta = (width - height)/2
		box = (delta, 0, delta+height, height)
		region = photo.crop(box)
	elif height > width:
		delta = (height - width)/2
		box = (0, delta, width, delta+width)
		region = photo.crop(box)
	else:
		region = photo

	thumb = region.resize((size, size), Image.ANTIALIAS)
	#circle the thumb
	size = thumb.size
	r2 = min(size[0], size[1])
	if size[0] != size[1]:
		thumb = thumb.resize((r2, r2), Image.ANTIALIAS)
	pima = thumb.load()
	pimb = bg.load()

	r = float(r2/2)

	for i in range(r2):
		for j in range(r2):
			lx = abs(i-r+0.5)
			ly = abs(j-r+0.5)
			l = pow(lx, 2) + pow(ly, 2)
			if l <= pow(r, 2):
				pimb[i + x, j + y] = pima[i, j]

# merge barcode
def merge_barcode(barcode, bg, x, y, scale):

	barcode = barcode.resize((scale, scale), Image.ANTIALIAS)

	width, height = barcode.size
	box = (0, 0, width, height)
	region = barcode.crop(box)

	bg.paste(region, (x, y))


if __name__ == '__main__':
	image_merge('bg.jpg', 'https://pbs.twimg.com/profile_images/473506797462896640/_M0JJ0v8.png', 'https://chart.googleapis.com/chart?chl=this+is+a+test+code&chs=200x200&cht=qr&chld=H%7C0')
	print "successed!"