
import random
import numpy as np
import sympy as sp
import os,codecs,re
socau = 20
nganhang = []
for i in range(socau):
    naxit=np.random.randint(1, 31) * 0.01
    maxit= round(naxit*60,3)
    H=np.arange(60,85,5)
    hs=random.choice(H)
    mestethucte=round(88*naxit*hs/100,3)
    debai = f"Cho ${maxit}$ gam $CH_3COOH$ tác dụng với lượng dư $C_2H_5OH$ (xúc tác ${{H_2SO_4}}_{{\\text{{đặc}}}}$, đun nóng) "\
        +f"thu được ${mestethucte}$ gam $CH_3COOC_2H_5$. Viết phương trình hóa học xảy ra và tính hiệu suất của phản ứng"
    loigiai = f"\\vphantom{{x}}\\hfill\\textbf{{Đáp số: }}${hs}\\%$" 
    cauhoi = "\n%%%=============BT_"+str(i+1)+"=================%%%\n" + \
    "\\begin{bt}\n" + \
    debai + "\n" + \
    "\\loigiai{\n" + \
    loigiai + "\n" + \
    "}\n" + \
    "\\end{bt}\n"
    nganhang.append(cauhoi)
Tempt = """
\\begin{name}[Kiểm tra cuối kì II][Hóa][9][Sở Giáo dục và Đào tạo]{Trường THCS}{2023 - 2024}
\\end{name}
""" 
for cauhoi in nganhang:
    Tempt += cauhoi
Tempt=Tempt.strip()
cur_path = os.path.dirname(__file__)
Thumucdulieu=cur_path+"\\DuLieu"
os.chdir(Thumucdulieu)
Thumucluu=cur_path 
if not os.path.exists(Thumucluu):
	os.makedirs(Thumucluu)
TDir=Thumucluu
if not os.path.exists(TDir):
   	os.makedirs(TDir)
luufileN="DuLieu/Hieu_suat_phan_ung_este.tex"
fileN=TDir+"/"+luufileN
with codecs.open(fileN, 'w', 'utf-8') as (f):
	f.write(Tempt)
	f.close()
####======Tạo file Main==============####
filedau= cur_path +"\\DuLieu\\begin.tex"
filecuoi= cur_path +"\\DuLieu\\end.tex"
fileMain = TDir + '\\Hoa_9_Phan_ung_este_hoa.tex'
Begin=codecs.open(filedau, 'r', 'utf-8').read()
Begin=Begin.strip()
Midle=f"""\n\\setcounter{{tocdepth}}{{2}}
\\tableofcontents % Hiện mục lục
\\chapter{{Tổng hợp các dạng toán hóa 9}}
\\input{{{luufileN}}}
\\fileend
"""
End=codecs.open(filecuoi, 'r', 'utf-8').read()
with codecs.open(fileMain, 'w', 'utf-8') as (f):
	f.write(Begin)
	f.write(Midle)
	f.write(End)
	f.close()
# os.startfile(fileMain)
# os.startfile(TDir)