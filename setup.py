import argparse
import subprocess
import sys
import time


def _install_libs():
    proc = subprocess.run([
        sys.executable,
        '-m',
        'pip',
        'install',
        '-r',
        'requirements.txt',
    ])
    if proc.returncode == 0:
        print('ライブラリインストール: 成功')
    else:
        print('ライブラリインストール: 失敗')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ci', action='store_true')
    args = parser.parse_args()
    _install_libs()
    if not args.ci:
        print('3秒後に終了します...')
        time.sleep(3)
