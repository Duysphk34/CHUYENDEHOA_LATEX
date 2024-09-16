
import random
import numpy as np
import sympy as sp
import os,codecs,re
cur_path = os.path.dirname(__file__)
TDir=cur_path
# Thumuclamviec="D:\\MYDOCUMENT\\LATEX_DOCUMENT\\SOANLATEX_2024\\MYTEMPLATE_DETHI_2024\\DuLieu\\Toan_9"
Thumuclamviec=cur_path+"\\DuLieu\\Toan_9"
os.chdir(Thumuclamviec)
Cacfile=os.listdir(Thumuclamviec)
fileN=Thumuclamviec+"\\Tuyensinhvao10"
if not os.path.exists(fileN):
	os.makedirs(fileN)
Tempt= "Xin chào Duy"
with codecs.open(fileN+"\\Tugiacnoitiep.tex",'w', 'utf-8') as (f):
	f.write(Tempt)
	f.close()
# ####======Tạo file Main==============####
Pathinput="DuLieu/Toan_9/Tuyensinhvao10/Tugiacnoitiep.tex"
filedau= cur_path +"\\DuLieu\\begin.tex"
filecuoi= cur_path +"\\DuLieu\\end.tex"
fileMain = cur_path + '\\Tuyensinhvao10-23-24.tex'
Begin=codecs.open(filedau, 'r', 'utf-8').read()
Begin=Begin.strip()
Midle=f"""\n\\chapter{{Tổng hợp bài toán tứ giác nội tiếp 9}}
\\input{{{Pathinput}}}
"""
End=codecs.open(filecuoi, 'r', 'utf-8').read()
with codecs.open(fileMain, 'w', 'utf-8') as (f):
	f.write(Begin)
	f.write(Midle)
	f.write(End)
	f.close()
# os.startfile(fileMain)
# os.startfile(TDir)