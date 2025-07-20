import re
class CommandConverter:
    def __init__(self):

        self.templates = {
            'soanex': """%%%=============SOẠN EX===============%%%
\\Opensolutionfile{ansex}[Ans/LGEX-filename]
\\Opensolutionfile{ans}[Ans/Ans-filename]

\\Closesolutionfile{ans}
\\Closesolutionfile{ansex}
%\\bangdapan{Ans-filename}""",

            'soanextf': """%%%=============SOẠN EXTF===============%%%
\\Opensolutionfile{ansex}[Ans/LGTF-filename]
\\Opensolutionfile{ansbook}[Ansbook/AnsTF-filename]
\\Opensolutionfile{ans}[Ans/Tempt-filename]

\\Closesolutionfile{ans}
\\Closesolutionfile{ansbook}
\\Closesolutionfile{ansex}
%\\bangdapanTF{AnsTF-filename}""",

        'orbital':"""
\\squarerow[2ud][0.5][\\maunhan][-4pt]{1}
""",
        'elementcell': """
\\nguyento[show notes=false,color=\\mauphu,width=2.3cm,height=3cm]{\\num}{\\mass}{\\sym}{\\name}{\\config}{\\ox}
""",
        'tieudekithi': """
\\begin{name}[Đề thi thử giữa HKI][Hóa][10][Phòng GD \\& ĐT Phù Mỹ][Ngày 20 tháng 7 năm 2024]{Trường THPT Số 2 Phù Mỹ}{2024 - 2025}\\end{name}
""",
        'subfile': """
\\documentclass[FileMain_Ver1.tex]{subfiles}
%%%==============Cách 1 soạn tiêu đề bai thi bằng \\section======================%%%
\\gdef\\sophong{Phòng Giáo dục \\& ĐT Phù Mỹ}
\\gdef\\truong{Trường THPT Số 2 Phù Mỹ}
\\gdef\\monhoc{Hóa học}
\\gdef\\lop{10}
\\gdef\\nh{2024 - 2025}
\\gdef\\thoigian{50}
\\setcounter{demsode}{0}
\\gdef\\loaide{ĐỀ SỐ \\circlenumH[\\mycolor]{\\fontfamily{ugq}\\selectfont\\large\\thedemsode}}
\\pgfmathsetmacro{\\made}{random(100,401)}
\\begin{document}
	\\setcounter{tocdepth}{1}
	\\setcounter{secnumdepth}{3}
	\\tableofcontents
	%\\section[Thi thử lần 1 Thái Hòa  - Nghệ AN  - Mã đề \\made]{Đề thi thử giữa HKI}
	\\begin{name}[Đề thi thử giữa HKI][Hóa][10][Phòng GD \\& ĐT Phù Mỹ]{Trường THPT Số 2 Phù Mỹ}{2024 - 2025}\\end{name}
	\\input{DuLieu/Hoa_10/KTGKI/KT_GK1_HOA_DE01.tex} %file 1
	\\begin{name}[Đề thi thử giữa HKI][Hóa][10][Phòng GD \\& ĐT Phù Mỹ]{Trường THPT Số 2 Phù Mỹ}{2024 - 2025}\\end{name}
	%\\section[Thi thử lần 1 Thái Hòa  - Nghệ AN  - Mã đề \\made]{Đề thi thử giữa HKI}
	\\input{DuLieu/Hoa_10/KTGKI/KT_GK1_HOA_DE01.tex} %file 2
	\\begin{name}[Đề thi thử giữa HKI][Hóa][10][Phòng GD \\& ĐT Phù Mỹ]{Trường THPT Số 2 Phù Mỹ}{2024 - 2025}\\end{name}
	%\\section[Thi thử lần 1 Thái Hòa  - Nghệ AN  - Mã đề \\made]{Đề thi thử giữa HKI}
	\\input{DuLieu/Hoa_10/KTGKI/KT_GK1_HOA_DE01.tex} %file 3
	\\fileend
\\end{document}
"""
        }
                
        self.command_groups = {
            'Cấu trúc văn bản': {
                'Phần': 'part',
                'Chương': 'chapter',
                'Bài,Mục': 'section',
                'Mục con cấp 1': 'subsection',
                'Mục con cấp 2': 'subsubsection'

            },
            'Lệnh soạn chuyên đề': {
                'Nổi bật (4 tùy chon)': 'Noibat[\\maunhan][][\\faStar][]',
                'Phần (1 tùy chọn màu sắc)': 'phan[\\mycolor]',
                'Thông tin': 'thongtin',
                'Font (qag,phv,put)':'myfont[13]',
                'Hộp công thức không có $':'khungct[\\mycolor]',
                'Hộp công thức toán':'hopcttoan}[\\maunhan]',
                'Hộp công thức có $':'boxct[\\maunhan][3pt][\\sffamily]',
                'In đậm':'indam[\\maunhan]',
            },
            'Templates': {
                'Cặp Open/Close solutionfile': { 
                    'Mẫu EX': 'soanex',
                    'Mẫu EXTF': 'soanextf',
                    'Mẫu BT': 'soanbt',
                },
                'Lệnh cho hóa học': { 
                    'Ô lượng tử': 'orbital',
                    'Ô nguyên tố': 'elementcell',
                },
                'Mẫu đề thi': { 
                    'Tiêu đề kì thi': 'tieudekithi',
                    'File mẫu đề thi (subfile)': 'subfile',
                }
                
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
        """Xử lý văn bản theo mode được chọn"""
        # Kiểm tra nếu là template
        if command in self.templates:
            return self.templates[command]
            
        # Xử lý theo mode
        if mode == "single":
            # Xử lý đơn dòng: bọc một dòng văn bản trong một lệnh
            return f"\\{command}{{{text}}}"
            
        elif mode == "multi":
            # Xử lý nhiều dòng: giữ nguyên cấu trúc nhiều dòng
            lines = text.strip().split('\n')
            # Thụt lề cho các dòng sau dòng đầu
            formatted_lines = []
            for i, line in enumerate(lines):
                if i == 0:
                    # Dòng đầu tiên không thụt lề
                    formatted_lines.append(line.strip())
                else:
                    # Các dòng sau thụt vào 4 dấu cách
                    formatted_lines.append("" + line.strip())
            # Kết hợp tất cả các dòng thành một khối văn bản
            formatted_text = '\n'.join(formatted_lines)
            # Bọc toàn bộ khối văn bản trong một lệnh
            return f"\\{command}{{\n{formatted_text}\n}}"
            
        elif mode == "batch":
            # Xử lý hàng loạt: mỗi dòng là một lệnh riêng biệt
            lines = text.strip().split('\n')
            return '\n'.join(f"\\{command}{{{line.strip()}}}" 
                           for line in lines if line.strip())
                           
        return text

    def taolenh(self, command, text):
        return self.process_text(command, text)

    def get_template(self, template_id):
        """Lấy nội dung mẫu theo ID"""
        return self.templates.get(template_id)

    def get_all_templates(self):
        """Lấy danh sách tất cả các mẫu"""
        return self.templates