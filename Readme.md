
> 拉个机器人到群组里，对骗子进行监控，一旦骗子发消息，将会提醒群组

### 使用方法
```angular2html
# 私信机器人，只有管理员才能使用命令
# 添加骗子用户名到数据库
/add_user username
# 从数据库删除
/remove_user username
```
### 下载&安装依赖

```angular2html
git clone https://github.com/RoySean6/TrustBot.git
cd TrustBot
pipenv shell
pip install requirements.txt
```

### 配置
新建.env文件设置bot token和admin id
```angular2html
TELEBOT_TOKEN=''
ADMIN_ID=''
REPLY_MESSAGE="Attention!!! A damn scammer has sent a message"
```
### 启动
```angular2html
python main.py
```
挂机的话可以尝试用screen 或者 supervisor后台运行

### bot的创建、设置

```angular2html
https://telegram.me/BotFather
```
按提示设置bot名称，然后你会获取token，填入上面的env文件
你刚拉入群组是不能接受消息的，显示`has no access to messages`
你需要在BotFather 输入`/setprivacy`
再输入 `Disable`，提升机器人权限。
如果发现机器人依然收不到消息.
我们将机器人踢出群, 再拉进群, 就可以收到消息了.

获取用户id
```angular2html
https://telegram.me/userinfobot
```