# 使用指南

## 快速开始

```bash
# 1. 进入目录
cd docs/crawler

# 2. 激活虚拟环境
source activate.sh

# 3. 运行爬虫
python3 crawler.py
```

## 命令选项

```bash
# 默认模式：启用断点续爬
python3 crawler.py

# 从头开始：忽略之前的进度
python3 crawler.py --no-resume

# 运行演示（爬取少量数据）
python3 demo.py

# 运行测试
python3 test_crawler.py

# 查看示例
python3 example.py
```

## 实时查看进度

### 方法 1：查看索引文件

```bash
# 在另一个终端窗口
cat ../api_docs/README.md

# 或实时监控
watch -n 2 'cat ../api_docs/README.md | head -30'
```

### 方法 2：统计文件数量

```bash
# 查看已生成的 Markdown 文件数量
ls ../api_docs/*.md 2>/dev/null | wc -l

# 实时监控
watch -n 2 'ls ../api_docs/*.md 2>/dev/null | wc -l'
```

### 方法 3：查看访问记录

```bash
# 查看已访问的 URL 数量
cat ../api_docs/.visited_urls.json | grep '"https:' | wc -l
```

## 输出文件说明

### 实时生成的文件

```
api_docs/
├── README.md           # API 索引（实时更新）
│                      # 每爬取一个接口就更新
│
├── 91201.md           # 单个 API 文档（立即保存）
├── 91202.md           # 每提取一个就保存一个
├── ...
│
└── .visited_urls.json # 访问记录（实时更新）
                       # 用于断点续爬
```

### 最后生成的文件

```
api_docs/
└── api_docs.json      # 完整的 JSON 数据
                       # 在爬取完成后生成
```

## 中断和恢复

### 正常中断

按 `Ctrl+C` 中断爬虫：

```
正在爬取: https://...
  ✓ 提取文档: 获取access_token
    → 已保存: 91201.md
^C

已爬取 5 个 API 文档
所有已提取的文档都已保存 ✓
```

### 继续爬取

重新运行命令即可继续：

```bash
python3 crawler.py
```

输出会显示：

```
断点续爬模式: 已跳过 15 个已访问的页面
```

## 自定义配置

### 在代码中配置

编辑 `crawler.py` 的 `main()` 函数：

```python
def main():
    BASE_URL = "https://developer.work.weixin.qq.com"
    START_PATH = "/document/path/91201"  # 修改起始页面
    OUTPUT_DIR = "../api_docs"            # 修改输出目录
    
    crawler = WeChatWorkAPICrawler(BASE_URL, START_PATH, OUTPUT_DIR)
    crawler.crawl()
```

### 使用 Python 脚本

创建自己的脚本：

```python
from crawler import WeChatWorkAPICrawler

crawler = WeChatWorkAPICrawler(
    base_url="https://developer.work.weixin.qq.com",
    start_path="/document/path/90194",  # 通讯录管理
    output_dir="../api_docs_contacts",
    resume=True
)

crawler.crawl()
```

## 常见场景

### 场景 1：首次完整爬取

```bash
cd docs/crawler
source activate.sh
python3 crawler.py
```

等待爬取完成，所有文档会保存在 `../api_docs/`

### 场景 2：爬取过程被中断

爬取时网络断开或手动中断：

```bash
# 重新运行即可，会自动跳过已爬取的
python3 crawler.py
```

### 场景 3：想重新爬取所有内容

```bash
# 方法 1：删除访问记录
rm ../api_docs/.visited_urls.json
python3 crawler.py

# 方法 2：使用 --no-resume 参数
python3 crawler.py --no-resume

# 方法 3：使用新的输出目录
# 修改 OUTPUT_DIR 为新目录
```

### 场景 4：只爬取特定章节

```python
# 创建 my_crawler.py
from crawler import WeChatWorkAPICrawler

# 只爬取通讯录管理 API
crawler = WeChatWorkAPICrawler(
    base_url="https://developer.work.weixin.qq.com",
    start_path="/document/path/91201",
    output_dir="../api_docs_contacts",
    resume=True
)

crawler.crawl()
```

### 场景 5：批量爬取多个章节

使用 `example.py` 中的 `example_multiple_sections()` 函数。

## 故障排除

### 问题：虚拟环境未激活

```bash
# 解决方法
source venv/bin/activate
# 或
source activate.sh
```

### 问题：缺少依赖包

```bash
# 解决方法
pip install -r requirements.txt
```

### 问题：网络超时

爬虫会自动跳过失败的页面，重新运行即可重试。

### 问题：权限错误

```bash
# 确保脚本有执行权限
chmod +x run.sh activate.sh demo.py
```

### 问题：输出目录权限不足

```bash
# 检查并修改输出目录权限
ls -ld ../api_docs/
chmod 755 ../api_docs/
```

## 性能优化

### 当前设置

- 请求间隔：2 秒（避免给服务器压力）
- 超时时间：30 秒
- 实时保存：每个文件立即保存

### 如果想加快速度

编辑 `crawler.py`，修改延迟时间：

```python
def _crawl_page(self, url: str):
    # ...
    time.sleep(2)  # 修改这个值（不建议小于 1 秒）
```

⚠️ **注意**：降低延迟可能导致被服务器限制，请谨慎修改。

## 进阶使用

### 与其他工具集成

```bash
# 爬取完成后转换为 PDF
for md in ../api_docs/*.md; do
    pandoc "$md" -o "${md%.md}.pdf"
done

# 上传到文档系统
rsync -av ../api_docs/ user@server:/docs/wxwork/
```

### 定时爬取

```bash
# 添加到 crontab（每天凌晨 2 点更新）
0 2 * * * cd /path/to/docs/crawler && source venv/bin/activate && python3 crawler.py
```

## 帮助和支持

- 查看完整文档：`../README.md`
- 查看新功能说明：`FEATURES.md`
- 快速开始指南：`QUICKSTART.md`
- 运行测试：`python3 test_crawler.py`
