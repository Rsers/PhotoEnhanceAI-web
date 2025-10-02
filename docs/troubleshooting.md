# 故障排除

## GitHub 访问问题

### 问题：无法推送代码到 GitHub
**症状**：`git push` 时出现连接超时、SSL错误或网络错误

**解决方案**：

1. **修改 Hosts 文件 (推荐)**：
   ```bash
   # 备份原始 hosts 文件
   sudo cp /etc/hosts /etc/hosts.backup
   
   # 添加 GitHub IP 地址
   sudo tee -a /etc/hosts << 'EOF'
   
   # GitHub IP addresses (2025)
   140.82.113.4 github.com
   185.199.108.153 assets-cdn.github.com
   199.232.69.194 github.global.ssl.fastly.net
   140.82.112.3 api.github.com
   EOF
   
   # 刷新 DNS 缓存
   sudo systemctl restart systemd-resolved
   ```

2. **使用 GitHub CLI**：
   ```bash
   # 安装 GitHub CLI
   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
   sudo apt update
   sudo apt install gh
   
   # 登录 GitHub
   gh auth login
   
   # 推送代码
   gh repo sync
   ```

3. **配置 SSH 访问**：
   ```bash
   # 生成 SSH 密钥
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   
   # 查看公钥
   cat ~/.ssh/id_rsa.pub
   
   # 将公钥添加到 GitHub 账户
   # 访问: https://github.com/settings/keys
   
   # 切换到 SSH 方式
   git remote set-url origin git@github.com:Rsers/PhotoEnhanceAI-web.git
   ```

4. **使用镜像站 (备选)**：
   ```bash
   # 尝试不同的镜像站
   git remote set-url origin https://github.com.cnpmjs.org/Rsers/PhotoEnhanceAI-web.git
   # 或
   git remote set-url origin https://hub.fastgit.xyz/Rsers/PhotoEnhanceAI-web.git
   # 或
   git remote set-url origin https://ghproxy.com/https://github.com/Rsers/PhotoEnhanceAI-web.git
   ```

## 端口连接问题

### 问题：前端无法连接后端 API
**症状**：上传图片后显示"连接失败"或"网络错误"

**解决方案**：
1. **检查 8000 端口是否开放**：
   ```bash
   # 检查端口监听状态
   netstat -tlnp | grep 8000
   
   # 如果显示 "tcp 0.0.0.0:8000"，说明端口已监听
   ```

2. **检查防火墙设置**：
   ```bash
   # Ubuntu/Debian
   sudo ufw status
   sudo ufw allow 8000
   
   # CentOS/RHEL
   sudo firewall-cmd --list-ports
   sudo firewall-cmd --permanent --add-port=8000/tcp
   sudo firewall-cmd --reload
   ```

3. **检查云服务器安全组**：
   - 登录云服务器控制台
   - 进入安全组/防火墙设置
   - 确保 8000 端口已开放，来源为 0.0.0.0/0

4. **测试端口连通性**：
   ```bash
   # 从外部测试端口
   telnet your-server-ip 8000
   
   # 或使用 curl 测试
   curl http://your-server-ip:8000/api/v1/status/test
   ```

## GPU服务器管理问题

### 问题：GPU服务器注册失败
**症状**：调用注册接口返回401错误或注册失败

**解决方案**：
1. **检查密码设置**：
   ```bash
   # 检查A服务器密码设置
   echo $WEBHOOK_SECRET
   
   # 检查GPU服务器密码设置
   echo $SHARED_SECRET
   ```

2. **测试网络连通性**：
   ```bash
   # 测试A服务器连通性
   curl -X POST https://www.gongjuxiang.work/webhook/register \
     -H "Content-Type: application/json" \
     -d '{"server_id":"test","ip":"127.0.0.1","port":8000,"secret":"your-secret"}'
   ```

3. **检查服务器ID冲突**：
   ```bash
   # 查看已注册的服务器
   curl "https://www.gongjuxiang.work/webhook/servers?secret=your-secret"
   ```

### 问题：负载均衡不工作
**症状**：请求总是转发到同一台服务器

**解决方案**：
1. **检查多GPU服务器模式**：
   ```bash
   # 启用多GPU服务器模式
   curl -X POST https://www.gongjuxiang.work/api/v1/config/multi-backend \
     -H "Content-Type: application/json" \
     -d '{"enabled": true}'
   ```

2. **检查GPU服务器状态**：
   ```bash
   # 查看GPU服务器健康状态
   python3 test_b_client.py list --secret your-secret
   ```

3. **检查健康检测**：
   ```bash
   # 查看健康检测状态
   curl https://www.gongjuxiang.work/api/v1/info | grep health_check
   ```

## 前端样式修改不生效问题

### 常见原因及解决方法

1. **CSS 优先级问题**
   - 检查是否有 `!important` 冲突
   - 确认选择器优先级是否正确

2. **浏览器缓存问题**
   - 强制刷新：`Ctrl+F5` (Windows) 或 `Cmd+Shift+R` (Mac)
   - 清除浏览器缓存

3. **热重载问题**
   - 重启开发服务器：`npm run dev`
   - 检查 Vite 配置是否正确

4. **作用域问题**
   - 检查 `<style scoped>` 是否正确应用
   - 确认组件选择器是否匹配

5. **导入问题**
   - 检查 CSS 文件是否正确导入
   - 确认路径是否正确

### 调试技巧
- 使用浏览器开发者工具检查样式是否被应用
- 检查控制台是否有错误信息
- 使用 `console.log` 调试组件状态
- 检查网络面板中的 API 请求状态
