import re,docx,os,difflib,time
from PyQt5.QtWidgets import *
from pathlib import Path

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

# 判断文件后缀
def endWith(s,*endstring):
    array = map(s.endswith, endstring)
    return True in array

from datasketch import MinHash, MinHashLSH
from nltk import ngrams

# data = ['而且因为没丝黛芬妮水电费我是猪',
#   '我是猪',
#   'ni是猪',
# ]



# Create an MinHashLSH index optimized for Jaccard threshold 0.5,
# that accepts MinHash objects with 128 permutations functions
# lsh = MinHashLSH(threshold=0.3, num_perm=128)
#
# # Create MinHash objects
# minhashes = {}
# for c, i in enumerate(data):
#   minhash = MinHash(num_perm=128)
#   for d in ngrams(i, 1):
#     minhash.update("".join(d).encode('utf-8'))
#   lsh.insert(c, minhash)
#   minhashes[c] = minhash
#
# for i in range(len(minhashes.keys())):
#   result = lsh.query(minhashes[i])
#   print("Candidates with Jaccard similarity > 0.5 for input", i,":", result)


def checkDuplicateWithoutTitle(dir):

    if dir=='':
        print("请选择需要查重试卷的存放路径！")
        return

    if Path(dir).exists()==False:
        print('该路径不存在！')
        return

    start = time.time()
    dirFiles = os.listdir(dir)

    pattern = re.compile(r'\n[1-9][0-9]{0,2}[、|.].*?(?=\n[1-9][0-9]{0,2}[、|.])', re.S)  # 查找数字
    filenameList = []
    hasDocx = False
    questionList = []

    for file in dirFiles:
        if endWith(file, 'docx'):
            # print(file)
            hasDocx = True
            try:
                text = getText(dir + '/' + file)
            except Exception as e:
                print("文件【"+file+"】已打开，请关闭后重试！")
                return
            text=text+"\n100."
            resList = pattern.findall(text)
            questionList.extend(resList)

            for res in resList:
                filenameList.append(file)

            print('【' + file + '】 | 共匹配到【%d】题' % len(resList))
    print('======================================')

    if not (hasDocx):
        print('该目录下找不到任何docx文件')

    print('【共匹配到%d题】' % len(questionList))

    questionlistFixed=[]

    for question in questionList:
        questionlistFixed.append(re.sub('\s+', '', question).strip())

    collectionIndexArray=[-1 for i in range(len(questionlistFixed))]
    collections=[]

    lsh = MinHashLSH(threshold=0.85, num_perm=256)

    # Create MinHash objects
    minhashes = {}
    for c, i in enumerate(questionlistFixed):
        minhash = MinHash(num_perm=256)
        for d in ngrams(i, 2):
            minhash.update("".join(d).encode('utf-8'))
        lsh.insert(c, minhash)
        minhashes[c] = minhash

    for i in range(len(minhashes.keys())):
        result = lsh.query(minhashes[i])
        if len(result) >= 2:

            newcollection = True
            findIndex = -1

            for index in result:
                if collectionIndexArray[index] != -1:
                    newcollection = False
                    findIndex = collectionIndexArray[index]
                    break;

            if newcollection:
                collections.append(result)
            else:
                collections[findIndex] = list(set(collections[findIndex]).union(set(result)))

            letindex = len(collections)-1 if newcollection else findIndex

            for index in result:
                collectionIndexArray[index] = letindex

    print(len(collections))

    for array in collections:
        print("\r")
        for index in array:
            print(filenameList[index],"")

        for index in array:
            print(questionlistFixed[index])

    end = time.time()
    print("Execution Time: %f" %(end - start))

checkDuplicateWithoutTitle("E:\\mcp\\word试题查重\\test\\")
