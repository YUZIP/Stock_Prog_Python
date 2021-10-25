#student_sort = sorted(data, key=lambda datas: datas[i] , reverse=True)

a = [[1,2,3],[1.1,1.9,3]]
aa = sorted(a,key= lambda aa: aa[0],reverse=True)
print(aa)

from time import clock
aa = clock()
a =1
for i in range(100000):
    a +=1
print("Finish Time",clock()-aa)