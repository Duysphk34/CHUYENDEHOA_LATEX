import sys
import os
import codecs
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,QDialog,QScrollArea,
                            QPushButton, QMenu, QMessageBox, QTextEdit, QHBoxLayout,
                            QInputDialog, QLineEdit, QLabel, QSplitter, QTabWidget)
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtGui import QClipboard,QIcon
from list_converter import ListConverter
from command_converter import CommandConverter
import re
class LatexEnvironmentGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_width = 4
        self.list_converter = ListConverter()
        self.command_converter = CommandConverter()
        self.last_result = None
        
        # Thêm icon cho ứng dụng
        app_icon = QIcon(resource_path("icon.ico"))  # Đường dẫn tới file icon của bạn
        self.setWindowIcon(app_icon)
        QApplication.setWindowIcon(app_icon)


        self.initUI()

        
    def initUI(self):
        self.setWindowTitle('LaTeX Generator')
        self.setGeometry(100, 100, 1000, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
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
        
        # Tab lệnh mới
        command_tab = QWidget()
        tab_widget.addTab(command_tab, "Chuyển Lệnh")
        self.setup_command_tab(command_tab)


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
        
        input_label = QLabel("Nội dung hiện tại (từ kết quả trước):")
        input_layout.addWidget(input_label)
        
        self.input_text = QTextEdit()
        # Tự động cập nhật input từ clipboard khi tab được tạo
        clipboard_text = QApplication.clipboard().text().strip()
        if clipboard_text:
            self.input_text.setText(clipboard_text)
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
        help_dialog.setWindowIcon(self.windowIcon()) 
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
        """Xử lý chuyển đổi danh sách với hỗ trợ clipboard"""
        try:
            text = self.get_input_text(self.list_input_text)
            
            if text:
                result = self.list_converter.convert_list_menu(text, conversion_type)
                
                # Cập nhật output và clipboard
                self.update_io_content(result)
                
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


    def update_io_content(self, new_content):
        """Cập nhật nội dung cho cả input và output"""
        try:
            # Cập nhật clipboard
            QApplication.clipboard().setText(new_content)
            
            # Xác định tab hiện tại
            current_tab_index = self.findChild(QTabWidget).currentIndex()
            
            # Cập nhật input và output dựa vào tab hiện tại
            if current_tab_index == 0:  # Tab môi trường
                self.result_text.blockSignals(True)
                self.result_text.setText(new_content)
                self.result_text.blockSignals(False)
            
            elif current_tab_index == 1:  # Tab danh sách
                self.list_result_text.blockSignals(True)
                self.list_result_text.setText(new_content)
                self.list_result_text.blockSignals(False)
                
            elif current_tab_index == 2:  # Tab lệnh
                self.command_result_text.blockSignals(True)
                self.command_result_text.setText(new_content)
                self.command_result_text.blockSignals(False)
            
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
        """Lấy text từ clipboard (kết quả trước) hoặc từ input box"""
        # Ưu tiên lấy từ clipboard (kết quả của thao tác trước)
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text().strip()
        
        if clipboard_text:
            # Cập nhật input box với nội dung từ clipboard
            input_textbox.blockSignals(True)
            input_textbox.setText(clipboard_text)
            input_textbox.blockSignals(False)
            return clipboard_text
        
        # Nếu không có nội dung trong clipboard, lấy từ input box
        return input_textbox.toPlainText().strip()

    
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
        """Tạo môi trường LaTeX với hỗ trợ clipboard"""
        try:
            text = self.get_input_text(self.input_text)
            
            if text:
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
                
                latex_env = self.taomt(env_type, text, title)
                
                # Cập nhật output và clipboard
                self.update_io_content(latex_env)
                
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
            
#####Các phương thức xử lý lệnh##############
    def convert_command(self):
        """Xử lý chuyển đổi lệnh"""
        try:
            command = self.command_input.text().strip()
            if not command:
                QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập tên lệnh')
                return
                
            text = self.get_input_text(self.command_text_input)
            if not text:
                QMessageBox.warning(self, 'Lỗi', 'Không tìm thấy nội dung để xử lý')
                return
                
            result = self.command_converter.taolenh(command, text)
            self.update_io_content(result)
            
            QMessageBox.information(self, 'Thành công', 
                'Đã chuyển đổi lệnh và tự động cập nhật nội dung')
                
        except Exception as e:
            QMessageBox.warning(self, 'Lỗi', 
                f'Lỗi khi chuyển đổi lệnh: {str(e)}')

    def setup_command_tab(self, tab_widget):
        """Thiết lập tab chuyển lệnh"""
        layout = QVBoxLayout()
        
        # Layout cho nút
        button_layout = QHBoxLayout()
        
        # Nút chuyển lệnh với menu
        self.cmd_button = QPushButton('Chuyển Lệnh', self)
        self.setup_command_menu()
        button_layout.addWidget(self.cmd_button)
        
        # Nút tùy chỉnh lệnh
        custom_cmd_button = QPushButton('Lệnh tùy chỉnh', self)
        custom_cmd_button.clicked.connect(self.show_custom_command_dialog)
        button_layout.addWidget(custom_cmd_button)
        
        # Nút copy
        copy_command_button = QPushButton('Copy lại kết quả', self)
        copy_command_button.clicked.connect(self.copy_command_result)
        button_layout.addWidget(copy_command_button)
        
        # Nút xóa
        clear_command_button = QPushButton('Xóa Tất cả', self)
        clear_command_button.clicked.connect(self.clear_command)
        button_layout.addWidget(clear_command_button)
        
        layout.addLayout(button_layout)
        
        # Splitter cho input/output
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Widget input
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)
        
        # Label cho input
        input_label = QLabel("Nội dung hiện tại:")
        input_layout.addWidget(input_label)
        
        # Input cho nội dung
        self.command_text_input = QTextEdit()
        clipboard_text = QApplication.clipboard().text().strip()
        if clipboard_text:
            self.command_text_input.setText(clipboard_text)
        input_layout.addWidget(self.command_text_input)
        
        splitter.addWidget(input_widget)
        
        # Widget output
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_widget.setLayout(output_layout)
        
        output_label = QLabel("Kết quả:")
        output_layout.addWidget(output_label)
        
        self.command_result_text = QTextEdit()
        self.command_result_text.setReadOnly(False)
        font = self.command_result_text.font()
        font.setFamily("Courier New")
        self.command_result_text.setFont(font)
        self.command_result_text.textChanged.connect(self.on_command_output_changed)
        output_layout.addWidget(self.command_result_text)
        
        splitter.addWidget(output_widget)
        
        # Thiết lập kích thước ban đầu cho splitter
        splitter.setSizes([300, 300])
        
        layout.addWidget(splitter)
        tab_widget.setLayout(layout)

    def setup_command_menu(self):
        """Thiết lập menu cho nút chuyển lệnh"""
        self.cmd_menu = QMenu(self)
        
        # Thêm các nhóm lệnh vào menu
        for group_name, commands in self.command_converter.command_groups.items():
            group_menu = self.cmd_menu.addMenu(group_name)
            for cmd_name, cmd_code in commands.items():
                action = group_menu.addAction(cmd_name)
                action.triggered.connect(lambda checked, c=cmd_code, n=cmd_name: self.create_command(c, n))
        
        self.cmd_button.setMenu(self.cmd_menu)

    def show_custom_command_dialog(self):
        """Hiển thị dialog cho lệnh tùy chỉnh"""
        command, ok = QInputDialog.getText(
            self,
            'Lệnh tùy chỉnh',
            'Nhập tên lệnh LaTeX:',
            QLineEdit.EchoMode.Normal
        )
        if ok and command:
            self.create_command(command, 'Lệnh tùy chỉnh')

    def create_command(self, cmd_code, cmd_name):
        """Tạo lệnh LaTeX với hỗ trợ clipboard"""
        try:
            text = self.get_input_text(self.command_text_input)
            
            if text:
                # Hiển thị dialog chọn chế độ xử lý
                modes = {
                    "Xử lý đơn dòng": "single",
                    "Xử lý nhiều dòng": "multi",
                    "Xử lý hàng loạt": "batch"
                }
                mode, ok = QInputDialog.getItem(
                    self,
                    'Chọn chế độ xử lý',
                    'Chọn cách xử lý văn bản:',
                    modes.keys(),
                    current=0,
                    editable=False
                )
                
                if ok:
                    # Lấy chế độ xử lý từ dictionary
                    process_mode = modes[mode]
                    
                    # Xử lý văn bản theo chế độ đã chọn
                    latex_cmd = self.command_converter.process_text(cmd_code, text, process_mode)
                    
                    # Cập nhật output và clipboard
                    self.update_io_content(latex_cmd)
                    
                    QMessageBox.information(self, 'Thành công',
                        f'Đã tạo lệnh {cmd_name} và tự động cập nhật nội dung')
            else:
                QMessageBox.warning(self, 'Lỗi',
                    'Không tìm thấy nội dung để xử lý')
        except Exception as e:
            QMessageBox.warning(self, 'Lỗi',
                f'Lỗi khi xử lý: {str(e)}')

    def on_command_output_changed(self):
        """Xử lý khi nội dung output lệnh thay đổi"""
        try:
            new_content = self.command_result_text.toPlainText()
            if new_content and new_content != self.last_result:
                self.update_io_content(new_content, update_input=False)
        except Exception as e:
            print(f"Lỗi khi cập nhật clipboard: {str(e)}")

    def clear_command(self):
        """Xóa tất cả nội dung tab lệnh"""
        self.command_text_input.clear()
        self.command_result_text.clear()
        self.last_result = None
        QApplication.clipboard().clear()
        QMessageBox.information(self, 'Thành công', 'Đã xóa tất cả nội dung')

    def copy_command_result(self):
        """Copy kết quả từ khung kết quả lệnh vào clipboard"""
        result = self.command_result_text.toPlainText()
        if result:
            QApplication.clipboard().setText(result)
            QMessageBox.information(self, 'Thành công', 
                'Đã copy lại kết quả vào clipboard')
        else:
            QMessageBox.warning(self, 'Lỗi', 
                'Không có kết quả để copy')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)
    window = LatexEnvironmentGenerator()
    # Set app ID for Windows
    import ctypes
    myappid = 'Latex.generate.Ver1' # tùy chỉnh ID
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    # Set icon
    icon_path = resource_path('icon.ico')
    app_icon = QIcon(icon_path)
    
    # Add different sizes
    for size in [16, 24, 32, 48, 256]:
        app_icon.addFile(icon_path, QSize(size, size))
    # Set icon for the application
    app.setWindowIcon(app_icon)
    # Create and show main window
    window.setWindowIcon(app_icon)  # Set icon for the main window
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()