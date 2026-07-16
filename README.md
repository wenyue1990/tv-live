# 飞牛电视直播 (fnOS TV Live)

一款专为飞牛NAS (fnOS) 设计的网络电视直播应用，支持IPTV直播源播放。

## 功能特点

- 📺 **丰富的频道**: 支持央视、卫视、地方频道等数百个电视频道
- 🎯 **分类管理**: 自动分类频道，快速找到想看的内容
- ⭐ **收藏功能**: 收藏喜欢的频道，下次快速打开
- 🔍 **搜索功能**: 支持频道名称搜索
- 📋 **播放列表**: 支持M3U/M3U8格式的IPTV播放列表
- 🎨 **美观界面**: 深色主题设计，适合电视观看
- 📱 **响应式设计**: 支持手机、平板、电脑等多种设备
- 🐳 **Docker部署**: 一键部署到飞牛NAS

## 快速开始

### 方法一：Docker部署（推荐）

#### 1. 在fnOS上安装Docker

确保你的飞牛NAS已安装并启用了Docker功能。

#### 2. 下载项目

```bash
# 克隆项目到本地
git clone https://github.com/your-username/fnos-tv-live.git
cd fnos-tv-live
```

或者直接将项目文件上传到NAS。

#### 3. 构建Docker镜像

```bash
docker build -t fnos-tv-live .
```

#### 4. 运行容器

```bash
docker run -d \
  --name fnos-tv-live \
  --restart unless-stopped \
  -p 8080:8080 \
  -v $(pwd)/config:/config \
  -v $(pwd)/playlist:/playlist \
  -e TZ=Asia/Shanghai \
  fnos-tv-live
```

或使用docker-compose：

```bash
docker-compose up -d
```

#### 5. 访问应用

打开浏览器，访问：`http://你的NAS-IP:8080`

### 方法二：直接运行

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 启动服务

```bash
python server.py
```

#### 3. 访问应用

打开浏览器，访问：`http://localhost:8080`

## 使用说明

### 基本操作

1. **选择频道**: 点击频道列表中的任意频道即可播放
2. **切换分类**: 点击左侧分类按钮筛选频道
3. **搜索频道**: 在搜索框输入频道名称
4. **收藏频道**: 点击频道右侧的星标或播放界面的收藏按钮
5. **切换频道**: 使用键盘上下键或播放界面的切换按钮

### 设置直播源

1. 点击左下角的"设置"按钮
2. 输入M3U播放列表URL，或上传本地M3U文件
3. 点击"保存"按钮

### 推荐直播源

项目内置了来自 [fanmingming/live](https://github.com/fanmingming/live) 的公开直播源，包含：

- CCTV 央视全套频道
- 各地方卫视
- 国际频道

你也可以使用自己的IPTV直播源。

### 键盘快捷键

| 按键 | 功能 |
|------|------|
| ↑ | 上一个频道 |
| ↓ | 下一个频道 |
| F | 收藏/取消收藏 |
| ESC | 关闭弹窗 |

## 项目结构

```
tv-live/
├── index.html          # 主页面
├── css/
│   └── style.css       # 样式文件
├── js/
│   └── app.js          # 前端逻辑
├── server.py           # 后端服务
├── requirements.txt    # Python依赖
├── Dockerfile          # Docker配置
├── docker-compose.yml  # Docker Compose配置
├── playlist/
│   └── demo.m3u        # 示例播放列表
└── README.md           # 说明文档
```

## 技术栈

- **前端**: HTML5 + CSS3 + JavaScript
- **后端**: Python + Flask
- **视频播放**: hls.js (HLS流播放)
- **部署**: Docker

## 在fnOS上部署的详细步骤

### 步骤1：准备工作

1. 确保飞牛NAS已开启Docker功能
2. 确保NAS有足够的存储空间

### 步骤2：上传文件

1. 打开fnOS的文件管理器
2. 创建一个新文件夹，如 `/vol1/docker/fnos-tv-live`
3. 将项目所有文件上传到该文件夹

### 步骤3：构建镜像

通过SSH连接到NAS，执行：

```bash
cd /vol1/docker/fnos-tv-live
docker build -t fnos-tv-live .
```

### 步骤4：运行容器

```bash
docker run -d \
  --name fnos-tv-live \
  --restart unless-stopped \
  -p 8080:8080 \
  -v /vol1/docker/fnos-tv-live/config:/config \
  -v /vol1/docker/fnos-tv-live/playlist:/playlist \
  -e TZ=Asia/Shanghai \
  fnos-tv-live
```

### 步骤5：访问

在浏览器中访问 `http://NAS-IP:8080` 即可开始观看电视直播。

## 常见问题

### 1. 无法播放频道

- 检查网络连接
- 确认直播源URL有效
- 尝试更换其他直播源

### 2. 频道加载失败

- 检查直播源URL是否可访问
- 尝试使用本地M3U文件
- 检查NAS的网络连接

### 3. 端口冲突

修改docker运行命令中的端口映射：

```bash
-p 8081:8080  # 将8081改为你想要的端口
```

### 4. 如何更新直播源

在设置中输入新的直播源URL，或上传新的M3U文件。

## 直播源格式

支持的M3U格式示例：

```m3u
#EXTM3U
#EXTINF:-1 tvg-name="频道名称" tvg-logo="频道图标URL" group-title="分组",显示名称
视频流地址
```

## 免责声明

本项目仅供学习交流使用，所有直播源均来自网络公开资源，版权归原作者所有。

## 许可证

MIT License

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持基本的电视直播功能
- 支持Docker部署到fnOS