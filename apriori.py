import pandas as pd
from collections import defaultdict
from itertools import chain, combinations
from optparse import OptionParser
import sys


# 加载数据
def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    df = pd.read_csv(fname,index_col=False)
    return df


# 返回item的数组 和交易数组
def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = data_iterator.columns.tolist()

    for indexes in data_iterator.index:
        transaction = data_iterator.loc[indexes].values
        transactionList.append(frozenset([itemSet[i] for i in range(len(itemSet)) if transaction[i] == 1]))

    itemSet = set([frozenset([item]) for item in itemSet])
    return itemSet, transactionList

def subsets(arr):
    """ Returns non empty subsets of arr"""
    # 从 1 个 开始全排
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)]) # 接受一个可迭代对象列表作为输入，并返回一个迭代器，有效的屏蔽掉在多个容器中迭代细节


# 根据最小支持度 筛选item
def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    '''
        support = frq(x)/N
    '''
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                localSet[item] += 1
                freqSet[item] += 1
    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)
    return _itemSet

# 对 set 合并
def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def runApriori(data_iter, minSupport, minConfidence):
    # get item list, transaction list
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    largeSet = dict()
    freqSet = defaultdict(int)
    # Global dictionary which stores (key=n-itemSets,value=support)
    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    # combine the set until
    k = 2
    while (currentLSet != set([])):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet, transactionList, minSupport, freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        """local function returnning the support of each item"""
        return float(freqSet[item]) / len(transactionList)

    # specific item combination with related support value
    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    # specific rule with
    toRetRules = []
    for key, value in largeSet.items():
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules


# print function
def printResults(items, rules):
    for item, support in sorted(items, key=lambda item: item[1], reverse=True):
        print("item: %s, %.3f" % (str(item), support))
    print("\n--------------------------------------RULES:")

    for rule, confindence in sorted(rules, key=lambda rules: rules[1], reverse=True):
        pre, post = rule
        print("Rule: %s ==> %s, %.3f" % (str(pre), str(post), confindence))

if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default="D://工作//Apriori-master//INTEGRATED-DATASET.csv")

    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.01,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.7,
                         type='float')

    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
            inFile = sys.stdin.readline()
    elif options.input is not None:
            inFile = dataFromFile(options.input)
    else:
            print('No dataset filename specified, system with exit\n')
            sys.exit('System will exit')

    minSupport = options.minS
    minConfidence = options.minC

    items, rules = runApriori(inFile, minSupport, minConfidence)

    printResults(items, rules)
