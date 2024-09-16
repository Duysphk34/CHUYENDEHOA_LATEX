
import random
nganhang={
"cauNB":["Câu 1", "Câu 2", "Câu 3"],
"cauTH":["Câu 4", "Câu 5", "Câu 6"],
"cauVD":["Câu 7", "Câu 8", "Câu 9"],
"cauVDC":["Câu 10", "Câu 11", "Câu 12","Câu 13"]
}
socauNB=2
socauTH=2
socauVD=1
socauVDC=2
Matran=[socauNB,socauTH,socauVD,socauVDC]
detaora=[]
for i in range(Matran[0]):
    random.shuffle(nganhang["cauNB"])
    choncauNB=random.choice(nganhang["cauNB"])
    detaora.append(choncauNB)
    nganhang["cauNB"].remove(choncauNB)
for j in range(Matran[1]):
    random.shuffle(nganhang["cauTH"])
    choncauTH=random.choice(nganhang["cauTH"])
    detaora.append(choncauTH)
    nganhang["cauTH"].remove(choncauTH)
for k in range(Matran[2]):
    random.shuffle(nganhang["cauVD"])
    choncauVD=random.choice(nganhang["cauVD"])
    detaora.append(choncauVD)
    nganhang["cauVD"].remove(choncauVD)
for l in range(Matran[3]):
    random.shuffle(nganhang["cauVDC"])
    choncauVDC=random.choice(nganhang["cauVDC"])
    detaora.append(choncauVDC)
    nganhang["cauVDC"].remove(choncauVDC)
print(detaora)
    


