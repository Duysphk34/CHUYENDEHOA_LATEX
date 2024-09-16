import random
import numpy as np
import sympy as sp
import os,codecs,re
def DanhSoMoiTruong(File):
	Noidung=File
	#Xoa đánh số cũ
	Noidung=re.sub('\n\\s*%%(.*?)%%?','',Noidung)
	#Đánh số câu hỏi
	DanhSachMoiTruong=['ex','bt','dn']
	for mt in DanhSachMoiTruong:
		i=0
		while '\\begin{'+mt+'}' in Noidung:
			i+=1
			Noidung=Noidung.replace('\\begin{'+mt+'}','\n%%%============='+mt.upper()+'_' + str(i) +'=============%%%\nbegin@ex@#',1)
		Noidung=Noidung.replace('begin@ex@#','\\begin{'+mt+'}')
	Noidung=re.sub(r'\n\s*\n+','\n\n',Noidung)
	return Noidung.strip()