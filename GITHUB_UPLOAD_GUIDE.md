# 将飞牛电视直播上传到GitHub指南

## 方法一：使用GitHub网页界面（无需Git）

### 步骤1：注册GitHub账号
1. 访问 https://github.com
2. 点击 "Sign up" 注册账号
3. 完成邮箱验证

### 步骤2：创建新仓库
1. 登录后，点击右上角 "+" → "New repository"
2. 填写信息：
   - Repository name: `fnos-tv-live` （或其他名称）
   - Description: `飞牛NAS电视直播应用`
   - 选择 "Public" 或 "Private"
   - 勾选 "Add a README file"
3. 点击 "Create repository"

### 步骤3：上传文件
1. 在新建的仓库页面，点击 "Add file" → "Upload files"
2. 将 `tv-live` 文件夹中的所有文件拖拽到上传区域
3. 等待上传完成
4. 点击 "Commit changes"

### 步骤4：获取代码地址
上传完成后，你的代码地址为：
```
https://github.com/你的用户名/fnos-tv-live
```

---

## 方法二：使用Git命令行（需要先安装Git）

### 步骤1：下载并安装Git
1. 访问 https://git-scm.com/download/win
2. 下载并安装Git for Windows
3. 安装时选择 "Use Git from Git Bash only" 即可

### 步骤2：配置Git
打开Git Bash，执行：
```bash
# 设置用户名
git config --global user.name "你的GitHub用户名"

# 设置邮箱
git config --global user.email "你的邮箱"
```

### 步骤3：初始化仓库并上传
在项目目录下执行：
```bash
# 进入项目目录
cd tv-live

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始版本：飞牛电视直播应用"

# 添加远程仓库（替换为你的GitHub用户名和仓库名）
git remote add origin https://github.com/你的用户名/fnos-tv-live.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

---

## 创建Docker Hub镜像（可选）

如果你想让飞牛NAS直接拉取Docker镜像，需要推送到Docker Hub：

### 步骤1：注册Docker Hub账号
1. 访问 https://hub.docker.com
2. 注册账号

### 步骤2：登录Docker Hub
```bash
docker login
```
输入用户名和密码。

### 步骤3：构建并推送镜像
```bash
# 构建镜像（替换为你的Docker Hub用户名）
docker build -t 你的用户名/fnos-tv-live:latest .

# 推送镜像
docker push 你的用户名/fnos-tv-live:latest
```

### 步骤4：在飞牛NAS上拉取镜像
在飞牛NAS的Docker管理界面：
1. 点击 "镜像" → "拉取镜像"
2. 输入：`你的用户名/fnos-tv-live:latest`
3. 点击拉取

---

## 在飞牛NAS上部署

### 方式一：使用拉取的镜像
```bash
docker run -d \
  --name fnos-tv-live \
  --restart unless-stopped \
  -p 8080:8080 \
  -v /path/to/config:/config \
  -v /path/to/playlist:/playlist \
  -e TZ=Asia/Shanghai \
  你的用户名/fnos-tv-live:latest
```

### 方式二：使用docker-compose
创建 `docker-compose.yml` 文件：
```yaml
version: '3.8'

services:
  tv-live:
    image: 你的用户名/fnos-tv-live:latest
    container_name: fnos-tv-live
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ./config:/config
      - ./playlist:/playlist
    environment:
      - TZ=Asia/Shanghai
```

然后执行：
```bash
docker-compose up -d
```

---

## 常见问题

### Q: 上传失败怎么办？
A: 检查文件大小，GitHub单文件限制为100MB。如果文件过大，需要使用Git LFS。

### Q: 如何更新代码？
A: 在GitHub网页界面直接编辑文件，或使用Git命令行推送更新。

### Q: 如何让别人使用我的镜像？
A: 将Docker Hub镜像设为公开，别人就可以直接拉取使用。