# 后端服务器IP配置管理

## 📍 统一配置原则

**后端GPU服务器IP地址只需在一个地方配置！**

### 唯一配置文件
```
/home/ubuntu/PhotoEnhanceAI-web/api-gateway/gateway_config.json
```

修改这个文件的 `backend_api_base` 字段即可：
```json
{
  "backend_api_base": "http://新IP地址:8000",
  "backend_timeout": 300,
  "gateway_port": 443,
  "max_file_size": 104857600,
  ...
}
```

## 🔄 架构说明

### 请求流程
```
浏览器
  ↓ HTTPS
https://gongjuxiang.work/api/v1/enhance
  ↓ Nginx (443端口)
https://127.0.0.1:8443/api/v1/enhance
  ↓ API网关 (读取gateway_config.json)
http://后端GPU服务器:8000/api/v1/enhance
  ↓
处理完成
```

### 配置层级

1. **Nginx配置** (`/etc/nginx/sites-enabled/gongjuxiang.work`)
   - 所有 `/api/*` 请求 → 转发到 `https://127.0.0.1:8443`
   - 不包含后端IP硬编码
   - 无需修改

2. **API网关配置** (`gateway_config.json`)
   - ✅ **这是唯一需要修改后端IP的地方**
   - 网关读取此配置转发到后端GPU服务器

3. **默认配置** (`config.py`)
   - 当 `gateway_config.json` 不存在时使用
   - 建议也同步更新保持一致

## 🚀 快速更新后端IP

### 方法一：使用更新脚本（推荐）
```bash
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway
python3 update_backend.py --url http://新IP:8000
```

### 方法二：手动更新
```bash
# 1. 编辑配置文件
nano /home/ubuntu/PhotoEnhanceAI-web/api-gateway/gateway_config.json

# 2. 修改 backend_api_base 字段

# 3. 重启API网关服务
sudo pkill -f "python3 app.py"
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway
sudo nohup python3 app.py > app.log 2>&1 &

# 4. 验证
curl -s https://gongjuxiang.work/api/v1/info | python3 -m json.tool
```

## ✅ 验证清单

更新后端IP后，请检查：

1. **配置已生效**
   ```bash
   curl -s https://gongjuxiang.work/api/v1/info | grep backend
   # 应该显示新的后端IP地址
   ```

2. **后端服务可访问**
   ```bash
   curl http://新IP:8000/
   # 应该返回服务信息
   ```

3. **前端功能正常**
   - 访问 https://gongjuxiang.work
   - 上传图片测试增强功能

## 📝 注意事项

1. **只修改一个文件**：`gateway_config.json`
2. **修改后需重启**：API网关服务（不需要重启Nginx）
3. **微信支付不影响**：微信支付API有独立的配置路径
4. **配置会持久化**：gateway_config.json 的修改会永久保存

## 🔧 故障排查

### 问题：修改配置后不生效
**原因**：API网关服务未重启
**解决**：
```bash
sudo pkill -f "python3 app.py"
cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway
sudo nohup python3 app.py > app.log 2>&1 &
```

### 问题：Network Error
**原因**：新后端IP无法访问
**解决**：
```bash
# 测试后端连通性
curl http://新IP:8000/
# 检查防火墙和网络配置
```

### 问题：API网关启动失败
**原因**：配置文件JSON格式错误
**解决**：
```bash
# 验证JSON格式
python3 -m json.tool gateway_config.json
# 或使用测试脚本
python3 test_config.py
```

## 📊 当前配置

查看当前使用的后端IP：
```bash
cat /home/ubuntu/PhotoEnhanceAI-web/api-gateway/gateway_config.json | grep backend_api_base
```

或通过API查询：
```bash
curl -s https://gongjuxiang.work/api/v1/info | python3 -m json.tool | grep backend
```

---

**最后更新**: 2025-10-01
**当前后端IP**: 49.232.44.156:8000

