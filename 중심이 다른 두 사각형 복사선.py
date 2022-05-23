Python 3.10.4 (tags/v3.10.4:9d38120, Mar 23 2022, 23:13:41) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import matplotlib.pyplot as plt
import math
import random
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  

xal=float(input('복사면A의 x 방향 길이 ='))
yal=float(input('복사면A의 y 방향 길이 ='))
xbl=float(input('입사면B의 x 방향 길이 ='))
ybl=float(input('입사면B의 y 방향 길이 ='))
xxd=float(input('복사면과 입사면의 x축 중심 차이 ='))   #====== *중심이 다른 부분 추가*
yyd=float(input('복사면과 입사면의 y축 중심 차이 ='))   #====== *중심이 다른 부분 추가*
zab=float(input('두 면 사이의 거리 ='))
xd=int(input('입사면 구역의 x방향 개수='))
yd=int(input('입사면 구역의 y방향 개수='))

#반복할 광선 개수
NRay=int(input('광선개수 ='))
NRay_V=int(input('보고싶은 광선 개수 ='))
# 3D 그래프 범위 및 그림 그리기 설정
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-3*xbl/2, 3*xbl/2)
ax.set_ylim(-3*ybl/2, 3*ybl/2)
ax.set_zlim(0, zab+1)   

# 배열 개수는 xd * yd 가 된다.
# 행 개수 xd, 열 개수 yd 만큼의 0 행렬 생성
M = np.zeros([yd,xd])

xdl = xbl/xd # 한 구역의 길이 
ydl = ybl/yd 

etc =  0   # 기타 외부로 나가는 요소 개수 측정용


#광선 개수 만큼 반복
for a in range(NRay):

  # 복사면에서 임의의 점 선정
  xa=xal*(random.random()-0.5)   # -0.5 ~ 0.5 까지 임의의 값
  ya=yal*(random.random()-0.5)
  # 점에서 방출되는 광선의 임의의 xy평면에서와,z 축 방향 각도
  theta_xy=math.pi*2*random.random()   # xy 평면에서 나갈때 방향각  0~360
  theta_z=math.pi*1/2*random.random()      # z 방향으로 나갈때 xy 평면과의 방향각 0~180
  # 복사면(z=0)의 한 점에서 출발하여 xy,z 각도 만큼 진행하는 벡터가 입사면(Z=zab)까지 진행 했을 때 x,y 좌표
  l=zab/math.sin(theta_z)   # z방향각 으로 나가는 직선이 입사면평면의 z 좌표 위치까지 도달할때 필요한 길이 (xa,ya,0)~(x,y,zab)까지의 길이
  x=xa+l*math.cos(theta_xy)*math.cos(theta_z) # z좌표가 zab 일때의 직선의 x 좌표
  y=ya+l*math.sin(theta_xy)*math.cos(theta_z) # z좌표가 zab 일때의 직선의 y 좌표
  # 도출한 x,y 좌표가 입사면 안에 들어갈 때 실행
  if -xbl/2 +xxd < x < xbl/2 +xxd and -ybl/2 +yyd < y < ybl/2 +yyd :  #====== *중심이 다른 부분 추가*
    # 들어온 x,y 좌표를 각 요소 길이로 나누어 요소가 존재하는 위치를 행렬로 나타냄
    xcolumn=int((x-xxd+(xbl/2))//xdl)  #====== *중심이 다른 부분 추가*   # ex. 도착지 x좌표가 2.4 이고 평면이 -3 ~ 3 이고 x축을 5로 나누었을때 2.4를 각 요소 길이 6/5 로 나눈 몫은 요소의 x 행렬 
    yrow=int((y-yyd+(ybl/2))//ydl)  #====== *중심이 다른 부분 추가*
    element = M[yrow,xcolumn]
    M[yrow,xcolumn]= element + 1

  
  else :
    etc = etc + 1
  if a in range(NRay-NRay_V,NRay):  # 가장 최근~ 보고싶은 광선 개수까지의 광선 그리기
    x_m,y_m,z_m=[xa,x],[ya,y],[0,zab]   # 직선에서 2개의 각각 x , y , z 좌표
    ax.plot(x_m,y_m,z_m,alpha=0.3)
    ax.view_init(30,20) # 3차원 그래프 방향을 조절하기 위한 함수 인수1 = 상하 회전각도(0~90) 인수2 = 좌우 회전 각도(양수-시계,음수-반시계 회전)

# 각 요소에 위치한 광선들의 개수와 입사면 밖으로 나간 광선 개수
print(M)
print(etc)


# 복사면의 평면 그리기 (z=0인 x-y 평면)
xsa=np.linspace(-xal/2,xal/2,xd)
ysa=np.linspace(-yal/2,yal/2,yd)
Xa,Ya=np.meshgrid(xsa,ysa)
zsa=np.zeros_like(Xa)
ax.plot_surface(Xa,Ya,zsa,color='r',alpha=0.7)

# 입사면의 평면 그리기 (z=zab 인 x-y 평면)
xsb=np.linspace(-xbl/2+xxd,xbl/2+xxd,xd) # x 의 범위  #====== *중심이 다른 부분 추가*
ysb=np.linspace(-ybl/2+yyd,ybl/2+yyd,yd)              #====== *중심이 다른 부분 추가*
Xb,Yb=np.meshgrid(xsb,ysb)   # x,y 범위의 매쉬그리드 생성
zsb=np.zeros_like(Xb)+zab    # z를 x와 같은 크기의 0행렬을 만들고 +zab를 하여 모든 모든 요소가 zab 인 행렬 생성
ax.plot_surface(Xb,Yb,zsb,alpha=0.7)


# 표면형 차트 그리기 만들어 놓은 M 행렬을 이용하여 위치에 따른 개수를 색으로 나타내는 그림 그리기
cmap = plt.get_cmap('plasma')
plt.matshow(M,cmap=cmap)
plt.colorbar(shrink=0.8, aspect=10)
plt.show()