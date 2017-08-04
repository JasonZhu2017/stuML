
import KNN

# group, labels = KNN.createDataSet()
# print KNN.classify0([0, 0], group, labels, 3)
datingFeaturesMat, datingLabelsVector = KNN.file2matrix('datingTestSet2.txt')
print datingFeaturesMat
# print datingLabelsVector