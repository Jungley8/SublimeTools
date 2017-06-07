import sublime
import sublime_plugin
import os
from os.path import splitext, basename, dirname, exists
import subprocess


def get_setting(view, key):
    settings = view.settings().get('Tools')
    if settings is None:
        settings = sublime.load_settings('Tools.sublime-settings')
    return settings.get(key)


def get_syntax(view):
    return splitext(basename(view.settings().get('syntax')))[0]


def get_extension(view):
    file_name = view.file_name()
    return splitext(file_name)[1]


def is_scss(view):
    return get_syntax(view) in ('SASS', 'SCSS') \
        or get_extension(view) == '.scss'


def cmd(command, tip):
    # 执行系统命令
    try:
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    except OSError:
        raise Exception(tip)

    stdout, stderr = p.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if stderr:
        raise Exception(stderr)
    else:
        return stdout


class ScssCompileOnSaveCommand(sublime_plugin.EventListener):
    def on_post_save(self, view):
        debug = get_setting(view, 'debug')
        if is_scss(view):
            scssdir = dirname(view.file_name())
            # D:\code\www\tp5\public\static\scss
            # basedir = dirname(scssdir)
            # D:\code\www\tp5\public\static
            fullname = basename(view.file_name())
            # admin.scss
            filename = splitext(fullname)
            # ['admin','.scss']

            print('scssdir: ', scssdir)
            print('fullname: ', fullname)
            print('filename: ', filename)

            # 输出目录
            out = get_setting(view, 'scss-compile-out')
            cssdir = scssdir + out
            # D:\code\www\tp5\public\static\css
            if not exists(cssdir):
                os.makedirs(cssdir)

            # 拼接scss命令
            command = 'scss ' + fullname
            command += ' ' + out + filename[0]
            command += get_setting(view, 'scss-compile-ext')

            command += ' --style '
            command += get_setting(view, 'scss-compile-style')

            command += ' ' + (' ').join(
                get_setting(view,
                            'scss-compile-other'))

            if debug:
                print(command)

            # 执行系统命令
            try:
                os.chdir(scssdir)
                tip = '请先安装scss环境，并添加到系统环境变量$PATH中'
                return cmd(command, tip)
            except Exception as e:
                sublime.error_message('Scss Compile ERROR!\n%s' % e)


class FoldParentFolderCommand(sublime_plugin.WindowCommand):

    def run(self, paths):
        branch, leaf = os.path.split(paths[0])
        print(branch)
        print(leaf)

    def is_enabled(self, paths):
        return len(paths) == 1
