# BreakTimer 休息定时器

## 休息模式：

<img src="https://user-images.githubusercontent.com/30487483/214987725-7ce7976c-08e0-422f-ad97-0e9c3f9bb444.png" width="600">

## 学习模式：
<img src="https://github.com/baizhiren/timer/assets/30487483/949311ed-37cf-41ff-832b-d92ffa581e60" width="300">


## 主要功能：
1. 点击“开始自律”，程序会按照 学习 小休息 学习 小休息 .... 学习 大休息 运行（更加灵活的番茄钟），可以根据自己的需求自定义时间

   休息模式会全屏显示，无法更改时间，如果此时为强制模式，会同时全屏显示并置于最上层，锁定鼠标和键盘, 非常适合沉迷代码\久坐人士

2. 点击立刻休息，会立即进入休息阶段，可在config中配置break_now_time时间长度

3. 点击重置按钮：会重新开始计时

4. “永无止境”按钮： 启动循环模式， 当大休息阶段结束后，会继续开启学习模式，进入下一个循环

5. “肝数”统计：会统计学习阶段的次数

6. "重置按钮": 重新启动一轮学习休息循环，重置时间

7. 绯红之王: 跳过当前学习阶段

8. 延迟休息功能: 当进入休息模式后，可以按下三次回车键来进入一个时长为5分钟的“学习模式”，退出全屏，下次休息阶段时长 + 3分钟，该功能对同一个休息阶段仅能使用3次, (config中配置delay_break)

9. 锁机模式（护肝模式):  默认每晚10:30到次日6：00为养肝时间，在此阶段类似于休息模式，用户不能操作电脑
    
   自定义时间的方式: 删除config中"target_end" 和 "target" 选项, 并修改 "liver", "liver_to" 设置时间，**需要重启应用**

   紧急解锁方式：和普通的休息模式不同，锁机模式下更为严格，锁机模式下需要正好按下99下空格（不能多按），解除锁键盘锁定

11. 学习模式黑名单（针对应用）:
    学习模式可以启动黑名单来关掉一些让人分心的应用（参考config参数中的"black_lists"项配置）

12. 学习模式黑名单（针对网页）:
    可以阻止一些网络域名，通过代理的方式实现，同时支持链接vpn后的网站过滤

    若想使用这个功能，请下载[mitmproxy 证书](https://docs.mitmproxy.org/stable/concepts-certificates/)，并参考config参数中"block_website"配置，

14. 休息模式白名单
    如果想在一些时间段禁止休息模式的开启（以防止开会等情况）, 可以参考config参数中的"white_sheet""项配置

15. 离开检测：
    如果软件检测到没有活动，会自动清零计时（config中"leave_restart"）

**运行方式**：解压release 中的breakTimer.zip文件后，运行其中的breakTimer.exe文件

**都看到这了，给个小星星吧~**

---
## 时间参数

黑白名单都支持自定义开启时间，有如下几种模式：
 1. 天循环
   ```
    'time':{
        'mode': 'day',
        'interval': '8:30-10:30'
    }
   ```
 2. 周循环
    ```
    'time':{
        'mode': 'week',
        'value': [1, 2, 4],
        'interval': '8:30-10:30'
    }
    ```
 3. 时段
    ```
    'time':{
        'mode': 'period',
        'interval': '2024.2.20 8:30-2024.2.26 8:30'
    }
    ```
 4. 总是开启
    ```
    'time':{
        'mode': 'always',
    }
    ```

5. 点击开始自律按钮开启（目前仅限于应用的黑名单）
    ```
   'time':{
        'mode': 'click',
    }
    ```


---
## config.json 文件中配置选项
```
 "smallTime": 6  小休时间
 
 "bigTime": 12, 大休时间
 
 "studyTime": 40, 学习时间
 
 "smallNum": 3, 学习次数
 
 "isLoop": 1, 是否循环
 
 "liver": "22:30", 锁机开始时间
 
 "liver_to": "6:00" 锁机结束时间
 
 "force": 1, 是否开启强制模式，该模式下全屏显示
 
 "width": "450", 页面宽度
 
 "length": "450", 页面长度
 
 "is_music": 0, 是否开启提示音乐
 
 "auto_start": 1, 打开应用自动开始计时
 
 "fast_start": 1, 开机后是否要等待一会启动
  
 "split_screen": 1, 是否开启多个屏幕锁定
   
 "mouse lock": 1, 是否开启鼠标锁定
 
 "auto_boot": 1, 是否自启动,

 "break_now_time": 20, 强制休息时间，单位分钟

 "block_keyboard": 1,  是否开启键盘锁定

 "full_screen": 1, 是否全屏显示

 "topmost": 1, 是否置于最上层应用提醒
        
 "lock_screen_when_start_rest": 1 是否开启电脑默认锁屏

 "leave_restart": 1,离开检测

 "pause_current_app_when_break": 1, 休息模式自动关闭当前播放

 "delay_break": 1, 延迟休息

 "check_window_position": 1, 是否检查屏幕位置，如果不对自动矫正
    
 #黑名单：
    "black_lists": [
      {
         "name": "study", #名字
          # 禁用列表
         "list": [
            "msedge.exe",
            "steam.exe",
            "chrome.exe"
         ],
         "enable": 1, # 是否开启
         'time':{
             'mode': 'click',
          }
      }
   ],

  # 阻止网页，需要安装mitmproxy的证书
   "block_website": {
      "enable": 1, # 是否开启
      "proxy_rules_location": "C:\\Users\\chao/config/clash/profiles", #clash代理文件的位置
      "websites": [
         {
            "name": "zhihu.com", # 网站名
            "time": {
               "mode": "day", # 每天
               "interval": "16:00-16:38" # 时段
            }
         }
      ]
   },
    
   # 白名单
  "white_sheet": [
    "time": {
       "mode": "week", # 每周
       "interval": "6:00-12:00" # 时段
        value:[3, 4] 每周三和每周四
    }
   ], 
```
   
