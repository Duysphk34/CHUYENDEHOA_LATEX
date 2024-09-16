settings.outformat="png";
settings.prc=false;
settings.render=12;

import three;
import solids;

size(200);

currentprojection = orthographic(
  camera=(15,4,5),
  up=(0,1,0),
  target=(0,0,0),
  zoom=1.0
);

// Định nghĩa góc và độ dài liên kết
real bondAngle = acos(-1/3); // Góc tứ diện chính xác (arccos(-1/3) ≈ 109.47°)
real bondLength = 1.54; // Ångström (độ dài liên kết C-C)
real CHbondLength = 1.09; // Ångström (độ dài liên kết C-H)
real rotationAngle = 60 * pi/180; // Góc xoay 60 độ

// Tính toán vị trí các nguyên tử
triple C1 = (0,0,0);  // Carbon 1 ở tâm

// Hàm tạo vector cho liên kết từ tâm với phép xoay
triple bondVector(real theta, real phi, real rotation) {
    real x = sin(theta)*cos(phi);
    real y = sin(theta)*sin(phi);
    real z = cos(theta);
    real newX = x*cos(rotation) - y*sin(rotation);
    real newY = x*sin(rotation) + y*cos(rotation);
    return unit((newX, newY, z));
}

// Tính toán vị trí các nguyên tử ở đỉnh tứ diện
triple C2 = C1 + bondLength * bondVector(0, 0, 0); // Carbon 2 ở trục z dương
triple H1 = C1 + CHbondLength * bondVector(bondAngle, 0, 0);
triple H2 = C1 + CHbondLength * bondVector(bondAngle, 2pi/3, 0);
triple H3 = C1 + CHbondLength * bondVector(bondAngle, 4pi/3, 0);

// Tính toán vị trí các nguyên tử H xung quanh C2 với phép xoay
triple H4 = C2 + CHbondLength * bondVector(pi - bondAngle, 0, rotationAngle);
triple H5 = C2 + CHbondLength * bondVector(pi - bondAngle, 2pi/3, rotationAngle);
triple H6 = C2 + CHbondLength * bondVector(pi - bondAngle, 4pi/3, rotationAngle);

// Hàm vẽ hình cầu
void drawAtom(triple center, real radius, pen p) {
  draw(sphere(center, radius).surface(new pen(int i, real j) {return p;}));
}

// Hàm vẽ liên kết
void drawBond(triple start, triple end, real radius, pen p) {
  draw(cylinder(start, radius, abs(end-start), end-start).surface(new pen(int i, real j) {return p;}));
}

// Vẽ các nguyên tử
drawAtom(C1, 0.3, 0.5*black+0.3*gray);  // Carbon 1 (tâm)
drawAtom(C2, 0.3, 0.5*black+0.3*gray);  // Carbon 2
drawAtom(H1, 0.15, white);  // Hydro 1
drawAtom(H2, 0.15, white);  // Hydro 2
drawAtom(H3, 0.15, white);  // Hydro 3
drawAtom(H4, 0.15, white);  // Hydro 4
drawAtom(H5, 0.15, white);  // Hydro 5
drawAtom(H6, 0.15, white);  // Hydro 6

// Vẽ các liên kết
drawBond(C1, C2, 0.07, gray(0.7));  // Liên kết C-C
drawBond(C1, H1, 0.04, gray(0.7));
drawBond(C1, H2, 0.04, gray(0.7));
drawBond(C1, H3, 0.04, gray(0.7));
drawBond(C2, H4, 0.04, gray(0.7));
drawBond(C2, H5, 0.04, gray(0.7));
drawBond(C2, H6, 0.04, gray(0.7));

