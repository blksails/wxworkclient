# Crawler 更新日志

## 2026-02-03 v2 - 重要修复

### 问题修复

#### 多接口页面参数混杂问题 🔧
**问题**：某些文档页面（如 99935）包含多个接口，但参数表格是混杂的，自动分割导致每个接口都包含所有接口的参数。

**解决方案**：
- ✅ **默认禁用**多接口自动分割
- ✅ 新增 `--split-multi-api` 参数（实验性）
- ✅ 保持文档完整性，避免参数混杂

**使用建议**：
```bash
# 推荐：默认行为，保持完整文档
python3 crawler.py --doc-ids 99935

# 不推荐：启用分割（会导致参数混杂）
python3 crawler.py --doc-ids 99935 --split-multi-api
```

详细说明：[MULTI_API_ISSUE.md](./MULTI_API_ISSUE.md)

## 2026-02-03 v1 - 重大更新

### 新增功能

#### 1. 多接口识别和分组 ✨
- 自动识别一个页面中包含多个 API 接口的情况
- 检测模式：`请求方式：POST（HTTPS）请求地址: https://...`
- 为每个接口生成独立的 Markdown 文档
- 文件命名：`{doc_id}-{index}-{api_name}-{score}.md`
  - 例如：`99935-1-get_sheet_priv-6.md`

**实现细节**：
- 新增 `_detect_multiple_apis()` 方法识别多个接口
- 新增 `_extract_api_name_from_url()` 从 URL 提取 API 名称
- 新增 `_save_single_markdown_grouped()` 保存分组文档
- 新增 `_generate_markdown_grouped()` 生成分组 Markdown

**数据结构更新**：
- `APIDoc` 新增字段：
  - `api_name`: API 名称（如 `get_sheet_priv`）
  - `group_title`: 分组标题

#### 2. 指定文档 ID 爬取 🎯
- 支持命令行参数 `--doc-ids` 指定要爬取的文档
- 可以逗号分隔多个文档 ID
- 在指定模式下，不会爬取其他链接

**使用示例**：
```bash
# 爬取单个文档
python3 crawler.py --doc-ids 99935

# 爬取多个文档
python3 crawler.py --doc-ids 99935,90601,90350
```

#### 3. Query 参数提取 🔍
- 从请求地址中自动提取 Query 参数
- 示例：`?access_token=TOKEN` → 提取 `access_token` 参数
- 智能推测参数类型：
  - `token/key/secret` → `string`
  - `*id` → `string`
  - `limit/offset/page` → `int`
  - 纯数字 → `int`
  - `true/false` → `bool`

**实现方法**：
- 新增 `_extract_query_params_from_url()` 提取 Query 参数
- 新增 `_infer_query_param_type()` 推测参数类型

#### 4. JSON 参数类型推测 🤖
- 从"请求包体：json"中提取参数并推测类型
- 支持嵌套对象和数组
- 自动推测基本类型：`int`、`string`、`bool`、`float`、`array`、`object`

**实现方法**：
- 新增 `_extract_params_from_json_examples()` 从 JSON 提取参数
- 新增 `_infer_json_params()` 递归推测参数类型
- 新增 `_infer_type()` 推测值类型

#### 5. 智能参数合并 🔄
- 表格参数与 JSON 参数自动合并
- Query 参数与表格参数自动合并
- 表格中的信息优先级更高
- 避免参数重复

**合并策略**：
1. JSON 推测的类型 → 表格中缺失类型时使用
2. Query 参数从 URL 提取 → 表格中找到同名参数时更新
3. JSON 中独有的参数 → 自动添加并标注"(从请求示例中推测)"

### 改进功能

#### 命令行参数支持
- 使用 `argparse` 代替简单的参数检查
- 新增 `--output-dir` 指定输出目录
- 改进帮助信息

```bash
python3 crawler.py --help
```

#### JSON 导出改进
- 包含新增的 `api_name` 和 `group_title` 字段
- 更完整的参数信息

### 技术改进

#### 代码结构
- 更清晰的方法职责划分
- 支持多接口页面的模块化处理
- 改进的错误处理

#### 类型推测
- 支持嵌套对象：`user.name`、`user.profile.age`
- 支持数组类型：`array[int]`、`array[object]`
- 支持复杂类型：`object`

### 向后兼容
- 所有现有功能保持不变
- 单接口页面的处理逻辑保持兼容
- 输出格式向后兼容（单接口文档格式不变）

### 文档
- 新增 `USAGE.md` - 完整使用指南
- 新增 `CHANGELOG.md` - 更新日志

## 使用示例

### 示例 1：爬取包含多个接口的文档
```bash
python3 crawler.py --doc-ids 99935
```

**输出**：
```
99935-1-get_sheet_priv-6.md       # 查询智能表格子表权限
99935-2-update_sheet_priv-6.md    # 更新智能表格子表权限
99935-3-create_rule-5.md          # 新增智能表格指定成员额外权限
99935-4-mod_rule_member-6.md      # 更新智能表格指定成员额外权限
99935-5-delete_rule-6.md          # 删除智能表格指定成员额外权限
```

### 示例 2：批量爬取指定文档
```bash
python3 crawler.py --doc-ids 99935,93798,90195,90350,100776
```

### 示例 3：重新爬取文档
```bash
python3 crawler.py --doc-ids 99935 --no-resume
```

## 已知问题

1. **多接口内容分割**：目前多个接口共享整个页面内容，未来可以改进为精确分割每个接口的内容区域
2. **接口标题识别**：对于某些特殊格式的页面，接口标题可能识别不准确

## 未来计划

- [ ] 精确分割多接口页面的内容区域
- [ ] 改进接口标题识别算法
- [ ] 支持更多参数类型推测规则
- [ ] 添加参数验证功能
- [ ] 生成 OpenAPI/Swagger 格式
