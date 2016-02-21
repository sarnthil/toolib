import sys
# from toolib import Tree
from homework6 import PTree, Tree
from collections import defaultdict

rules = {
        'S' :{('NP','VP'):1.0},
        'NP' : {('Det', 'N'):0.7, ('NP', 'PP'):0.3},
        'VP' : {('V', 'NP'):0.6, ('VP', 'PP'):0.4},
        'PP' : {('P', 'NP'):1.0},
        }
r = defaultdict(dict)
for key, value in rules.items():
    for element in value:
        r[element][key] = value[element]
rules = r

lexicon = {
            'N': {'cat':0.2,'man':0.3,'woman':0.3,'telescope':0.1,'saw':0.1},
            'Det' : {'the':0.7,'a':0.3},
            'P' : {'with':0.3,'on':0.25,'above':0.25,'under':0.1,'by':0.1},
            'V' : {'fucked':0.5,'saw':0.5},
            }

l = defaultdict(dict)
for head in lexicon:
    for word, prob in lexicon[head].items():
        l[word][head] = prob
lexicon = l

chart = defaultdict(list)

def cyk(sentence):
    """Given a sentence return a list of possible tree parses."""
    sentence = sentence.split()
    for index, word in enumerate(sentence):
        for pos in lexicon[word]:
            tree = PTree(pos, lexicon[word][pos])
            tree.children = [PTree(word)]
            chart[(index,index)].append(tree)
    length = len(sentence)
    for i in range(1, length):
        for j in range(length-i):
            for k in range(i):
                # print((j, j+k), (j+k+1, j+i))
                for left in chart[(j,j+k)]:
                    for right in chart[(j+k+1,j+i)]:
                        for head in rules[left.label,right.label]:
                            tree = PTree(head, rules[left.label, right.label][head])
                            tree.children = [left, right]
                            chart[(j,j+i)].append(tree)
    return chart[(0,length-1)]


if __name__ == '__main__':
    trees = cyk('the saw saw the saw')
    for tree in trees:
        print(tree, tree.prob)
