import numpy as np
import os
import warnings

path_ = os.path.dirname(os.path.realpath(__file__))


class imgshape():
    def __init__(self, img):
        self.info = img.shape
        self.img = img

    def flatten(self):
        return self.img.reshape([-1, self.info[-1]])

    def inv_flatten(self, img2):
        return img2.reshape(list(self.info[:2]) + [-1])

def block_extract(img, row, line, inc, r):
    value = []
    scale = int(r / 3)
    c, l, s = img.shape
    for i in range(row):
        for j in range(line):
            x, y = r + i * (inc + 2 * r), j * (inc + 2 * r) + r

            box = img[x - scale:x + scale, y - scale:y + scale]
            value.append(np.mean(box.reshape([-1, s]), axis=0))
    return np.asarray(value)

def downsample(img, scale, type='spatial', band2=np.array(range(400, 710, 10)),Band = np.arange(400,710,10)):
    '''
        :img 被下采样图像
        :scale 下采样因子，如2，即原图像长宽各缩小2倍
        :type spatial/spectral 可选 分别表示空间和光谱下采样。当进行光谱维度重采样时，需要填入参数band2与Band。
        最后更新：2021年9月15日 曹栩珩

    '''

    if type.lower() == 'spatial':
        img = img[scale-1::scale,scale-1::scale]

    elif type.lower() == 'spectral_iq':
        '''
        Specim-IQ 专用； 由397~780 超至 任意维度
        需要传入band2 列表，进行插值
        '''
        Band = np.array(
            [397.32, 400.2, 403.09, 405.97, 409, 412, 415, 418, 420, 423, 426, 429, 432, 435, 438, 441, 443, 446, 449,
             452, 455, 458,
             461, 464, 467, 469, 472, 476, 478, 481, 484, 487, 490, 493, 496, 499, 502, 505, 508, 510, 513, 516, 519,
             522, 525, 528, 531, 534, 537, 540, 543, 545, 548, 551, 554, 557, 560, 563, 566, 569, 572, 575, 577, 581,
             584, 587, 590, 593, 596, 599, 602, 605, 607, 610, 613, 616, 619, 622, 625, 628, 631, 634, 637, 640, 643,
             646, 649, 652, 655, 658, 661, 664, 666, 669, 672, 676, 679, 682, 685, 688, 691, 694, 697, 700, 702.58,
             705.57, 708.57, 711.56, 714.55, 717.54, 720.54, 723.53, 726.53, 729.53, 732.53, 735.53, 738.53, 741.53,
             744.53, 747.54, 750.54,
             753.55, 756.56, 759.56, 762.57, 765.58, 768.6, 771.61, 774.62, 777.64, 780.65])

        _img = imgshape(img)
        img = _img.flatten()

        img_ = np.empty([img.shape[0]] + list(band2.shape))
        for x in range(img.shape[0]):
            img_[x] = np.interp(band2, Band, img[x])

        img = _img.inv_flatten(img_)

    elif type.lower() == 'spectral':
        '''
        对光谱图像进行光谱维度上采样
        '''

        _img = imgshape(img)
        img = _img.flatten()

        img_ = np.empty([img.shape[0]] + list(band2.shape))
        for x in range(img.shape[0]):
            img_[x] = np.interp(band2, Band, img[x])

        img = _img.inv_flatten(img_)

    return img

def square_(n):
    import math
    i = int(math.sqrt(n))
    j = int(n / i)
    erro = n - i * j
    ind = 0

    while erro % i != 0 and erro % j != 0:
        if ind % 2 == 0:
            i -= 1
        else:
            j -= 1
        erro = n - i * j
        ind += 1

    if erro % i == 0:
        j += erro / i
    else:
        i += erro / j
    return (int(i), int(j))

class cvtcolor():
    def __init__(self,illuminant='d65'):
        if type(illuminant) is not str:
            raise TypeError(
                f'illuminant期望是字符串类型，然而输入类型为{type(illuminant)}。\n可选光源【A/B/C/D50/D55/D65/D75】。\n 例如：选择D55光源时传入illuminant=\'d65\'')

        self.illuminant = illuminant
    def lab2xyz(self, lab,):
        s_xyz = spectra(self.illuminant).sxyz()
        w = np.sum(s_xyz,axis=0).reshape([1,1,3])
        w/=w[:,:,1]
        T = 4 / 29
        __xyz = np.empty(lab.shape)
        __xyz[:, :, 1] = (1 / 116) * (lab[:, :, 0] + 16)
        __xyz[:, :, 0] = __xyz[:, :, 1] + (1 / 500) * lab[:, :, 1]
        __xyz[:, :, 2] = __xyz[:, :, 1] - (1 / 200) * lab[:, :, 2]
        fxyz = np.empty(lab.shape)
        fxyz[__xyz > T] = __xyz[__xyz > T] ** 3
        fxyz[__xyz <= T] = 3 * T ** 2 * (__xyz[__xyz <= T] - T)
        return fxyz * w

    def lab2rgb(self,lab,space = 'srgb'):
        xyz = self.lab2xyz(lab)
        if space.lower() =='srgb':
            return self.xyz2srgb(xyz)
        elif space.lower() =='adobergb':
            return  self.xyz2adrgb(xyz)

    def rgb2xyz(self,img_,type ='srgb'):
        wp = self.illuminant
        info = img_.shape
        img = img_.reshape([-1, 3])
        if type.lower() =='srgb' or type.lower() =='apple' or type.lower() =='adp3' or type.lower() =='apple display p3' or type.lower() =='display p3':

            if type.lower() =='srgb':
                trans = np.array([[0.4124564, 0.3575761, 0.1804357],
                                  [0.2126729, 0.7151522, 0.0721750],
                                  [0.0193339, 0.1191920, 0.9503041]])
            elif type.lower() == 'apple' or type.lower() == 'adp3' or type.lower() == 'apple display p3' or type.lower() == 'display p3':
                trans = np.array([[0.4866, 0.2657, 0.1982],
                                  [0.2290, 0.6917, 0.0793],
                                  [0.0, 0.0451, 1.0437]])
            img[img <= 0.04045] /= 12.92
            img[img > 0.04045] = np.power((img[img > 0.04045] + 0.055) / 1.055, 2.4)

            xyz = np.dot(trans, img.T).T.reshape(info)

        elif type.lower() =='adobergb':
            img **=2.19921875
            trans = np.linalg.inv(np.array(
                [[2.04159, -0.56501, -0.34473], [-0.96924, 1.87597, 0.04156], [0.01344, -0.11836, 1.01517]]))
            xyz = np.dot(trans, img.T).T.reshape(info)
        else:
            xyz = 0
        s_xyz = spectra(wp).sxyz()
        w = np.sum(s_xyz,axis=0).reshape([1,1,3])
        D65_w = np.sum(spectra('d65').sxyz(),axis=0).reshape([1,1,3])
        xyz*=100
        xyz*=w/D65_w
        return xyz

    def xyz2lab(self,xyz):
        s_xyz = spectra(self.illuminant).sxyz()
        w = np.sum(s_xyz, axis=0).reshape([1, 1, 3])
        w /= w[:, :, 1]
        T = pow(6/29,2)
        fxyz = np.empty(xyz.shape)
        __lab = np.empty(xyz.shape)
        fx = xyz[:, :, 0] / w[:, :, 0]
        fy = xyz[:, :, 1] / w[:, :, 1]
        fz = xyz[:, :, 2] / w[:, :, 2]
        fxyz[:,:,0][fx>T] = fx[fx > T] ** (1 / 3)
        fxyz[:, :, 0][fx <= T] =(1/3)*pow(29/6,2)* fx[fx <= T] +16/166
        fxyz[:,:,1][fy>T] = fy[fy > T] ** (1 / 3)
        fxyz[:, :, 1][fy <= T] =(1/3)*pow(29/6,2)* fy[fy <= T] +16/166
        fxyz[:,:,2][fz>T] = fz[fz > T] ** (1 / 3)
        fxyz[:, :, 2][fz <= T] =(1/3)*pow(29/6,2)* fz[fz <= T] +16/166

        __lab[:, :, 0] = 116 * fxyz[:,:,1] - 16
        __lab[:, :, 1] =  500 * (fxyz[:,:,0]-fxyz[:,:,1])
        __lab[:, :, 2] = 200 * (fxyz[:,:,1]-fxyz[:,:,2])
        return __lab

    def xyz2srgb(self,xyz):
        rgbtran = np.array([[3.2404541, -1.5371385, -0.4985314], [-0.9692660, 1.8760108, 0.0415560],
                            [0.0556434, -0.2040259, 1.0572252]])
        var_rgb = np.dot( xyz,rgbtran.T)
        var_rgb_ = var_rgb.copy()
        var_rgb_[var_rgb > 0.0031308] = 1.055 * (var_rgb[var_rgb > 0.0031308] ** (1 / 2.4)) - 0.055
        var_rgb_[var_rgb <= 0.0031308] = 12.92 * var_rgb[var_rgb <= 0.0031308]
        return var_rgb_

    def xyz2adrgb(self,xyz):
        rgbtran = np.array([[2.04159, -0.56501, -0.34473], [-0.96924, 1.87597, 0.04156], [0.01344, -0.11836, 1.01517]])
        var_rgb = np.dot( xyz,rgbtran)
        return np.power(var_rgb,1 / 2.19921875)

    def rgb2hsv(self, img_, img_type='Norm'):
        '''

        :param img: img 为[0,1]时，type = 'Norm'; [0,255]时，type为任意字符串
        :return:HSV H:0~360 S:0~1 V:0~1
        '''
        if type(img_type) != str:
            raise TypeError(
                f'img_type期望是字符串类型，然而输入类型为{type(img_type)}。\n1.若图像数值在0~1之间应传入\'Norm\'\n2.若图像数值在0~255之间应传入任意字符串')
        img = img_.copy()
        if img_type == 'Norm':
            img *= 255
        flaten = imgshape(img)
        img = flaten.flatten()
        hsv_ = np.empty(img.shape)
        Cmax = np.max(img, axis=-1)
        Cmin = np.min(img, axis=-1)
        Delt_C = Cmax - Cmin
        hsv_[:, 1] = Delt_C / Cmax
        hsv_[:, 2] = Cmax / 255
        hsv_[:, 0][Delt_C == 0] = 0
        No_zero = [Delt_C != 0]
        mid_r, mid_g, mid_b = [Cmax == img[:, 0]], [Cmax == img[:, 1]], [Cmax == img[:, 2]]
        hsv_[:, 0][mid_r[0] * No_zero[0]] = 60 * (img[:, 1][mid_r[0] * No_zero[0]] - img[:, 2][mid_r[0] * No_zero[0]]) / \
                                            Delt_C[mid_r[0] * No_zero[0]] + 0
        hsv_[:, 0][mid_g[0] * No_zero[0]] = 60 * (img[:, 2][mid_g[0] * No_zero[0]] - img[:, 0][mid_g[0] * No_zero[0]]) / \
                                            Delt_C[mid_g[0] * No_zero[0]] + 120
        hsv_[:, 0][mid_b[0] * No_zero[0]] = 60 * (img[:, 0][mid_b[0] * No_zero[0]] - img[:, 1][mid_b[0] * No_zero[0]]) / \
                                            Delt_C[mid_b[0] * No_zero[0]] + 240
        hsv_[:, 0][hsv_[:, 0] < 0] += 360
        return flaten.inv_flatten(hsv_)

    def rgb2lab(self,rgb,type = 'srgb'):

        return self.xyz2lab(self.rgb2xyz(rgb,type)/100)

    def hsv2rgb(self, img):
        flaten = imgshape(img)
        img = flaten.flatten()
        RGB = np.empty(img.shape)
        C = img[:, 1] * img[:, 2]
        X = C * (1 - np.abs(img[:, 0] / 60 % 2 - 1))
        m = img[:, 2] - C
        idx_L = [C, X, np.zeros(C.shape)]
        idx = [[0, 1, 2], [1, 0, 2], [2, 0, 1], [2, 1, 0], [1, 2, 0], [0, 2, 1]]
        for i in range(3):
            RGB[:, i][tuple([img[:, 0] < 0 + 60] and [img[:, 0] >= 0])] = idx_L[idx[0][i]][
                tuple([img[:, 0] < 0 + 60] and [img[:, 0] >= 0])]
            RGB[:, i][tuple([img[:, 0] < 60 + 60] and [img[:, 0] >= 60])] = idx_L[idx[1][i]][
                tuple([img[:, 0] < 60 + 60] and [img[:, 0] >= 60])]
            RGB[:, i][tuple([img[:, 0] < 120 + 60] and [img[:, 0] >= 120])] = idx_L[idx[2][i]][
                tuple([img[:, 0] < 120 + 60] and [img[:, 0] >= 120])]
            RGB[:, i][tuple([img[:, 0] < 180 + 60] and [img[:, 0] >= 180])] = idx_L[idx[3][i]][
                tuple([img[:, 0] < 180 + 60] and [img[:, 0] >= 180])]
            RGB[:, i][tuple([img[:, 0] < 240 + 60] and [img[:, 0] >= 240])] = idx_L[idx[4][i]][
                tuple([img[:, 0] < 240 + 60] and [img[:, 0] >= 240])]
            RGB[:, i][tuple([img[:, 0] < 300 + 60] and [img[:, 0] >= 300])] = idx_L[idx[5][i]][
                tuple([img[:, 0] < 300 + 60] and [img[:, 0] >= 300])]

        RGB = np.asarray([RGB[:, i] + m for i in range(3)])

        return flaten.inv_flatten(RGB.T)

class spectra():

    def __init__(self, illuminant='D65',band = np.arange(400,710,10),deg = 10,band2 = None):
        '''
        创建一个光谱转换器。该光谱转换器将需要预先定义光源类型，光源波段以及视场。
        注意：自定义的光源信息需要填充band信息，否则将自动压缩至400nm~700nm，10nm间隔。
        :param illuminant: 字符串或数组| 选择光源，D65，A，D50均为CIE规定光源信息.
        :param band: 数组 | 光谱波段，默认400nm~700nm,10nm间隔
        :param deg: 整数 | CIE 视角，默认10°，可选2°
        最后更新：2021年10月28日 曹栩珩
        '''
        path = path_ + '/data/'
        bar_xyz = np.load(path + 'CIExyz_deg'+str(deg)+'.npy')
        __bar_xyz = np.empty([band.shape[0],3])
        for i in range(3):
            __bar_xyz[:, i] = np.interp(band, np.arange(360, 805, 5), bar_xyz[:,i])

        if type(illuminant) == str:
            self.illu = illuminant.lower()
            illuminant_list = ['a','d65','d50','b','c','d55']
            if self.illu not in illuminant_list:
                print(f"Unkown illuminant{self.illu}, only support 'A','D65','D50', 'D55', 'B', 'C' or the custom")
            _illuminance = np.load(path + self.illu+'.npy')
            self.illuminance = np.interp(band,np.arange(360, 805, 5),_illuminance)
        else:
            if band2 is None:
                band2 = band
            self.illuminance =  np.interp(band,band2,illuminant)
        if len(self.illuminance.shape) ==1:
            self.illuminance = self.illuminance.reshape([-1,1])
        self.S_xyz = self.illuminance * __bar_xyz


    def k(self):
        k = 100 / sum(self.S_xyz[:, 1])
        return k



    def space(self, img, space='adrgb', wp=None, xyz=False):
        '''

        :param img: 传入待转换的高光谱图像或XYZ图像（XYZ图像需填写xyz=True）
        :param space: 字符串 | 转换的目标空间，默认AdobeRGB，可选’sRGB‘，’XYZ‘
        :param wp: 是否进行白点校正
        :param xyz: XYZ图像校正
        :return: 目标颜色空间图像
        最后更新：2021年6月30日 曹栩珩
        '''

        self.info = np.shape(img)

        if xyz == True:
            self.XYZ = img
        else:
            self.rad_rs = img.reshape(self.info[0] * self.info[1], self.info[2], 1)
            k = 100 / sum(self.S_xyz[:, 1])
            self.XYZ = np.sum(k * self.rad_rs * self.S_xyz, axis=1).reshape(self.info[0], self.info[1], 3)
        if space.lower() == 'xyz':
            return self.XYZ
        elif space.lower() == 'adrgb':
            xyz = self.XYZ.T.reshape(3, self.info[0] * self.info[1])
            xyz = xyz / 100
            rgbtran = np.array(
                [[2.04159, -0.56501, -0.34473], [-0.96924, 1.87597, 0.04156], [0.01344, -0.11836, 1.01517]])
            var_rgb = np.dot(rgbtran, xyz).reshape(3, self.info[1], self.info[0]).T
            var_rgb = pow(var_rgb, (1 / 2.19921875))
            return var_rgb
        elif space.lower() == 'srgb':
            if wp:
                if self.illu.lower() == 'a' or self.illu.lower() == 'al':
                    M = np.array([[0.8652435, 0.0000000, 0.0000000], [0.0000000, 1.0000000, 0.0000000],
                                  [0.0000000, 0.0000000, 3.0598005]])
                    self.XYZ = np.dot(self.XYZ, M)
            xyz = self.XYZ.T.reshape(3, self.info[0] * self.info[1])

            xyz = xyz / 100
            rgbtran = np.array([[3.2404541, -1.5371385, -0.4985314], [-0.9692660, 1.8760108, 0.0415560],
                                [0.0556434, -0.2040259, 1.0572252]])
            var_rgb = np.dot(rgbtran, xyz).reshape(3, self.info[1], self.info[0]).T
            var_rgb_ = var_rgb.copy()
            var_rgb_[var_rgb>0.0031308] = 1.055 * (var_rgb[var_rgb>0.0031308] ** (1 / 2.4)) - 0.055
            var_rgb_[var_rgb <= 0.0031308] = 12.92*var_rgb[var_rgb <= 0.0031308]

            return var_rgb_

        else:
            warnings.warn('Not found such a color space. if you need it, please contact caoxuhengcn@gmail.com')

    def sxyz(self):
        return self.S_xyz

    def space_spectrum(self, img, space='adrgb', wp=None, xyz=False):

        img = img.ravel()
        self.info = [1, np.shape(img)[0]]
        if xyz == True:
            self.XYZ = img
        else:
            self.rad_rs = img.reshape(self.info[0], self.info[1], 1)

            k = 100 / sum(self.S_xyz[:, 1])

            self.XYZ = np.sum(k * self.rad_rs * self.S_xyz, axis=1).reshape(self.info[0], 3)

        if space.lower() == 'xyz':
            return self.XYZ
        elif space.lower() == 'adrgb':
            xyz = self.XYZ.T.reshape(3, self.info[0])
            xyz = xyz / 100
            rgbtran = np.array(
                [[2.04159, -0.56501, -0.34473], [-0.96924, 1.87597, 0.04156], [0.01344, -0.11836, 1.01517]])
            var_rgb = np.dot(rgbtran, xyz).reshape(3, self.info[0]).T
            var_rgb = pow(var_rgb, (1 / 2.19921875))
            return var_rgb
        elif space.lower() == 'srgb':
            if wp:
                if self.illu.lower() == 'a' or self.illu.lower() == 'al':
                    M = np.array([[0.8652435, 0.0000000, 0.0000000], [0.0000000, 1.0000000, 0.0000000],
                                  [0.0000000, 0.0000000, 3.0598005]])
                    self.XYZ = np.dot(self.XYZ, M)
            xyz = self.XYZ.T.reshape(3, self.info[0])

            xyz = xyz / 100
            rgbtran = np.array([[3.2404541, -1.5371385, -0.4985314], [-0.9692660, 1.8760108, 0.0415560],
                                [0.0556434, -0.2040259, 1.0572252]])
            var_rgb = np.dot(rgbtran, xyz).reshape(3, self.info[0]).T
            for i in range(3):
                for j in range(self.info[0]):
                    if var_rgb[j, i] > 0.0031308:
                        var_rgb[j, i] = 1.055 * (var_rgb[j, i] ** (1 / 2.4)) - 0.055
                    else:
                        var_rgb[j, i] = 12.92 * var_rgb[j, i]
            return var_rgb
        else:
            print('Erro:no such color space in the function. If you need, contact Email: caoxuhengcn@gmail.com')

class spectra_metric():

    def __init__(self,x1,x2,max_v = 1,scale =6):
        self.scale = scale
        self.info = x1.shape
        self.max_v = max_v
        if len(self.info) == 3:
            self.x1_ = x1.reshape([-1, self.info[-1]])
            self.x2_ = x2.reshape([-1, self.info[-1]])
        else:
            self.x1_ = x1
            self.x2_ = x2


    def SAM(self,mode=''):
        A = np.sum(self.x1_ * self.x2_, axis=-1) / (np.sqrt(np.sum(self.x1_ * self.x1_, axis=-1)) * np.sqrt(np.sum(self.x2_ * self.x2_, axis=-1)))
        _SAM = np.arccos(A) * 180 / np.pi
        if mode =='mat':
            return _SAM
        else:
            return np.mean(_SAM)

    def MSE(self,mode = ''):
        if mode =='mat':
            self.MSE_mat = np.mean(np.power(self.x1_ - self.x2_, 2),axis=0)
            return self.MSE_mat
        else:
            return np.mean( np.power(self.x1_-self.x2_,2) )

    def ERGAS(self):
        k = 100/self.scale
        return k*np.sqrt(np.mean(self.MSE('mat') /np.power(np.mean(self.x2_,axis=0),2)))

    def PSNR(self,mode=''):
        _PSNR = 10*np.log10(np.power(np.max(self.max_v,axis=0),2)/self.MSE('mat'))
        if mode=='mat':
            return _PSNR
        else:
            return np.mean(_PSNR)

    def SSIM(self, k1=0.01, k2=0.03, mode=''):
        l=self.max_v
        u1 = np.mean(self.x1_, axis=0).reshape([1, -1])
        u2 = np.mean(self.x2_, axis=0).reshape([1, -1])
        Sig1 = np.std(self.x1_, axis=0).reshape([1, -1])
        Sig2 = np.std(self.x2_, axis=0).reshape([1, -1])
        sig12 = np.sum((self.x1_ - u1) * (self.x2_ - u2), axis=0) / (self.info[0] * self.info[1] - 1)
        c1, c2 = pow(k1 * l, 2), pow(k2 * l, 2)
        SSIM = (2 * u1 * u2 + c1) * (2 * sig12 + c2) / ((u1 ** 2 + u2 ** 2 + c1) * (Sig1 ** 2 + Sig2 ** 2 + c2))
        if mode == 'mat':
            return SSIM
        else:
            return np.mean(SSIM)

    def Evaluation(self,idx=0,k1=0.01,k2=0.03):
        print(f'{idx}\t{self.PSNR()}\t{self.SAM()}\t{self.ERGAS()}\t{self.SSIM(k1=k1,k2=k2)}')

class distance():

    def cosine(self,a, b):
        assert a.shape == b.shape
        info = a.shape
        if len(info) == 3:
            a_ = a.reshape([-1, info[-1]])
            b_ = b.reshape([-1, info[-1]])
        else:
            a_ = a.copy()
            b_ = b.copy()

        cos_dist = np.empty(a_.shape[0])

        for i in range(a_.shape[0]):
            cos_dist[i] = np.dot(a_[i], b_[i].T) / (np.sqrt(np.dot(a_[i], a_[i].T) * np.dot(b_[i], b_[i].T)))

        return 1 - cos_dist

    def DEab(self,truth,sample,type ='mean'):
        matrix =  np.sqrt(np.sum(np.power(sample-truth,2),axis=-1))
        if type =='mean':
            return np.mean(matrix)
        elif type == 'mat':
            return matrix

    def DEab_RGB_LAB(self,RGB,LAB,type='srgb',illuminant='d65',m_type = 'mean'):
        LAB_S = cvtcolor().rgb2lab(RGB,type,illuminant)

        return self.DEab(LAB,LAB_S,m_type)

class cluster():

    def cosine_predict(img, centre):
        centre = centre.squeeze()
        img_ = img.reshape([-1, 3])
        img_ = np.tile(img_, (centre.shape[0], 1, 1))
        img_ = np.transpose(img_, (1, 0, 2))

        centre_mat = np.tile(centre, (img_.shape[0], 1, 1))

        dist = np.sum(centre_mat * img_, axis=-1) / np.sqrt(
            np.sum(centre_mat * centre_mat, axis=-1) * (np.sum(img_ * img_, axis=-1)))

        min_id = np.argmin(dist, axis=-1)
        return min_id

