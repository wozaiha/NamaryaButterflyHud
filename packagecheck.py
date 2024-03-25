import os

import pkg_resources
import subprocess
import sys


def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"安装 {package} 失败: {e}")
        print(f"failed to install {package} : {e}")
        return False
    return True


def package_check():
    # 读取requirements.txt文件
    with open(os.path.split(os.path.realpath(__file__))[0] + '\\requirements.txt', 'r') as f:
        packages = f.read().splitlines()

    # 检查并安装每个库
    for package in packages:
        try:
            dist = pkg_resources.get_distribution(package)
            print("{} ({}) 已安装".format(dist.key, dist.version))
            print("{} ({}) is installed".format(dist.key, dist.version))
        except pkg_resources.DistributionNotFound:
            print("{} 未安装，正在安装...".format(package))
            print("{} is not installed, try to install...".format(package))
            if not install(package):
                print(f"无法安装 {package}，请手动安装。")
                print(f"failed to install {package}, please install it manually")
                continue


package_check()

