import re
class CommandConverter:
    def __init__(self):
        self.command_groups = {
            'Cấu trúc văn bản': {
                'Phần': 'part',
                'Chương': 'chapter',
                'Bài,Mục': 'section',
                'Mục con cấp 1': 'subsection',
                'Mục con cấp 2': 'subsubsection'

            },
            'Lệnh mới có đối số': {
                'Nổi bật (4 tùy chon)': 'Noibat[\\maunhan][][\\faStar][]',
                'Phần (1 tùy chọn màu sắc)': 'phan[\\mycolor]',
                'Thông tin': 'thongtin',
                'Font (qag,phv,put)':'myfont[13]',
                'Hộp công thức không có $':'khungct[\\mycolor]',
                'Hộp công thức toán':'hopcttoan}[\\maunhan]',
                'Hộp công thức có $':'boxct[\\maunhan][3pt][\\sffamily]',
                'In đậm':'indam[\\maunhan]',
            }
        }

    def clean_text(self, text):
        """Xử lý và làm sạch text đầu vào"""
        text = text.strip()
        text = re.sub(r"^[Cc][Hh][UuƯư][OoƠơ][Nn][Gg]\s*\d+\s*[\.):/_\-]*", '', text)
        text = re.sub(r"^[Bb][AaÀà][Ii]\s*\d+\s*[\.):/_\-]*", '', text)
        text = re.sub(r"^\d+\s*[\.):/_\-]*", '', text)
        text = re.sub(r"^(?:IX|IV|V?I{1,3}|I[XV]|X[LC]|L?X{1,3}|C[DM]|D?C{1,3}|M{1,3})\s*[\.):/_\-]+", '', text)
        text = re.sub(r"^[A-Za-z]+\s*[\.):/_\-]+", '', text)
        return text.strip()

    def taolenh(self, command, text, multi_line=True):
        """
        Chuyển đổi văn bản thành lệnh LaTeX
        
        Args:
            command (str): Tên lệnh LaTeX
            text (str): Nội dung cần chuyển đổi
            multi_line (bool): Có xử lý nhiều dòng không
            
        Returns:
            str: Lệnh LaTeX đã được định dạng
        """
        if not multi_line:
            # Xử lý đơn dòng như cũ
            clean_text = self.clean_text(text)
            return f"\n\\{command}{{{clean_text}}}"
        
        # Xử lý nhiều dòng
        lines = text.split('\n')
        result = []
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:  # Bỏ qua dòng trống
                continue
                
            # Kiểm tra nếu là tiêu đề bài mới
            if re.match(r"^[Bb][AaÀà][Ii]\s*\d+", line) or \
               re.match(r"^[Cc][Hh][UuƯư][OoƠơ][Nn][Gg]\s*\d+", line) or \
               re.match(r"^\d+\s*[\.):/_\-]", line) or \
               re.match(r"^(?:IX|IV|V?I{1,3}|I[XV]|X[LC]|L?X{1,3}|C[DM]|D?C{1,3}|M{1,3})\s*[\.):/_\-]", line) or \
               re.match(r"^[A-Za-z]+\s*[\.):/_\-]", line):
                
                # Xử lý nội dung đã tích lũy trước đó
                if current_content:
                    clean_text = self.clean_text('\n'.join(current_content))
                    if clean_text:
                        result.append(f"\\{command}{{{clean_text}}}")
                    current_content = []
            
            # Thêm dòng hiện tại vào nội dung đang xử lý
            current_content.append(line)
        
        # Xử lý phần nội dung còn lại
        if current_content:
            clean_text = self.clean_text('\n'.join(current_content))
            if clean_text:
                result.append(f"\\{command}{{{clean_text}}}")
        
        return '\n'.join(result)

    def taolenh_batch(self, command, text, delimiter='\n\n'):
        """
        Chuyển đổi hàng loạt văn bản thành các lệnh LaTeX
        
        Args:
            command (str): Tên lệnh LaTeX
            text (str): Nội dung cần chuyển đổi
            delimiter (str): Ký tự phân cách giữa các phần
            
        Returns:
            str: Các lệnh LaTeX đã được định dạng
        """
        # Tách văn bản thành các phần dựa vào delimiter
        sections = text.split(delimiter)
        result = []
        
        for section in sections:
            section = section.strip()
            if section:
                # Xử lý từng phần
                clean_text = self.clean_text(section)
                if clean_text:
                    result.append(f"\\{command}{{{clean_text}}}")
        
        return '\n'.join(result)

    def process_text(self, command, text, mode="single"):
        """
        Xử lý văn bản với các chế độ khác nhau
        
        Args:
            command (str): Tên lệnh LaTeX
            text (str): Nội dung cần chuyển đổi
            mode (str): Chế độ xử lý ("single", "multi", "batch")
            
        Returns:
            str: Kết quả đã được định dạng
        """
        if mode == "single":
            return self.taolenh(command, text, multi_line=False)
        elif mode == "multi":
            return self.taolenh(command, text, multi_line=True)
        elif mode == "batch":
            return self.taolenh_batch(command, text)
        else:
            raise ValueError("Chế độ xử lý không hợp lệ")