from sklearn import svm
from sklearn import datasets

clf = svm.SVC()
iris = datasets.load_iris()
x, y = iris.data, iris.target
clf.fit(x, y)

### 方法1  使用 pickle
import pickle
# 导入
# with open('../data/clf.picle', 'wb') as f:
#     # 将训练出来的模型clf，导入到 f中
#     pickle.dump(clf, f)

# 导出
with open('../data/clf.picle', 'rb') as f:
    # 从 保存的 clf.picle还原模型
    clf2 = pickle.load(f)
    print(clf2.predict(x[0:1]))

###  方法2  使用 joblib   joblib比pickle更快一点，因为会使用多线程存储文件
from sklearn.externals import joblib

# Save
joblib.dump(clf, '../data/clf.pkl')

# restore
clf3 = joblib.load('../data/clf.pkl')

print(clf3.predict(x[0:1]))
