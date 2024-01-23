# timer 休息定时器

![image](https://user-images.githubusercontent.com/30487483/214989507-abcffbc9-8187-42af-980a-d4dfaf152e0f.png)

![image](https://user-images.githubusercontent.com/30487483/214987725-7ce7976c-08e0-422f-ad97-0e9c3f9bb444.png)


程序会按照 学习 小休 学习 小休 .... 学习 大休 运行（类似番茄钟），可以根据自己的需求自定义时间

休息模式会全屏显示，此时无法更改时间，同时全屏显示，非常适合沉迷代码\久坐人士

**运行方式**：breakTimer.ext **请使用管理员身份运行**


更新
---
1. 增加无线循环功能和轮数统计
2. 新增护肝时间：到晚上十点半强制进入休息模式
3. 新增鼠标锁定
---

config 参数
---
可以在config.json 文件中修改配置

 "smallTime": 6 （小休时间
 
 "bigTime": 12, （大休时间
 
 "studyTime": 40, （学习时间
 
 "smallNum": 3, （学习次数
 
 "isLoop": 1, （是否循环
 
 "liver": "22:30",（锁机开始时间
 
 "liver_to": "6:00" (锁机结束时间
 
 "force": 1,（强制模式，该模式下休息时间会锁定鼠标，并全屏显式
 
 "width": "450",（页面宽度
 
 "length": "450",（页面长度
 
 "is_music": 0,（提示音乐
 
 "auto_start": 1,（自当开始
 
 "fast_start": 1,（快速启动








