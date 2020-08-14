---
layout: post
title: MATLAB：图像旋转与插值并比较前后MSE
date: 2019-01-27
author: Jianqiao Mo
tags: [document, in Chinese]
comments: true
toc: true
pinned: false
---

《MATLAB：图像旋转与插值并比较前后MSE》
本文地址 [https://blog.csdn.net/qq_39475211/article/details/86668957](https://blog.csdn.net/qq_39475211/article/details/86668957)

<!-- more -->

# 为什么图像旋转需要插值？
图像旋转或者放大后，原本大小将发生改变，需要对一些新的像素点进行计算。MATLAB自带函数`imrotate()`可以实现图像旋转（MATLAB使用双三次插值）。感兴趣还可以了解flipdim、mirror、transp等函数。
# 常用的插值方法
## 最近邻插值
在一维空间中，最近邻插值就相当于四舍五入取整。在二维图像中，像素点的坐标都是整数，该方法就是选取离目标点最近的点。
最近相邻插值算法的优点是计算量很小，算法也简单，因此运算速度较快。但它仅使用离待测采样点最近的像素的灰度值作为该采样点的灰度值，而没考虑其他相邻像素点的影响，因而重新采样后灰度值有明显的不连续性，图像质量损失较大，会产生明显的马赛克和锯齿现象。

<div align="center">
    <img src="https://img-blog.csdnimg.cn/20190127201727350.png#pic_center" width=516 height=250 />
</div>

例如：我们约定，使用左/上原有像素点对放大的图像插值，将得到类似的结果。
## 双线性插值
两次线性插值算法(Bilinear Interpolation)是一种通过平均周围像素颜色值来添加像素的方法。该方法可生成中等品质的图像。

两次线性插值算法输出的图像的每个像素都是原图中四个像素(2×2)运算的结果，由于它是从原图四个像素中运算的，因此这种算法很大程度上消除了锯齿现象，而且效果也比较好。只是计算量稍大一些，但缩放后图像质量高，基本克服了最近邻插值法灰度值不连续的特点，因为它考虑了待测采样点周围四个直接邻点对该采样点的相关性影响。

但是，此方法仅考虑待测样点周围四个直接邻点灰度值的影响，而未考虑到各邻点间灰度值变化率的影响，因此具有低通滤波器的性质，从而导致缩放后图像的高频分量受到损失，图像边缘在一定程度上变得较为模糊。

<div align="center">
    <img src="https://img-blog.csdnimg.cn/20190127202757324.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center" width=560 height=300  />
</div>

<div align="center">
    <img src="https://img-blog.csdnimg.cn/20190127203919172.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center" width=360 height=300  />
</div>

可以直观地像上图那样理解双线性插值。

<div align="center">
    <img src="https://imgconvert.csdnimg.cn/aHR0cHM6Ly9pbWFnZXMwLmNuYmxvZ3MuY29tL2kvNTcxNjE4LzIwMTQwMy8xMjE5MzMyNTE4OTcyMDcuanBn?x-oss-process=image/format,png#pic_center" width=360 height=300  />
</div>

严谨的计算公式：
$f( i+u, j+v)=(1-u)(1-v) f(i,j) + (1-u) v f(i,j+1) + u (1-v) f( i+1,j ) + u v f( i+1, j+1)$

具体的实现还要结合下面讲的**映射方法**再操作。

## 双三次插值
这里涉及到复杂的计算公式，[详细可以查看大佬的文章](https://blog.csdn.net/u010979495/article/details/78428898)
# 常见的映射方法
通常情况下，一个整数位置(x,y)经过图像变换后，往往都位于非整数位置。此时就要采用插值技术。此时对于向前映射和向后映射，需要采取不同的策略。
## 前向映射（前向插值）
![前向映射](https://img-blog.csdnimg.cn/2018122115191820.png#pic_center)
即：通过公式（变换函数U、V）计算出目标像素位置，将灰度映射过去。（x~0~，y~0~）是原图某点，经过计算，得到旋转/放大后对应像素点（x，y），所以将灰度从原图映射到新图。

**存在问题：**

 1. 浮点坐标：如（1,1）映射成（0.5,0.5），这是无效坐标，这是可以用插值计算法进一步处理；
 2. 映射不完全：输入图像的像素总数小于输出的像素总数，会使得输出图像的部分像素与原始图像并没有映射关系，如放大操作；
 3. 映射重叠：与映射不完全正好相反，输出图像可能会存在映射后的像素重叠。
 
 通常==不建议==使用前向映射。
 
## 后向映射
![后向映射](https://img-blog.csdnimg.cn/20181221153454836.png#pic_center)
旋转/放大后像素点（x，y）经过反推寻找，得到对应原图点（x~0~，y~0~）。
通过变换函数反函数 U’、V’ ，在新图像 每一个像素反推寻找它在原图的位置，进行映射。

这避免了映射不完全、映射重叠的问题，是常用做法。

# 图像旋转方法
旋转的矩阵公式：旋转变换的矩阵公式：

$$\begin{bmatrix}
{x_{1}}&{y_{1}}&{1}\\
\end{bmatrix} = \begin{bmatrix}
{x_{0}}&{y_{0}}&{1}\\
\end{bmatrix}\begin{bmatrix}
{cos(\theta)}&{sin(\theta)}&{0}\\
{-sin(\theta)}&{cos(\theta)}&{0}\\
{0)}&{0}&{1}\\
\end{bmatrix}$$ 


逆运算矩阵公式： 

$$\begin{bmatrix}
{x_{0}}&{y_{0}}&{1}\\
\end{bmatrix} = \begin{bmatrix}
{x_{1}}&{y_{1}}&{1}\\
\end{bmatrix}\begin{bmatrix}
{cos(\theta)}&{-sin(\theta)}&{0}\\
{sin(\theta)}&{cos(\theta)}&{0}\\
{0)}&{0}&{1}\\
\end{bmatrix}$$ 

对数学推导有兴趣可以看看大佬的文章：[详细的推导过程](https://blog.csdn.net/Bryan_QAQ/article/details/78805201)

利用这个矩阵计算公式，我们可以对像素直接计算出图像旋转后的结果。有需要则再进行插值。
# 小实验示例代码
小实验：
1. 读取cameraman.tif，==自行编写代码==，分别使用前向插值（使用最邻近法），后向插值（自己选择合适的插值方法），将图像绕左上角逆时针旋转30度，再顺时针旋转30度，显示并计算旋转前后图像的MSE，分析原因。
<div align="center">
    <img src="https://img-blog.csdnimg.cn/20190127211642293.png#pic_center" width=180 height=50  />
</div>
<div align="center">
    <img src="https://img-blog.csdnimg.cn/20190127211815606.png#pic_center" width=180 height=50  />
</div>

前向映射：旋转30°，再插值比较：需要对映射不完全像素（黑色小点）处理。
<div align="center">
    <img src="https://img-blog.csdnimg.cn/20190127212118235.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center" />
</div>

后向映射：
<div align="center">
    <img src="https://img-blog.csdnimg.cn/201901272123412.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDc1MjEx,size_16,color_FFFFFF,t_70#pic_center" />
</div>

计算结果： MSE =    8.9182，旋转时需要对一些像素进行插值，故再次转回来的时候，插值产生的灰度值（计算产生的）将会与原本的图像的不同。

```
clc
clear;
I = imread('cameraman.tif');
[r1,c1]=size(I); 
J = uint8(myimrotatef(I,30));%rotate 30 degrees clockwise
K = uint8(myimrotatef(J,-30));%rotate 30 degrees anticlockwise
[r2,c2]=size(K); 
K = K((r2-r1)/2+1:(r2+r1)/2,(c2-c1)/2+1:(c2+c1)/2);%cut the picture as large as the sample
subplot(1,3,1),imshow(I),title("Sample 256*256"),
subplot(1,3,2),imshow(J),title("Rotation1 350*350"),
subplot(1,3,3),imshow(K),title("Rotation2 256*256");
[PSNR, MSE] = psnr_mse(I, K);%calculate MSE and display MSE
```
完整代码包地址: [https://download.csdn.net/download/qq_39475211/10940665](https://download.csdn.net/download/qq_39475211/10940665)