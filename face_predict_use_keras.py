#-*- coding: utf-8 -*-

import cv2
import sys
import gc
from face_train_use_keras import Model

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
        sys.exit(0)
        
    #����ģ��
    model = Model()
    model.load_model(file_path = './model/me.face.model.h5')    
              
    #��ס�����ľ��α߿���ɫ       
    color = (0, 255, 0)
    
    #����ָ������ͷ��ʵʱ��Ƶ��
    cap = cv2.VideoCapture(0)
    
    #����ʶ����������ش洢·��
    cascade_path = "C:Soft/opencv/sources/data/haarcascades/haarcascade_frontalface_alt2.xml"    
    
    #ѭ�����ʶ������
    while True:
        _, frame = cap.read()   #��ȡһ֡��Ƶ
        
        #ͼ��һ������ͼ��㸴�Ӷ�
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #ʹ������ʶ������������������
        cascade = cv2.CascadeClassifier(cascade_path)                

        #���÷�����ʶ����ĸ�����Ϊ����
        faceRects = cascade.detectMultiScale(frame_gray, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))        
        if len(faceRects) > 0:                 
            for faceRect in faceRects: 
                x, y, w, h = faceRect
                
                #��ȡ����ͼ���ύ��ģ��ʶ������˭
                image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                faceID = model.face_predict(image)   
                
                #����ǡ��ҡ�
                if faceID == 0:                                                        
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness = 2)
                    
                    #������ʾ��˭
                    cv2.putText(frame,'me', 
                                (x + 30, y + 30),                      #����
                                cv2.FONT_HERSHEY_SIMPLEX,              #����
                                1,                                     #�ֺ�
                                (255,0,255),                           #��ɫ
                                2)                                     #�ֵ��߿�
                else:
                    pass
                            
        cv2.imshow("who are you", frame)
        
        #�ȴ�10���뿴�Ƿ��а�������
        k = cv2.waitKey(10)
        #�������q���˳�ѭ��
        if k & 0xFF == ord('q'):
            break

    #�ͷ�����ͷ���������д���
    cap.release()
    cv2.destroyAllWindows()