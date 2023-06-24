
import os
import shutil
import subprocess
import re

def run_cmd(cwd, arguments):
    print(f'Running command: {arguments}')
    p = subprocess.Popen(arguments, cwd=cwd)
    retcode = p.wait()
    if retcode != 0:
        raise Exception(f'Command failed with exit code {retcode}: {arguments}')

class BuildTools:
    packwiz_command = 'packwiz'

    def __init__(self):
        # FIXME: Locate tools and check versions
        pass

    def rm_dir(self, path):
        shutil.rmtree(path)

    def packwiz(self, *args):
        run_cmd(cwd='src/packwiz', arguments=[self.packwiz_command] + list(args))

    def asciidoctor(self, *args):
        run_cmd(cwd='.', arguments=['asciidoctor'] + list(args))

    def pandoc(self, *args):
        run_cmd(cwd='.', arguments=['pandoc'] + list(args))

    def convert_to_markdown(self, inputfile, tempfile, outputfile):
        self.asciidoctor('-b', 'docbook', '-o', tempfile, inputfile)
        self.pandoc('-f', 'docbook', '-t', 'markdown', '--wrap=none', tempfile, '-o', outputfile)
        self.remove_file(tempfile)

    def remove_file(self, path):
        os.remove(path)


def find_pack_version():
    with open('src/packwiz/pack.toml', 'r') as f:
        for line in f:
            m = re.match(r'version\s*=\s*"([0-9.\-]+)"', line)
            if m:
                return m.group(1)
    raise Exception('Could not find pack version in pack.toml')

def build(bt: BuildTools):
    # Re-create target directory
    # FIXME: It would be better to keep the directory, but empty it
    # bt.clear_dir(target)
    target = os.path.realpath('target')
    bt.rm_dir(target)
    os.makedirs('target')
    # Build modpack via packwiz
    pack_version = find_pack_version()
    print(f'Pack version: {pack_version}')
    bt.packwiz('modrinth', 'export', '-o', f'{target}/q1cc-create-modpack-{pack_version}.mrpack')
    # Build CHANGELOG and Modrinth-Description
    bt.convert_to_markdown('CHANGELOG.adoc', f'{target}/CHANGELOG.xml', f'{target}/CHANGELOG.md')
    bt.convert_to_markdown('Modrinth-Description.adoc', f'{target}/Modrinth-Description.xml', f'{target}/Modrinth-Description.md')

if __name__ == '__main__':
    build(BuildTools())
