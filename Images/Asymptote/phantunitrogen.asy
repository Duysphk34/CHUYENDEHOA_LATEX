settings.outformat="png";
settings.prc=true;
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

// Định nghĩa độ dài liên kết
real bondLength = 1.1; // Ångström (giá trị gần đúng cho N2)
pen xanhdam = rgb(0,112,192); // Màu xanh đậm tùy chỉnh
pen redcolor = rgb(237,85,101);// Màu đỏ tùy chỉnh
// Tính toán vị trí các nguyên tử
triple N1 = (-bondLength/2, 0, 0);
triple N2 = (bondLength/2, 0, 0);

// Hàm vẽ hình cầu
void drawAtom(triple center, real radius, pen p) {
  draw(sphere(center, radius).surface(new pen(int i, real j) {return p;}));
}

// Hàm vẽ liên kết
void drawBond(triple start, triple end, real radius, pen p) {
  draw(cylinder(start, radius, abs(end-start), end-start).surface(new pen(int i, real j) {return p;}));
}

// Vẽ các nguyên tử nitrogen
drawAtom(N1, 0.3, xanhdam);  // Nitrogen 1
drawAtom(N2, 0.3, xanhdam);  // Nitrogen 2

// Vẽ ba liên kết (để tạo liên kết ba)
real bondRadius = 0.04;
real bondOffset = 0.15; // Tăng khoảng cách giữa các liên kết
drawBond(N1, N2, bondRadius, redcolor);
drawBond(N1 + (0,bondOffset,0), N2 + (0,bondOffset,0), bondRadius, redcolor);
drawBond(N1 + (0,-bondOffset,0), N2 + (0,-bondOffset,0), bondRadius, redcolor);

//// Thêm nhãn cho các nguyên tử
//label("\large\bfseries\sffamily N", N1, 3.0W, xanhdam);
//label("\large\bfseries\sffamily N", N2, 3.0E, xanhdam);

//// Hiển thị độ dài liên kết
//triple bondLabelPos = (0, bondLength/2, 0);
//label(format("\sffamily %.2f Å", bondLength), bondLabelPos, 2.0N, xanhdam);














