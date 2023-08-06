# ApiTestEz

### 介绍
让API测试变得简单。<br>
ApiTestEz（以下简称EZ）主要提供以下3方面的核心功能：<br>
1. `ez.cfg`提供多个层级的配置环境；
2. 完成对http请求的封装，测试人员只用关注*Request*参数的传递，和*Response*的断言；
3. 引入反序列化模型断言。

---
### 安装教程

    pip install ApiTestEz

---

### Quick Start

### 项目目录 
---
1. 一个简单项目

       |-- EzTestDemo
           |-- <project_name>
           |   |-- test_whatever.py
           |-- settings
           |-- project.cfg

     `test_whatever.py`

   ```python
   import unittest
   
   from api_test_ez.core.case import UnitCase
      
      
   class SomeTest(UnitCase):
      
       def beforeRequest(self):
           self.request.url = "http://www.baidu.com"
      
       def test_something(self):
           assert self.response.status_code == 200
      
      
   if __name__ == '__main__':
       unittest.main()

   ```
---
2. 完整项目

        |-- EzTestDemo
          |-- <project_name>
          |   |-- <test_api_dir>
          |   |   |-- test_whatever.py
          |   |   |-- ez.cfg (optional: package priority)
          |   |   |-- model.py (optional)
          |   |-- ez.cfg (optional: module priority)
          |-- settings
          |-- project.cfg
          |-- ez.cfg (optional: project priority)
          |-- <resource> (optional)
              |-- <case_files> (optional)

     *`project.cfg`*为项目标识，它告诉EZ项目根目录和项目*`settings.py`*存放位置。<br>
     *`setting.py`*提供项目初始化设置项，如**`log`**、**`report`**配置。<br>
     *`ez.cfg`*与*`settings`*的区别在于，*`ez.cfg`*提供业务相关的配置，如*`http`*的*`headers`*、*`case_filepath`*（用例存放目录）、*`auto_request`*（自动完成请求）开关等，你还可以在里面放置业务需要的特殊变量，这些变量将会存放在*self.request.meta*中。它包含了多个层级`['case', 'package', 'module', 'project', 'command', 'default']`，优先级一次递减。<br>
     关于*`setting.py`*和*`ez.cfg`*支持的配置详情后述。<br>
     <br>
     *ez.cfg*是EZ框架的核心功能之一。下面，通过使用ez.cfg，我们来完成一个简单的请求。<br>

     `ez.cfg`

   ```ini
   [HTTP] 
   url = http://www.baidu.com
   ```
        
     `test_whatever.py`
        
     ```python
     import unittest

     from api_test_ez.core.case import UnitCase


     class SomeTest(UnitCase):

         def test_something(self):
             assert self.response.status_code == 200


     if __name__ == '__main__':
         unittest.main()
      ```
---
3. EZ和[ddt](https://github.com/datadriventests/ddt)一起工作
   EZ支持`ddt`
   假设我们有多个接口需要测试。（这里我们使用一些fake api：https://dummyjson.com/products/<page> ）。
   我们得到10个需要测试的接口 https://dummyjson.com/products/1 ~ https://dummyjson.com/products/10 。它们将返回10种不同型号的手机信息。<br>
   显然，这10个接口在测试过程中很大程度上是相似的，我们希望编写同一个类来完成对这10个接口的测试。<br>
   首先，我们需要一份用例文件，它负责储存用例编号、接口信息、期望结果等内容。EZ支持多种格式的用例文件：*Excel*、*YAML*、*JSON*、*Pandas*、*HTML*、*Jira*等，它使用[tablib](https://tablib.readthedocs.io/en/stable/)读取用例文件。
   这里我们使用*Excel*作为存储用例文件。<br>
   <br>
`case.xlsx`<br>

   
| case_name | path         |
|-----------|--------------|
| TC0001    | /products/1  |
| TC0002    | /products/2  |
| TC0003    | /products/3  |
| TC0004    | /products/4  |
| TC0005    | /products/5  |
| TC0006    | /products/6  |
| TC0007    | /products/7  |
| TC0008    | /products/8  |
| TC0009    | /products/9  |
| TC0010    | /products/10 |


   我们将请求的域名放在`ez.cfg`中以便切换测试环境时统一管理，同时将用例路径存放在`ez.cfg`中，以便EZ发现用例。<br>

```ini
[CASE]
case_filepath = /<some path>/case.xlsx

[HTTP]
host = https://dummyjson.com
```
   > *在`ez.cfg`中，HTTP method默认为GET*
   
   在`test_whatever.py`中，现阶段我们并不需要做出
      
      
      
      
      
---
### TODO
1.  用例支持入参，例：f"{'X-Forwarded-For': ${province_ip} }"
2.  url拆分host + path
3.  ~~报告~~
4.  ~~ORM响应断言实现~~
5.  cmdline
6.  项目构建工具：ez create xxxx
7.  基于pytest的用例实现
8.  ~~pypi setup~~
9. 完善注释，文档