---
layout: post
title: MATLAB：图像半调转换（halftone）和抖动转换（dither）
date: 2019-01-27
author: Jianqiao Mo
tags: [document, Chinese]
comments: true
toc: true
pinned: false
---

《MATLAB: 图像半调（halftone）显示和抖动（dither）显示》
本文地址 [https://blog.csdn.net/qq_39475211/article/details/86664284](https://blog.csdn.net/qq_39475211/article/details/86664284)
# 什么是半色调（halftone）

半色调（Halftone）技术是传统印刷中用来处理阶调并模拟连续调(Continue tone)的方法。
        [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-AflhTJyJ-1597071269788)(https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Halftoning_introduction.svg/260px-Halftoning_introduction.svg.png#pic_center)]图：不连续与连续阶调

印刷机或打印机上所打印的图像，只能借由着墨或不着墨两种阶调来表现层次，像这样的两值化影像称为半色调影像。只要借由调整不同形式、不同大小的墨点，利用人眼可以将图像中邻近墨点进行视觉积分的原理，在一定的距离观察下，便可以使二值化影像重现连续调的感觉。
![ 半色调 ](https://img-blog.csdn.net/20180114002859872?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMzE2NTkyMQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast#pic_center)
可以直观理解为牺牲空间来实现不同深浅度，利用墨点数实现印刷的深浅变化。

## 通常的分类
半色调分别为调幅(Amplitude Modulation, AM)与调频(Frequency Modulation, FM)，简单来说，AM是利用网点面积大小来表现图像的浓淡深浅；FM则是以网点排列间距的疏密不同，来呈现图像的层次。

## 小实验1

 1.读取cameraman.tif图像，自行编写代码，完成4x4的halftone转换并显示；
 
 AM方法：
 将图像的像素灰度值分成16阶（其实也可以是17阶），然后对应在原像素位置扩大成4x4网格。不同灰度阶强度就涂黑不同的网格数。
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190127113313465.png#pic_center)
比如，在256级灰度中，某个像素灰度是30，由于我们将图像的像素灰度值分成16阶（灰度0~15为1阶，16-31为2阶……），所以这个像素在4x4网格中涂上2格。

（在具体什么位置涂格子呢？其实涂色的位置不是很关键，关键是涂的数目。）

这样处理后，原本30x30图像会变成120x120大小。
![实验效果](https://img-blog.csdnimg.cn/20190127113433580.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center)
相同涂色数，不同涂色位置-对比：
![不同涂色](https://img-blog.csdnimg.cn/20190127113832657.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center)
# 抖动（dither）
抖动（dither）也算是半色调的一个分类，主要分为随机抖动和有序抖动两大类。这两种算法都需要一个模板，也称为抖动矩阵或阈值矩阵，抖动矩阵不仅决定了当亮度或灰度值减小时网点变成黑点的顺序，而且也决定了半色调图像的质量，所以抖动算法的关键是抖动矩阵的构造。

具体的原理可以参考大佬的文章：https://blog.csdn.net/songzitea/article/details/40832565

## 小实验2

 1. 阅读dither.pdf文档，理解后使用matlab自带的dither函数对cameraman.tif图像进行dither转换并显示。
我们直接使用MATLAB自带的dither()函数：
MATLAB官网（https://ww2.mathworks.cn/help/matlab/ref/dither.html?s_tid=srchtitle） 有中文的介绍。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190127114649332.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center)
# 附：主要代码 MATLAB
## 小实验1（半调halftone）

```
I=imread('cameraman.tif'); %读取图像
J=I/16; %灰度分16级
K=zeros(1024,1024); %新建一个空矩阵来保存结果
for x=1:1:256
   for y=1:1:256
       switch J(x,y) %匹配16级不同灰度,在空矩阵用4X4 halftone保存
           case 1
           case 2
               K(4*x-3,4*y-3)=1;
           case 3
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;
           case 4
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;
           case 5
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
           case 6
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;
           case 7
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;K(4*x-3,4*y-2)=1;
           case 8
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;K(4*x-3,4*y-2)=1;K(4*x-1,4*y)=1;
               case 9
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;K(4*x-3,4*y-2)=1;K(4*x-1,4*y)=1;K(4*x-3,4*y-1)=1;
           case 10
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;K(4*x-3,4*y-2)=1;K(4*x-1,4*y)=1;K(4*x-3,4*y-1)=1;
               K(4*x-2,4*y)=1;
           case 11
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;K(4*x-3,4*y-2)=1;K(4*x-1,4*y)=1;K(4*x-3,4*y-1)=1;
               K(4*x-2,4*y)=1;K(4*x-3,4*y)=1;
           case 12
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;K(4*x-3,4*y-2)=1;K(4*x-1,4*y)=1;K(4*x-3,4*y-1)=1;
               K(4*x-2,4*y)=1;K(4*x-3,4*y)=1;K(4*x-2,4*y-3)=1;
           case 13
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;K(4*x-3,4*y-2)=1;K(4*x-1,4*y)=1;K(4*x-3,4*y-1)=1;
               K(4*x-2,4*y)=1;K(4*x-3,4*y)=1;K(4*x-2,4*y-3)=1;K(4*x-1,4*y-2)=1;
           case 14
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;K(4*x-3,4*y-2)=1;K(4*x-1,4*y)=1;K(4*x-3,4*y-1)=1;
               K(4*x-2,4*y)=1;K(4*x-3,4*y)=1;K(4*x-2,4*y-3)=1;K(4*x-1,4*y-2)=1;
               K(4*x-1,4*y-3)=1;
                case 15
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;K(4*x-3,4*y-2)=1;K(4*x-1,4*y)=1;K(4*x-3,4*y-1)=1;
               K(4*x-2,4*y)=1;K(4*x-3,4*y)=1;K(4*x-2,4*y-3)=1;K(4*x-1,4*y-2)=1;
               K(4*x-1,4*y-3)=1;K(4*x,4*y-2)=1;
           case 16
               K(4*x-3,4*y-3)=1;K(4*x-2,4*y-2)=1;K(4*x-1,4*y-1)=1;K(4*x,4*y)=1;
               K(4*x-2,4*y-1)=1;K(4*x-3,4*y-2)=1;K(4*x-1,4*y)=1;K(4*x-3,4*y-1)=1;
               K(4*x-2,4*y)=1;K(4*x-3,4*y)=1;K(4*x-2,4*y-3)=1;K(4*x-1,4*y-2)=1;
               K(4*x-1,4*y-3)=1;K(4*x,4*y-2)=1;K(4*x,4*y-1)=1;
       end
   end
end

```
完整代码在 https://download.csdn.net/download/qq_39475211/10940207
没办法修改C币……实在要下载可以找某宝代下

## 小实验2（抖动dither）

```
I = imread('cameraman.tif');
X = dither(I);
subplot(1,2,1),imshow(I),title("sample"); 
subplot(1,2,2),imshow(X),title("dither");

```
