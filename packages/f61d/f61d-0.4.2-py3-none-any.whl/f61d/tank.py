from PIL import Image as img
import sys
import numpy as np
from gmpy2 import invert
from tqdm import tqdm

def TANK(imgA,imgB):
    siz = imgA.size
    i = img.new("RGBA",siz)
    for w in range(siz[0]):
        for h in range(siz[1]):
            try:
                pA = imgA.getpixel((w,h))
                pB = imgB.getpixel((w,h))
                
                #print(pA,pB,end=' ')
                a = 255 - (pA - pB)
                if a == 0:
                    gray = 0
                else:
                    gray = 255 * pB // a
                #print(gray)
                i.putpixel((w,h),(gray,gray,gray,a))
            except:
                print("Something wrong")
                raise ValueError
            
    return i



def make(imgOuter,imgInner,output):
    a1 = np.array(imgOuter)
    a2 = 255-(255-a1)//2
    img1 = img.fromarray(a2)
    #img1.show()

    #imgInner = img.open("D:\\Pictures\\bh3rd\\2.png").convert('L')
    a2 = np.array(imgInner)
    img2 = img.fromarray(a2//2)
    #img2.show()
    
    OutputImg = TANK(img1,img2)
    OutputImg.save(output)
    print(f'Mirage tank saved as {output}')


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) not in [3,4]:
        print(f'Usage: {sys.argv[0]} [OutImg] [InnerImg] <Output>')
    outimg = img.open(sys.argv[1])
    innerimg = img.open(sys.argv[2])
    if len(sys.argv) == 4:
        output = sys.argv[-1]
    else:
        output = 'output.png'
    
    make(outimg,innerimg,output,processbar=0)
