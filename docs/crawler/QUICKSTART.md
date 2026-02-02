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
# 运行爬虫（默认启用断点续爬）
python3 crawler.py

# 从头开始爬取（忽略之前的进度）
python3 crawler.py --no-resume

# 运行测试
python3 test_crawler.py

# 查看示例
python3 example.py

# 退出虚拟环境
deactivate
```

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

## ⚙️ 环境变量配置（可选）

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
