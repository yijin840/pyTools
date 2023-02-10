from sklearn.cluster import KMeans
import numpy as np
list1=[88.0,74.0,96.0,85.0]
list2=[92.0,99.0,95.0,94.0]
list3=[91.0,87.0,99.0,95.0]
list4=[78.0,99.0,97.0,81.0]
list5=[88.0,78.0,98.0,84.0]
list6=[100.0,95.0,100.0,92.0]
X=np.array([list1,list2,list3,list4,list5,list6])
kmeans=KMeans(n_clusters=2).fit(X)#fit方法,对确定了类别之后的数据集进行聚类
pred=kmeans.predict(X)#predict方法，根据聚类的结果确定所属的类别
print(pred)