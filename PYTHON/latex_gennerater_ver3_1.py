import sys
import os
import codecs
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,QDialog,QScrollArea,
                            QPushButton, QMenu, QMessageBox, QTextEdit, QHBoxLayout,
                            QInputDialog, QLineEdit, QLabel, QSplitter, QTabWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard
from list_converter import ListConverter
import re
class LatexEnvironmentGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_width = 4
        self.list_converter = ListConverter()
        # Thêm biến để lưu kết quả gần nhất
        self.last_result = None
        self.initUI()

        
    def initUI(self):
        self.setWindowTitle('LaTeX Generator')
        self.setGeometry(100, 100, 1000, 600)
        
        # Tạo widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Tạo TabWidget để chứa hai chức năng
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # Tab môi trường
        env_tab = QWidget()
        tab_widget.addTab(env_tab, "Chuyển Môi trường")
        self.setup_environment_tab(env_tab)
        
        # Tab danh sách
        list_tab = QWidget()
        tab_widget.addTab(list_tab, "Chuyển Danh sách")
        self.setup_list_tab(list_tab)
    



    def setup_environment_tab(self, tab_widget):
        layout = QVBoxLayout()
        
        # Tạo layout ngang cho các nút
        button_layout = QHBoxLayout()
        
        # Các nút cho môi trường
        self.env_button = QPushButton('Môi trường', self)
        button_layout.addWidget(self.env_button)
        
        self.copy_button = QPushButton('Copy lại kết quả', self)
        self.copy_button.clicked.connect(self.copy_result)
        button_layout.addWidget(self.copy_button)
        
        self.clear_button = QPushButton('Xóa Tất cả', self)
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # Splitter cho input/output
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Input widget
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)
        
        input_label = QLabel("Nhập, paste nội dung hoặc để trống để sử dụng clipboard:")
        input_layout.addWidget(input_label)
        
        self.input_text = QTextEdit()
        input_layout.addWidget(self.input_text)
        splitter.addWidget(input_widget)
        
        # Output widget
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_widget.setLayout(output_layout)
        
        output_label = QLabel("Kết quả:")
        output_layout.addWidget(output_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(False)
        font = self.result_text.font()
        font.setFamily("Courier New")
        self.result_text.setFont(font)
        # Kết nối signal textChanged với hàm xử lý
        self.result_text.textChanged.connect(self.on_output_changed)
        output_layout.addWidget(self.result_text)
        
        splitter.addWidget(output_widget)
        layout.addWidget(splitter)
        
        tab_widget.setLayout(layout)
        
        # Tạo menu môi trường
        self.setup_environment_menu()
        
    def setup_list_tab(self, tab_widget):
        layout = QVBoxLayout()
        
        # Tạo layout ngang cho các nút
        button_layout = QHBoxLayout()
        
        # Tạo menu cho nút chuyển đổi danh sách
        self.list_button = QPushButton('Danh sách', self)
        self.list_menu = QMenu(self)
        
        # Thêm các tùy chọn chuyển đổi vào menu
        convert_options = {
            'Chuyển sang itemize một cấp': 1,
            'Chuyển sang enumerate/itemize hai cấp': 2,
            'Chuyển từ itemize sang enumerate': 3,
            'Chuyển từ enumerate sang itemize': 4,
            'Hướng dẫn sử dụng': 'help'  # Thêm tùy chọn hướng dẫn
        }
        
        # Thêm separator trước mục Hướng dẫn
        for option_name, option_type in convert_options.items():
            if option_type == 'help':
                self.list_menu.addSeparator()
            action = self.list_menu.addAction(option_name)
            if option_type == 'help':
                action.triggered.connect(self.show_help)
            else:
                action.triggered.connect(lambda checked, t=option_type: self.convert_list(t))
        
        self.list_button.setMenu(self.list_menu)
        button_layout.addWidget(self.list_button)
        
        copy_list_button = QPushButton('Copy lại kết quả', self)
        copy_list_button.clicked.connect(self.copy_list_result)
        button_layout.addWidget(copy_list_button)
        
        # Nút xóa tất cả
        clear_list_button = QPushButton('Xóa Tất cả', self)
        clear_list_button.clicked.connect(self.clear_list)
        button_layout.addWidget(clear_list_button)
        
        # Thêm layout nút vào layout chính
        layout.addLayout(button_layout)
        
        # Tạo splitter để chia màn hình thành 2 phần
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Widget cho phần input
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # Label cho input
        input_label = QLabel("Nhập, paste nội dung hoặc để trống để sử dụng clipboard:")
        input_layout.addWidget(input_label)
        
        # TextEdit cho input
        self.list_input_text = QTextEdit()
        self.list_input_text.setAcceptRichText(False)  # Chỉ chấp nhận plain text
        input_layout.addWidget(self.list_input_text)
        
        # Thêm widget input vào splitter
        splitter.addWidget(input_widget)
        
        # Widget cho phần output
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        
        # Label cho output
        output_label = QLabel("Kết quả:")
        output_layout.addWidget(output_label)
        
        # Cập nhật TextEdit cho output với kết nối signal
        self.list_result_text = QTextEdit()
        self.list_result_text.setReadOnly(False)
        font = self.list_result_text.font()
        font.setFamily("Courier New")
        self.list_result_text.setFont(font)
        # Kết nối signal textChanged với hàm xử lý
        self.list_result_text.textChanged.connect(self.on_list_output_changed)
        output_layout.addWidget(self.list_result_text)
        
        # Thêm widget output vào splitter
        splitter.addWidget(output_widget)
        
        # Thiết lập kích thước ban đầu cho splitter
        splitter.setSizes([300, 300])  # Chia đều không gian cho input và output
        
        # Thêm splitter vào layout chính
        layout.addWidget(splitter)
        
        # Thiết lập layout cho tab
        tab_widget.setLayout(layout)

    def on_output_changed(self):
        """Xử lý khi nội dung output môi trường thay đổi"""
        try:
            new_content = self.result_text.toPlainText()
            if new_content and new_content != self.last_result:
                self.update_io_content(new_content, update_input=False)
        except Exception as e:
            print(f"Lỗi khi cập nhật clipboard: {str(e)}")

    def on_list_output_changed(self):
        """Xử lý khi nội dung output danh sách thay đổi"""
        try:
            new_content = self.list_result_text.toPlainText()
            if new_content and new_content != self.last_result:
                self.update_io_content(new_content, update_input=False)
        except Exception as e:
            print(f"Lỗi khi cập nhật clipboard: {str(e)}")



    def show_help(self):
        """Hiển thị cửa sổ hướng dẫn"""
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Hướng dẫn sử dụng")
        help_dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        
        guide_text = """<h2>Hướng dẫn chuyển đổi danh sách</h2>

    <h3>1. Chuyển sang itemize một cấp</h3>
    <ul>
        <li>Chuyển các dạng danh sách một cấp sang môi trường itemize</li>
        <li>Hỗ trợ các định dạng:
            <ul>
                <li>Dấu gạch đầu dòng (-)</li>
                <li>Dấu cộng (+)</li>
                <li>Số có dấu chấm (1.)</li>
                <li>Số có dấu ngoặc đơn (1)</li>
                <li>Số trong ngoặc đơn (1)</li>
                <li>Chữ cái (a., a), (a))</li>
            </ul>
        </li>
    </ul>

    <h3>2. Chuyển sang enumerate/itemize hai cấp</h3>
    <ul>
        <li>Cấp 1 (số) -> enumerate:
            <ul>
                <li>1), 1., 1/, (1)</li>
            </ul>
        </li>
        <li>Cấp 2 (chữ) -> enumerate:
            <ul>
                <li>a), a., a/, (a)</li>
            </ul>
        </li>
        <li>Cấp 2 dấu gạch ngang -> itemize:
            <ul>
                <li>-, +, *</li>
            </ul>
        </li>
    </ul>

    <h3>3. Chuyển từ itemize sang enumerate</h3>
    <ul>
        <li>Thay thế \\begin{itemize} thành \\begin{enumerate}</li>
        <li>Giữ nguyên nội dung các item</li>
    </ul>

    <h3>4. Chuyển từ enumerate sang itemize</h3>
    <ul>
        <li>Thay thế \\begin{enumerate} thành \\begin{itemize}</li>
        <li>Giữ nguyên nội dung các item</li>
    </ul>

    <h3>Lưu ý quan trọng</h3>
    <ul>
        <li>Đảm bảo các mục cùng cấp có cùng định dạng thụt lề</li>
        <li>Đối với danh sách hai cấp, cần thụt lề rõ ràng cho cấp 2</li>
        <li>Kết quả sẽ tự động được copy vào clipboard</li>
    </ul>"""

        help_text.setHtml(guide_text)
        layout.addWidget(help_text)
        
        # Nút đóng
        close_button = QPushButton("Đóng")
        close_button.clicked.connect(help_dialog.close)
        layout.addWidget(close_button)
        
        help_dialog.setLayout(layout)
        help_dialog.exec()

    def convert_list(self, conversion_type):
        """Xử lý chuyển đổi danh sách với hỗ trợ tự động cập nhật"""
        try:
            # Sử dụng kết quả trước đó làm input nếu có
            input_text = self.last_result if self.last_result else self.get_input_text(self.list_input_text)
            
            if input_text:
                result = self.list_converter.convert_list_menu(input_text, conversion_type)
                # Chỉ cập nhật output và clipboard, không cập nhật input
                self.update_io_content(result, update_input=False)
                
                messages = {
                    1: 'Chuyển sang itemize một cấp',
                    2: 'Chuyển sang enumerate/itemize hai cấp',
                    3: 'Chuyển từ itemize sang enumerate',
                    4: 'Chuyển từ enumerate sang itemize'
                }
                QMessageBox.information(self, 'Thành công',
                    f'Đã {messages[conversion_type].lower()} và tự động cập nhật nội dung')
            else:
                QMessageBox.warning(self, 'Lỗi',
                    'Không tìm thấy nội dung để xử lý')
        except Exception as e:
            QMessageBox.warning(self, 'Lỗi',
                f'Lỗi khi chuyển đổi: {str(e)}')



    def setup_environment_menu(self):
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
        
        for group_name, environments in self.environment_groups.items():
            group_menu = self.env_menu.addMenu(group_name)
            for env_name, env_code in environments.items():
                action = group_menu.addAction(env_name)
                action.triggered.connect(lambda checked, e=env_code, n=env_name: self.create_environment(e, n))
            
        self.env_button.setMenu(self.env_menu)


    def update_io_content(self, new_content, update_input=False):
        """
        Cập nhật nội dung cho output và clipboard
        update_input: True nếu muốn cập nhật cả input, False nếu chỉ cập nhật output
        """
        try:
            # Cập nhật clipboard
            QApplication.clipboard().setText(new_content)
            
            # Xác định tab hiện tại
            current_tab_index = self.findChild(QTabWidget).currentIndex()
            
            # Cập nhật output và input tùy theo tab
            if current_tab_index == 0:  # Tab môi trường
                if update_input:
                    self.input_text.blockSignals(True)
                    self.input_text.setText(new_content)
                    self.input_text.blockSignals(False)
                
                self.result_text.blockSignals(True)
                self.result_text.setText(new_content)
                self.result_text.blockSignals(False)
            else:  # Tab danh sách
                if update_input:
                    self.list_input_text.blockSignals(True)
                    self.list_input_text.setText(new_content)
                    self.list_input_text.blockSignals(False)
                
                self.list_result_text.blockSignals(True)
                self.list_result_text.setText(new_content)
                self.list_result_text.blockSignals(False)
            
            # Lưu kết quả gần nhất
            self.last_result = new_content
            
        except Exception as e:
            print(f"Lỗi khi cập nhật nội dung: {str(e)}")


    def on_output_changed(self):
        """Xử lý khi nội dung output môi trường thay đổi"""
        try:
            new_content = self.result_text.toPlainText()
            if new_content and new_content != self.last_result:
                self.update_io_content(new_content)
        except Exception as e:
            print(f"Lỗi khi cập nhật clipboard: {str(e)}")

    def on_list_output_changed(self):
        """Xử lý khi nội dung output danh sách thay đổi"""
        try:
            new_content = self.list_result_text.toPlainText()
            if new_content and new_content != self.last_result:
                self.update_io_content(new_content)
        except Exception as e:
            print(f"Lỗi khi cập nhật clipboard: {str(e)}")


    
    def get_input_text(self, input_textbox):
        """Lấy text từ input box, clipboard hoặc kết quả trước đó"""
        # Ưu tiên lấy từ input box
        text = input_textbox.toPlainText().strip()
        
        if not text:
            # Thử lấy từ kết quả trước đó
            if self.last_result:
                input_textbox.blockSignals(True)
                input_textbox.setText(self.last_result)
                input_textbox.blockSignals(False)
                return self.last_result
            
            # Nếu không có kết quả trước đó, lấy từ clipboard
            clipboard = QApplication.clipboard()
            text = clipboard.text().strip()
            
            if text:
                input_textbox.blockSignals(True)
                input_textbox.setText(text)
                input_textbox.blockSignals(False)
        
        return text

    
    # Các phương thức xử lý môi trường
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
        """Tạo môi trường LaTeX với hỗ trợ tự động cập nhật"""
        try:
            # Sử dụng kết quả trước đó làm input nếu có
            input_text = self.last_result if self.last_result else self.get_input_text(self.input_text)
            
            if input_text:
                title = None
                if env_type in ['dang', 'tongket']:
                    title, ok = QInputDialog.getText(
                        self,
                        f'Nhập tiêu đề cho {env_name}',
                        'Tiêu đề:',
                        QLineEdit.EchoMode.Normal,
                        'Tiêu đề'
                    )
                    if not ok:
                        return
                
                latex_env = self.taomt(env_type, input_text, title)
                # Chỉ cập nhật output và clipboard, không cập nhật input
                self.update_io_content(latex_env, update_input=False)
                
                QMessageBox.information(self, 'Thành công',
                    'Đã tạo môi trường LaTeX và tự động cập nhật nội dung')
            else:
                QMessageBox.warning(self, 'Lỗi',
                    'Không tìm thấy nội dung để xử lý')
        except Exception as e:
            QMessageBox.warning(self, 'Lỗi',
                f'Lỗi khi xử lý: {str(e)}')
    
    def clear_all(self):
        """Xóa tất cả nội dung và reset trạng thái"""
        self.input_text.clear()
        self.result_text.clear()
        self.last_result = None
        QApplication.clipboard().clear()
        QMessageBox.information(self, 'Thành công', 'Đã xóa tất cả nội dung')

    def clear_list(self):
        """Xóa tất cả nội dung tab danh sách và reset trạng thái"""
        self.list_input_text.clear()
        self.list_result_text.clear()
        self.last_result = None
        QApplication.clipboard().clear()
        QMessageBox.information(self, 'Thành công', 'Đã xóa tất cả nội dung')

    def copy_list_result(self):
        """Copy kết quả từ khung kết quả vào clipboard (khi cần copy lại)"""
        result = self.list_result_text.toPlainText()
        if result:
            QApplication.clipboard().setText(result)
            QMessageBox.information(self, 'Thành công', 
                'Đã copy lại kết quả vào clipboard')
        else:
            QMessageBox.warning(self, 'Lỗi', 
                'Không có kết quả để copy')

    def copy_result(self):
        """Copy kết quả từ khung kết quả môi trường vào clipboard (khi cần copy lại)"""
        result = self.result_text.toPlainText()
        if result:
            QApplication.clipboard().setText(result)
            QMessageBox.information(self, 'Thành công', 
                'Đã copy lại kết quả vào clipboard')
        else:
            QMessageBox.warning(self, 'Lỗi', 
                'Không có kết quả để copy')

def main():
    app = QApplication(sys.argv)
    window = LatexEnvironmentGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()