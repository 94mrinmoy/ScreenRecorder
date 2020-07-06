import time
import cv2
import mss
import numpy
import os
import keyboard
import ctypes
import pyautogui as pa
from pynput.mouse import Listener

flag = False
def on_click(x, y, button, pressed):
    # print(x, y, button, pressed,flag)
    if pressed:
        global xLeft 
        global xTop 
        global yLeft 
        global yTop
        if flag==True:
            xLeft = x
            xTop = y
        elif flag==False:
            yLeft = x
            yTop = y
        print('Clicked ! ') #in your case, you can move it to some other pos
        return False


# with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
#     listener.join()

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
filename = input('Give the file name - ')
filename = filename + '.avi'
# monitor = {'top': 0, 'left': 0, 'width': 1366, 'height': 768}
monitor = {'top': 0, 'left': 0, 'width' :screensize[0], 'height': screensize[1]}
img_array = []
# size = (monitor['width'],monitor['height'])
choice = input("For Full dcreen recording press y and for custom size press n : ")
if choice.casefold() == "y" :
    size = screensize
elif choice.casefold() == "n" :    
    print ("click on the top left corner : ")
    flag = True
    with Listener( on_click=on_click) as listener:
        listener.join()

    print ("click on the down right corner : ")
    flag=False
    with Listener( on_click=on_click) as listener:
        listener.join()    

    width = yLeft-xLeft
    height = yTop - xTop    
    monitor = {'top': xTop, 'left': xLeft, 'width' :width, 'height': height}   
    size = (width,height) 
    
# out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*'DIVX'), 19, size)
out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc('M','P','E','G'), 20, size)
# out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc('H', '2', '6', '4'), 19, size)
# cap.set(CV_CAP_PROP_FOURCC, CV_FOURCC('H', '2', '6', '4'));
# fourcc = cv2.VideoWriter_fourcc(*'XVID')

# out = cv2.VideoWriter('output.avi', -1, 1, size)
image_folder = 'temp'
with mss.mss() as sct:
    # Part of the screen to capture
    
    # 
    count = 0
    print('screen recording started..')
    while 'Screen capturing':
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Display the picture
        # 

        # height, width, layers = img.shape
        # global size
        # size = (width,height)
        # img_array.append(img)
        # cv2.imshow('OpenCV/Numpy normal', img)
        # cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        cv2.imwrite('temp/' + str(count) + '.jpg', img)
        f = image_folder + '/'+str(count)+'.jpg'
        out.write(cv2.imread(f))
        os.remove(f)
        count = count + 1
        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        # cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        # print('fps: {0}'.format(1 / (time.time()-last_time)))

        # Press "q" to quit
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            print('You Pressed q Key!')
            print('screen recording ended..')
            break 
    # print(img_array)


    image_folder = 'temp' # make sure to use your folder 
      
    # images = [img for img in os.listdir(image_folder) 
    #           if img.endswith(".jpg") or
    #              img.endswith(".jpeg") or
    #              img.endswith("png")] 

    
    # print(images)
    # for i in range(count):
    #     f = image_folder + '/'+str(i)+'.jpg'
    #     out.write(cv2.imread(f))
    #     os.remove(f)
    out.release()
