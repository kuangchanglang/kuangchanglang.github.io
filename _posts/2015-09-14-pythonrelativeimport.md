---
layout: post
title:  "python相对引用"
date: 2015-9-14 22:19:10 
categories: python
---

Python的相对引用略微坑了一点，一开始用的时候心理默喷，想引用兄弟包下的一个模块（文件）都报错。说好的python大法好，延年益寿呢。  
喷归喷，还是要找到解决问题的方法。  

关于相对引用的有好几个[pep 0328](https://www.python.org/dev/peps/pep-0328/)
  
# 目录结构，单元测试和源文件分开文件夹存放。  
{% highlight shell %}
pkg/  
    __init__.py  
    src/  
        __init__.py  
        module.py  
    test/  
        __init__.py  
        test_module.py  
{% endhighlight %}

# 方法1，绝对引用，修改sys.path  
python的import从sys.path路径由前向后中搜索。所以可以将src加入到sys.path中，就可以通过绝对路径引用pa了在test_module顶部添加如下代码  

{% highlight python %}
import sys  
sys.append('../')  #将pkg文件夹加入sys.path  
from src import module  
{% endhighlight %}
  
运行方法：在test所在文件夹中执行  
{% highlight python %}
python test_module.py
{% endhighlight %}

# 方法2，相对引用，使用python -m模块化运行
test_module使用相对引用，一个"."为当前目录，两个点为其父目录，依次类推，代码如下：  
{% highlight python %}
from ..src import module
{% endhighlight %}
  
运行方式：在pkg的上一层目录执行  
{% highlight python %}
python -m pkg.test.test_module
{% endhighlight %}

# 方法3，绝对引用，使用python -m模块化运行  
test_module中直接引用，代码如下：  
{% highlight python %}
from src import module
{% endhighlight %}
  
运行方式：在pkg文件夹下执行  
{% highlight python %}
python -m test.test_module
{% endhighlight %}

# it's all about sys.path  
其实这里面最关键的地方就在于sys.path这个变量，当import的内容在sys.path中找不到时自然就报错，方法1手动将要引用的路径加入sys.path中，运行py文件。  
后面两种方法都通过-m以模块的形式运行，python -m的说明：

> -m module-name  
>      Searches sys.path for the named module and runs the corresponding .py file as a script. 

需找sys.path中的模块执行py文件，在test_module中打印sys.path会发现，使用-m运行和直接运行python有所不同：

- 运行python py时sys.path添加文件所在目录。
- 运行python -m时sys.path添加''，也就是当前目录。

所以方法2运行python -m pkg.test.test_module时，sys.path中包含pkg的上一层目录，搜索pkg包时命中pkg文件夹（里面包含了__init__.py）。依次找到test_module.py，然后执行。test_module.py中的相对引用from ..src import module，先找上一层的package，也就是pkg，再找到src。也就是因为这个要求pkg必须是package，运行时需在其父目录。  

而方法3也同样的道理，运行时sys.path包含pkg目录，from src import module语句从pkg目录中寻找src的包（包含__init__.py），命中src目录，然后找到module。这时不要求pkg必须是package（__init__.py可以删掉）。   
