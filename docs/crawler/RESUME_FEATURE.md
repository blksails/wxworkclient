# 断点续传功能详解

## 概述

爬虫支持可靠的断点续传功能，中断后可以无缝继续爬取，不会丢失任何未爬取的页面。

## 核心设计

### 架构：BFS + 队列

**为什么不用 DFS（深度优先搜索）？**

DFS 的问题：
```
起始URL (已访问)
  └─ 递归爬取子页面
     └─ 中断后，无法从起始URL继续
        └─ 起始URL在visited中，直接return
           └─ 无法发现其他页面
```

**BFS + 队列的优势：**

```
队列 = [URL1, URL2, URL3, ...]
  ├─ 取出 URL1 → 爬取 → 发现新URL → 加入队列
  ├─ 取出 URL2 → 爬取 → 发现新URL → 加入队列
  ├─ 中断！保存队列
  └─ 重启 → 加载队列 → 继续从URL3爬取
```

### 关键组件

| 组件 | 作用 | 持久化文件 |
|------|------|-----------|
| **visited** | 已访问的URL集合 | `.visited_urls.json` |
| **queue** | 待爬取的URL列表 | `.crawl_queue.json` |
| **need_rescan** | 重新扫描模式标志 | 无（运行时状态） |

## 工作流程

### 场景1：首次运行

```
1. visited = {}
2. queue = []
3. 初始化：queue = [起始URL]
4. 开始爬取：
   - 从queue取出起始URL
   - 爬取页面，提取文档
   - 扫描链接，发现URL_A, URL_B, URL_C
   - queue = [URL_A, URL_B, URL_C]
   - visited = {起始URL}
5. 继续从queue取出URL_A...
6. 定期保存 visited 和 queue
```

### 场景2：中断后重启（队列不为空）

```
1. 加载 visited = {已访问的URLs}
2. 加载 queue = [未爬取的URLs]
3. 显示：断点续爬模式: 已访问 150 个页面，队列中还有 243 个待爬取
4. 继续从 queue 取出URL爬取
5. 无缝恢复，不会重复爬取
```

### 场景3：中断后重启（队列为空）

```
1. 加载 visited = {已访问的URLs}
2. 加载 queue = []  （空！）
3. 检测到：队列为空但有已访问页面
4. 进入重新扫描模式：need_rescan = True
5. 添加起始URL到队列（用于重新扫描）
6. 爬取起始URL：
   - 检测到 already_visited = True
   - 但 need_rescan = True，继续处理
   - 跳过内容提取（不重复）
   - 扫描链接，发现遗漏的URLs
   - 发现542个新链接！
   - 关闭重新扫描模式
7. 继续正常爬取新发现的URLs
```

## 代码实现

### 初始化

```python
def __init__(self, ..., resume: bool = True):
    self.visited = set()
    self.queue = []
    self.need_rescan = False
    
    if resume:
        self._load_visited_urls()  # 加载已访问
        self._load_queue()         # 加载队列
    
    # 如果队列为空
    if not self.queue:
        if self.visited and resume:
            # 有已访问页面，需要重新扫描
            print("队列为空但有已访问页面，将重新扫描...")
            self.need_rescan = True
        self.queue.append(self.start_url)
```

### 爬取循环

```python
def crawl(self):
    while self.queue:
        url = self.queue.pop(0)  # 从队列头部取出
        self._crawl_page(url)
        
        # 每10个页面保存一次
        if len(self.visited) % 10 == 0:
            self._save_queue()
    
    # 完成后保存
    self._save_visited_urls()
    self._save_queue()
```

### 页面爬取

```python
def _crawl_page(self, url):
    already_visited = url in self.visited
    
    # 如果已访问且不需要重新扫描，跳过
    if already_visited and not self.need_rescan:
        return
    
    if already_visited:
        print(f"重新扫描链接: {url}")
    else:
        self.visited.add(url)
        print(f"正在爬取: {url}")
    
    # 获取页面
    response = requests.get(url, ...)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取文档（仅新页面）
    if not already_visited:
        api_doc = self._extract_api_doc(soup, url)
        if api_doc:
            self._save_single_markdown(api_doc)
    
    # 扫描链接（无论是否已访问）
    new_links = 0
    for link in soup.find_all('a', href=True):
        full_url = urljoin(self.base_url, link['href'])
        if (full_url not in self.visited and 
            full_url not in self.queue):
            self.queue.append(full_url)
            new_links += 1
    
    if already_visited and new_links > 0:
        print(f"  ✓ 发现 {new_links} 个新链接")
        self.need_rescan = False  # 关闭重新扫描模式
```

## 状态文件

### .visited_urls.json

**作用：** 记录所有已访问的URL

**格式：**
```json
{
  "visited": [
    "https://developer.work.weixin.qq.com/document/path/91201",
    "https://developer.work.weixin.qq.com/document/path/90332",
    ...
  ],
  "timestamp": "2024-12-10 16:30:00"
}
```

### .crawl_queue.json

**作用：** 记录待爬取的URL队列

**格式：**
```json
{
  "queue": [
    "https://developer.work.weixin.qq.com/document/path/90335",
    "https://developer.work.weixin.qq.com/document/path/90336",
    ...
  ],
  "timestamp": "2024-12-10 16:30:00",
  "queue_size": 243
}
```

## 使用示例

### 正常爬取

```bash
$ python3 crawler.py

开始爬取企业微信 API 文档...
输出目录: ../api_docs

正在爬取: https://developer.work.weixin.qq.com/document/path/91201
  ✓ 提取文档: 获取 access_token
  → 已保存: 91201-6.md (完整度: 6/6)
...
```

### 中断（Ctrl+C）

```bash
^C
============================================================
⚠️  用户中断爬取
============================================================

正在保存当前进度...

✓ 进度已保存
  - 已爬取: 45 个 API 文档
  - 已访问: 78 个页面
  - 队列剩余: 165 个待爬取
  - 输出目录: ../api_docs

重新运行命令继续爬取：
  python3 crawler.py
============================================================
```

### 重启继续

```bash
$ python3 crawler.py

开始爬取企业微信 API 文档...
输出目录: ../api_docs
已加载 78 个已访问的 URL
已加载 165 个待爬取的 URL
断点续爬模式: 已访问 78 个页面，队列中还有 165 个待爬取

正在爬取: https://developer.work.weixin.qq.com/document/path/90337
  ✓ 提取文档: 更新成员
  → 已保存: 90337-6.md (完整度: 6/6)
...
```

### 队列为空重启

```bash
$ python3 crawler.py

开始爬取企业微信 API 文档...
输出目录: ../api_docs
已加载 282 个已访问的 URL
已加载 0 个待爬取的 URL
队列为空但有 282 个已访问页面
将重新扫描部分页面来发现未爬取的链接...

重新扫描链接: https://developer.work.weixin.qq.com/document/path/91201
  ✓ 发现 542 个新链接

正在爬取: https://developer.work.weixin.qq.com/document/path/93010
  ✓ 提取文档: 通讯录回调通知
  → 已保存: 93010-4.md (完整度: 4/6)
...
```

## 测试工具

### test_resume.py - 检查状态

```bash
$ python3 test_resume.py

============================================================
断点续传状态检查
============================================================
已访问 URL 数量: 282
待爬取队列大小: 543

队列前5个 URL:
  1. https://developer.work.weixin.qq.com/document/path/93010
  2. https://developer.work.weixin.qq.com/document/path/92694
  3. https://developer.work.weixin.qq.com/document/path/101134
  4. https://developer.work.weixin.qq.com/document/path/95195
  5. https://developer.work.weixin.qq.com/document/path/93332

============================================================

✓ 断点续传功能正常
  可以继续爬取剩余的 543 个 URL
```

### test_crawl_resume.py - 测试流程

```bash
$ python3 test_crawl_resume.py

测试爬取: https://developer.work.weixin.qq.com/document/path/91201

重新扫描链接: https://developer.work.weixin.qq.com/document/path/91201
  ✓ 发现 542 个新链接

爬取后状态:
  已访问: 282 个 URL
  队列: 543 个待爬取
  已提取文档: 0 个

✓ 测试完成！
```

## 常见问题

### Q1: 为什么重启后从起始URL开始？

**A:** 如果队列为空，爬虫会重新扫描起始URL来发现遗漏的链接。这不会重复提取文档，只是扫描链接。

### Q2: 会重复爬取已访问的页面吗？

**A:** 不会。`visited` 集合确保每个URL只被爬取一次。重新扫描模式只扫描链接，不提取内容。

### Q3: 队列文件丢失了怎么办？

**A:** 爬虫会自动重新扫描来重建队列，不会重新爬取已访问的页面。

### Q4: 可以手动清空队列重新开始吗？

**A:** 可以。删除两个状态文件：
```bash
rm ../api_docs/.visited_urls.json
rm ../api_docs/.crawl_queue.json
```

### Q5: 队列会占用很多内存吗？

**A:** 不会。队列只存储URL字符串，即使10000个URL也只有几MB。而且队列会定期保存到磁盘。

### Q6: 如何查看当前进度？

**A:** 运行 `python3 test_resume.py` 或查看状态文件：
```bash
# 查看已访问数量
cat ../api_docs/.visited_urls.json | jq '.visited | length'

# 查看队列大小
cat ../api_docs/.crawl_queue.json | jq '.queue_size'
```

## 高级配置

### 调整保存频率

默认每10个页面保存一次队列。修改 `crawl()` 方法：

```python
def crawl(self):
    while self.queue:
        url = self.queue.pop(0)
        self._crawl_page(url)
        
        # 改为每5个页面保存一次
        if len(self.visited) % 5 == 0:
            self._save_queue()
```

### 禁用断点续传

```python
crawler = WeChatWorkAPICrawler(
    base_url="https://developer.work.weixin.qq.com",
    start_path="/document/path/91201",
    output_dir="../api_docs",
    resume=False  # 禁用断点续传
)
```

### 从特定URL重新开始

```python
# 1. 清空状态文件
import os
os.remove('../api_docs/.visited_urls.json')
os.remove('../api_docs/.crawl_queue.json')

# 2. 修改起始URL
crawler = WeChatWorkAPICrawler(
    base_url="https://developer.work.weixin.qq.com",
    start_path="/document/path/90332",  # 新的起始URL
    output_dir="../api_docs",
    resume=False
)
```

## 最佳实践

1. **定期检查进度**
   ```bash
   python3 test_resume.py
   ```

2. **长时间运行时**
   - 减少保存间隔（改为每5个页面）
   - 使用 screen 或 tmux 防止终端关闭

3. **遇到验证码时**
   - 不要着急重启
   - 等待30分钟以上
   - 或更换IP/代理

4. **批量爬取时**
   - 增加延迟时间（改为3-5秒）
   - 分批次爬取（设置最大页面数）

## 总结

断点续传功能的核心优势：

- ✅ **可靠** - BFS + 队列，中断后无缝继续
- ✅ **智能** - 自动重新扫描，发现遗漏的链接
- ✅ **高效** - 不重复爬取，不重复提取
- ✅ **可观察** - 实时显示进度，清楚了解状态
- ✅ **容错** - 多重保存机制，不丢失数据

从 DFS 到 BFS + 队列，这是一个架构级的改进！🎉
