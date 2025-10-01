#!/bin/bash

# GitHub推送脚本 - 专门推送到GitHub，通过多次重试克服网络问题
# 使用方法: ./github_push.sh

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# GitHub仓库URL
GITHUB_URL="https://github.com/Rsers/PhotoEnhanceAI-web.git"

echo -e "${BLUE}🚀 开始推送到GitHub...${NC}"

# 进入项目目录
cd /home/ubuntu/PhotoEnhanceAI-web || {
    echo -e "${RED}错误: 无法进入项目目录${NC}"
    exit 1
}

# 设置GitHub URL
git remote set-url origin "$GITHUB_URL"

# 检查待推送的提交
ahead_count=$(git rev-list --count origin/main..HEAD 2>/dev/null)
if [ "$ahead_count" -eq 0 ]; then
    echo -e "${YELLOW}没有待推送的提交${NC}"
    exit 0
fi

echo -e "${BLUE}发现 $ahead_count 个待推送的提交${NC}"

# 推送函数
push_to_github() {
    local max_retries=20  # 最多重试20次
    local retry_count=0
    local retry_delay=30  # 每次重试间隔30秒
    
    while [ $retry_count -lt $max_retries ]; do
        echo -e "${BLUE}第 $((retry_count + 1)) 次尝试推送...${NC}"
        
        # 先尝试拉取远程更改
        echo -e "${BLUE}同步远程更改...${NC}"
        if timeout 300 git pull origin main 2>&1; then
            echo -e "${GREEN}✅ 远程更改同步成功${NC}"
        else
            echo -e "${YELLOW}⚠️ 远程同步失败，继续尝试推送${NC}"
        fi
        
        # 尝试推送主分支
        if timeout 300 git push origin main 2>&1; then
            echo -e "${GREEN}✅ 主分支推送成功！${NC}"
            
            # 推送标签
            if git tag -l | grep -q "v1.0"; then
                echo -e "${BLUE}推送标签 v1.0...${NC}"
                if timeout 300 git push origin v1.0 2>&1; then
                    echo -e "${GREEN}✅ 标签推送成功！${NC}"
                else
                    echo -e "${YELLOW}⚠️ 标签推送失败，但主分支推送成功${NC}"
                fi
            fi
            
            echo -e "${GREEN}🎉 GitHub推送完成！${NC}"
            return 0
        else
            echo -e "${RED}❌ 第 $((retry_count + 1)) 次推送失败${NC}"
            retry_count=$((retry_count + 1))
            
            if [ $retry_count -lt $max_retries ]; then
                echo -e "${YELLOW}等待 $retry_delay 秒后重试...${NC}"
                sleep $retry_delay
                
                # 逐渐增加重试间隔
                if [ $retry_count -gt 5 ]; then
                    retry_delay=60  # 5次后增加到60秒
                fi
                if [ $retry_count -gt 10 ]; then
                    retry_delay=120  # 10次后增加到120秒
                fi
            fi
        fi
    done
    
    echo -e "${RED}❌ 达到最大重试次数 ($max_retries)，推送失败${NC}"
    return 1
}

# 检查网络连接
check_github_connection() {
    echo -e "${BLUE}检查GitHub连接...${NC}"
    
    # 尝试ping GitHub
    if ping -c 1 -W 10 github.com >/dev/null 2>&1; then
        echo -e "${GREEN}✅ GitHub连接正常${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️ GitHub连接较慢，但继续尝试推送${NC}"
        return 0
    fi
}

# 主函数
main() {
    # 检查连接
    check_github_connection
    
    # 开始推送
    if push_to_github; then
        echo -e "${GREEN}🎉 推送成功！${NC}"
        exit 0
    else
        echo -e "${RED}❌ 推送失败${NC}"
        echo -e "${YELLOW}💡 建议稍后再试，或者使用: ./auto_push.sh --daemon${NC}"
        exit 1
    fi
}

# 运行主函数
main "$@"
