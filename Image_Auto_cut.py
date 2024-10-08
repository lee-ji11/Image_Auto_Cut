import cv2
import os
import numpy as np 

Data_loc_T = 'Test_img/MALIGNANT'
Data_loc_M = 'Test_img/MALIGNANT_mask'

Save_loc_T = 'Test_img/img_crop/MALIGNANT/'
Save_loc_M = 'Test_img/img_crop/MALIGNANT_mask/'

main_list = os.listdir(Data_loc_T)
mask_list = os.listdir(Data_loc_M)

for ii in mask_list:

    OR_img = cv2.imread(Data_loc_T+'/'+ii)
    mask = cv2.imread(Data_loc_M+'/'+ii, cv2.IMREAD_GRAYSCALE)
    img_h, img_w = mask.shape 
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    total_point = list()
    Min_point_x, Min_point_y, Max_point_x, Max_point_y = 10000, 10000,0,0

    for i in range(len(contours)):
        contours_min = np.argmin(contours[i], axis = 0)
        contours_max = np.argmax(contours[i], axis = 0)

        # print("x-Min =", contours[i][contours_min[0][0]][0][0])
        # print("y-Min =", contours[i][contours_min[0][1]][0][1])
        # print("x-Max =", contours[i][contours_max[0][0]][0][0])
        # print("y-Max =", contours[i][contours_max[0][1]][0][1])
        # print('--------------------------------------------')

        x_Min = contours[i][contours_min[0][0]][0][0]
        y_Min = contours[i][contours_min[0][1]][0][1]
        x_Max = contours[i][contours_max[0][0]][0][0]
        y_Max = contours[i][contours_max[0][1]][0][1]

        if x_Min < Min_point_x:
            Min_point_x = x_Min.copy()
        if y_Min < Min_point_y:
            Min_point_y = y_Min.copy()

        if x_Max > Max_point_x:
            Max_point_x = x_Max.copy()
        if y_Max > Max_point_y:
            Max_point_y = y_Max.copy()
        total_point.append([x_Min,y_Min,x_Max,y_Max])

    # cv2.rectangle(mask, (Min_point_x, Min_point_y),(Max_point_x, Max_point_y), (0,255,0), 10)

    x_length = Max_point_x-Min_point_x
    y_length = Max_point_y-Min_point_y
    print('x_length, y_length:',x_length, y_length)

    if x_length > y_length:
        print('a')
        Minx = Min_point_x-10
        Miny = Min_point_y-((x_length-y_length)/2)-10
        Maxx = Max_point_x+10
        Maxy = Max_point_y+((x_length-y_length)/2)+10
        # print('a',Min_point_x-10, Min_point_y-((x_length-y_length)/2),Max_point_x+10, Max_point_y+((x_length-y_length)/2))
        # cv2.rectangle(mask, (Minx,int(Miny)),(Maxx,int(Maxy)), (255,0,0), 10)
    elif x_length < y_length:
        print('b')
        Minx = Min_point_x-((y_length-x_length)/2)-10
        Miny = Min_point_y-10
        Maxx = Max_point_x+((y_length-x_length)/2)+10
        Maxy = Max_point_y+10
        # print('b',Min_point_x-((y_length-x_length)/2), Min_point_y-10,Max_point_x-((y_length-x_length)/2), Max_point_y+10)
        # cv2.rectangle(mask, (int(Minx),Miny),(int(Maxx),Maxy), (255,0,0), 10)
    # print('ori_loc:',Minx, Miny, Maxx, Maxy)
    elif x_length == y_length:
        print('c')
        Minx = Min_point_x-10
        Miny = Min_point_y-10
        Maxx = Max_point_x+10
        Maxy = Max_point_y+10
    
    print(ii)

    if Minx <0 and Miny < 0 and Maxx < img_w and Maxy < img_h:
        print('aa')
        print('ori_loc:',Minx, Miny, Maxx, Maxy)
        print(0, 0, int(Maxx-Minx), int(Maxy-Miny))
        mask = mask[0:int(Maxy-Miny), 0:int(Maxx-Minx)]
        OR_img = OR_img[0:int(Maxy-Miny), 0:int(Maxx-Minx)]
        # cv2.rectangle(mask, (0, 0), (int(Maxx-Minx), int(Maxy-Miny)), (0,0,255), 10)
    elif Minx <0 and Miny > 0 and Maxx < img_w and Maxy < img_h:
        print('bb')
        print('ori_loc:',Minx, Miny, Maxx, Maxy)
        print(0, Miny, int(Maxx-Minx), Maxy)
        mask = mask[int(Miny):int(Maxy), 0:int(Maxx-Minx)]
        OR_img = OR_img[int(Miny):int(Maxy), 0:int(Maxx-Minx)]
        # cv2.rectangle(mask, (0, Miny),(int(Maxx-Minx), Maxy), (0,0,255), 10)
    elif Minx <0 and Miny > 0 and Maxx < img_w and Maxy > img_h:
        print('cc')
        print('ori_loc:',Minx, Miny, Maxx, Maxy)
        print(0, int(Miny-(Maxy-img_h)), int(Maxx-Minx), img_h)
        mask = mask[int(Miny-(Maxy-img_h)):img_h, 0:int(Maxx-Minx)]
        OR_img = OR_img[int(Miny-(Maxy-img_h)):img_h, 0:int(Maxx-Minx)]
        # cv2.rectangle(mask, (0, int(Miny-(Maxy-img_h))),(int(Maxx-Minx), img_h), (0,0,255), 10)
    elif Minx > 0 and Miny<0 and Maxx < img_w and Maxy < img_h:
        print('dd')
        print('ori_loc:',Minx, Miny, Maxx, Maxy)
        print(Minx, 0, Maxx, int(Maxy-Miny))
        mask = mask[0:int(Maxy-Miny), Minx:Maxx]
        OR_img = OR_img[0:int(Maxy-Miny), Minx:Maxx]
        # cv2.rectangle(mask, (Minx, 0), (Maxx, int(Maxy-Miny)), (0,0,255), 10)
    elif Minx > 0 and Miny>0 and Maxx < img_w and Maxy > img_h:
        print('ee')
        print('ori_loc:',Minx, Miny, Maxx, Maxy)
        print(Minx, int(Miny-(Maxy-img_h)), Maxx, img_h)
        mask = mask[int(Miny-(Maxy-img_h)):img_h, Minx:Maxx]
        OR_img = OR_img[int(Miny-(Maxy-img_h)):img_h, Minx:Maxx]
        # cv2.rectangle(mask, (Minx, int(Miny-(Maxy-img_h))), (Maxx, img_h), (0,0,255), 10)
    else:
        print('ff')
        print('ori_loc:',Minx, Miny, Maxx, Maxy)
        print(Minx, Miny, Maxx, Maxy)
        mask = mask[int(Miny):int(Maxy), int(Minx):int(Maxx)]
        OR_img = OR_img[int(Miny):int(Maxy), int(Minx):int(Maxx)]
        # cv2.rectangle(mask, (int(Minx),int(Miny)),(int(Maxx),int(Maxy)), (255,0,0), 10)

    cv2.imwrite(Save_loc_T+ii, OR_img)
    cv2.imwrite(Save_loc_M+ii, mask)
    print('--------------------------------------------')




    # if Minx <0 and Miny > 0:
    #     print('aa')
    #     print(Minx, Miny, Maxx, Maxy)
    #     print(0, Miny, int(Maxx-Minx), Maxy)
    #     mask = mask[Miny:Maxy, 0:int(Maxx-Minx)]
    #     OR_img = OR_img[Miny:Maxy, 0:int(Maxx-Minx)]
    #     # cv2.rectangle(mask, (0, Miny),(int(Maxx-Minx), Maxy), (0,0,255), 10)
    # elif Miny <0 and Minx >0:
    #     print('bb')
    #     print(Minx, Miny, Maxx, Maxy)
    #     print(Minx, 0, Maxx, int(Maxy-Miny))
    #     mask = mask[0:int(Maxy-Miny), 0:Maxx]
    #     OR_img = OR_img[0:int(Maxy-Miny), 0:Maxx]
    #     # cv2.rectangle(mask, (Minx, 0), (Maxx, int(Maxy-Miny)), (0,0,255), 10)
    # elif Minx <0 and Miny < 0:
    #     print('cc')
    #     print(Minx, Miny, Maxx, Maxy)
    #     print(0, 0, int(Maxx-Minx), int(Maxy-Miny))
    #     mask = mask[0:int(Maxy-Miny), 0:int(Maxx-Minx)]
    #     OR_img = OR_img[0:int(Maxy-Miny), 0:int(Maxx-Minx)]
    #     # cv2.rectangle(mask, (0, 0), (int(Maxx-Minx), int(Maxy-Miny)), (0,0,255), 10)
    # else:
    #     mask = mask[int(Miny):int(Maxy), int(Minx):int(Maxx)]
    #     OR_img = OR_img[int(Miny):int(Maxy), int(Minx):int(Maxx)]
    #     # cv2.rectangle(mask, (int(Minx),int(Miny)),(int(Maxx),int(Maxy)), (255,0,0), 10)


    # cv2.imwrite('img_crop/MALIGNANT/'+ii, OR_img)
    # cv2.imwrite('img_crop/MALIGNANT_mask/'+ii, mask)
