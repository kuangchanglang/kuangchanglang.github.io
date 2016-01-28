---
layout: post
title:  "extundelete数据恢复"
date:   2015-07-21 12:24:39
categories: jekyll update
---

今天开机想上传昨天的更新，发现一个文件不见了。history一查，原来被自己删掉了。不知道昨天脑子怎么抽的，这个文件改动最多，总不能把旧版本更新回来重新改吧。所以又去搬救兵：extundelete。 记录一下用法，下次不用去google了。  
  
先``df -T -h``看一下被删掉的文件挂载在哪块盘下。然后对那块盘进行相应的恢复（单个文件，单个目录，全部恢复）。  

恢复单个文件的命令如下：  
``extundelete /dev/sda9 --restore-file relative/path/to/file``  
其中，/dev/sda9换成你的文件所挂载所在的硬盘，也就是前面df的结果第一列。后面填从挂载点开始的相对路径。举个栗子，假如文件路径是/home/data/pyfile/a.py，而/home挂载在/dev/sda9，则文件相对路径填写就是data/pyfile/a.py，最前面不用加斜杠。  

恢复文件夹操作也同理。恢复后会帮你存在当前目录下的子目录RESTORE_FILES里面。当然，不是所有删除的文件都可以被恢复，时间太久的文件，磁盘内容会被覆盖，是恢复不回来的。  

不能再手抖了！  
