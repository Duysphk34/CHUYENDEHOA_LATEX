if(!settings.multipleView) settings.batchView=false;
settings.tex="pdflatex";
defaultfilename="propan-1";
if(settings.render < 0) settings.render=4;
settings.outformat="";
settings.inlineimage=true;
settings.embed=true;
settings.toolbar=false;
viewportmargin=(2,2);

settings.outformat = "pdf";
settings.prc=false;
settings.render = 12;
import three;
import solids;
size(10cm,0);
currentprojection = orthographic(
camera = (15, 4, 5),
up = (0, 1, 0),
target = (0, 0, 0),
zoom = 1.0
);

real bondAngle = acos(-1/3);
real bondLength = 1.4;
real CHbondLength = 0.8;
real rotationAngle = 60 * pi/180;

triple bondVector(real theta, real phi, real rotation) {
real x = sin(theta) * cos(phi);
real y = sin(theta) * sin(phi);
real z = cos(theta);
real newX = x * cos(rotation) - y * sin(rotation);
real newY = x * sin(rotation) + y * cos(rotation);
return unit((newX, newY, z));
}

triple C1 = (0, 0, 0);
triple C2 = C1 + bondLength * bondVector(0, 0, 0);
triple H1 = C1 + CHbondLength * bondVector(bondAngle, 0, 0);
triple H2 = C1 + CHbondLength * bondVector(bondAngle, 2pi/3, 0);
triple C3 = C1 + bondLength * bondVector(bondAngle, 4pi/3, 0);

triple H3 = C2 + CHbondLength * bondVector(pi - bondAngle, 0, rotationAngle);
triple H4 = C2 + CHbondLength * bondVector(pi - bondAngle, 2pi/3, rotationAngle);
triple H5 = C2 + CHbondLength * bondVector(pi - bondAngle, 4pi/3, rotationAngle);

triple H6 = C3 + CHbondLength * bondVector(pi, 0, rotationAngle);
triple H7 = C3 + CHbondLength * bondVector(pi - bondAngle, 2pi/3, rotationAngle);
triple H8 = C3 + CHbondLength * bondVector(pi - bondAngle, 4pi/3, rotationAngle);

void drawAtom(triple center, real radius, pen p) {
draw(sphere(center, radius).surface(new pen(int i, real j) {return p;}));
}

void drawBond(triple start, triple end, real radius, pen p) {
draw(cylinder(start, radius, abs(end - start), end - start).surface(new pen(int i, real j) {return p;}));
}

drawAtom(C1, 0.3, 0.5 * black + 0.3 * gray);
drawAtom(C2, 0.3, 0.5 * black + 0.3 * gray);
drawAtom(C3, 0.3, 0.5 * black + 0.3 * gray);
drawAtom(H1, 0.15, white);
drawAtom(H2, 0.15, white);
drawAtom(H3, 0.15, white);
drawAtom(H4, 0.15, white);
drawAtom(H5, 0.15, white);
drawAtom(H6, 0.15, white);
drawAtom(H7, 0.15, white);
drawAtom(H8, 0.15, white);

drawBond(C1, C2, 0.09, gray(0.7));
drawBond(C1, C3, 0.09, gray(0.7));
drawBond(C1, H1, 0.06, gray(0.7));
drawBond(C1, H2, 0.06, gray(0.7));
drawBond(C2, H3, 0.06, gray(0.7));
drawBond(C2, H4, 0.06, gray(0.7));
drawBond(C2, H5, 0.06, gray(0.7));
drawBond(C3, H6, 0.06, gray(0.7));
drawBond(C3, H7, 0.06, gray(0.7));
drawBond(C3, H8, 0.06, gray(0.7));
