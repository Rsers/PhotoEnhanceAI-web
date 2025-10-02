# 后端服务器IP配置管理

## 📍 统一配置原则

**后端GPU服务器IP地址通过多B服务器管理系统动态管理！**

### 多B服务器管理系统

现在系统支持多台B服务器动态注册和管理：

```
B服务器1 (B1) → 自动注册IP → A服务器负载均衡
B服务器2 (B2) → 自动注册IP → A服务器负载均衡  
B服务器3 (B3) → 自动注册IP → A服务器负载均衡
```

## 🔄 架构说明

### 请求流程
```
浏览器
  ↓ HTTPS
https://gongjuxiang.work/api/v1/enhance
  ↓ Nginx (443端口)
https://127.0.0.1:8443/api/v1/enhance
  ↓ API网关 (负载均衡选择B服务器)
http://B服务器IP:8000/api/v1/enhance
  ↓
处理完成
```

### 配置层级

1. **Nginx配置** (`/etc/nginx/sites-enabled/gongjuxiang.work`)
   - 所有 `/api/*` 请求 → 转发到 `https://127.0.0.1:8443`
   - 不包含后端IP硬编码
   - 无需修改

2. **多B服务器管理** (`backend_manager.py`)
   - ✅ **B服务器自动注册和管理**
   - 支持负载均衡和健康检测
   - 动态IP更新

3. **配置文件** (`gateway_config.json`)
   - 不再硬编码IP地址
   - 支持多B服务器模式配置

## 🚀 B服务器注册

### 注册B服务器
```bash
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway
python3 test_b_client.py register \
  --server-id B1 \
  --ip 192.168.1.100 \
  --port 8000 \
  --secret your-secret-password-2024
```

### 查看B服务器状态
```bash
python3 test_b_client.py list \
  --secret your-secret-password-2024
```

### 注销B服务器
```bash
python3 test_b_client.py unregister \
  --server-id B1 \
  --secret your-secret-password-2024
```

## ✅ 验证清单

B服务器注册后，请检查：

1. **B服务器已注册**
   ```bash
   curl -s https://gongjuxiang.work/webhook/servers?secret=your-secret
   # 应该显示注册的B服务器信息
   ```

2. **负载均衡正常**
   ```bash
   curl -s https://gongjuxiang.work/api/v1/info | grep backend_servers
   # 应该显示B服务器统计信息
   ```

3. **前端功能正常**
   - 访问 https://gongjuxiang.work
   - 上传图片测试增强功能

## 📝 注意事项

1. **动态IP管理**：B服务器IP变化时自动更新
2. **负载均衡**：请求自动分发到可用的B服务器
3. **健康检测**：自动检测B服务器状态
4. **故障转移**：B服务器故障时自动切换

## 🔧 故障排查

### 问题：没有可用的B服务器
**原因**：B服务器未注册或全部离线
**解决**：
```bash
# 注册B服务器
python3 test_b_client.py register --server-id B1 --ip 192.168.1.100

# 检查B服务器状态
python3 test_b_client.py list
```

### 问题：B服务器注册失败
**原因**：密码错误或网络问题
**解决**：
```bash
# 检查密码设置
echo $WEBHOOK_SECRET

# 测试网络连通性
curl -X POST https://gongjuxiang.work/webhook/register \
  -H "Content-Type: application/json" \
  -d '{"server_id":"test","ip":"127.0.0.1","port":8000,"secret":"your-secret"}'
```

### 问题：负载均衡不工作
**原因**：多B服务器模式未启用
**解决**：
```bash
# 启用多B服务器模式
curl -X POST https://gongjuxiang.work/api/v1/config/multi-backend \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'
```

## 📊 当前配置

查看当前B服务器状态：
```bash
curl -s https://gongjuxiang.work/webhook/servers?secret=your-secret | python3 -m json.tool
```

或通过API查询：
```bash
curl -s https://gongjuxiang.work/api/v1/info | python3 -m json.tool | grep backend_servers
```

---

**最后更新**: 2025-01-01
**系统状态**: 多B服务器动态管理
**配置方式**: B服务器自动注册，无需手动配置IP