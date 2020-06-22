import numpy as np
import cv2
from skimage import filters
import datetime

class Picture:
    def __init__(self, filename):
        self.im = cv2.imread(filename)
        self.width = len(self.im[0])
        self.height = len(self.im)
        grayscale = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        self.energy = filters.sobel(grayscale) 

    def find_seams(self):
        distTo = self.energy.copy()
        edgeTo = np.zeros((self.height, self.width))

        for i in range(1, self.height):
            for j in range(self.width):
                if j == 0:
                    minpath = np.argmin(distTo[i - 1][j:j + 2])
                elif j == self.width - 1:
                    minpath = j + np.argmin(distTo[i - 1][j - 1:j + 1]) - 1
                else:
                    minpath = j + np.argmin(distTo[i - 1][j - 1:j + 2]) - 1
                
                distTo[i][j] = distTo[i - 1][minpath] + self.energy[i][j]
                edgeTo[i][j] = minpath

        return distTo, edgeTo.astype(int)

    def create_mask(self):
        distTo, edgeTo = self.find_seams()
        mask = np.ones((self.height, self.width), dtype = np.bool)
        index = np.argmin(distTo[-1])
        for i in range(self.height - 1, -1, -1):
            if index == 0:
                mask[i][index:index+3] = False   
            elif index == self.width - 1:
                mask[i][index-2:index+1] = False
            else:   
                mask[i][index-1:index+2] = False
            index = edgeTo[i][index]

        return mask

    def remove_seam(self, mask):
        mask = np.stack([mask]*3, axis=2)
        self.im = self.im[mask].reshape(self.height, self.width - 3, 3)
        self.width = self.width - 3
        grayscale = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        self.energy = filters.sobel(grayscale) 

    def highlight(self, mask):
        self.im[mask == False] = [0,0,255]


        
if __name__ == "__main__":
    pic = Picture('./HJoceanSmall.png')
    pic.highlight()
    cv2.waitKey(0)
    '''
    print(pic.im.size)
    iter = len(pic.im[0])//3
    for i in range(iter):
        now = datetime.datetime.now()
        pic.remove_seam()
        then = datetime.datetime.now()
        print(then - now)

    print(pic.im.size)
    cv2.imshow('test', pic.im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''