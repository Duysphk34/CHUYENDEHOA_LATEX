import re

class ListConverter:
    def __init__(self):
        # Patterns cho cấp 1 (số)
        self.level1_patterns = [
            r'^\d+\)\s+(.*)',     # 1) 
            r'^\d+\.\s+(.*)',     # 1.
            r'^\d+\/\s+(.*)',     # 1/
            r'^\(\d+\)\s+(.*)'    # (1)
        ]
        
        # Patterns cho cấp 2 (chữ cái)
        self.level2_patterns = [
            r'^[a-z]\)\s+(.*)',     # a)
            r'^[a-z]\.\s+(.*)',     # a.
            r'^[a-z]\/\s+(.*)',     # a/
            r'^\([a-z]\)\s+(.*)'    # (a)
        ]
        
        # Patterns cho itemize
        self.itemize_patterns = [
            r'^-\s+(.*)',           # -
            r'^\+\s+(.*)',          # +
            r'^\*\s+(.*)'           # *
        ]
        
        # Tổng hợp tất cả patterns cho trường hợp 1
        self.all_patterns = (
            self.level1_patterns + 
            self.level2_patterns + 
            self.itemize_patterns
        )
        
        self.tab_width = 4  # Số space cho mỗi tab

    def convert_to_latex_itemize(self, text):
        """Chuyển đổi văn bản thành môi trường itemize của LaTeX"""
        if not text:
            return text
            
        # Nếu đã là định dạng LaTeX itemize, trả về nguyên văn
        if "\\begin{itemize}" in text and "\\end{itemize}" in text:
            return text
            
        lines = text.split('\n')
        result = []
        in_list = False
        current_item_content = []
        
        def process_item_content():
            if current_item_content:
                content = ' '.join(current_item_content).strip()
                if content:
                    result.append(f"{' ' * self.tab_width}\\item {content}")
                current_item_content.clear()
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if not stripped_line:  # Dòng trống
                if in_list:
                    process_item_content()
                if result and i < len(lines) - 1:  # Nếu không phải dòng cuối
                    result.append('')
                continue
            
            # Kiểm tra xem có phải dòng danh sách không
            is_list_item = False
            item_content = stripped_line
            
            for pattern in self.all_patterns:
                match = re.match(pattern, stripped_line)
                if match:
                    is_list_item = True
                    if not in_list:
                        if result and not result[-1].strip():
                            result.pop()  # Xóa dòng trống trước \begin{itemize}
                        result.append('\\begin{itemize}')
                        in_list = True
                    
                    process_item_content()  # Xử lý item trước đó nếu có
                    
                    # Lấy nội dung sau pattern
                    item_content = match.group(1).strip()
                    current_item_content.append(item_content)
                    break
            
            if not is_list_item:  # Dòng thường
                if in_list:
                    # Nếu dòng này không có pattern nhưng là tiếp theo của item trước
                    if current_item_content:
                        current_item_content.append(stripped_line)
                    else:
                        # Nếu không phải tiếp theo của item nào, kết thúc danh sách
                        process_item_content()
                        result.append('\\end{itemize}')
                        in_list = False
                        result.append(line)  # Giữ nguyên định dạng gốc
                else:
                    result.append(line)  # Giữ nguyên định dạng gốc
        
        # Xử lý item cuối cùng nếu có
        if in_list:
            process_item_content()
            result.append('\\end{itemize}')
        
        return '\n'.join(result)
    
    def detect_pattern_type(self, line, patterns):
        """Phát hiện pattern phù hợp từ danh sách patterns"""
        for pattern in patterns:
            if re.match(pattern, line.strip()):
                return pattern
        return None

    def get_indent_level(self, line):
        """Xác định mức độ thụt lề của dòng"""
        return len(line) - len(line.lstrip())

    def process_line(self, line, pattern):
        """Xử lý một dòng văn bản theo pattern"""
        match = re.match(pattern, line.strip())
        if match:
            return match.group(1).strip()
        return line.strip()

    def convert_to_enumerate(self, block, indent=0):
        """Chuyển đổi khối văn bản thành enumerate"""
        lines = block.split('\n')
        result = []
        result.append(' ' * indent + '\\begin{enumerate}')
        
        for line in lines:
            if line.strip():
                result.append(' ' * (indent + self.tab_width) + 
                            '\\item ' + line.strip())
                
        result.append(' ' * indent + '\\end{enumerate}')
        return '\n'.join(result)

    def convert_itemize_to_enumerate(self, text):
        """Chuyển đổi từ itemize sang enumerate"""
        if not text or 'itemize' not in text:
            return text
        return text.replace('\\begin{itemize}', '\\begin{enumerate}')\
                  .replace('\\end{itemize}', '\\end{enumerate}')

    def convert_enumerate_to_itemize(self, text):
        """Chuyển đổi từ enumerate sang itemize"""
        if not text or 'enumerate' not in text:
            return text
        return text.replace('\\begin{enumerate}', '\\begin{itemize}')\
                  .replace('\\end{enumerate}', '\\end{itemize}')

    def convert_multilevel_list(self, text):
        """Chuyển đổi danh sách hai cấp sang LaTeX"""
        if not text:
            return text

        lines = text.split('\n')
        result = []
        in_list = False
        level2_start = False
        prev_indent = 0
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if not stripped_line:
                if i < len(lines) - 1 and lines[i+1].strip():
                    result.append('')
                continue

            indent = self.get_indent_level(line)
            
            # Xử lý cấp 1
            if self.detect_pattern_type(stripped_line, self.level1_patterns):
                if not in_list:
                    result.append('\\begin{enumerate}')
                    in_list = True
                if level2_start:
                    if self.detect_pattern_type(lines[i-1].strip(), self.itemize_patterns):
                        result.append('\t\\end{itemize}')
                    else:
                        result.append('\t\\end{enumerate}')
                    level2_start = False
                content = self.process_line(stripped_line, 
                         self.detect_pattern_type(stripped_line, self.level1_patterns))
                result.append('\t\\item ' + content)
                prev_indent = indent
                
            # Xử lý cấp 2
            elif self.detect_pattern_type(stripped_line, self.level2_patterns) or \
                 self.detect_pattern_type(stripped_line, self.itemize_patterns):
                if not level2_start:
                    if self.detect_pattern_type(stripped_line, self.itemize_patterns):
                        result.append('\t\\begin{itemize}')
                    else:
                        result.append('\t\\begin{enumerate}')
                    level2_start = True
                
                if self.detect_pattern_type(stripped_line, self.level2_patterns):
                    pattern = self.detect_pattern_type(stripped_line, self.level2_patterns)
                else:
                    pattern = self.detect_pattern_type(stripped_line, self.itemize_patterns)
                    
                content = self.process_line(stripped_line, pattern)
                result.append('\t\t\\item ' + content)
                
            else:
                # Dòng thường
                if not in_list:
                    result.append(line)
        
        # Đóng các môi trường còn mở
        if level2_start:
            if self.detect_pattern_type(lines[-1].strip(), self.itemize_patterns):
                result.append('\t\\end{itemize}')
            else:
                result.append('\t\\end{enumerate}')
        if in_list:
            result.append('\\end{enumerate}')
            
        return '\n'.join(result)

    def convert_list_menu(self, text, conversion_type):
        """Hàm chính để xử lý chuyển đổi theo menu"""
        if not text:
            return text
            
        try:
            if conversion_type == 1:
                # Chuyển sang itemize một cấp
                return self.convert_to_latex_itemize(text)
            elif conversion_type == 2:
                # Chuyển sang enumerate/itemize hai cấp
                return self.convert_multilevel_list(text)
            elif conversion_type == 3:
                # Chuyển từ itemize sang enumerate
                return self.convert_itemize_to_enumerate(text)
            elif conversion_type == 4:
                # Chuyển từ enumerate sang itemize
                return self.convert_enumerate_to_itemize(text)
            else:
                return text
        except Exception as e:
            print(f"Lỗi khi chuyển đổi: {str(e)}")
            return text