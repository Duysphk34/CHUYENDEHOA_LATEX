if(!settings.multipleView) settings.batchView=false;
settings.tex="pdflatex";
defaultfilename="Dagiacdeu-1";
if(settings.render < 0) settings.render=4;
settings.outformat="";
settings.inlineimage=true;
settings.embed=true;
settings.toolbar=false;
viewportmargin=(2,2);

settings.outformat="pdf";
import math;
size(200);
unitsize(1cm);dotfactor=1.2;
defaultpen(fontsize(5pt));
//Khai báo các điểm
pair A=(0,0),B=(2,0),C=(2,2),D=(0,2), O=(0,0);
//Định nghĩa màu
pen mycolor = rgb(3,52,110);
real r=2;
pen pa=fontsize(5pt)+1bp+mycolor; // dinh nghia kieu but
add(shift(-2,-2)*grid(4,4,gray));
draw(rotate(22.5)*scale(r)*polygon(8),mycolor);
//------
label("\sffamily N",O+r*N,N,pa);
label("\sffamily S",O+r*S,S,pa);
label("\sffamily W",O+r*W,W,pa);
label("\sffamily E",O+r*E,E,pa);
label(rotate(45)*"\sffamily NE",O+r*NE,NE,pa);
label(rotate(-45)*"\sffamily SE",O+r*SE,SE,pa);
label(rotate(-45)*"\sffamily NW",O+r*NW,NW,pa);
label(rotate(45)*"\sffamily SW",O+r*SW,SW,pa);
