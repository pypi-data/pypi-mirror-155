import sys
import os
from optparse import OptionParser
from rosdep2.main import rosdep_main

def main(args=None):
    command = sys.argv[1]
    print('欢迎使用国内版rosdep之rosdepc，我是作者小鱼！\n')
    print('小鱼制作了11万字的ROS2教程和配套视频，关注公众号《鱼香ROS》即可领取！\n')
    print('小鱼rosdepc正式为您服务')
    print("---------------------------------------------------------------------------")
    if command=="init":
        os.system("sudo mkdir -p /etc/ros/rosdep/sources.list.d/")
        os.system("sudo wget https://mirrors.tuna.tsinghua.edu.cn/github-raw/ros/rosdistro/master/rosdep/sources.list.d/20-default.list -O /etc/ros/rosdep/sources.list.d/20-default.list ")
        print('小鱼提示：恭喜你完成初始化，快点使用\n\n rosdepc update\n\n更新吧')
    elif command=='update':
        os.system("export ROSDISTRO_INDEX_URL=https://mirrors.tuna.tsinghua.edu.cn/rosdistro/index-v4.yaml && rosdep update")
        print('小鱼恭喜：rosdepc已为您完成更新!!')
    else:
        rosdep_main(sys.argv[1:])
    print("---------------------------------------------------------------------------")
    print('如果再使用过程中遇到任何问题，欢迎通过fishros.org.cn反馈，或者加入QQ交流群(139707339)')

