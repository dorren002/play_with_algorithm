import numpy as np

class Node():
    def __init__(self,lchild,rchild,value,split_dim):
        self.lchild=lchild#节点的左子树
        self.rchild=rchild#节点的右子树
        self.value=value#节点的数值
        self.split_dim=split_dim#用来做划分的维度


class KDTree():
    def __init__(self,data):
        self.dims=len(data[0])#总特征数
        self.nearest_point=None
        self.nearest_dist=np.inf#初始化为无穷大
        
    def create_kdtree(self,current_data,split_dim):
        #设置递归出口：当全部样本划分完毕时就退出
        if len(current_data)==0:
            return None
        
        mid=self.cal_current_medium(current_data)#计算中位数所在下标
        data_sorted=sorted(current_data,key=lambda x:x[split_dim])#按照切分维度从小到大排序

        #下面三句代码本质上就是二叉树的后序遍历
        lchild=self.create_kdtree(data_sorted[0:mid],self.cal_split_dim(split_dim))#递归地构造左子树
        rchild=self.create_kdtree(data_sorted[mid+1:],self.cal_split_dim(split_dim))#递归地构造右子树
        return Node(lchild,rchild,data_sorted[mid],split_dim)#连接从根节点出发的左右子树，并返回
    
    #计算下一个划分维度
    def cal_split_dim(self,split_dim):
        return (split_dim+1) % self.dims
    
    #计算当前维度中位数所在下标
    def cal_current_medium(self,current_data):
        return len(current_data)//2

    #计算两点之间的欧氏距离
    def cal_dist(self,sample1,sample2):
        return np.sqrt(np.sum((sample1-sample2)**2))
        
    #传入kd树的根节点root和待搜索的点element,搜索element的最近邻点
    def search(self,node,element):
        if node is  None:
            return
        
        #计算当前划分维度上目标节点与当前节点的单一维度上的距离
        dist = node.value[node.split_dim] - element[node.split_dim]
        
        #前向搜索
        if dist>0:#当前节点在目标节点的上侧或左侧（在二维空间中）
            self.search(node.lchild,element)#递归地搜索左子树
        else:#否则，当前节点在目标节点的下侧或右侧（在二维空间中）
            self.search(node.rchild,element)#递归地搜索右子树
        #计算目标节点与当前节点的欧氏距离
        curr_dist = self.cal_dist(node.value,element)
        print(node.value, curr_dist)
        #更新最近邻节点
        if curr_dist < self.nearest_dist:
            self.nearest_dist = curr_dist
            self.nearest_point = node
            #print(self.nearest_point.value)
        #回溯
        #比较“最近距离”是否超过“目标节点与当前节点在当前划分维度上的距离”，超过了就说明可能在当前节点的另一侧子树中存在更近的点，所以需要到当前节点的另一侧子树中去搜索
        if self.nearest_dist > abs(dist):
            #由于是去当前节点的另一侧子树中进行搜索，因此正好与之前的前向搜索相反
            if dist>0:
                self.search(node.rchild,element)
            else:
                self.search(node.lchild,element)
    
    def get_nearest(self,root,element):
        self.search(root,element)
        return self.nearest_point.value,self.nearest_dist


dataset = np.array([(2,3),(4,7),(5,4),(7,4),(8,7),(9,1)])#构建训练数据集
kdtree = KDTree(dataset)
root = kdtree.create_kdtree(dataset,0)#创建KD树,以特征的第0个维度开始做划分

nearest_point,nearest_dist=kdtree.get_nearest(root,[3,4.5])#搜索[2,4.5]的最近邻点
print('最近邻点：{}\n最近距离：{}'.format(nearest_point,nearest_dist))

# from collections import deque

# def level_order_with_levels(root):
#     if not root:
#         return []
    
#     queue = deque([root])
#     result = []
    
#     while queue:
#         level_size = len(queue)  # 当前层的节点数量
#         level_nodes = []  # 记录本层的所有节点
        
#         for _ in range(level_size):
#             node = queue.popleft()
#             if node:
#                 level_nodes.append(node.value)
#                 queue.append(node.lchild)
#                 queue.append(node.rchild)
#             else:
#                 level_nodes.append(None)  # 保留 None 以维持树的结构
        
#         result.append(level_nodes)  # 记录当前层的所有节点
    
#     empty_layer = -1
#     for i, layer in enumerate(result):
#         isEmpty = True
#         for node in layer:
#             if node is not None:
#                 isEmpty = False
#                 break
#         if isEmpty:
#             empty_layer = i
    
#     result = result[:empty_layer]
#     return result

# def print_trees(levels):
#     if not levels:
#         return
    
#     for layer in levels:
#         print(layer)
    
    
# levels = level_order_with_levels(kdtree)

# print_trees(levels)

import matplotlib.pyplot as plt

# 提取 x 和 y 坐标
x = [point[0] for point in dataset]
y = [point[1] for point in dataset]

# 创建散点图
plt.scatter(x, y)

red_points_x = [3]
red_points_y = [4.5]

# 在散点图中绘制两个红色点
plt.scatter(red_points_x, red_points_y, color='red', label='Red Points')

plt.xlim(0, 10)  # x 轴限制在 0 到 10 之间
plt.ylim(0, 10)  # y 轴限制在 0 到 10 之间

# 显示图形
plt.savefig("kd_tree_visualization.png")


# 参考：https://blog.csdn.net/luoganttcc/article/details/134087812