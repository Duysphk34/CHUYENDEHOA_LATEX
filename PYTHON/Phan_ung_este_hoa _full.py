
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
###==========Tạo câu hỏi===================###
nganhang = []
naxit=np.arange(0.01, 0.31, 0.01)
H=[60,65,70,75,80]
DB=[[x,round(60*x,3),hs,round(88*x*hs/100,3)] for x in naxit for hs in H]
random.shuffle(DB)
for i in range(len(DB)):
    debai = f"Cho ${DB[i][1]}$ gam $CH_3COOH$ tác dụng với lượng dư $C_2H_5OH$ (xúc tác ${{H_2SO_4}}_{{\\text{{đặc}}}}$, đun nóng) "\
           +f"thu được ${DB[i][3]}$ gam $CH_3COOC_2H_5$. Viết phương trình hóa học xảy ra và tính hiệu suất của phản ứng"
    loigiai = f"\\vphantom{{x}}\\hfill\\textbf{{Đáp số: }}${DB[i][2]}\\%$" 
    cauhoi = "\\begin{bt}\n" + \
     debai + "\n" + \
     "\\loigiai{\n" + \
     loigiai + "\n" + \
     "}\n" + \
     "\\end{bt}\n"
    nganhang.append(cauhoi)
Tempt = """
\\begin{tcolorbox}[
colback=\\mycolor!10,
frame empty,
fontupper =\\LARGE\\bfseries\\color{\\maudam},
halign =center
]
BÀI TẬP VỀ HIỆU SUẤT PHẢN ỨNG ESTE HÓA
\\end{tcolorbox}
""" 
start=0
end=20
for cauhoi in nganhang[start:end]:
    Tempt += cauhoi
Noidung=DanhSoMoiTruong(Tempt)	
cur_path = os.path.dirname(__file__)
Thumucdulieu=cur_path+"\\DuLieu"
os.chdir(Thumucdulieu)
Thumucluu=cur_path+"\\DuLieu\\Lop_9" 
if not os.path.exists(Thumucluu):
	os.makedirs(Thumucluu)
TDir=cur_path
if not os.path.exists(TDir):
   	os.makedirs(TDir)
input_path="DuLieu/Lop_9/Hieu_suat_phan_ung_este.tex"
fileN=Thumucluu+"\\Hieu_suat_phan_ung_este.tex"
with codecs.open(fileN, 'w', 'utf-8') as (f):
	f.write(Noidung)
	f.close()
####======Tạo file Main==============####
filedau= cur_path +"\\DuLieu\\begin.tex"
filecuoi= cur_path +"\\DuLieu\\end.tex"
fileMain = TDir + '\\Hoa_9_Phan_ung_este_hoa.tex'
Begin=codecs.open(filedau, 'r', 'utf-8').read()
Begin=Begin.strip()
Midle=f"""\\input{{{input_path}}}
"""
End=codecs.open(filecuoi, 'r', 'utf-8').read()
with codecs.open(fileMain, 'w', 'utf-8') as (f):
	f.write(Begin)
	f.write(Midle)
	f.write(End)
	f.close()
# # os.startfile(fileMain)
# os.startfile(TDir)