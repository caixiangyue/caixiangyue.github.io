import sys
import urllib.request
import json
import os, time
from rss import Rss

class MarkdownConvert():
    def __init__(self, md):
        self.data = {
            'text' : md,
            'mode' : 'gfm'
        }
    def md2html(self):
        params = json.dumps(self.data).encode('utf8')
        handle = urllib.request.urlopen('https://api.github.com/markdown', params)
        return handle.read()

class GenerateCXY():
    post_dir = './post'
    def _save_file(self, filename, content):
        with open(filename, 'w') as f:
            f.write(content)
            f.flush()
    # def _get_filename(self, path):
    #     base = os.path.basename(path)
    #     return os.path.splitext(base)[0]
    def _get_title(self, filename):
        return filename.replace('-', ' ')
    def _get_post_dir(self):
        ret = []
        posts = os.listdir(self.post_dir)
        for post in posts:
            filepath = os.path.join(self.post_dir, post)
            if os.path.isfile(filepath):
                filename = os.path.splitext(post)[0]
                ret.append({
                    'title': self._get_title(filename),
                    'create_time' : os.stat(filepath).st_mtime,
                    'filename' : filename,
                    'filepath' : filepath,
                    'html_file' : filename + '.html'
                })
        ret.sort(key=lambda item: item['create_time'], reverse=True)
        return ret
    def _get_css(self):
        return '<link rel="stylesheet" type="text/css" href="./css/github_new.css">'
    def build_index_md(self):
        header = """## cxy's blog
just for fun. mail:caixiangyue007@gmail.com    
[RSS](rss.xml)

-----
        """
        header += '\n\n'
        posts = self._get_post_dir()
        for post in posts:
            if post['filename'] != 'index':
                header += f'[{post["title"]}]({post["html_file"]})\n'
        self._save_file(os.path.join(self.post_dir, 'index.md'), header)
    def _read_md(self, filepath):
        with open(filepath, 'r') as f:
            return f.read()
    def build_html(self, build_all=False):
        utteranc = """<script src="https://utteranc.es/client.js"
        repo="caixiangyue/caixiangyue.github.io"
        issue-term="pathname"
        theme="github-light"
        crossorigin="anonymous"
        async>
</script>
"""
        google_analytics = """<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-160306868-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-160306868-1');
</script>
"""
        posts = self._get_post_dir()
        for post in posts:
            html =  '<!DOCTYPE html>'
            html += '<html><head><meta charset="utf-8">'
            html += self._get_css()
            html += '<link rel="shortcut icon" href="favicon.png" type="image/x-icon">'
            html += google_analytics
            title = '<title>cxy</title>'
            if post['filename'] != 'index':
                title = f'<title>{post["title"]}</title>'
                if not build_all and time.time() - post['create_time'] > 1800:
                    continue
            html += title
            html += '</head><body>'
            html += MarkdownConvert(self._read_md(post['filepath'])).md2html().decode('utf8')
            if post['filename'] != 'index':
                html += f'<hr><p>{time.ctime(post["create_time"])}</p>'
                html += utteranc
            html += '</body>'
            html += '</html>'
            self._save_file(post['html_file'], html)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'all':
            build_all = True
    g = GenerateCXY()
    g.build_index_md()
    g.build_html(build_all)
    r = Rss()
    r.gen_rss()
    
