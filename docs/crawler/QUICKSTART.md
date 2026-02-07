# 快速开始指南

## 🚀 三种使用方式

### 1️⃣ 最简单：自动激活环境（推荐）

#### 使用 direnv（一次配置，永久生效）

```bash
# 1. 安装 direnv（只需要一次）
brew install direnv

# 2. 配置 shell（添加到 ~/.zshrc）
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc

# 3. 允许自动激活（只需要一次）
cd /Users/hysios/Projects/BlackSail/pkgs/wxwork-client/docs/crawler
direnv allow
```

**完成！** 以后每次进入 `crawler` 目录，虚拟环境会自动激活 ✨

#### 或使用 activate.sh 脚本

```bash
cd /Users/hysios/Projects/BlackSail/pkgs/wxwork-client/docs/crawler
source activate.sh
```

### 2️⃣ 一键运行

```bash
cd /Users/hysios/Projects/BlackSail/pkgs/wxwork-client/docs/crawler
./run.sh
```

脚本会自动完成所有设置并运行爬虫。

### 3️⃣ 手动激活

```bash
cd /Users/hysios/Projects/BlackSail/pkgs/wxwork-client/docs/crawler
source venv/bin/activate
python3 crawler.py
```

## 📝 可用命令

激活虚拟环境后，你可以运行：

```bash
# 运行爬虫（默认启用断点续爬 + LLM 提取）
python3 crawler.py

# 从头开始爬取（忽略之前的进度）
python3 crawler.py --no-resume

# 仅爬取特定文档（通过 ID）
python3 crawler.py --doc-ids 101100 101158

# 必须同时包含"第三方应用开发"和"服务端API"，排除"服务商代开发"
python3 crawler.py --route-filter "第三方应用开发" "服务端API" --route-exclude "服务商代开发"

# 运行测试
python3 test_crawler.py

# 查看示例
python3 example.py

# 退出虚拟环境
deactivate
```

**提示：** 如果已配置 `OPENAI_API_KEY`，爬虫会自动使用 AI 提取模式，提供更高的准确性。

## 🔄 实时保存和断点续爬

爬虫会在爬取过程中：
- ✅ **立即保存** - 每提取一个 API 立即保存 Markdown 文件
- ✅ **实时索引** - 实时更新 `README.md` 索引文件
- ✅ **保存进度** - 记录已访问的 URL，支持断点续爬
- ✅ **可查看进度** - 随时打开 `../api_docs/README.md` 查看进度

如果爬取中断（Ctrl+C 或网络问题），只需重新运行命令，会自动跳过已爬取的内容！

## 🔧 虚拟环境状态

查看是否在虚拟环境中：

```bash
# 应该显示类似：/Users/hysios/Projects/BlackSail/pkgs/wxwork-client/docs/crawler/venv/bin/python3
which python3

# 检查已安装的包
pip list
```

## 📦 已安装的依赖

- ✅ requests (HTTP 请求)
- ✅ beautifulsoup4 (HTML 解析)
- ✅ lxml (高性能解析器)
- ✅ markitdown (HTML 转 Markdown，支持 LLM 提取)
- ✅ openai (OpenAI API 客户端，用于 LLM 提取)

## 🎯 下一步

1. **运行测试** - 确保一切正常
   ```bash
   python3 test_crawler.py
   ```

2. **开始爬取** - 运行爬虫
   ```bash
   python3 crawler.py
   ```

3. **查看结果** - 生成的文档在 `../api_docs/` 目录

## ⚙️ 环境变量配置

### OpenAI API Key（LLM 提取模式）

爬虫现在支持使用 AI (GPT-3.5) 来提取 API 文档信息，准确性更高且能自动处理多 API 页面。

**配置方法：**

```bash
# 设置 OpenAI API Key
export OPENAI_API_KEY="your-api-key-here"

# 如果需要使用代理访问 OpenAI（可选）
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
# 或者使用 socks5 代理
export all_proxy=socks5://127.0.0.1:7890

# 或者添加到 ~/.zshrc 或 ~/.bashrc 永久生效
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
echo 'export https_proxy=http://127.0.0.1:7890' >> ~/.zshrc
source ~/.zshrc
```

**使用说明：**

- ✅ **已配置 API Key** → 自动使用 LLM 提取模式（推荐，更准确）
- ❌ **未配置 API Key** → 使用传统 BeautifulSoup 解析模式
- 🔄 **LLM 失败时** → 自动回退到 BeautifulSoup 模式（默认启用）

**LLM 模式优势：**

1. **更准确**：通过语义理解而非规则匹配，使用 GPT-4 Turbo 模型
2. **自动识别多 API**：一个页面包含多个接口时自动分离
3. **完整嵌套字段**：自动展开 object 和 array 类型的所有嵌套字段
4. **更智能**：能处理不规范的文档格式

### 其他配置（可选）

复制 `env.example` 为 `.env` 来自定义配置：

```bash
cp env.example .env
# 编辑 .env 文件修改配置
```

## 💡 提示

- 使用 direnv 可以在进入目录时自动激活环境，离开时自动退出
- 虚拟环境已经包含所有必需的依赖
- 首次运行可能需要几分钟来爬取所有文档

## 🆘 故障排除

### 虚拟环境未激活
```bash
source venv/bin/activate
```

### 依赖未安装
```bash
pip install -r requirements.txt
```

### 清理并重新开始
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
