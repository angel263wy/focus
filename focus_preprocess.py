import numpy as np
import glob
import struct
'''
对焦预处理程序
用于图像求平均 扣本底 校正帧转移
对443 490P2 565 670P2波动进行预处理
每一个垫片厚度 形成4个预处理后的文件
文件夹名称需要包含垫片厚度信息
'''


'''
求图像平均值函数
返回值：np列表 宽×高个元素
'''
def get_mean_img(filelist, width, height):
    #生成空数组 并导入图像
    raw_data = np.empty([len(filelist), width*height], dtype=np.uint16)
    for i, filename in enumerate(filelist):
        raw_data[i] = np.fromfile(filename, dtype=np.uint16)
        print('导入图像'+str(i)+': '+filename)
    
    return np.mean(raw_data, axis=0)

'''
帧转移校正
算法：取最先转移的前N行，每列求平均，再用正常图像相同列减去平均值  
注意：np中x表示列 y表示行
输入：img---np列表 宽×高个元素
'''
def disposal_smearing(img, width, height):
    raw_data = np.reshape(img, (raw_height, raw_width))
    
    # 取暗行数据 提取前10行暗行数据    
    dark_lines = raw_data[0:10, :]
    # 暗行求平均
    dark_lines_mean = np.mean(dark_lines, axis=0)
    # 帧转移校正 按行扣暗行平均值 广播算法 矩阵每行减去向量 并扣除负值
    raw_data = np.clip(raw_data - dark_lines_mean, 0, 65530)
    
    return raw_data



# raw文件输出
def raw_file_output(fname, raw_data):
    raw_data= raw_data.flatten()
    with open(fname, 'wb') as f:
        raw_data = np.clip(raw_data, 0, 65536)  # 除去负数
        for i in raw_data:
            foo = struct.pack('H', int(i))
            f.write(foo)

'''
主函数 
需要修改的参数为宽、高、垫片厚度
thinkness为垫片厚度 str类型 文件夹需要包含厚度
'''
if __name__ == "__main__":
    raw_width = 512
    raw_height = 380
    thinkness = '2.85'
    # 本底图像获取
    darkfile = glob.glob('*_'+ thinkness +'*/RAW*/DPC*_8.raw') 
    img_dark = get_mean_img(darkfile, raw_width, raw_height)
    
    #490P2图像处理
    band490 = glob.glob('*_'+ thinkness +'*/RAW*/DPC*_2.raw')
    img490 = get_mean_img(band490, raw_width, raw_height)  # 求平均    
    img490 = img490 - img_dark  # 扣本底    
    img490 = disposal_smearing(img490, raw_width, raw_height)  # 帧转移校正
    raw_file_output('490P2-'+thinkness+'.raw', img490)
    
    #565图像处理
    band565 = glob.glob('*_'+ thinkness +'*/RAW*/DPC*_4.raw')
    img565 = get_mean_img(band565, raw_width, raw_height)  # 求平均    
    img565 = img565 - img_dark  # 扣本底    
    img565 = disposal_smearing(img565, raw_width, raw_height)  # 帧转移校正
    raw_file_output('565-'+thinkness+'.raw', img565)
    
    #670P2图像处理
    band670 = glob.glob('*_'+ thinkness +'*/RAW*/DPC*_4.raw')
    img670 = get_mean_img(band670, raw_width, raw_height)  # 求平均    
    img670 = img670 - img_dark  # 扣本底    
    img670 = disposal_smearing(img670, raw_width, raw_height)  # 帧转移校正
    raw_file_output('670P2-'+thinkness+'.raw', img670)
    
    #443图像处理
    band443 = glob.glob('*_'+ thinkness +'*/RAW*/DPC*_4.raw')
    img443 = get_mean_img(band443, raw_width, raw_height)  # 求平均    
    img443 = img443 - img_dark  # 扣本底    
    img443 = disposal_smearing(img443, raw_width, raw_height)  # 帧转移校正
    raw_file_output('443-'+thinkness+'.raw', img443)
    
    
    print('end')