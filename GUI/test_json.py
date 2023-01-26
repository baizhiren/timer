import json

path = "te.json"
# try:
#     with open(path, "r", encoding="utf-8") as f:
#         data = json.load(f)   # 加载我们的数据
#         print(data['a'])
# except:
#     print("error ")

data = {}
with open(path, "w", encoding="utf-8") as f:
    data["a"] = 1
    data["hello"] = "wolrd"
    json.dump(data, f, indent=3, ensure_ascii=False)
