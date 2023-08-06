import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


from sklearn.model_selection import train_test_split
import time


def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    print(time_stamp)
def show(y_true, y_pred,title):
    classes=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]
    C = confusion_matrix(y_true, y_pred, labels=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,
                                                 23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])
    plt.matshow(C, cmap=plt.cm.Greens)
    plt.colorbar()
    plt.title(title)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=-45)
    plt.yticks(tick_marks, classes)
    for i in range(len(C)):
        for j in range(len(C)):
            plt.annotate(C[i, j], xy=(i, j), horizontalalignment='center', verticalalignment='center')
    plt.xlabel('True label')
    plt.ylabel('Predicted label')
    plt.show()

def get_toy_config():
    config = {}
    ca_config = {}
    ca_config["random_state"] = 0
    ca_config["max_layers"] = 100
    ca_config["early_stopping_rounds"] = 3
    ca_config["n_classes"] = 10
    ca_config["estimators"] = []
    ca_config["estimators"].append(
            {"n_folds": 5, "type": "XGBClassifier", "n_estimators": 10,
             "max_depth": 5,"objective": "multi:softprob", "silent":
            True, "nthread": -1, "learning_rate": 0.1} )
    ca_config["estimators"].append({"n_folds": 5, "type": "RandomForestClassifier",
            "n_estimators": 10, "max_depth": None, "n_jobs": -1})
    ca_config["estimators"].append({"n_folds": 5, "type": "ExtraTreesClassifier",
            "n_estimators": 10, "max_depth": None, "n_jobs": -1})
    ca_config["estimators"].append({"n_folds": 5, "type": "LogisticRegression"})
    config["cascade"] = ca_config
    return config

# 1.获取原数据
#columns_names=['x轴加速度','y轴加速度','z轴加速度','pitch','roll','yaw','温度','状态']
def get_raw_data():
columns_names = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0,
                 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 'label']
data=pd.read_excel("E:/total3_temp.xls",names=columns_names)


# 2.分割数据集为训练集、测试集
def division_data():
X_train,X_test,y_train,y_test=train_test_split(data[columns_names[0:27]],data[columns_names[27]],test_size=0.25,random_state=33)
print(type(X_train))

conf_mat = np.zeros([4,4])

# 3.数据标准化、归一化（先进行训练集和测试集的划分，再进行数据预处理）
def normalization_data():
ss=StandardScaler()
X_train=ss.fit_transform(X_train)
X_test=ss.transform(X_test)

# 4.定义模型，进行分类
def classification_data():
RC1 = RandomForestClassifier()
get_time_stamp()
RC1.fit(X_train,y_train)
get_time_stamp()

# 5.评价模型（score方法）
def estimate_model():
print('Accuarcy of forest Classifier:',RC1.score(X_test,y_test))
print('RF classification_report')
print(classification_report(y_test,RC1.predict(X_test),target_names=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37']))
predict = RC1.predict(X_test)
# plt.figure(figsize=(24, 16), dpi=60)
show(y_test,predict,'RF_matrix')
