# 使用一个基础的 Node.js 镜像作为构建环境
FROM node:18 as builder

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json 文件到容器中
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制前端应用源代码到容器中
COPY . .

# 执行构建命令
RUN npm run build

# 创建一个新的容器镜像
FROM nginx:latest

# 复制构建产物到 Nginx 的默认静态文件目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 将自定义的 nginx.conf 文件复制到容器中，覆盖默认配置
# remove the default conf
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露容器的 80 端口
EXPOSE 80
