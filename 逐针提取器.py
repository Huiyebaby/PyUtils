import os
import cv2
import windnd
import tkinter
 
def video_to_imgs(sourceFileName):
        video_path = os.path.join("", "", sourceFileName+'.MP4')
        times=0
        frameFrequency=4 #在此处更改每X帧截取一张
        outPutDirName=''+sourceFileName+'\\'
        if not os.path.exists(outPutDirName):
                os.makedirs(outPutDirName) 
        camera = cv2.VideoCapture(video_path)
        while True:
                times+=1
                res, image = camera.read()
                if not res:
                        break
                if times%frameFrequency==0:
                        cv2.imencode('.jpg', image)[1].tofile(outPutDirName + str(times)+'.jpg')
                        print(outPutDirName + str(times)+'.jpg')
        camera.release()
        print('已输出至' + sourceFileName + '\\')
def accept_video(files):
        print(files[0][0:-4].decode('GBK'))
        video_to_imgs(files[0][0:-4].decode('GBK'))
tk = tkinter.Tk()
tk.wm_attributes('-topmost',1)
tk.title("视频逐帧提取丨吾爱破解")
windnd.hook_dropfiles(tk, func=accept_video)
tk.mainloop()