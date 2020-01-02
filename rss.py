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

        #print(content)
        body = pattern.findall(content)
        return body[0]
    def gen_rss(self):
        self.buffer = '''<?xml version="1.0"?>
<rss version="2.0">
<channel>
<language>zh-cn</language>
<copyright>cxy</copyright>
<generator>cxy.fun</generator>
<title>cxy</title>
<link>https://cxy.fun</link>
<description> cxy's blog </description>
'''
        htmls = os.listdir(self.dir)
        for html in htmls:
            if html.endswith('html') and not html.startswith('index'):
                self.buffer += '<item>\n'
                self.buffer += '<title>{}</title>\n'.format(self._get_title(os.path.splitext(html)[0]))
                link = 'https://cxy.fun/{}'.format(html)
                self.buffer += '<link>{}</link>\n'.format(link)
                self.buffer += '<description> <![CDATA[{}]]></description>\n'.format(self._get_html_body(html))
                self.buffer += '</item>\n'
        self.buffer += '</channel>\n'
        self.buffer += '</rss>'
        with open('rss.xml', 'w+') as f:
            f.write(self.buffer)
