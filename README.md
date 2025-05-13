# 🔌 USBIP Web 管理界面（基于 Flask + WebSocket）

这是一个通过网页实时查看并控制 USBIP 设备绑定状态的轻量级管理工具，适用于 iStoreOS 等设备。  
该项目部署在 Docker 容器中，**usbip 实际执行仍在宿主机完成**。

---

## ✨ 功能特点

- 实时显示 USB 设备列表（BUS ID / 设备信息 / 绑定状态）
- 一键 Bind / Unbind 操作
- WebSocket 实时刷新设备状态
- 简洁美观的网页前端，适配移动端和桌面端

---

## 📸 截图预览

![alt text](image.png)
![alt text](image-1.png)

---

## 🗂 项目结构

```
usbip_web/
├── app.py               # Flask 主应用
├── usbip_utils.py       # 调用宿主 usbip 的工具封装
├── Dockerfile           # 容器构建配置
├── docker-compose.yml   # 一键部署配置
├── templates/
│   └── index.html       # 网页模板
└── static/
    ├── main.js          # 前端逻辑 (含 WebSocket)
    └── style.css        # 样式美化
```

---

## 🚀 部署方式（iStoreOS 环境）

### 1️⃣ 准备项目

上传整个 `usbip-webui` 项目到 iStoreOS 路由器或使用以下命令克隆：

```bash
git clone https://github.com/ChongZhiJie0216/usbip-webui
cd usbip-webui
```

---

### 2️⃣ 启动服务

使用 Docker Compose 启动：

```bash
docker-compose up -d
```

---

### 3️⃣ 访问界面

在浏览器中打开：

```
http://<你的iStoreOS IP>:8080
```

即可查看并管理 USBIP 设备。

---

## ⚙ docker-compose.yml 内容

```yaml
version: "3.8"
services:
  usbip-web:
    container_name: usbip_web
    build: .
    ports:
      - "8080:5000"
    privileged: true
    volumes:
      - /dev/bus/usb:/dev/bus/usb
      - /sys/bus/usb:/sys/bus/usb
      - /sys/devices:/sys/devices
      - /dev:/dev
    restart: unless-stopped
```

### 📌 挂载说明

| 宿主路径       | 用途                         |
| -------------- | ---------------------------- |
| `/dev/bus/usb` | 读取设备信息                 |
| `/sys/bus/usb` | 设备绑定状态判断             |
| `/sys/devices` | 获取设备描述、驱动信息       |
| `/dev`         | 某些系统交互需要访问设备节点 |

---

## 🔧 前提要求

- 宿主机（iStoreOS）已正确安装并配置好 `usbip`
- `usbip` 命令需可通过容器访问（通过 volume 映射实现）
- 宿主 USB 设备需支持 USBIP，并正确绑定/解绑驱动

---

## ✅ 示例操作

查看设备：

```bash
usbip list -l
```

手动绑定（在宿主）：

```bash
usbip bind -b 1-1
```

---

## 📌 注意事项

- 本项目容器**不提供 USB 设备共享服务**（usbipd），仅提供管理前端
- 所有实际操作依赖宿主机的 usbip 工具
- Web 前端默认监听 8080 端口，可根据需要修改

---

## 📝 来源

### [USB over IP tunnel](https://openwrt.org/docs/guide-user/services/usb.iptunnel)
