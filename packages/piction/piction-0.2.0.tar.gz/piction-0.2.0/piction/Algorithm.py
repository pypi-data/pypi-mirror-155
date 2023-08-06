import cv2
import numpy as np
import sys
import math

sys.setrecursionlimit(100000)

point_tree_y=[]
point_tree_x=[]
detedge=[]

def initialize():
	global point_tree_x,point_tree_y
	point_tree_x=[]
	point_tree_y=[]



def getDetedge():
	return detedge

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def size(self, x):
        return -self.parents[self.find(x)]

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self):
        return len(self.roots())

    def all_group_members(self):
        group_members = defaultdict(list)
        for member in range(self.n):
            group_members[self.find(member)].append(member)
        return group_members

    def __str__(self):
        return '\n'.join(f'{r}: {m}' for r, m in self.all_group_members().items())

#深さ優先探索
def dfs(x,y):
	
	#壁
	if y<0 or x<0 or y>=len(detedge) or x>=len(detedge[0]):
		return
	#線じゃない
	if detedge[y][x]<10:
		return
	#見た
	if flag[y*len(detedge[0])+x]==1:
		return
	# detedge[y][x]=c2
	# c2=c2+16
	# c2=c2%255
	point_tree_y.append(y)
	point_tree_x.append(x)
	flag[y*len(detedge[0])+x]=1
	dfs(x+1, y)
	dfs(x-1, y)
	dfs(x, y+1)
	dfs(x, y-1)
	dfs(x+1, y-1)
	dfs(x-1, y-1)
	dfs(x+1, y+1)
	dfs(x-1, y+1)

def makeUT(image):
	img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
	img_gray_flip =cv2.flip(img_gray, 0)
	global detedge
	detedge = cv2.Canny(img_gray_flip, 100, 1200)
	p=[]
	for i in range(len(detedge)):
		for j in range(len(detedge[0])):
			if detedge[i][j]>0:
				p.append(int(i*len(detedge[0])+j))
	d = {p[i]: i for i in range(len(p))}
	d2 = {i: p[i] for i in range(len(p))}
	global flag
	flag = {p[i]: 0 for i in range(len(p))}
	ut = UnionFind(len(p))
	for i in p:
		y=int(i/len(detedge[0]))
		x=i%len(detedge[0])
		
		if y-1>=0:
			if x-1>=0:
				if detedge[y-1][x-1]>0:
					ut.union(d[y*len(detedge[0])+x],d[(y-1)*len(detedge[0])+(x-1)])
			if x+1<len(detedge[0]):
				if detedge[y-1][x+1]>0:
					ut.union(d[y*len(detedge[0])+x],d[(y-1)*len(detedge[0])+(x+1)])
			if detedge[y-1][x]>0:
				ut.union(d[y*len(detedge[0])+x],d[(y-1)*len(detedge[0])+(x)])
		if y+1<len(detedge):
			if x-1>=0:
				if detedge[y+1][x-1]>0:
					ut.union(d[y*len(detedge[0])+x],d[(y+1)*len(detedge[0])+(x-1)])
			if x+1<len(detedge[0]):
				if detedge[y+1][x+1]>0:
					ut.union(d[y*len(detedge[0])+x],d[(y+1)*len(detedge[0])+(x+1)])
			if detedge[y+1][x]>0:
				ut.union(d[y*len(detedge[0])+x],d[(y+1)*len(detedge[0])+(x)])
		if x-1>=0:
			if detedge[y][x-1]>0:
				ut.union(d[y*len(detedge[0])+x],d[(y)*len(detedge[0])+(x-1)])
		if x+1<len(detedge[0]):
			if detedge[y][x+1]>0:
				ut.union(d[y*len(detedge[0])+x],d[(y)*len(detedge[0])+(x+1)])
	
	return ut,d2






def getPoint(image,maxPointNum=0):
	initialize()
	ut,d2 = makeUT(image)
	for i in ut.roots():
		dfs(d2[i]%len(detedge[0]),int(d2[i]/len(detedge[0])))
	xplus= {i:0 for i in range(len(detedge[0]))}
	for i in range(len(point_tree_x)):
		point_tree_x[i]=point_tree_x[i]+xplus[int(point_tree_x[i])]
		xplus[int(point_tree_x[i])]=xplus[int(point_tree_x[i])]+0.001
	ret_x=[]
	ret_y=[]
	if maxPointNum==0 or len(point_tree_x)<=maxPointNum :
		ret_x,ret_y=point_tree_x,point_tree_y
	else:
		mod = math.ceil(len(point_tree_x)/maxPointNum)
		for i in range(len(point_tree_x)):
			if i%mod==0:
				ret_x.append(point_tree_x[i])
				ret_y.append(point_tree_y[i])
			
	return ret_x,ret_y


def getPointArray(image,maxPointNum=0):
	ut,d2 = makeUT(image)
	ret_x=[]
	ret_y=[]
	for i in ut.roots():
		initialize()
		dfs(d2[i]%len(detedge[0]),int(d2[i]/len(detedge[0])))
		xplus= {i:0 for i in range(len(detedge[0]))}
		for i in range(len(point_tree_x)):
			point_tree_x[i]=point_tree_x[i]+xplus[int(point_tree_x[i])]
			xplus[int(point_tree_x[i])]=xplus[int(point_tree_x[i])]+0.001
		temp_x=[]
		temp_y=[]
		if maxPointNum==0 or len(point_tree_x)<=maxPointNum :
			temp_x,temp_y=point_tree_x,point_tree_y
		else:
			mod = math.ceil(len(point_tree_x)/maxPointNum)
			for i in range(len(point_tree_x)):
				if i%mod==0:
					temp_x.append(point_tree_x[i])
					temp_y.append(point_tree_y[i])
		ret_x.append(temp_x)
		ret_y.append(temp_y)
	return ret_x,ret_y
		