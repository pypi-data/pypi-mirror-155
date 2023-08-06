#!/usr/bin/python3
#Copyright by Chen Chuan (kcchen@139.com)

import os,random,datetime,math,sys,shutil

def 同步文件(源,目标):
    if not os.path.isfile(源):return
    源修改时间=os.stat(源).st_mtime
    if os.path.exists(目标):
        目标修改时间=os.stat(目标).st_mtime
    else:
    	目标修改时间=0
    if 源修改时间>目标修改时间:
        print("%s  ==>  %s" %(源,目标))
        shutil.copy2(源,目标)

def dsync():    #双向同步
    目录1=""
    目录2=""
    if len(sys.argv)>1:
        配置文件=sys.argv[1]
    else:
        配置文件="dsync.conf"
    if not os.path.isfile(配置文件):
        print("未找到文件 " + 配置文件)
    f=open(配置文件)
    配置内容=f.readlines()
    f.close()
    for conf in 配置内容:
        conf=conf.strip().split("=")
        if len(conf)!=2:continue
        i,v=conf
        if i.lower()=="d1":目录1=v
        if i.lower()=="d2":目录2=v
        if i.lower()=="f":
            文件1=os.path.join(目录1,v)
            文件2=os.path.join(目录2,v)
            同步文件(文件1,文件2)
            同步文件(文件2,文件1)

if __name__ == "__main__":
    dsync()
