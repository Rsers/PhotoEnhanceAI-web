#!/bin/bash

# 简单重试推送脚本
# 使用方法: ./simple_retry.sh

echo "🚀 开始简单重试推送..."

cd /home/ubuntu/PhotoEnhanceAI-web || exit 1

# 设置GitHub URL
git remote set-url origin "https://github.com/Rsers/PhotoEnhanceAI-web.git"

# 检查待推送的提交
ahead_count=$(git rev-list --count origin/main..HEAD 2>/dev/null)
if [ "$ahead_count" -eq 0 ]; then
    echo "没有待推送的提交"
    exit 0
fi

echo "发现 $ahead_count 个待推送的提交"

# 简单重试逻辑
for i in {1..10}; do
    echo "第 $i 次尝试..."
    
    # 尝试推送
    if git push origin main; then
        echo "✅ 推送成功！"
        
        # 推送标签
        if git tag -l | grep -q "v1.0"; then
            echo "推送标签 v1.0..."
            git push origin v1.0
        fi
        
        echo "🎉 完成！"
        exit 0
    else
        echo "❌ 第 $i 次失败"
        if [ $i -lt 10 ]; then
            echo "等待 60 秒后重试..."
            sleep 60
        fi
    fi
done

echo "❌ 所有尝试都失败了"
exit 1


