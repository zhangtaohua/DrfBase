# 1 app 功能说明
1 实现字典功能

# 2 app 实现要点
1、数据表采用自关联的方式
2、可以达到多级

# 3 app 使用方法

## 3.1 初始化数据
```
 python ./apps/dictionary/dbinit/seeder.py 
```


# 4 TODO
1、创建serializers 数据没有做较验，全部传空也能创建一条数据
2、可不可以修改出一个serializer 实现如下数据结构，就是不要是list，是dict版本的

```
{
  "gender": {
    "id": 1,
    "code": "gender",
    "label": "性别",
    "children": {
      "male": {
        "id": 2,
        "code": "mele",
        "label": "男",
      },
      "female": {
        "id": 3,
        "code": "female",
        "label": "女",
      }

    },
    ……
  }
}
```