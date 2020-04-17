import numpy as np
import glob

'''
对焦算法
用方差函数 对所有图像求平均值 再每个像元减去平均值后平方 平方后所有值求和

对于0度视场 取窗口（136,223）--（164,282）  （X,Y）表示（行，列）
对于30度视场 取窗口（265,238）--（290,287）  （X,Y）表示（行，列） 注意 与S3定义不一致
'''
def cal_variance(filename, raw_width, raw_height, startX, startY, endX, endY):
    # 导入图像 转换为矩阵形式后 切片
    img = np.fromfile(filename, dtype=np.uint16)
    img = np.reshape(img, (raw_height, raw_width))
    img_window = img[startX:endX+1, startY:endY+1]
    # 所有像素点求平均
    img_mean = np.mean(img_window)
    # 生成平均值矩阵 便于作差    
    window_col, window_row = np.shape(img_window)
    img_window_mean = img_mean * np.ones((window_col, window_row))
    
    # 作差 平方 求和
    sub_window = img_window - img_window_mean
    res = np.sum(sub_window * sub_window) # 求和 得到结果

    print('res=',res)
    return res

if __name__ == "__main__":    
    # 中心视场
    # x1=136
    # y1=223
    # x2=164
    # y2=282
    # 30度视场
    x1=265
    y1=238
    x2=290
    y2=287
    
    filelist = glob.glob('*.raw')
    if len(filelist):
        for fname in filelist:            
            foo = cal_variance(fname, raw_height=380, raw_width=512 ,
                                startX=x1, startY=y1, endX=x2, endY=y2)
            print('现在处理文件', fname)
            with open('variance.csv', 'a+') as f:
                f.write(fname + ',' + str(foo) + '\n')
    else:
        print('未找到文件')        

