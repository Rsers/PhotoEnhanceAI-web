#!/bin/bash

# 快速推送脚本 - 立即尝试推送一次
# 使用方法: ./quick_push.sh

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 开始快速推送...${NC}"

# 进入项目目录
cd /home/ubuntu/PhotoEnhanceAI-web || {
    echo -e "${RED}错误: 无法进入项目目录${NC}"
    exit 1
}

# 检查待推送的提交
ahead_count=$(git rev-list --count origin/main..HEAD 2>/dev/null)
if [ "$ahead_count" -eq 0 ]; then
    echo -e "${YELLOW}没有待推送的提交${NC}"
    exit 0
fi

echo -e "${BLUE}发现 $ahead_count 个待推送的提交${NC}"

# 镜像源列表
mirrors=(
    "https://ghproxy.com/https://github.com/Rsers/PhotoEnhanceAI-web.git"
    "https://github.com.cnpmjs.org/Rsers/PhotoEnhanceAI-web.git"
    "https://hub.fastgit.xyz/Rsers/PhotoEnhanceAI-web.git"
    "https://github.com/Rsers/PhotoEnhanceAI-web.git"
)

# 尝试每个镜像源
for mirror in "${mirrors[@]}"; do
    echo -e "${BLUE}尝试镜像源: $mirror${NC}"
    
    # 设置远程URL
    git remote set-url origin "$mirror"
    
    # 尝试推送
    if git push origin main; then
        echo -e "${GREEN}✅ 推送成功！${NC}"
        
        # 推送标签
        if git tag -l | grep -q "v1.0"; then
            echo -e "${BLUE}推送标签 v1.0...${NC}"
            git push origin v1.0
        fi
        
        echo -e "${GREEN}🎉 所有推送完成！${NC}"
        exit 0
    else
        echo -e "${RED}❌ 推送失败，尝试下一个镜像源...${NC}"
    fi
done

# 恢复原始URL
git remote set-url origin "https://github.com/Rsers/PhotoEnhanceAI-web.git"

echo -e "${RED}❌ 所有镜像源都推送失败${NC}"
echo -e "${YELLOW}💡 建议运行: ./auto_push.sh --daemon${NC}"
exit 1


