# Remind Recharge

饿死了🐎

跪谢这个仓库 [你还好🐎](https://github.com/unbyte/are-u-ok)

## 2021.6.30 更新（不能依靠Github Action了）
挂了国外的 proxy 访问 `pass.neu.edu.cn`，会显示404，这直接导致无法获取到登录信息，无法进行下一步操作了

所以依赖Github Action，自动发邮件提醒的功能恐怕是无法使用了

不过在本地（国内本地）运行 `python main.py <学号> <密码>`，还是可以正常获取到余额的


## 能干什么

能获取你的校园卡余额

## 如何使用

### 本地使用

1. 克隆本仓库
2. 运行
```
python main.py <学号> <密码>
```

3. 会在控制台上打印出你的余额

### 低于某个值时自动发邮件提醒

总体上和 [你还好🐎](https://github.com/unbyte/are-u-ok) 的自动打卡用法类似，可以先去看看 [你还好🐎](https://github.com/unbyte/are-u-ok) 的自述文档，那边文档写的很好了

1. Fork本仓库，进入你自己Fork之后的仓库
2. 在 Settings 里面，设置以下7个Secrets
   - `USER` 学号
   - `PASS` 一网通密码（**不是饭卡的6位消费密码**）
   - `WARN_NUM` 阈值，低于这个值会发邮件提醒
   - `MAIL_HOST` 邮件的SMTP服务器地址，带上端口号，不支持SSL，例如 smtp.163.com:25
   - `MAIL_USER` 登录邮件服务器的用户名
   - `MAIL_PASS` 登录邮件服务器的密码
   - `MAIL_RECEIVER` 邮件收件人

3. 可以对 README.md 进行一次在线修改并保存（比如加一行空行之类的），然后去 Actions 标签中查看运行结果

## 已知 Issue
- 不定时会发生 Connection timed out ，也许和 GitHub WorkFlow 服务器在国外有关
