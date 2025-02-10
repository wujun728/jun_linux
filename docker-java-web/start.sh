#!/bin/bash
set -e
#运行脚本容器脚本

#检测是否存在相应命令
command_exists() {
	command -v "$@" > /dev/null 2>&1
}

#检测系统是否安装docker
if !(command_exists docker) ; then
    echo -e  "此系统未安装docker，请先安装docker"
    exit 1;
fi

echo "============docker version========="
docker version | cat
echo -e "\n"
echo -e "\n"

#检测系统是否安装docker-compose
if !(command_exists docker-compose) ; then
    echo "此系统未安装 docker-compose，请先安装 docker-compose"
    exit 1;
fi

echo "============docker-compose version========="
docker-compose version | cat
echo -e "\n"
echo -e "\n"

#检测是否安装git
if !(command_exists git) ; then
   echo "此系统未安装git，请先安装git"
   exit 1;
fi
echo "==========git version================"
git version | cat 
echo -e "\n"
echo -e "\n"

#获取项目git地址 （由用户输入，未输入则默认使用本地配置）


#切换到对应分支下


#todo 通过tag发布


#使用maven打包项目


#将项目解压到对应目录内


#启动容器
echo "===========启动容器========="
docker-compose up -d

#根据参数选择是否在控制台显示docker日志

set -- `getopt acdhimwe:fo "$@"`
while  [ -n "$1" ]
do
    case $1 in
        -a)
            make_arch
            ;;
        -c)
            make_clean
            ;;
        -d)
            make_decoder
            ;;
        -h)
            build_help
            ;;
        -i)
            make_decoder_image
            ;;
        -m)
            move_bin
            ;;
        -w)
            build_welcom
            ;;
        --)
            shift
            break
            ;;
        -o)
            echo "find -o option"
            ;;
        -f)
            echo "find -f option"
            ;;
        -e)
            echo "find -e option with param $2"
            shift
            ;;
        *)
            echo $1
            echo "unknow option"
    esac
    shift
done
