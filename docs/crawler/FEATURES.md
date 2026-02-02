# 新功能说明

## ✨ 实时保存功能

### 工作原理

爬虫现在会在提取每个 API 文档后立即保存，而不是等所有内容爬取完成后再保存。

```python
# 旧的方式（之前）
爬取所有接口 → 一次性保存所有文件

# 新的方式（现在）
爬取接口1 → 立即保存文件1 → 更新索引
爬取接口2 → 立即保存文件2 → 更新索引
爬取接口3 → 立即保存文件3 → 更新索引
...
```

### 优势

✅ **实时查看进度**
- 可以随时打开 `api_docs/README.md` 查看已爬取的接口
- 每个 Markdown 文件立即可读

✅ **容错能力强**
- 如果中途出错或中断，已爬取的内容都已保存
- 不会丢失任何已经提取的数据

✅ **更好的用户体验**
- 看到实时进度反馈
- 不用等待全部完成才能查看结果

## 🔄 断点续爬功能

### 工作原理

爬虫会记录所有访问过的 URL，重新运行时自动跳过已访问的页面。

```python
# 第一次运行
python3 crawler.py
# 爬取了 URL1, URL2, URL3...
# 保存访问记录到 .visited_urls.json

# 中断后重新运行
python3 crawler.py
# 自动加载访问记录
# 跳过 URL1, URL2, URL3...
# 继续爬取新的 URL
```

### 使用方式

```bash
# 默认启用断点续爬（推荐）
python3 crawler.py

# 从头开始爬取（清除之前的进度）
python3 crawler.py --no-resume
```

### 状态文件

爬虫会在输出目录创建 `.visited_urls.json` 文件：

```json
{
  "visited": [
    "https://developer.work.weixin.qq.com/document/path/91201",
    "https://developer.work.weixin.qq.com/document/path/91202",
    ...
  ],
  "timestamp": "2024-12-10 15:30:45"
}
```

### 优势

✅ **节省时间**
- 中断后不需要重新爬取已有的内容
- 对于大规模爬取特别有用

✅ **网络友好**
- 避免重复请求同一个 URL
- 降低对服务器的压力

✅ **灵活控制**
- 可以选择继续之前的进度
- 也可以选择从头开始

## 📊 实时索引更新

### 工作原理

每爬取一个接口，立即更新 `README.md` 索引文件。

### 索引格式

```markdown
# 企业微信 API 文档索引

生成时间: 2024-12-10 15:30:45

共 10 个 API 接口

## API 列表

- `POST` [获取access_token](91201.md) - 获取访问令牌
- `GET` [获取企业信息](91202.md) - 获取企业基本信息
...
```

### 优势

✅ **实时进度**
- 打开索引文件即可看到当前进度
- 不需要等待全部完成

✅ **方便查看**
- 按照 HTTP 方法标注（GET/POST）
- 按 path 排序，便于查找

## 🎯 使用示例

### 示例 1：基本使用

```python
from crawler import WeChatWorkAPICrawler

crawler = WeChatWorkAPICrawler(
    base_url="https://developer.work.weixin.qq.com",
    start_path="/document/path/91201",
    output_dir="../api_docs",
    resume=True  # 启用断点续爬（默认）
)

crawler.crawl()
```

### 示例 2：监控进度

在爬取过程中，可以在另一个终端窗口查看进度：

```bash
# 终端 1: 运行爬虫
python3 crawler.py

# 终端 2: 实时查看进度
watch -n 1 'cat ../api_docs/README.md | head -20'

# 或查看文件数量
watch -n 1 'ls -l ../api_docs/*.md | wc -l'
```

### 示例 3：中断和恢复

```bash
# 开始爬取
python3 crawler.py
# ... 爬取了一些内容
# 按 Ctrl+C 中断

# 稍后继续（自动跳过已爬取的）
python3 crawler.py

# 或者从头开始
python3 crawler.py --no-resume
```

## 🔍 文件结构

爬取过程中会生成以下文件：

```
api_docs/
├── README.md              # 索引文件（实时更新）
├── 91201.md              # API 文档（立即保存）
├── 91202.md              # API 文档（立即保存）
├── ...
├── .visited_urls.json    # 访问记录（用于断点续爬）
└── api_docs.json         # 完整数据（最后生成）
```

## 💡 最佳实践

1. **长时间爬取**
   - 使用断点续爬（默认启用）
   - 可以随时中断，不会丢失进度

2. **监控进度**
   - 打开 `api_docs/README.md` 查看实时进度
   - 或使用 `watch` 命令监控

3. **失败重试**
   - 如果某个页面失败，重新运行即可
   - 已成功的页面会自动跳过

4. **清理重爬**
   - 如果想从头开始，删除 `.visited_urls.json`
   - 或使用 `--no-resume` 参数

## 🆚 对比

### 之前的方式

```
优点：
- 实现简单

缺点：
- 中断会丢失所有数据
- 无法查看进度
- 失败需要全部重来
```

### 现在的方式

```
优点：
✅ 实时保存，不怕中断
✅ 可查看实时进度
✅ 支持断点续爬
✅ 失败重试高效
✅ 用户体验好

缺点：
- 无（稍微增加了少量 I/O 操作，但完全值得）
```

## 🚀 性能影响

实时保存对性能的影响微乎其微：

- **磁盘写入**：每个文件写入约 1-10KB，非常快
- **网络请求**：仍然有 2 秒延迟，是主要瓶颈
- **总体影响**：< 1% 的额外时间

收益远大于成本！
