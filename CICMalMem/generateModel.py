from xml.sax.handler import feature_namespace_prefixes
import pandas as pd
import numpy
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, zero_one_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz
from pydotplus import graph_from_dot_data
from sklearn.cluster import KMeans 


# Must declare data_dir as the directory of training and test files
#data_dir="./datasets/CIC/"
data_dir="../"
#raw_data_filename = data_dir + "Obfuscated-MalMem2022.csv"
raw_data_filename = data_dir + "Obfuscated-MalMem2022_labeled.10_percent.csv"

print ("Loading raw data")

raw_data = pd.read_csv(raw_data_filename, header=None)

print ("Transforming data")
# Categorize columns: "protocol", "service", "flag", "attack_type"
#raw_data[1], protocols= pd.factorize(raw_data[1])
#raw_data[2], services = pd.factorize(raw_data[2])
#raw_data[3], flags    = pd.factorize(raw_data[3])
#raw_data[41], attacks = pd.factorize(raw_data[41])

# Column 1 has specific malware name, ignore it
# Last column has malware class (Benign, Spyware, Ransomware, Trojan)
# Last but one column has the malware type (Benign, Spyware, Ransomware, Trojan)
# separate features (columns 1..40) and label (column 0)
labels= raw_data.iloc[:,raw_data.shape[1]-1:]
features= raw_data.iloc[:,1:raw_data.shape[1]-2]
print("labels:", raw_data[raw_data.shape[1]-1].unique(),"\n")

# convert them into numpy arrays
#features= numpy.array(features)
#labels= numpy.array(labels).ravel() # this becomes an 'horizontal' array
labels= labels.values.ravel() # this becomes a 'horizontal' array

# TODO: get features names and target name

# Separate data in train set and test set
df= pd.DataFrame(features)
# create training and testing vars
# Note: train_size + test_size < 1.0 means we are subsampling
# Use small numbers for slow classifiers, as KNN, Radius, SVC,...
X_train, X_test, y_train, y_test = train_test_split(df, labels, train_size=0.8, test_size=0.2)
print ("X_train, y_train:", X_train.shape, y_train.shape)
print ("X_test, y_test:", X_test.shape, y_test.shape)

def calculos(clf1):
    trained_model= clf1.fit(X_train, y_train)
    print ("Score: ", trained_model.score(X_train, y_train))
    # Predicting
    print ("Predicting")
    y_pred = clf.predict(X_test)

    print ("Computing performance metrics")
    results = confusion_matrix(y_test, y_pred)
    error = zero_one_loss(y_test, y_pred)

    print ("Confusion matrix:\n", results)
    print ("Error: ", error)
    # NUEVO: Calcular precision, recall y F1
    from sklearn.metrics import precision_score
    precision = precision_score(y_test, y_pred, average='micro')
    from sklearn.metrics import recall_score
    recall = recall_score(y_test, y_pred, average='micro')
    from sklearn.metrics import f1_score
    f1 = f1_score(y_test, y_pred, average='micro')
    print('precision_score: ', precision)
    print('recall_score:', recall)
    print('f1_score: ', f1)

###### Decision tree
print ("---------Training model - DecisionTree")
clf = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, class_weight=None)
calculos(clf)

##### RandomForest
print ("-----------Training model - RandomForest")
clf= RandomForestClassifier(n_jobs=-1, random_state=3, n_estimators=102)
calculos(clf)

##### KMeans
print ("-----------Training model - Kmeans")
clf = KMeans(n_clusters=3, random_state=0)

