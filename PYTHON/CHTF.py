
import random
CHTF=[]
###===========Nội dung cau hỏi dạng 1===============####
df = {}
###===============Câu hoi 1=================###
cau1="Trong các phát biểu sau, phát biểu nào đúng, phát biểu nào sai?"
PAcau1={
    "sub1": ["\\True ", "Nội dung phát biểu A"],
    "sub2": ["", "Nội dung phát biểu  B"],
    "sub3": ["\\True ", "Nội dung phát biểu  C"],
    "sub4": ["\\True ", "Nội dung phát biểu  D"],
    "sub5": ["", "Nội dung phát biểu  E"],
    "sub6": ["\\True", "Nội dung phát biểu  F"],
    "sub6": ["\\True", "Nội dung phát biểu  G"],
    "sub7": ["\\True", "Nội dung phát biểu  H"],
    "sub8": ["\\True", "Nội dung phát biểu  I"],
}
PAcau1["sub1"].append("Nội dung lời giải phát biểu ý 1")
PAcau1["sub2"].append("Nội dung lời giải phát biểu ý 2")
PAcau1["sub3"].append("Nội dung lời giải phát biểu ý 3")
PAcau1["sub4"].append("Nội dung lời giải phát biểu ý 4")
PAcau1["sub5"].append("Nội dung lời giải phát biểu ý 5")
PAcau1["sub6"].append("Nội dung lời giải phát biểu ý 6")
PAcau1["sub7"].append("Nội dung lời giải phát biểu ý 7")
PAcau1["sub8"].append("Nội dung lời giải phát biểu ý 8")
###===============Câu hoi 2=================###
cau2="Trong các mệnh đề sau, mệnh đề nào đúng, mệnh đề nào sai?"
PAcau2={
    "sub1": ["\\True ", "Nội dung mệnh đề A"],
    "sub2": ["","Nội dung mệnh đề B"],
    "sub3": ["\\True ", "Nội dung mệnh đề C"],
    "sub4": ["\\True ", "Nội dung mệnh đề D"],
    "sub5": ["", "Nội dung mệnh đề E"],
    "sub6": ["\\True", "Nội dung phát biểu  F"],
    "sub6": ["\\True", "Nội dung phát biểu  G"],
    "sub7": ["\\True", "Nội dung phát biểu  H"],
    "sub8": ["\\True", "Nội dung phát biểu  I"],
    
}
PAcau2["sub1"].append("Nội dung lời giải mệnh đề ý 1")
PAcau2["sub2"].append("Nội dung lời giải mệnh đề ý 2")
PAcau2["sub3"].append("Nội dung lời giải mệnh đề ý 3")
PAcau2["sub4"].append("Nội dung lời giải mệnh đề ý 4")
PAcau2["sub5"].append("Nội dung lời giải mệnh đề ý 5")
PAcau2["sub5"].append("Nội dung lời giải mệnh đề ý 5")
PAcau2["sub6"].append("Nội dung lời giải mệnh đề ý 6")
PAcau2["sub7"].append("Nội dung lời giải mệnh đề ý 7")
PAcau2["sub8"].append("Nội dung lời giải mệnh đề ý 8")
###===============Câu hoi 3=================###
cau3="Trong các phát biểu sau, nhận định nào đúng, nhận định nào sai?"
PAcau3={
    "sub1": ["\\True ", "Nội dung nhận định A"],
    "sub2": ["","Nội dung nhận định B"],
    "sub3": ["\\True ", "Nội dung nhận định C"],
    "sub4": ["\\True ", "Nội dung nhận định D"],
    "sub5": ["\\True ", "Nội dung nhận định E"],
    "sub6": ["\\True", "Nội dung phát biểu  F"],
    "sub6": ["\\True", "Nội dung phát biểu  G"],
    "sub7": ["\\True", "Nội dung phát biểu  H"],
    "sub8": ["\\True", "Nội dung phát biểu  I"],
}
PAcau3["sub1"].append("Nội dung lời giải nhận định ý 1")
PAcau3["sub2"].append("Nội dung lời giải nhận định ý 2")
PAcau3["sub3"].append("Nội dung lời giải nhận định ý 3")
PAcau3["sub4"].append("Nội dung lời giải nhận định ý 4")
PAcau3["sub5"].append("Nội dung lời giải nhận định ý 5")
PAcau3["sub6"].append("Nội dung lời giải nhận định ý 6")
PAcau3["sub7"].append("Nội dung lời giải nhận định ý 7")
PAcau3["sub8"].append("Nội dung lời giải nhận định ý 8")
###==============Câu hỏi 4============================%%%
df.update({cau1:PAcau1})
df.update({cau2:PAcau2})
df.update({cau3:PAcau3})
cau=list(df.keys())
random.shuffle(cau)
Tempt=""
n=0
for db in cau:
    n+=1
    i=2*n-1
    ih=2*n
    PA=list(df[db].keys())
    random.shuffle(PA)
    Tempt+=f"\n%%%=======EX_{i}========%%%"\
     +"\n\\begin{ex}"
    Tempt+=f"\n{db}"
    Tempt+="\n\\choiceTF"
    for j in range(0,4):
        Tempt+=f"\n\t{{{df[db][PA[j]][0]}{df[db][PA[j]][1]}}}"
    Tempt+=f"\n\\loigiai{{"\
        +"\n\t\\begin{enumerate}[a)]"
    for k in range(0,4):
        Tempt+=f"\n\t\\item {df[db][PA[k]][2]}"
    Tempt+="\n\t\\end{enumerate}"\
        +f"\n}}"
    Tempt+="\n\\end{ex}"

    Tempt+=f"\n%%%=======EX_{ih}========%%%"\
     +"\n\\begin{ex}"
    Tempt+=f"\n{db}"
    Tempt+="\n\\choiceTF"
    for jm in range(4,8):
        Tempt+=f"\n\t{{{df[db][PA[jm]][0]}{df[db][PA[jm]][1]}}}"
    Tempt+=f"\n\\loigiai{{"\
        +"\n\t\\begin{enumerate}[a)]"
    for km in range(4,8):
        Tempt+=f"\n\t\\item {df[db][PA[km]][2]}"
    Tempt+="\n\t\\end{enumerate}"\
        +f"\n}}"
    Tempt+="\n\\end{ex}"
print(Tempt)

    


