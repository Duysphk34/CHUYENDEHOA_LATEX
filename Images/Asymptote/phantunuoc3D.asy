import three;
import solids;
size(200);
currentprojection = orthographic(
  camera=(4,3,2),
  up=(0,0,1),
  target=(0,0,0),
  zoom=0.8
);

// Định nghĩa góc và độ dài liên kết
real bondAngle = 108; // độ
real bondLength = 0.95; // Ångström

// Tính toán vị trí các nguyên tử
triple O = (0,0,0);  // Oxy ở tâm
triple H1 = bondLength * (sin(bondAngle/2 * pi/180), cos(bondAngle/2 * pi/180), 0);
triple H2 = bondLength * (-sin(bondAngle/2 * pi/180), cos(bondAngle/2 * pi/180), 0);

// Hàm vẽ hình cầu
void drawAtom(triple center, real radius, pen p) {
  draw(sphere(center, radius).surface(new pen(int i, real j) {return p;}));
}

// Hàm vẽ liên kết
void drawBond(triple start, triple end, real radius, pen p) {
  draw(cylinder(start, radius, abs(end-start), end-start).surface(new pen(int i, real j) {return p;}));
}

// Vẽ các nguyên tử
drawAtom(O, 0.3, red);  // Oxy
drawAtom(H1, 0.1, gray(0.5));  // Hydro 1
drawAtom(H2, 0.1, gray(0.5));  // Hydro 2

// Vẽ các liên kết
drawBond(O, H1, 0.05, gray(0.7));
drawBond(O, H2, 0.05, gray(0.7));

// Thêm nhãn cho các nguyên tử
label("O", O, S);
label("H", H1, N);
label("H", H2, N);

// Vẽ góc để minh họa
draw(arc(O, 0.4*H1, 0.4*H2), blue+dashed);
label(format("%.1f°", bondAngle), (0, 0.3, 0), blue);