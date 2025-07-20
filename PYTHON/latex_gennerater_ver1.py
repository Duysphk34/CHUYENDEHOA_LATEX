import sys
import os
import codecs
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QMenu, QMessageBox, QTextEdit, QHBoxLayout,
                            QInputDialog, QLineEdit, QLabel, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard

class LatexEnvironmentGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_width = 4  # Số space cho mỗi tab
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('LaTeX Environment Generator')
        self.setGeometry(100, 100, 800, 600)
        
        # Tạo widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Tạo layout ngang cho các nút
        button_layout = QHBoxLayout()
        
        # Tạo nút chính cho môi trường
        self.env_button = QPushButton('Môi trường', self)
        button_layout.addWidget(self.env_button)
        
        # Tạo nút copy kết quả
        self.copy_button = QPushButton('Copy Kết quả', self)
        self.copy_button.clicked.connect(self.copy_result)
        button_layout.addWidget(self.copy_button)
        
        # Tạo nút xóa clipboard
        self.clear_button = QPushButton('Xóa Tất cả', self)
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)
        
        # Thêm layout nút vào layout chính
        main_layout.addLayout(button_layout)
        
        # Tạo splitter để chia màn hình thành 2 phần
        splitter = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(splitter)
        
        # Tạo widget cho phần input
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)
        
        # Label cho input
        input_label = QLabel("Nhập hoặc paste nội dung:")
        input_layout.addWidget(input_label)
        
        # TextEdit cho input
        self.input_text = QTextEdit()
        input_layout.addWidget(self.input_text)
        
        # Thêm widget input vào splitter
        splitter.addWidget(input_widget)
        
        # Tạo widget cho phần output
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_widget.setLayout(output_layout)
        
        # Label cho output
        output_label = QLabel("Kết quả (có thể chỉnh sửa):")
        output_layout.addWidget(output_label)
        
        # TextEdit cho output - cho phép chỉnh sửa
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(False)
        # Thiết lập font monospace để căn chỉnh tab
        font = self.result_text.font()
        font.setFamily("Courier New")
        self.result_text.setFont(font)
        output_layout.addWidget(self.result_text)
        
        # Thêm widget output vào splitter
        splitter.addWidget(output_widget)
        
        # Tạo menu thả xuống
        self.env_menu = QMenu(self)
        
        # Định nghĩa các nhóm môi trường
        self.environment_groups = {
            'Cấu trúc bài học': {
                'Mục tiêu': 'Muctieu',
                'Khởi động': 'kd',
                'Câu hỏi khởi động': 'cauhoikd',
                'Hoạt động': 'hd',
                'Tri thức': 'trithuc',
                'Luyện tập': 'luyentap',
                'Tóm tắt': 'tomtat',
                'Tổng kết': 'tongket'
            },
            'Định nghĩa và lý thuyết': {
                'Định nghĩa': 'dn',
                'Định lý': 'dl',
                'Hệ quả': 'hq',
                'Tính chất': 'tc',
                'Dạng': 'dang'
            },
            'Phương pháp và giải bài': {
                'Phương pháp': 'phuongphap',
                'Phương pháp giải': 'pp',
                'Ví dụ mẫu': 'vidu',
                'Bài tập tương tự': 'bttuongtu'
            },
            'Ghi chú và bổ sung': {
                'Ghi chú': 'note',
                'Lưu ý': 'luuy',
                'Nhận xét': 'nx',
                'Phân tích': 'phantich',
                'Ghi nhớ': 'ghinho',
                'Hỏi và đáp': 'hoivadap',
                'Bạn có biết': 'emcobiet',
                'Em có biết': 'Bancobiet'
            }
        }
        
        # Tạo menu theo nhóm
        for group_name, environments in self.environment_groups.items():
            group_menu = self.env_menu.addMenu(group_name)
            for env_name, env_code in environments.items():
                action = group_menu.addAction(env_name)
                action.triggered.connect(lambda checked, e=env_code, n=env_name: self.create_environment(e, n))
            
        self.env_button.setMenu(self.env_menu)

    def format_content(self, text):
        # Tách nội dung thành các dòng
        lines = text.strip().split('\n')
        formatted_lines = []
        
        # Xử lý từng dòng
        for line in lines:
            # Loại bỏ khoảng trắng thừa
            line = line.strip()
            if line:
                # Thêm tab vào đầu mỗi dòng nội dung
                formatted_lines.append(' ' * self.tab_width + line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)

    def taomt(self, mt, Text, title=None):
        # Format nội dung với tab
        formatted_text = self.format_content(Text)
        
        if (mt == "dang") or (mt == "tongket"):
            if title is None:
                title = "Tiêu đề"
            MT = f"\\begin{{{mt}}}{{{title}}}\n{formatted_text}\n\\end{{{mt}}}"
        else:
            MT = f"\\begin{{{mt}}}\n{formatted_text}\n\\end{{{mt}}}"
        return MT
        
    def create_environment(self, env_type, env_name):
        # Lấy text từ input box
        text = self.input_text.toPlainText().strip()
        
        # Nếu input box trống, thử lấy từ clipboard
        if not text:
            clipboard = QApplication.clipboard()
            text = clipboard.text().strip()
        
        if text:
            # Nếu là môi trường dang hoặc tongket, hiện dialog nhập tiêu đề
            title = None
            if env_type in ['dang', 'tongket']:
                title, ok = QInputDialog.getText(
                    self, 
                    f'Nhập tiêu đề cho {env_name}',
                    'Tiêu đề:',
                    QLineEdit.EchoMode.Normal,
                    'Tiêu đề'
                )
                if not ok:  # Nếu người dùng bấm Cancel
                    return
            
            # Tạo môi trường LaTeX với định dạng tab
            latex_env = self.taomt(env_type, text, title)
            
            # Hiển thị kết quả trong TextEdit
            self.result_text.setText(latex_env)
            
            # Copy kết quả vào clipboard
            QApplication.clipboard().setText(latex_env)
            
            # Hiển thị thông báo thành công
            QMessageBox.information(self, 'Thành công', 
                'Đã tạo môi trường LaTeX và copy vào clipboard')
        else:
            QMessageBox.warning(self, 'Lỗi', 
                'Vui lòng nhập nội dung hoặc copy nội dung từ bên ngoài')
    
    def clear_all(self):
        # Xóa nội dung input
        self.input_text.clear()
        # Xóa nội dung output
        self.result_text.clear()
        # Xóa clipboard
        QApplication.clipboard().clear()
        QMessageBox.information(self, 'Thành công', 'Đã xóa tất cả nội dung')

    def copy_result(self):
        # Lấy nội dung từ TextEdit kết quả
        result = self.result_text.toPlainText()
        if result:
            # Copy vào clipboard
            QApplication.clipboard().setText(result)
            QMessageBox.information(self, 'Thành công', 'Đã copy kết quả vào clipboard')
        else:
            QMessageBox.warning(self, 'Lỗi', 'Không có kết quả để copy')

def main():
    app = QApplication(sys.argv)
    window = LatexEnvironmentGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()