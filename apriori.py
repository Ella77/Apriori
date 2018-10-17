"""
Description     : Simple Python implementation of the Apriori Algorithm

Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence

    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
import time

"""***********<post-processing>***********


rule: ((('ASIAN',), ('MBE',)), 0.9895470383275261)				  lift: 1.47445623759 		valid!!!
rule: ((('BLACK',), ('MBE',)), 1.0)						  lift: 1.49003147954 		valid!!!
rule: ((('NON-MINORITY',), ('WBE',)), 1.0)					  lift: 2.09439528024 		valid!!!
0 rules are removed


***********</post-processing>***********


item: ('MBE', 'New York') , 0.170
item: ('New York', 'WBE') , 0.175
item: ('MBE', 'ASIAN') , 0.200
item: ('ASIAN',) , 0.202
item: ('New York',) , 0.295
item: ('NON-MINORITY',) , 0.300
item: ('NON-MINORITY', 'WBE') , 0.300
item: ('BLACK',) , 0.301
item: ('MBE', 'BLACK') , 0.301
item: ('WBE',) , 0.477
item: ('MBE',) , 0.671

------------------------ RULES:
Rule: ('ASIAN',) ==> ('MBE',) , 0.990
Rule: ('BLACK',) ==> ('MBE',) , 1.000
Rule: ('NON-MINORITY',) ==> ('WBE',) , 1.000
Duration: 0.0832810401917
"""
def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
        """calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support"""
        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = float(count)/len(transactionList)

                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet


def joinSet(itemSet, length):
        """Join a set with itself and returns the n-element itemsets"""
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    #print itemSet
    #print transactionList
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)


    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
            #print item
            """local function which Returns the support of an item"""
            return float(freqSet[item])/len(transactionList)

    def getRawSupport(item):
        item = frozenset([item])
        #print item
        return float(freqSet[item])/len(transactionList)

    def getRawBothSupport(item1,item2):
        item = frozenset([item1,item2])
        #print item
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])


    toRetRules = []
    for key, value in largeSet.items()[1:]:
        #print key
        #print value
        #print '\n------\n'
        for item in value:
        #    print item
            _subsets = map(frozenset, [x for x in subsets(item)])
            # print _subsets
            # print '\n---******---\n'
            for element in _subsets:
                # print element
                remain = item.difference(element)
                # print remain
                # print '\n++++++\n'
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))

    # calculate lift for every rule and remove invalid elements
    print ('\n\n***********<post-processing>***********\n\n')
    removed_num = 0
    for rule in toRetRules:

        xy_supoort = getRawBothSupport(rule[0][0][0], rule[0][1][0])
        x_support = getRawSupport(rule[0][0][0])
        y_support = getRawSupport(rule[0][1][0])

        lift = xy_supoort/(x_support * y_support)
        content = 'rule: '+str(rule)+'\t\t\t\t\t\t\t  lift: '+str(lift)

        if lift <= 1:
            content += ' \t\tinvalidXXXXXXXXXX'
            toRetRules.remove(rule)
            removed_num += 1
        else:
            content += ' \t\tvalid!!!'
        print (content)
    print (str(removed_num) + ' rules are removed')
    print ('\n\n***********</post-processing>***********\n\n')


    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    for item, support in sorted(items, key=lambda (item, support): support):
        print ("item: %s , %.3f" % (str(item), support))
    print ("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        print ("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))




def dataFromFile(fname):
        """Function which reads from the file and yields a generator"""
        file_iter = open(fname, 'rU')
        for line in file_iter:
                line = line.strip().rstrip(',')
                # print(line)
                    # .rstrip(',')
                # Remove trailing comma'
                # list = line.split()[-1]

                record =frozenset(line.split(','))

                # print(record)
                yield record


if __name__ == "__main__":
    t = time.time()
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default='raw_user_follow.tsv')
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.005,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.4,
                         type='float')

    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
            inFile = sys.stdin
    elif options.input is not None:
            inFile = dataFromFile(options.input)
    else:
            print 'No dataset filename specified, system with exit\n'
            sys.exit('System will exit')

    minSupport = options.minS
    minConfidence = options.minC

    items, rules = runApriori(inFile, minSupport, minConfidence)

    printResults(items, rules)
    t2 = time.time()
    print "\nDuration: " + str(t2 - t)