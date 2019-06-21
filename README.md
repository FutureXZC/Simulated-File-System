# 模拟文件系统

## 题目要求

- 学习操作系统文件管理机制的相关知识  
- 设计一个简单多用户文件系统
- 要求系统具有分级文件目录、文件分权限操作、用户管理等
- 模拟文件管理的工作过程，加深理解文件系统的内部功能及内部实现机制
- 对所采用的算法、程序结构和主要函数过程以及关键变量进行详细的说明
- 提供关键程序的清单、源程序及可执行文件和相关的软件说明
- 对程序的调试过程所遇到的问题进行回顾和分析，对测试和运行结果进行分析
- 总结软件设计和实习的经验和体会，进一步改进的设想

## 课题相关数据结构及算法设计

### 1 主要数据结构

&emsp;&emsp;所有实体均封装成类，使用时将类实例化即可。由于类中包含的属性和方法较多，因此本模块的数据结构仅展示类的声明及符合google风格的python标准注释规范的类头部注释，相关属性介绍和接口介绍都在注释中给出。类的继承在类声明中给出，继承的属性若无变化则在子类中不再重复解释其功能，所有方法与属性均为公有属性。  

#### （1） 在后端文件backEnd.py中的类数据结构

① 用户User：  
class User():  
&emsp;&emsp;用户类，包含用户名和用户权限  
&emsp;&emsp;@attribute name: 用户名  
&emsp;&emsp;@attribute authority: 用户权限，只能是r、w和x三者的组合  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;权限r: 可读权限，默认每个用户都有，可以读取文件目录  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;权限w: 可写权限，可以读、增、删、改文件，不可执行文件  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;权限x: 可执行权限，除拥有上述权限外还可执行文件  
② 文件控制块FCB：  
class FCB():  
&emsp;&emsp;文件控制块，存储文件/文件夹的相关信息  
&emsp;&emsp;@attribute user: 当前操作用户，User对象  
&emsp;&emsp;@attribute parent: 父级目录对象，根节点无父级目录，Folder对象  
&emsp;&emsp;@attribute name: 当前文件/文件夹对象的名称，字符串  
&emsp;&emsp;@attribute author: 当前文件/文件夹对象的拥有者，字符串  
&emsp;&emsp;@attribute date: 当前文件/文件夹对象的最后修改时间，字符串  
&emsp;&emsp;@attribute path: 从根节点至当前文件/文件夹对象的路径，字符串  
&emsp;&emsp;@method get_config: 获取当前路径下的配置文件config.txt  
&emsp;&emsp;@method update_config: 更新当前路径下的配置文件config.txt  
&emsp;&emsp;@method rename: 重命名当前对象的name  
&emsp;&emsp;@method back: 获取父目录的文件列表  
③ 文件夹Folder（继承FCB）：  
class Folder(FCB):  
&emsp;&emsp;文件夹实例，继承FCB，附加部分特性  
&emsp;&emsp;@attribute children: 存放文件夹下的文件，列表  
&emsp;&emsp;@attribute _type: 文件类型为“文件夹”，字符串  
&emsp;&emsp;@method get_children: 获取当前文件夹下的所有子文件  
④ 文件File（继承FCB）：  
class File(FCB):  
&emsp;&emsp;文件实例，继承FCB，附加部分特性  
&emsp;&emsp;@attribute _type: 文件类型，由文件后缀决定，字符串  
&emsp;&emsp;@attribute size: 文件大小，单位为b，整型  
⑤ 根节点Root（继承Folder）：  
class Root(Folder):  
&emsp;&emsp;根节点，继承Folder，附加部分特性  
&emsp;&emsp;@method load: 初始化装载，完成对root节点的children的初始化  
⑥ 控制程序OSManager：  
class OSManager():  
&emsp;&emsp;控制程序  
&emsp;&emsp;@attribute user: 正在操作的用户，User实例  
&emsp;&emsp;@attribute main_board: 当前显示目录的节点列表，列表  
&emsp;&emsp;@attribute here: 当前节点位置，为Root/Folder/File实例对象  
&emsp;&emsp;@method ls: 展示当前目录下属于当前用户的所有文件  
&emsp;&emsp;@method cd_in: 进入下一级 或 运行目标程序  
&emsp;&emsp;@method cd_back: 返回上一级  
&emsp;&emsp;@method rename: 重命名，若用户有w权限则调用文件/文件夹本身的方法  
&emsp;&emsp;@method mkdir_or_touch: 创建文件夹/文件，若用户有w权限则调用系统api创建  
&emsp;&emsp;@method delete: 删除文件/文件夹，若用户有w权限则调用系统api删除  

#### （2） 在GUI界面程序GUI.py中的数据结构  

&emsp;&emsp;窗体中的控件也为类的成员变量，但在此省略，仅展示相关控件调用的功能函数。  
① 文件管理系统的主窗体MainWindow：   
class MainWindow():  
&emsp;&emsp;文件管理系统的主窗体(GUI)，  
&emsp;&emsp;显示当前用户、当前文件路径、当前路径下的文件及文件详细信息，  
&emsp;&emsp;提供双击鼠标左键打开文件夹或运行程序、单击鼠标右键重命名文件功能，  
&emsp;&emsp;提供可以新建或删除文件或文件夹的按钮，实现在模拟文件系统中的增删改查，  
&emsp;&emsp;实现针对不同用户不同权限的可视化操作。  
&emsp;&emsp;本类的所有方法均调用后端OSManager的方法  
&emsp;&emsp;@method get_win: 获取当前窗体实例  
&emsp;&emsp;@method ls: 展示当前目录下属于当前用户的所有文件  
&emsp;&emsp;@method cd_in: 双击鼠标左键 - 进入下一级 或 运行目标程序  
&emsp;&emsp;@method ca_back: 点击返回按钮 - 返回上一级  
&emsp;&emsp;@method refresh: 刷新当前文件列表  
&emsp;&emsp;@method mkdir: 新建文件夹，默认文件名为当前系统时间  
&emsp;&emsp;@method touch: 创建新文件，默认创建文本文件，文件名为当前系统时间  
&emsp;&emsp;@method f_delete: 删除文件，向后端传入选中的对象，  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;然后根据后端返回的状态码判断操作完成与否并输出  
&emsp;&emsp;@method rename: 单击鼠标右键，重命名文件或文件夹  
&emsp;&emsp;@method show: 绑定表格上的事件，运行窗口  
② 文件管理系统的登录窗口LoginWindow：  
class LoginWindow():  
&emsp;&emsp;文件管理系统的登录窗口(GUI)，生成窗体，在输入框内输入用户名和密码，  
&emsp;&emsp;若用户名和密码匹配成功则销毁当前窗体，进入主界面（即生成MainWindow）  
&emsp;&emsp;@method show: 运行窗体  
&emsp;&emsp;@method login: 登录，若用户名和密码匹配成功则进入主界面  
#### （3） 在用户管理程序admin.py中的数据结构  
管理员操作封装Admin：  
class Admin():  
&emsp;&emsp;管理员操作，包括登录和对用户信息的增删改查  
&emsp;&emsp;@attribute user_info: 存储用户信息，字典，format: {用户名:[密码，权限]}  
&emsp;&emsp;@method login: 登录验证，返回登录成功与否的结果  
&emsp;&emsp;@method update_user_info_file: 更新用户数据文件user_info.txt  
&emsp;&emsp;@method new_user: 创建一个新用户  
&emsp;&emsp;@method del_user: 删除一个已有用户  
&emsp;&emsp;@method edit_user: 修改一个现有用户的密码和权限，不可重命名  
&emsp;&emsp;@method view: 查看现有用户的详细信息  

### 2 主要算法与流程介绍  

#### （1）获取父节点的目录  

&emsp;&emsp;可通过当前节点的parent属性获取父节点对象，然后拼接父节点的路径path、名字name来获取获取父节点的实际路径parent_path，在该路径下调用系统api，即os.walk来获取文件/文件夹的目录，再将parent_path和“/config.txt”拼接获取父目录的config.txt文件，读取该文件可以获得父目录层级中的文件的拥有者。  

#### （2） 获取子节点的目录/执行子节点

&emsp;&emsp;由于本系统中规定，在同一级目录下（树的同一层下），无论是文件还是文件夹，都不能同名。因此，可以通过在前端点击文件目录表项获取的文件名target_name，以此在当前节点（必为Folder）的children列表中寻找与target_name同名的文件。  
&emsp;&emsp;若该文件为Folder类型，则将控制程序OSManager的当前节点here更新为子节点，当前目录节点列表main_board更新为子节点的列表，即当前节点的children列表。  
&emsp;&emsp;若该文件为File类型，则调用系统的start命令执行之。  

#### （3） 目录树的节点初始化与更新方式

&emsp;&emsp;在起始时，目录树只有根节点和与根节点直接相连的第一层节点。理论上目录树在用户登录成功后至退出程序时应该始终存在，每个节点都是一个Root、Folder或File对象，但事实上对象中存储的信息会在当前目录发生变化的时候变化，因此实际存在的只有当前节点、其父节点和其子节点。无论是用户双击某一文件夹时，在该文件夹节点下回生成其子节点，还是用户点击返回按钮返回上一级目录，会找到当前节点的父节点，目录树会完成一次更新。  

#### （4） 系统规定

&emsp;&emsp;与Windows和Linux系统相比，本模拟系统中存在一些值得注意的异同，如下：  
- 重命名文件时需在GUI上选择目标文件，然后单机鼠标右键，弹出输入框，重新键入文件名后，单击输入框右侧的“OK”按钮，提交修改。  
- 一切皆文件，故同级目录下的文件与文件夹不可同名。  
- 新建文件或文件夹时，默认名称为当前系统时间，格式为“年-月-日-时-分-秒”，若为文件，则默认新建的文件类型为txt。  
- 用户权限在用户被创建时就应该被指定，权限只能为“r”、“w”和“x”三者的组合，且至少包含“r”。其中，“r”为可读权限，“w”为可修改（包括增、删和改）权限，“x”为允许执行可执行文件的权限。  
- 资源配置文件config.txt不允许在本系统内被包括root在内的任何人修改、删除或查看，以防造成目录树节点的配置信息混乱。  
