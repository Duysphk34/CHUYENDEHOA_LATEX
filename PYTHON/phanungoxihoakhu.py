
import random
import numpy as np
import sympy as sp
import os,codecs,re
cur_path = os.path.dirname(__file__)
TDir=cur_path
Thumuclamviec=cur_path+"\\DuLieu"
Cacfile=os.listdir(Thumuclamviec)
os.chdir(Thumuclamviec)
Thumucluu=cur_path+"\\DuLieu\\Python"
if not os.path.exists(Thumucluu):
	os.makedirs(Thumucluu)
fileN=Thumucluu+"\\Redox_reaction.tex"
Tempt= "\n\\chapter{Phản ứng Oxi hóa - khử}"\
	+"\n\\section{Cân bằng phản ứng oxi hóa - khử}"\
	+"\n\\subsection{Các định nghĩa}"
with codecs.open(fileN,'w', 'utf-8') as (f):
	f.write(Tempt)
	f.close()
# ####======Tạo file Main==============####
filedau= cur_path +"\\DuLieu\\begin.tex"
filecuoi= cur_path +"\\DuLieu\\end.tex"
fileMain = cur_path + '\\Chuyen_de_Phan_ung_Oxi_hoa_khu.tex'
Begin=codecs.open(filedau, 'r', 'utf-8').read()
Begin=Begin.strip()
input_path="Dulieu/Python/Redox_reaction.tex"
Midle=f"""
\\input{{{input_path}}}
"""
End=codecs.open(filecuoi, 'r', 'utf-8').read()
with codecs.open(fileMain, 'w', 'utf-8') as (f):
	f.write(Begin)
	f.write(Midle)
	f.write(End)
	f.close()
# os.startfile(fileMain)
# os.startfile(TDir)