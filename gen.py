import urllib.request
import json
import os, time

class MarkdownConvert():
    def __init__(self, md):
        self.data = {
            "text" : md,
            "mode" : "gfm"
        }
    def md2html(self):
        params = json.dumps(self.data).encode('utf8')
        handle = urllib.request.urlopen("https://api.github.com/markdown", params)
        return handle.read()

class GenerateCXY():
    post_dir = './post'
    def _save_file(self, filename, content):
        with open(filename, 'w') as f:
            f.write(content)
    # def _get_filename(self, path):
    #     base = os.path.basename(path)
    #     return os.path.splitext(base)[0]
    def _get_title(self, filename : str):
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
                    'create_time' : time.ctime(os.stat(filepath).st_mtime),
                    'filename' : filename,
                    'filepath' : filepath,
                    'html_file' : filename + '.html'
                })
        ret.sort(key=lambda item: item['create_time'], reverse=True)
        return ret
    def _get_css(self):
        return '<link rel="stylesheet" type="text/css" href="{}">'.format('./css/github_new.css')
    def build_index_md(self):
        header = """## cxy's blog
just for fun. mail:caixiangyue007@gmail.com    

-----
        """
        header += '\n\n'
        posts = self._get_post_dir()
        for post in posts:
            if post['filename'] != 'index':
                header += '[{}]({})'.format(post['title'], post['html_file'])
        self._save_file(os.path.join(self.post_dir, 'index.md'), header)
    def _read_md(self, filepath):
        with open(filepath, 'r') as f:
            return f.read()
    def build_html(self):
        gitalk = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/gitalk@1/dist/gitalk.css">
<script src="https://cdn.jsdelivr.net/npm/gitalk@1/dist/gitalk.min.js"></script>
<script src="https://cdn.bootcss.com/blueimp-md5/2.10.0/js/md5.min.js"></script>
<div id="gitalk-container"></div>
<script>
  const gitalk = new Gitalk({
    clientID: 'a22a0da2e464b1b98761',
    clientSecret: 'b7630b913b13bd9cd26f93794d25367387bd2840',
    repo: 'caixiangyue.github.io',
    owner: 'caixiangyue',
    admin: ['caixiangyue'],
    id: md5(location.pathname), // Ensure uniqueness and length less than 50
    distractionFreeMode: false // Facebook-like distraction free mode
  });
  (function() {
    if (["localhost", "127.0.0.1"].indexOf(window.location.hostname) != -1) {
      document.getElementById('gitalk-container').innerHTML = 'Gitalk comments not available by default when the website is previewed locally.';
      return;
    }
    gitalk.render('gitalk-container');
  })();
</script>
"""
        posts = self._get_post_dir()
        for post in posts:
            html =  '<!DOCTYPE html>'
            html += '<html><head><meta charset="utf-8">'
            html += self._get_css()
            html += '<title>{}</title>'.format(post['title'])
            html += "</head><body>"
            html += MarkdownConvert(self._read_md(post['filepath'])).md2html().decode('utf8')
            if post['filename'] != 'index':
                html += '<hr><p>{}</p>'.format(post['create_time'])
                html += gitalk
            html += "</body>"
            html += "</html>"
            self._save_file(post['html_file'], html)


if __name__ == "__main__":
    g = GenerateCXY()
    g.build_index_md()
    g.build_html()
    