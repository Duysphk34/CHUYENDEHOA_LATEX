if(!settings.multipleView) settings.batchView=false;
settings.tex="pdflatex";
defaultfilename="cautructinhtheNaCl-1";
if(settings.render < 0) settings.render=4;
settings.outformat="";
settings.inlineimage=true;
settings.embed=true;
settings.toolbar=false;
viewportmargin=(2,2);

settings.outformat="pdf";
//settings.prc=true;
settings.prc=false;
settings.render=12;
import solids;
size(10cm,0);
currentprojection = orthographic(5,4,2);
pen cyl_color=lightgray;
real r=0.1;
for(int i=0; i<3; ++i)
for(int j=0; j<3; ++j) {
draw(surface(cylinder((i,0,j), 0.03, 2, Y)), cyl_color);
draw(surface(cylinder((0,i,j), 0.03, 2, X)), cyl_color);
draw(surface(cylinder((i,j,0), 0.03, 2, Z)), cyl_color);
}
for(int k=0; k<3; ++k)
for(int i=0; i<3; ++i)
for(int j=0; j<3; ++j) {
revolution s=sphere((i, j, k), r, n=100);
if (k%2==0) {
if ((i+j)%2==1) draw(surface(s), green);
else draw(surface(s), red);
} else {
if ((i+j)%2==1) draw(surface(s), red);
else draw(surface(s), green);
}
}
