# 反爬虫检测说明

## 检测机制

爬虫会自动检测企业微信的反爬虫验证码页面：

### 检测条件

1. **页面标题检测**
   - 标题包含 "企业微信-验证码"
   - 标题为 "验证码"

2. **页面内容检测**
   - 包含 "请完成验证"
   - 包含 "请输入验证码"
   - 包含 "人机验证" 等关键词

### 触发后的行为

当检测到验证码页面时，爬虫会：

1. ✅ **立即停止爬取** - 避免继续触发反爬虫机制
2. 💾 **保存当前进度** - 保存所有已提取的文档和访问记录
3. 📊 **显示统计信息** - 展示已爬取的文档数量和页面数
4. 💡 **给出建议操作** - 提示下一步应该怎么做

## 示例输出

```
正在爬取: https://developer.work.weixin.qq.com/document/path/xxxxx

============================================================
⚠️  检测到反爬虫验证码页面
============================================================
页面标题: 企业微信-验证码
触发 URL: https://developer.work.weixin.qq.com/document/path/xxxxx

正在保存当前进度...

✓ 进度已保存
  - 已爬取: 25 个 API 文档
  - 已访问: 30 个页面
  - 输出目录: ../api_docs

💡 建议操作：
  1. 等待一段时间后重新运行（建议 30 分钟以上）
  2. 更换 IP 地址或使用代理
  3. 增加请求延迟时间
  4. 使用浏览器手动完成验证后再继续

重新运行命令继续爬取：
  python3 crawler.py
============================================================
```

## 应对策略

### 策略 1：等待后重试（推荐）

最简单的方法，等待一段时间后重新运行：

```bash
# 等待 30 分钟到 1 小时
sleep 1800  # 等待 30 分钟

# 重新运行（会自动跳过已爬取的）
python3 crawler.py
```

### 策略 2：增加请求延迟

编辑 `crawler.py`，增加请求间隔：

```python
def _crawl_page(self, url: str):
    # ...
    # 原来是 2 秒
    time.sleep(2)
    
    # 改为 5 秒或更长
    time.sleep(5)
```

然后重新运行：

```bash
python3 crawler.py
```

### 策略 3：使用代理

添加代理支持（需要自己有代理服务器）：

```python
# 在 __init__ 方法中添加代理配置
self.proxies = {
    'http': 'http://your-proxy:port',
    'https': 'http://your-proxy:port',
}

# 修改请求
response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=30)
```

### 策略 4：更换 User-Agent

编辑 `crawler.py`，更换不同的浏览器标识：

```python
self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
```

### 策略 5：手动验证后继续

1. 在浏览器中打开触发验证码的 URL
2. 完成人机验证
3. 等待几分钟
4. 重新运行爬虫：

```bash
python3 crawler.py
```

### 策略 6：分批爬取

不要一次爬取所有内容，分批进行：

```python
# 第一天：爬取通讯录管理
crawler = WeChatWorkAPICrawler(
    base_url="https://developer.work.weixin.qq.com",
    start_path="/document/path/90194",
    output_dir="../api_docs_contacts"
)
crawler.crawl()

# 第二天：爬取消息推送
crawler = WeChatWorkAPICrawler(
    base_url="https://developer.work.weixin.qq.com",
    start_path="/document/path/90664",
    output_dir="../api_docs_messages"
)
crawler.crawl()
```

## 最佳实践

### ✅ 推荐做法

1. **使用默认延迟**（2 秒）开始爬取
2. **遇到验证码就停止**，等待 30-60 分钟
3. **重新运行继续爬取**，利用断点续爬功能
4. **如果再次触发**，增加延迟到 5 秒或更长
5. **分多天完成**，不要急于一次性爬取所有内容

### ❌ 不推荐做法

1. ❌ 降低延迟时间（< 2 秒）
2. ❌ 遇到验证码后立即重试
3. ❌ 使用多线程并发爬取
4. ❌ 短时间内大量请求

## 进度保护

### 自动保存

爬虫在检测到验证码后会自动保存：

- ✅ 所有已提取的 Markdown 文档
- ✅ 索引文件（README.md）
- ✅ 访问记录（.visited_urls.json）
- ✅ JSON 数据（api_docs.json）

### 数据完整性

所有已保存的数据都是完整和可用的：

```bash
# 查看已保存的文档
ls ../api_docs/*.md

# 查看索引
cat ../api_docs/README.md

# 查看已访问的 URL 数量
cat ../api_docs/.visited_urls.json | grep -c "https:"
```

## 恢复爬取

### 自动恢复

重新运行爬虫会自动从上次停止的地方继续：

```bash
# 直接运行，自动跳过已爬取的内容
python3 crawler.py
```

### 手动恢复

如果想从头开始：

```bash
# 删除访问记录
rm ../api_docs/.visited_urls.json

# 重新运行
python3 crawler.py --no-resume
```

## 监控和预防

### 监控爬取速度

```bash
# 实时查看文件数量变化
watch -n 5 'ls ../api_docs/*.md 2>/dev/null | wc -l'
```

### 预防性措施

1. **合理的延迟**
   - 默认 2 秒延迟已经比较保守
   - 如果遇到频繁验证码，增加到 5-10 秒

2. **限制爬取范围**
   - 不要一次爬取整个文档站点
   - 只爬取需要的章节

3. **分时段爬取**
   - 避开工作时间（早上 9 点到晚上 6 点）
   - 选择凌晨或周末进行

4. **尊重服务器**
   - 不要使用多线程
   - 保持合理的请求频率
   - 遵守 robots.txt 规则

## 故障排除

### Q: 爬取几个页面就触发验证码？

**A:** 可能的原因：
- IP 被标记（之前有频繁访问）
- 网络环境被识别（数据中心 IP）
- 请求特征异常

**解决方法：**
- 更换网络环境或使用代理
- 增加延迟到 5-10 秒
- 等待更长时间（1-2 小时）后重试

### Q: 重新运行还是立即触发验证码？

**A:** 说明 IP 被临时封禁

**解决方法：**
- 等待 24 小时
- 更换 IP 地址
- 使用浏览器完成一次人机验证

### Q: 如何知道是否会触发验证码？

**A:** 观察爬取速度：
- 正常：每 2 秒一个页面
- 异常：连续失败或页面内容异常

## 技术细节

### 检测代码

```python
def _check_captcha_page(self, soup: BeautifulSoup) -> bool:
    """检测是否为验证码页面"""
    # 检查页面标题
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        if '企业微信-验证码' in title or '验证码' == title:
            return True
    
    # 检查页面内容
    page_text = soup.get_text()
    if '请完成验证' in page_text or '请输入验证码' in page_text:
        return True
    
    return False
```

### 异常处理

```python
class CaptchaDetectedException(Exception):
    """检测到验证码页面的异常"""
    pass
```

这个自定义异常确保验证码检测能够优雅地停止爬虫。

## 总结

反爬虫检测机制的核心价值：

1. **保护进度** - 避免无效请求浪费时间
2. **数据安全** - 确保已爬取的数据不丢失
3. **友好提示** - 给出明确的后续操作建议
4. **智能恢复** - 支持断点续爬，不重复劳动

记住：**遇到验证码不是问题，关键是如何优雅地处理！** 🎯
