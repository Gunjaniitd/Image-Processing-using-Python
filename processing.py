import math

# name: File path of the pgm image file
# Output is a 2D list of integers
def readpgm(name):                                                 
	image = []
	with open(name) as f:
		lines = list(f.readlines())
		if len(lines) < 3:
			print("Wrong Image Format\n")
			exit(0)

		count = 0
		width = 0
		height = 0
		for line in lines:
			if line[0] == '#':
				continue

			if count == 0:
				if line.strip() != 'P2':
					print("Wrong Image Type\n")
					exit(0)
				count += 1
				continue

			if count == 1:
				dimensions = line.strip().split(' ')
				# print(dimensions)
				width = dimensions[0]
				height = dimensions[1]
				count += 1
				continue

			if count == 2:	
				allowable_max = int(line.strip())
				if allowable_max != 255:
					print("Wrong max allowable value in the image\n")
					exit(0)
				count += 1
				continue

			data = line.strip().split()
			data = [int(d) for d in data]
			image.append(data)
	return image	

# img is the 2D list of integers
# file is the output file path
def writepgm(img, file):
        with open(file, 'w') as fout:
                if len(img) == 0:
                        pgmHeader = 'p2\n0 0\n255\n'
                else:
                        pgmHeader = 'P2\n' + str(len(img[0])) + ' ' + str(len(img)) + '\n255\n'
                        fout.write(pgmHeader)
                        line = ''
                        for i in img:
                                for j in i:
                                        line += str(j) + ' '
                                line += '\n'
                fout.write(line)

# performs smoothening of image 
def avgfilter(img):
        h=len(img)
        w=len(img[0])
        a=[[0 for i in range(w)] for j in range(h)]
        
        for i in range(w):
                a[0][i]=img[0][i]
                
        for i in range(w):
                a[h-1][i]=img[h-1][i]

        for i in range(h):
                a[i][0]=img[i][0]

        for i in range(h):
                a[i][w-1]=img[i][w-1]

        for i in range(1,h-1):
                for j in range(1,w-1):
                        a[i][j]=int(round((img[i-1][j-1]+img[i-1][j]+img[i-1][j+1]+img[i][j-1]+img[i][j]+img[i][j+1]+img[i+1][j-1]+img[i+1][j]+img[i+1][j+1])/9))
        return a

# performs edge detectionn in the image
def edgedetection(img):        
        h=len(img)
        w=len(img[0])
        a=[[0 for i in range(w)] for j in range(h)]
        
        for i in range(h):
                for j in range(w):
                        if i==0 and j==0:
                                x = (img[h-1][w-1]-img[h-1][1]) + 2*(img[0][w-1]-img[0][1]) + (img[1][w-1]-img[1][1])  
                                y = (img[h-1][w-1]-img[1][w-1]) + 2*(img[h-1][0]-img[1][0]) + (img[h-1][1]-img[1][1])  
                                a[i][j] = round(math.sqrt( x**2 + y**2 ))
                        elif i==0 and j!=w-1:
                                x = (img[h-1][j-1]-img[h-1][j+1]) + 2*(img[0][j-1]-img[0][j+1]) + (img[1][j-1]-img[1][j+1])  
                                y = (img[h-1][j-1]-img[1][j-1]) + 2*(img[h-1][j]-img[1][j]) + (img[h-1][j+1]-img[1][j+1])  
                                a[i][j] = round(math.sqrt( x**2 + y**2 ))
                        elif i==0 and j==w-1:
                                x = (img[h-1][j-1]-img[h-1][0]) + 2*(img[0][j-1]-img[0][0]) + (img[1][j-1]-img[1][0])  
                                y = (img[h-1][j-1]-img[1][j-1]) + 2*(img[h-1][j]-img[1][j]) + (img[h-1][0]-img[1][0])  
                                a[i][j] = round(math.sqrt( x**2 + y**2 ))
                        elif j==0 and i!=h-1:
                                x = (img[i-1][w-1]-img[i-1][1]) + 2*(img[i][w-1]-img[i][1]) + (img[i+1][w-1]-img[i+1][1])  
                                y = (img[i-1][w-1]-img[i+1][w-1]) + 2*(img[i-1][0]-img[i+1][0]) + (img[i-1][1]-img[i+1][1])  
                                a[i][j] = round(math.sqrt( x**2 + y**2 ))
                        elif i==h-1 and j==0:
                                x = (img[i-1][w-1]-img[i-1][1]) + 2*(img[i][w-1]-img[i][1]) + (img[0][w-1]-img[0][1])  
                                y = (img[i-1][w-1]-img[0][w-1]) + 2*(img[i-1][0]-img[0][0]) + (img[i-1][1]-img[0][1])  
                                a[i][j] = round(math.sqrt( x**2 + y**2 ))
                        elif i==h-1 and j!=w-1:
                                x = (img[i-1][j-1]-img[i-1][j+1]) + 2*(img[i][j-1]-img[i][j+1]) + (img[0][j-1]-img[0][j+1])  
                                y = (img[i-1][j-1]-img[0][j-1]) + 2*(img[i-1][j]-img[0][j]) + (img[i-1][j+1]-img[0][j+1])  
                                a[i][j] = round(math.sqrt( x**2 + y**2 ))
                        elif i==h-1 and j==w-1:
                                x = (img[i-1][j-1]-img[i-1][0]) + 2*(img[i][j-1]-img[i][0]) + (img[0][j-1]-img[0][0])  
                                y = (img[i-1][j-1]-img[0][j-1]) + 2*(img[i-1][j]-img[0][j]) + (img[i-1][0]-img[0][0])  
                                a[i][j] = round(math.sqrt( x**2 + y**2 ))
                        elif j==w-1:
                                x = (img[i-1][j-1]-img[i-1][0]) + 2*(img[i][j-1]-img[i][0]) + (img[i+1][j-1]-img[i+1][0])  
                                y = (img[i-1][j-1]-img[i+1][j-1]) + 2*(img[i-1][j]-img[i+1][j]) + (img[i-1][0]-img[i+1][0])  
                                a[i][j] = round(math.sqrt( x**2 + y**2 ))       
                        else:        
                                x = (img[i-1][j-1]-img[i-1][j+1]) + 2*(img[i][j-1]-img[i][j+1]) + (img[i+1][j-1]-img[i+1][j+1])  
                                y = (img[i-1][j-1]-img[i+1][j-1]) + 2*(img[i-1][j]-img[i+1][j]) + (img[i-1][j+1]-img[i+1][j+1])  
                                a[i][j] =round(math.sqrt( x**2 + y**2 ))
        mx=0
        for i in a:
                if max(i)>mx:
                        mx=max(i)
        for i in range(h):
                for j in range(w):
                        a[i][j]=int(round((a[i][j])/(mx)*255))
        return a

########## Function Calls ##########

x = readpgm('input.pgm')                 # test.pgm is the image present in the same working directory

y=avgfilter(x)
writepgm(y, 'average.pgm')               # average.pgm is the image obtained after smoothening

z=edgedetection(x)
writepgm(z, 'edge.pgm')                  # test.pgm is the image obtained after edge detection

###################################

