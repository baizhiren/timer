# BreakTimer 休息定时器
学习模式：

![image](https://github.com/baizhiren/timer/assets/30487483/9b20752c-b536-4229-8df3-5f73006caeba)

休息模式：

![image](https://user-images.githubusercontent.com/30487483/214987725-7ce7976c-08e0-422f-ad97-0e9c3f9bb444.png)


1. 点击“开始自律”，程序会按照 学习 小休 学习 小休 .... 学习 大休 运行（更加灵活的番茄钟），可以根据自己的需求自定义时间

休息模式会全屏显示，无法更改时间，如果此时为强制模式，会同时全屏显示并置于最上层，非常适合沉迷代码\久坐人士

该模式下可以启动黑名单来关掉一些让人分心的应用（参考config参数中的黑名单配置）

2. 点击立刻休息，会立即进入休息阶段，可在config中配置break_now_time时间长度

3. 点击重置按钮：会重新开始计时

4. “永无止境的x月”按钮： 启动循环模式， 当大休阶段结束后，会继续开始学习模式，进入下一个循环

5. “肝数”统计：会统计学习阶段的次数


**运行方式**：解压release 中的breakTimer.zip文件后，运行其中的breakTimer.exe文件

更新
---
1. 增加无线循环功能和轮数统计
2. 新增护肝时间：到晚上十点半强制进入休息模式
3. 新增鼠标锁定
4. 新增多屏幕锁定功能
5. 新增学习模式黑名单
---

config 参数
---
可以在config.json 文件中修改配置
```
 "smallTime": 6 （小休时间
 
 "bigTime": 12, （大休时间
 
 "studyTime": 40, （学习时间
 
 "smallNum": 3, （学习次数
 
 "isLoop": 1, （是否循环
 
 "liver": "22:30",（锁机开始时间
 
 "liver_to": "6:00" (锁机结束时间
 
 "force": 1,（是否开启强制模式，该模式下全屏显示
 
 "width": "450",（页面宽度
 
 "length": "450",（页面长度
 
 "is_music": 0,（是否开启提示音乐
 
 "auto_start": 1,（打开应用自动开始计时
 
 "fast_start": 1,（开机后是否要等待一会启动
  
 "split_screen": 1,(是否开启多个屏幕锁定
   
 "mouse lock": 1,（是否开启鼠标锁定
 
 "auto_boot": 1, (是否自启动),

 "break_now_time": 20,(强制休息时间，单位分钟)

  
  "black_list_open": 1（是否开启黑名单）
  
  "mode": "study",
  
  "black_lists": {
      "study": [
         "msedge.exe",
      ]
   },
   
   可以自定义学习模式的黑名单， 可以通过修改mode来切换黑名单，这里新建了一个名为"study"的mode,
   
   在其中禁止了edge浏览器，让我们专心学习（
   
   注意黑名单只有在点击了确认修改按钮后才会开启，并在大休阶段结束后关闭
   
   下一次开启黑名单需要重新点击确认修改按钮
   
   如果想要让黑名单在学习阶段持续生效，可以在黑名单最后一项加上"always"，如

   "study": [
         "msedge.exe","always"
     ],

  "block_keyboard": 1,  是否开启键盘锁定
   
  "full_screen": 1, 是否全屏显示
            
  "lock_screen_when_start_rest": 1 是否开启电脑默认锁屏    

```
   
   
   
   
   
   
   








