import os
import re
class Rss():
    def __init__(self):
        self.buffer = ''
        self.dir = '.'
    def _get_title(self, filename : str):
        return filename.replace('-', ' ')
    def _get_html_body(self, filename) -> str:
        content = ''
        pattern = re.compile('<body>(.*?)</body>', re.DOTALL)
        with open(filename, 'r') as f:
            content = f.read()
        body = pattern.findall(content)
        return body[0]
    def gen_rss(self):
        self.buffer = '''<?xml version="1.0"?>
<rss version="2.0">
<channel>
<language>zh-cn</language>
<copyright>cxy</copyright>
<generator>caixiangyue.github.io</generator>
<title>cxy</title>
<link>https://caixiangyue.github.io</link>
<description> cxy's blog </description>
'''
        htmls = os.listdir(self.dir)
        for html in htmls:
            if html.endswith('html') and not html.startswith('index'):
                self.buffer += '<item>\n'
                self.buffer += f'<title>{self._get_title(os.path.splitext(html)[0])}</title>\n'
                link = f'https://caixiangyue.github.io/{html}'
                self.buffer += f'<link>{link}</link>\n'
                self.buffer += f'<description> <![CDATA[{self._get_html_body(html)}]]></description>\n'
                self.buffer += '</item>\n'
        self.buffer += '</channel>\n'
        self.buffer += '</rss>'
        with open('rss.xml', 'w+') as f:
            f.write(self.buffer)
            f.flush()
