import re,docx,os,difflib,time
from PyQt5.QtWidgets import *
from pathlib import Path

def getText(filename):
    doc = docx.Document(filename)
    fullText=[]
    for para in doc.paragraphs:
        fullText.append(para.text)
    fullText.append('100.')
    return '\n'.join(fullText)

def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

# 判断文件后缀
def endWith(s,*endstring):
    array = map(s.endswith, endstring)
    return True in array

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

    print(titleList)

    pattern = re.compile(r'\n[1-9][0-9]{0,2}[、|.].*?(?=\n[1-9][0-9]{0,2}[、|.])', re.S)  # 查找数字

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
            text = getText(dir + '/' + file)
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

                    resList = pattern.findall(text, startPos, endPos)

                    sectionQuesList[i].extend(resList)

                    for c in resList:
                        filenameList[i].append(file)

                    questionNum = questionNum + len(resList)
                    obj.appendSignal.emit("【" + file + "】 | 【" + titleList[i].replace('\n','') + "】匹配到【%d】条"%len(resList))
                else:
                    obj.appendSignal.emit(
                        "【" + file + "】 | 【" + titleList[i].replace('\n', '') + "】没有匹配到该标题！请检查！")

            obj.appendSignal.emit("======================================\n")

    if not(hasDocx):
        obj.appendSignal.emit('该目录下找不到任何docx文件')
        return

    progress=0
    for sectionQues in sectionQuesList:
        for i in range(len(sectionQues) - 1):
            for j in range(i + 1, len(sectionQues)):
                ss = string_similar(sectionQues[i], sectionQues[j])

                if ss > 0.9:
                    # print('【' + filenameList[sectionQuesList.index(sectionQues)][i] + '】' + sectionQues[i] + '\n\n【' +
                    #       filenameList[sectionQuesList.index(sectionQues)][j] + '】' + sectionQues[j])
                    # print("相似度=%f" % ss)
                    # print("=====================")
                    obj.appendSignal.emit('【' + filenameList[sectionQuesList.index(sectionQues)][i] + '】' + sectionQues[i] + '\n\n【' +
                           filenameList[sectionQuesList.index(sectionQues)][j] + '】' + sectionQues[j])
                    obj.appendSignal.emit("\n【相似度=%f】" % ss)
                    obj.appendSignal.emit("======================================")
                    QApplication.processEvents()
            progress = progress + 1
            percent = progress / (questionNum-1)
            obj.updateProgressSignal.emit(percent * 100)

        progress=progress+1

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

    obj.appendSignal.emit('======================================')
    for file in dirFiles:
        if endWith(file, 'docx'):
            # print(file)
            hasDocx = True
            text = getText(dir + '/' + file)
            resList = pattern.findall(text)
            questionList.extend(resList)

            for res in resList:
                filenameList.append(file)

            obj.appendSignal.emit('【' + file + '】 | 共匹配到【%d】题' % len(resList))
    obj.appendSignal.emit('======================================')

    if not (hasDocx):
        obj.appendSignal.emit('该目录下找不到任何docx文件')

    obj.appendSignal.emit('【共匹配到%d题】' % len(questionList))
    for i in range(len(questionList) - 1):

        for j in range(i + 1, len(questionList)):

            sim = string_similar(questionList[i], questionList[j])

            if sim > 0.9:
                obj.appendSignal.emit('======================================')
                obj.appendSignal.emit('【' + filenameList[i] + '】' + questionList[i] + '\n\n【' + filenameList[j] + '】' + questionList[j])
                obj.appendSignal.emit('\n【相似度=%f】' % sim)
                QApplication.processEvents()

        percent = (i+1) / (len(questionList)-1)
        # print(percent)
        obj.updateProgressSignal.emit(percent * 100)

    end = time.time()
    obj.appendSignal.emit("Execution Time: %f" %(end - start))