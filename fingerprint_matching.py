from struct import pack, unpack
import numpy as np
import itertools

def vectorized_result(j):
    """Return a 10-dimensional unit vector with a 1.0 in the jth
    position and zeroes elsewhere.  This is used to convert a digit
    (0...9) into a corresponding desired output from the neural
    network."""
    e = np.zeros((2, 1))
    e[j] = 1.0
    return e

def rot2(a):
	n = len(a)
	c = (n+1) / 2
	f = n / 2
	for x in range(c):
		for y in range(f):
			a[x][y] = a[x][y] ^ a[n-1-y][x]
			a[n-1-y][x] = a[x][y] ^ a[n-1-y][x]
			a[x][y] = a[x][y] ^ a[n-1-y][x]

			a[n-1-y][x] = a[n-1-y][x] ^ a[n-1-x][n-1-y]
			a[n-1-x][n-1-y] = a[n-1-y][x] ^ a[n-1-x][n-1-y]
			a[n-1-y][x] = a[n-1-y][x] ^ a[n-1-x][n-1-y]

			a[n-1-x][n-1-y] = a[n-1-x][n-1-y]^a[y][n-1-x]
			a[y][n-1-x] = a[n-1-x][n-1-y]^a[y][n-1-x]
			a[n-1-x][n-1-y] = a[n-1-x][n-1-y]^a[y][n-1-x]
	return a

class FingerprintImage:
	def __init__(self, file_name):
		self.image_file_path = file_name
		self.width = 0
		self.height = 0
		self.pixels = []
		self.offset = 0
		self.raw_data = None
		self.load_data()
	def load_data(self):
		#self.image_file_path = 'images/identify_2016-02-26_23-52-09_00.bmp'
		image_file = open(self.image_file_path, 'rb')
		image_raw_data = image_file.read()
		self.raw_data = image_raw_data
		image_file.close()
		# First obtain each field from the header. This usually goes up to the first 14 bytes.
		header_type = unpack('<h', image_raw_data[:2])[0]
		header_size = unpack('<i', image_raw_data[2:6])[0]
		header_reserved = unpack('<hh', image_raw_data[6:10])
		header_offset = unpack('<i', image_raw_data[10:14])[0]
		self.offset = header_offset
		# Now obtain the information which is the next 4o bytes.
		info_size = unpack('<i', image_raw_data[14:18])[0]
		info_width = unpack('<i', image_raw_data[18:22])[0]
		info_height = unpack('<i', image_raw_data[22:26])[0]
		# Set up local variables right here
		self.width = info_width
		self.height = info_height
		# End of setting up local variables
		info_planes = unpack('<h', image_raw_data[26:28])[0]
		info_bits = unpack('<h', image_raw_data[28:30])[0]
		info_compression = unpack('<i', image_raw_data[30:34])[0]
		info_imagesize = unpack('<i', image_raw_data[34:38])[0]
		info_xresolution, info_yresolution = unpack('<ii', image_raw_data[38:46])
		info_ncolors = unpack('<i', image_raw_data[46:50])[0]
		info_importantcolors = unpack('<i', image_raw_data[50:54])[0]
		pixel_data = image_raw_data[header_offset:]
		pixels = [ [  0 for j in range(self.width) ] for i in range(self.height) ]
		# Going to loop over the pixels.
		currentIndex = 0
		for i in range(self.height):
			for j in range(self.width):
				pixels[i][j] = unpack('<B', pixel_data[currentIndex: currentIndex + 1])[0]
				currentIndex = currentIndex + 1
		self.pixels = pixels
	def rotate(self):
		print len(self.pixels)
		print len(self.pixels[0])
		#print self.pixels
		#rotated = list(reversed(zip(*self.pixels)))
		self.pixels = np.rot90(self.pixels)
		#print self.pixels
		image_file = open(self.image_file_path, 'wb')
		image_file.write(self.raw_data[:self.offset])
		for pixel_array in self.pixels:
			for pixel in pixel_array:
				image_file.write(pack('<B', pixel))
		image_file.close()


