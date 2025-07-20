import re
def taolenh(command, Text):
    Text=Text.strip()
    Text=re.sub(r"^[Cc][Hh][UuƯư][OoƠơ][Nn][Gg]\s*\d+\s*[\.):/_\-]*",'',Text)
    Text=re.sub(r"^[Bb][AaÀà][Ii]\s*\d+\s*[\.):/_\-]*",'',Text)
    Text=re.sub(r"^\d+\s*[\.):/_\-]*",'',Text)
    Text=re.sub(r"^(?:IX|IV|V?I{1,3}|I[XV]|X[LC]|L?X{1,3}|C[DM]|D?C{1,3}|M{1,3})\s*[\.):/_\-]+",'',Text)
    Text=re.sub(r"^[A-Za-z]+\s*[\.):/_\-]+",'',Text)
    Text=Text.strip()
    Tempt=f'\n\\{command}{{{Text}}}'
    return Tempt
