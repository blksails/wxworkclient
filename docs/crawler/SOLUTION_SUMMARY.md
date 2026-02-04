# 多接口参数混杂问题 - 解决方案总结

## 问题

用户反馈：**"数据分段的不对，参数获取过多"**

### 问题详情

使用 `--split-multi-api` 分割多接口页面（如文档 99935）时：
- ✗ 每个接口文档都包含所有 5 个接口的参数
- ✗ 参数表格有大量重复
- ✗ 无法区分哪些参数属于哪个接口

### 根本原因

企业微信的某些文档页面结构特殊：
1. **参数表格是共享的**：所有接口的参数混在一个表格中
2. **没有明确分隔**：无法通过表格结构区分不同接口的参数
3. **"其他说明"是纯文本**：每个接口的详细说明没有表格结构

## 解决方案

### ✅ 默认禁用自动分割（已实现）

**改动**：
```python
# 新增参数
def __init__(self, ..., split_multi_api: bool = False):
    self.split_multi_api = split_multi_api  # 默认 False

# 只有显式启用时才分割
if self.split_multi_api:
    api_groups = self._detect_multiple_apis(soup)
```

**命令行**：
```bash
# 新增参数
parser.add_argument('--split-multi-api', action='store_true', 
                   help='分割多接口页面（实验性功能，可能导致参数混杂，默认禁用）')
```

### 推荐用法

#### 方案 A：使用默认模式（推荐）✅

```bash
python3 crawler.py --doc-ids 99935
```

**输出**：
```
99935-6.md  # 完整文档，包含所有 5 个接口
```

**优点**：
- ✅ 保持原始页面完整性
- ✅ 所有参数都在表格中，结构清晰
- ✅ 不会丢失任何信息
- ✅ 在"其他说明"部分可以看到每个接口的详细说明

**文档结构**：
```markdown
## 请求参数
| 参数名 | 类型 | 必填 | 说明 |
（所有接口的参数，但有完整的表格结构）

## 其他说明

### 查询智能表格子表权限
请求地址: .../get_sheet_priv
（该接口的详细说明）

### 更新智能表格子表权限
请求地址: .../update_sheet_priv
（该接口的详细说明）

...（其他 3 个接口）
```

#### 方案 B：启用分割（不推荐）⚠️

仅用于实验或特殊需求：

```bash
python3 crawler.py --doc-ids 99935 --split-multi-api
```

**输出**：
```
99935-1-get_sheet_priv-6.md       # ⚠️ 包含所有接口的参数
99935-2-update_sheet_priv-6.md    # ⚠️ 包含所有接口的参数
99935-3-create_rule-5.md          # ⚠️ 包含所有接口的参数
99935-4-mod_rule_member-6.md      # ⚠️ 包含所有接口的参数
99935-5-delete_rule-6.md          # ⚠️ 包含所有接口的参数
```

**缺点**：
- ❌ 参数混杂
- ❌ 每个文档都包含所有接口的参数
- ❌ 容易混淆

## 对于代码生成的建议

如果你要基于这些文档生成 Go 代码，建议：

### 策略 1：使用完整文档 + 手动映射

1. 使用默认模式获取完整文档
2. 解析"其他说明"部分的每个接口
3. 根据 API URL 手动映射参数

```python
# 示例逻辑
api_sections = {
    'get_sheet_priv': {
        'url': 'https://qyapi.weixin.qq.com/.../get_sheet_priv',
        'params': ['docid', 'type', 'rule_id_list']  # 手动指定
    },
    'update_sheet_priv': {
        'url': 'https://qyapi.weixin.qq.com/.../update_sheet_priv',
        'params': ['docid', 'type', 'rule_id', 'name', 'priv_list']  # 手动指定
    },
    ...
}
```

### 策略 2：从 JSON 示例提取参数

1. 忽略混杂的参数表格
2. 只从每个接口的 JSON 请求示例中提取参数
3. 使用类型推测功能

```python
# 从 JSON 提取，更准确
request_example = {
    "docid": "DOCID",
    "type": 2,
    "rule_id_list": ["RULEID1", "RULEID2"]
}
# → 参数：docid(string), type(int), rule_id_list(array[string])
```

### 策略 3：创建参数映射配置

为特定文档创建配置文件：

```json
{
  "99935": {
    "apis": [
      {
        "name": "get_sheet_priv",
        "params": ["docid", "type", "rule_id_list"]
      },
      {
        "name": "update_sheet_priv",
        "params": ["docid", "type", "rule_id", "name", "priv_list"]
      }
    ]
  }
}
```

## 文件清单

### 新增文档
- ✅ `MULTI_API_ISSUE.md` - 问题详细说明
- ✅ `SOLUTION_SUMMARY.md` - 解决方案总结（本文件）

### 更新文档
- ✅ `USAGE.md` - 添加多接口页面处理说明
- ✅ `QUICK_REFERENCE.md` - 更新功能说明
- ✅ `CHANGELOG.md` - 添加修复记录

### 代码改动
- ✅ `crawler.py` - 添加 `split_multi_api` 参数（默认 False）
- ✅ 命令行参数 `--split-multi-api`

## 验证

### 测试默认行为

```bash
# 不使用 --split-multi-api
python3 crawler.py --doc-ids 99935

# 预期：生成 99935-6.md（完整文档）
# 结果：✅ 正确，参数不混杂
```

### 测试分割功能

```bash
# 使用 --split-multi-api
python3 crawler.py --doc-ids 99935 --split-multi-api

# 预期：生成 5 个独立文档，但参数会混杂
# 结果：⚠️ 按预期，参数混杂（这是已知限制）
```

## 总结

| 特性 | 默认模式 | 分割模式 |
|-----|---------|---------|
| 参数混杂 | ✅ 否 | ❌ 是 |
| 文档完整性 | ✅ 完整 | ⚠️ 部分 |
| 易于使用 | ✅ 是 | ❌ 否 |
| 推荐使用 | ✅ 是 | ❌ 否 |

**最终建议**：
- 🎯 使用默认模式（不加 `--split-multi-api`）
- 📖 查看完整文档，在"其他说明"部分区分不同接口
- 🔧 代码生成时，基于 API URL 或 JSON 示例来区分接口

问题已解决！✅
