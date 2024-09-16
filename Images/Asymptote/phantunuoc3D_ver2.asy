settings.outformat="pdf";
settings.prc=true;
//settings.prc=false; 
settings.render=12;
import three;
import solids;
size(200);
currentprojection = orthographic(
  camera=(0,0.5,10),
  up=(0,0,1),
  target=(0,0,0),
  zoom=0.95
);

// Định nghĩa góc và độ dài liên kết
real bondAngle = 104.5; // độ (giá trị chính xác cho H2O)
real bondLength = 0.95; // Ångström
pen xanhdam = rgb(3,52,110); // Màu xanh đậm tùy chỉnh
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
label("\large\bfseries\sffamily O", O, 9.0S,xanhdam);
label("\bfseries\sffamily H", H1, 4.0NW,xanhdam);
label("\bfseries\sffamily H", H2, 4.0NE, xanhdam);

// Vẽ cung tròn để minh họa góc liên kết
path3 anglePath = arc(O, 0.6*H1, 0.6*H2);
draw(anglePath, xanhdam+dashed);

// Tính toán vị trí cho nhãn góc
triple angleLabel = relpoint(anglePath, 0.5);
angleLabel = angleLabel + -1.5*(0,0,1); // Điều chỉnh vị trí lên cao hơn

// Hiển thị nhãn góc
label(format("\sffamily %.1f°", bondAngle), angleLabel, xanhdam);