import decision_tree


def createDataSet():
    dataSet = [[1, 1, 'yes'],
            [1, 1, 'no'],
            [1, 0, 'no'],
            [0, 1, 'maybe'],
            [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

def test_calcShannonEnt():
    myData, labels = createDataSet()
    shannonEntropy = decision_tree.calcShannonEnt(myData)
    print shannonEntropy

def main():
    test_calcShannonEnt()

    
if __name__ == '__main__':
    main()