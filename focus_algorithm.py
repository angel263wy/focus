import numpy as np
import glob

'''
对焦算法
用brenner梯度函数 求相邻两个像元灰度之差

对于0度视场 取窗口（136,223）--（164,282）  （X,Y）表示（行，列）
对于30度视场 取窗口（265,238）--（290,287）  （X,Y）表示（行，列） 注意 与S3定义不一致
'''
def cal_brenner(filename, raw_width, raw_height, startX, startY, endX, endY):
    img = np.fromfile(filename, dtype=np.uint16)
    img = np.reshape(img, (raw_height, raw_width))
    img_window = img[startX:endX+1, startY:endY+1]
    window_col, window_row = np.shape(img_window)
    
    # brenner算法 用原矩阵右边补两列零 删除前两列 再两列相减
    # 生成补零矩阵
    tmp = np.zeros((window_col, 2))
    sub_window = np.concatenate((img_window, tmp), axis=1)
    sub_window = np.delete(sub_window, [0, 1], axis=1)  # delete函数 中间的参数为列序号，不是切片
    # 计算结果
    img_window = img_window - sub_window  # 相邻两个元素作差
    img_window = np.delete(img_window, -1, axis=1)  # 删除最后两列减0的数据
    img_window = np.delete(img_window, -1, axis=1)
    res = np.sum(img_window * img_window) # 求和 得到结果

    print('res=',res)
    return res

if __name__ == "__main__":    
    filelist = glob.glob('*.raw')
    if len(filelist):
        for fname in filelist:
            # 中心视场
            foo = cal_brenner(fname, raw_height=380, raw_width=512 ,
                                startX=136, startY=223, endX=164, endY=282)
            # 30度视场
            # foo = cal_brenner(fname, raw_height=380, raw_width=512 ,
            #                     startX=265, startY=238, endX=290, endY=287)
            print('现在处理文件', fname)
            with open('brenner.csv', 'a+') as f:
                f.write(fname + ',' + str(foo) + '\n')
    else:
        print('未找到文件')        

