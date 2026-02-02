# 文档完整度评分说明

## 概述

每个 API 文档在保存时会自动评估完整度，并在文件名中添加评分（0-6分）。

**评分标准：** 文档包含的必选信息数量

## 必选项（共6项）

| # | 必选项 | 字段名 | 说明 | 示例 |
|---|--------|--------|------|------|
| 1 | **请求方法** | `method` | HTTP 方法 | GET, POST, PUT, DELETE |
| 2 | **接口地址** | `api_url` | API URL | `https://qyapi.weixin.qq.com/cgi-bin/xxx` |
| 3 | **请求参数** | `request_params` | Query/Body 参数 | `corpid`, `limit` 等 |
| 4 | **请求示例** | `request_examples` | 请求代码示例 | JSON/XML 请求体 |
| 5 | **响应参数** | `response_params` | 返回字段说明 | `errcode`, `errmsg` 等 |
| 6 | **响应示例** | `response_examples` | 响应代码示例 | JSON/XML 返回数据 |

## 评分规则

**计算公式：**
```
评分 = 包含的必选项数量
范围：0-6 分
```

**评分等级：**
- 🟢 **6分** - 完整（包含所有6项）
- 🟡 **5分** - 较完整（缺1项）
- 🟡 **4分** - 较完整（缺2项）
- 🔴 **3分** - 不完整（缺3项）
- 🔴 **2分** - 不完整（缺4项）
- 🔴 **1分** - 不完整（缺5项）
- 🔴 **0分** - 极不完整（6项都没有）

## 文件命名

**格式：** `{id}-{score}.md`

**示例：**
```
95647-6.md  - 完整度 6/6 🟢
90335-5.md  - 完整度 5/6 🟡
90332-4.md  - 完整度 4/6 🟡
91144-3.md  - 完整度 3/6 🔴
90568-2.md  - 完整度 2/6 🔴
```

## 实际示例

### 示例 1：完整文档（6分）🟢

**文件：** `95647-6.md`

**包含项：**
- ✅ 请求方法：`POST`
- ✅ 接口地址：`https://qyapi.weixin.qq.com/cgi-bin/license/list_order`
- ✅ 请求参数：6个（corpid, start_time, end_time, cursor, limit 等）
- ✅ 请求示例：
  ```json
  {
    "corpid":"xxxxx",
    "start_time":1500000000,
    ...
  }
  ```
- ✅ 响应参数：7个（errcode, errmsg, order_list 等）
- ✅ 响应示例：
  ```json
  {
    "errcode": 0,
    "errmsg": "ok",
    ...
  }
  ```

**评分：6/6** ✅

### 示例 2：较完整文档（5分）🟡

**文件：** `90335-5.md`

**包含项：**
- ✅ 请求方法：`GET`
- ✅ 接口地址：`https://qyapi.weixin.qq.com/cgi-bin/corp/get`
- ✅ 请求参数：2个
- ❌ 请求示例：无
- ✅ 响应参数：5个
- ✅ 响应示例：有

**评分：5/6** （缺少请求示例）

### 示例 3：不完整文档（3分）🔴

**文件：** `90332-3.md`

**包含项：**
- ❌ 请求方法：无
- ❌ 接口地址：无
- ✅ 请求参数：有
- ✅ 请求示例：有
- ✅ 响应参数：有
- ❌ 响应示例：无

**评分：3/6** （缺少3项）

## 索引文件展示

**README.md 格式：**

```markdown
# 企业微信 API 文档索引

生成时间: 2024-12-10 16:30:00

共 164 个 API 接口

## 完整度统计

- 🟢 完整（6分）: 45 个
- 🟡 较完整（4-5分）: 78 个
- 🔴 不完整（0-3分）: 41 个

## 说明

文件名格式：`{id}-{score}.md`，其中 score 表示完整度（0-6分）

**必选项（共6项）：**
1. 请求方法 (GET/POST/PUT/DELETE)
2. 接口地址 (API URL)
3. 请求参数 (Query/Body 参数)
4. 请求示例 (JSON/XML 示例)
5. 响应参数 (返回字段说明)
6. 响应示例 (返回数据示例)

## API 列表

- 🟢 `POST` [获取订单列表](95647-6.md) `[6/6]` - 服务商查询...
- 🟢 `GET` [获取企业信息](90194-6.md) `[6/6]` - 获取企业基本...
- 🟡 `POST` [创建成员](90195-5.md) `[5/6]` - 创建企业成员
- 🔴 [授权通知](100964-3.md) `[3/6]` - 授权相关事件
```

## 使用场景

### 1. 快速找到完整文档

```bash
# 列出所有完整文档
ls ../api_docs/*-6.md

# 统计完整文档数量
ls ../api_docs/*-6.md | wc -l
```

### 2. 找到需要完善的文档

```bash
# 找出低分文档（需要完善）
ls ../api_docs/*-[0-3].md

# 找出缺少示例的文档（可能是4-5分）
ls ../api_docs/*-[45].md
```

### 3. 程序化处理

```python
from pathlib import Path
import re

docs_dir = Path('../api_docs')

# 按完整度分组
by_score = {i: [] for i in range(7)}

for md_file in docs_dir.glob('*-[0-6].md'):
    # 从文件名提取评分
    match = re.search(r'-(\d)\.md$', md_file.name)
    if match:
        score = int(match.group(1))
        by_score[score].append(md_file)

# 显示统计
for score, files in by_score.items():
    print(f"{score}分: {len(files)} 个文档")

# 优先处理完整文档
for doc in by_score[6]:
    print(f"完整文档: {doc.name}")
```

### 4. 生成质量报告

```python
import json

# 统计
total = sum(len(files) for files in by_score.values())
complete = len(by_score[6])
good = len(by_score[5]) + len(by_score[4])
poor = sum(len(by_score[i]) for i in range(4))

report = {
    'total': total,
    'complete': complete,
    'complete_rate': f"{complete/total*100:.1f}%",
    'good': good,
    'poor': poor
}

print(json.dumps(report, indent=2))
```

## 评分代码

```python
def _calculate_completeness_score(self, doc: APIDoc) -> int:
    """
    计算文档完整度分数（0-6分）
    """
    score = 0
    
    # 1. 请求方法
    if doc.method:
        score += 1
    
    # 2. 接口地址
    if doc.api_url:
        score += 1
    
    # 3. 请求参数（任意一种即可）
    if doc.request_params or doc.query_params or doc.body_params:
        score += 1
    
    # 4. 请求示例
    if doc.request_examples:
        score += 1
    
    # 5. 响应参数
    if doc.response_params:
        score += 1
    
    # 6. 响应示例
    if doc.response_examples:
        score += 1
    
    return score
```

## 常见问题

### Q: 为什么我的文档是5分而不是6分？

**A:** 检查6个必选项，看缺少哪一项：

```bash
# 打开文档查看
cat ../api_docs/xxxxx-5.md

# 检查各部分是否存在：
# 1. ## 基本信息 - 请求方法: `POST`
# 2. ## 基本信息 - 接口地址: `https://...`
# 3. ## 请求信息 - 请求参数表格
# 4. ## 请求信息 - 请求示例代码块
# 5. ## 响应信息 - 响应参数表格
# 6. ## 响应信息 - 响应示例代码块
```

### Q: 如何提高文档完整度？

**A:** 

1. **检查原始页面** - 可能原始文档就不完整
2. **改进提取逻辑** - 提交 PR 改进爬虫的提取算法
3. **手动补充** - 根据实际 API 调用补充缺失信息

### Q: 评分会影响文档内容吗？

**A:** 不会。评分只是一个质量指标，不改变文档内容本身。

### Q: 可以自定义评分标准吗？

**A:** 可以。修改 `_calculate_completeness_score` 方法即可。

## 最佳实践

1. **优先使用高分文档** - 6分文档信息最完整
2. **定期检查低分文档** - 看是否可以改进提取逻辑
3. **追踪质量趋势** - 记录每次爬取的完整度统计
4. **手动补充关键文档** - 对于常用但评分低的 API，手动补充

## 总结

完整度评分功能让你：

- ✅ **一眼识别** - 文件名就知道文档质量
- ✅ **快速筛选** - 轻松找到完整文档
- ✅ **质量管理** - 了解文档库整体质量
- ✅ **优化指导** - 知道哪些文档需要改进

从文件名 `95647-6.md` 就能知道这是一个完整的、高质量的 API 文档！🎯
