import re,docx,os,difflib,time,traceback
from PyQt5.QtWidgets import *
from pathlib import Path
from datasketch import MinHash, MinHashLSH
from nltk import ngrams

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

def lsh(questionList):
    collectionIndexArray = [-1 for i in range(len(questionList))]
    collections = []

    lsh = MinHashLSH(threshold=0.85, num_perm=256)

    minhashes = {}
    for c, i in enumerate(questionList):
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

            letindex = len(collections) - 1 if newcollection else findIndex

            for index in result:
                collectionIndexArray[index] = letindex

    return collections

def ckduplicate(dir,obj):

    if dir=='':
        QMessageBox.warning(obj.centralwidget, "Warning","请选择需要查重试卷的存放路径！")
        return

    questionNum=0
    start = time.time()

    # titleList = ['公共基础知识\n', '判断推理\n', '数量关系\n', '言语理解与表达\n', '资料分析\n']

    titleList=obj.string_list.copy()

    for i in range(len(titleList)):
        titleList[i]=titleList[i]+'\n'

    # 查找数字
    pattern = re.compile(r'\n[1-9][0-9]{0,2}[、|.].*?(?=\n[1-9][0-9]{0,2}[、|.])', re.S)

    # 获取文档对象
    # dir = 'E:\\mcp\\word试题查重'
    if Path(dir).exists() == False:
        obj.appendSignal.emit('该路径不存在！')
        return

    dirFiles = os.listdir(dir)

    sectionQuesList = []
    filenameList = []

    for title in titleList:
        sectionQuesList.append([])
        filenameList.append([])

    hasDocx=False
    for file in dirFiles:
        if endWith(file, 'docx'):
            hasDocx=True
            try:
                text = getText(dir + '/' + file)
            except Exception as e:
                obj.appendSignal.emit("文件【"+file+"】已打开，请关闭后重试！")
                return

            posList = []

            for i in range(len(titleList)):
                posList.append(text.find(titleList[i]))

            posList.append(len(text))

            tempPosList = posList.copy()
            tempPosList.sort()

            obj.appendSignal.emit("======================================")

            for i in range(len(posList) - 1):
                if (posList[i] != -1):
                    startPos = posList[i]

                    endPos = tempPosList[tempPosList.index(posList[i]) + 1]

                    foundStr=text[startPos:endPos]+"\n100."

                    resList = pattern.findall(foundStr)

                    sectionQuesList[i].extend(resList)

                    for c in resList:
                        filenameList[i].append(file)

                    questionNum = questionNum + len(resList)
                    obj.appendSignal.emit("【" + file + "】 | 【" + titleList[i].replace('\n','') + "】匹配到【%d】条"%len(resList))
                else:
                    obj.appendSignal.emit(
                        "【" + file + "】 | 【" + titleList[i].replace('\n', '') + "】没有匹配到该标题！请检查！")

            obj.appendSignal.emit("======================================")



    if not(hasDocx):
        obj.appendSignal.emit('该目录下找不到任何docx文件')
        return

    progress=1

    for x in range(len(sectionQuesList)):

        questionlistFixed = []

        # 删掉空格、制表符、换行符
        for question in sectionQuesList[x]:
            questionlistFixed.append(re.sub('\s+', '', question).strip())

        collections=lsh(questionlistFixed)

        try:
            printStr = ""

            for array in collections:
                for index in array:
                    printStr = printStr + "【"+filenameList[x][index] + "】\n"
                    printStr = printStr + questionlistFixed[index]+ "\n"

                printStr = printStr + "==============================\n"

            if len(printStr) != 0:
                obj.appendSignal.emit(printStr)
            percent = progress / len(sectionQuesList)
            obj.updateProgressSignal.emit(percent * 100)
            progress=progress+1

        except Exception as e:
            traceback.print_exc()

    end = time.time()
    obj.appendSignal.emit("Execution Time: %f" %(end - start))

def checkDuplicateWithoutTitle(dir,obj):

    if dir=='':
        QMessageBox.warning(obj.centralwidget, "Warning","请选择需要查重试卷的存放路径！")
        return

    if Path(dir).exists()==False:
        obj.appendSignal.emit('该路径不存在！')
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
                obj.appendSignal.emit("文件【"+file+"】已打开，请关闭后重试！")
                return
            text=text+"\n100."
            resList = pattern.findall(text)
            questionList.extend(resList)

            for res in resList:
                filenameList.append(file)

            obj.appendSignal.emit('【' + file + '】 | 共匹配到【%d】题' % len(resList))
    obj.appendSignal.emit('======================================')

    if not (hasDocx):
        obj.appendSignal.emit('该目录下找不到任何docx文件')

    obj.appendSignal.emit('【共匹配到%d题】' % len(questionList))

    obj.appendSignal.emit('======================================\n')

    questionlistFixed = []

    # 删掉空格、制表符、换行符
    for question in questionList:
        questionlistFixed.append(re.sub('\s+', '', question).strip())

    obj.updateProgressSignal.emit(30)

    collections = lsh(questionlistFixed)

    try:
        printStr = ""
        progress=1
        # 判断是否找到重复的题目
        if len(collections)==0:
            obj.updateProgressSignal.emit(100)
            obj.appendSignal.emit("在该题集中未找到重复的题目。")
        else:
            for array in collections:
                percent = progress / len(collections)
                obj.updateProgressSignal.emit(30 if percent * 100 <= 30 else percent * 100)
                progress=progress+1
                for index in array:
                    printStr = printStr + "【" + filenameList[index] + "】\n"
                    printStr = printStr + questionlistFixed[index] + "\n\n"

                printStr = printStr + "==============================\n"

                if len(printStr) != 0:
                    obj.appendSignal.emit(printStr)

    except Exception as e:
        traceback.print_exc()

    end = time.time()
    obj.appendSignal.emit("Execution Time: %f" %(end - start))