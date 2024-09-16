settings.outformat="pdf";
size(200);
unitsize(1cm);dotfactor=2;
texpreamble("\usepackage{sansmathfonts}");
defaultpen(fontsize(6pt) + linewidth(0.5bp));
pen xanhdam = rgb(3,52,110); // Màu xanh đậm tùy chỉnh
pen trang = rgb(255,255,255); // Màu trăng
//Trộn hai màu và tăng độ trong suốt
//pen customColor = 0.7*xanhdam + 0.3*trang + opacity(0.3);
pen customColor = 0.7*xanhdam;
pen p = linetype("3 6");
real r=1.6; 
real labelDistance=1.0; 
pair O =0;
pair A=r*dir(60);
dot("$\mathbf{O}$",O,align=dir(-90)*labelDistance);
//draw(Label("$x$",align=S,Relative(.5)),(-0.2,0)--(3.0,0),customColor,Arrow(HookHead(barb=1.2),size=0.8mm));
draw(Label("$\mathbf{x}$", EndPoint, align=N, currentpen), (-0.2,0)--(3.0,0),customColor,  Arrow(HookHead(barb=1.2),size=0.8mm));
draw(Label("$\mathbf{r}$", LeftSide,currentpen),O--A,customColor,Arrow(HookHead(barb=1.2),size=0.8mm));
//dot("$A=r*dir(60^\circ)$",A,align=E);
label("$A=r*dir(60^\circ)$",A,align=E);
draw(Label("\tiny $60^\circ$",align=-0.05*dir(40),Rotate(degrees(atan2(3.0-(-0.2), 0-0)))),arc(0,0.3,0,60),customColor,Arrow(HookHead(barb=1.2),size=0.5mm));