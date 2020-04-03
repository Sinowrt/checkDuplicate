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



