#!/bin/bash

# 网络优化推送脚本 - 使用多种网络配置尝试推送
# 使用方法: ./network_push.sh

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 开始网络优化推送...${NC}"

# 进入项目目录
cd /home/ubuntu/PhotoEnhanceAI-web || {
    echo -e "${RED}错误: 无法进入项目目录${NC}"
    exit 1
}

# 设置GitHub URL
git remote set-url origin "https://github.com/Rsers/PhotoEnhanceAI-web.git"

# 检查待推送的提交
ahead_count=$(git rev-list --count origin/main..HEAD 2>/dev/null)
if [ "$ahead_count" -eq 0 ]; then
    echo -e "${YELLOW}没有待推送的提交${NC}"
    exit 0
fi

echo -e "${BLUE}发现 $ahead_count 个待推送的提交${NC}"

# 方案1：使用IPv4强制连接
try_ipv4_push() {
    echo -e "${BLUE}方案1: 强制使用IPv4连接...${NC}"
    
    # 设置Git使用IPv4
    git config --global http.version HTTP/1.1
    git config --global http.sslVerify false
    
    # 尝试推送
    if timeout 600 git push origin main 2>&1; then
        echo -e "${GREEN}✅ IPv4推送成功！${NC}"
        return 0
    else
        echo -e "${RED}❌ IPv4推送失败${NC}"
        return 1
    fi
}

# 方案2：使用代理
try_proxy_push() {
    echo -e "${BLUE}方案2: 尝试使用代理...${NC}"
    
    # 设置代理（如果有的话）
    export http_proxy=""
    export https_proxy=""
    
    # 重置Git配置
    git config --global --unset http.version
    git config --global http.sslVerify true
    
    # 尝试推送
    if timeout 600 git push origin main 2>&1; then
        echo -e "${GREEN}✅ 代理推送成功！${NC}"
        return 0
    else
        echo -e "${RED}❌ 代理推送失败${NC}"
        return 1
    fi
}

# 方案3：分批推送
try_batch_push() {
    echo -e "${BLUE}方案3: 分批推送提交...${NC}"
    
    # 获取待推送的提交
    local commits=$(git rev-list origin/main..HEAD)
    local commit_array=($commits)
    local total=${#commit_array[@]}
    
    echo -e "${BLUE}总共 $total 个提交需要推送${NC}"
    
    # 尝试推送每个提交
    for ((i=0; i<total; i++)); do
        local commit=${commit_array[$i]}
        echo -e "${BLUE}推送第 $((i+1)) 个提交: ${commit:0:8}${NC}"
        
        if timeout 300 git push origin $commit:main 2>&1; then
            echo -e "${GREEN}✅ 提交 ${commit:0:8} 推送成功${NC}"
        else
            echo -e "${RED}❌ 提交 ${commit:0:8} 推送失败${NC}"
            return 1
        fi
        
        # 等待一下再推送下一个
        sleep 5
    done
    
    echo -e "${GREEN}✅ 所有提交推送成功！${NC}"
    return 0
}

# 方案4：使用SSH
try_ssh_push() {
    echo -e "${BLUE}方案4: 尝试SSH推送...${NC}"
    
    # 设置SSH URL
    git remote set-url origin "git@github.com:Rsers/PhotoEnhanceAI-web.git"
    
    # 尝试推送
    if timeout 600 git push origin main 2>&1; then
        echo -e "${GREEN}✅ SSH推送成功！${NC}"
        return 0
    else
        echo -e "${RED}❌ SSH推送失败${NC}"
        # 恢复HTTPS URL
        git remote set-url origin "https://github.com/Rsers/PhotoEnhanceAI-web.git"
        return 1
    fi
}

# 主函数
main() {
    # 尝试各种方案
    if try_ipv4_push; then
        echo -e "${GREEN}🎉 推送成功！${NC}"
        exit 0
    fi
    
    if try_proxy_push; then
        echo -e "${GREEN}🎉 推送成功！${NC}"
        exit 0
    fi
    
    if try_ssh_push; then
        echo -e "${GREEN}🎉 推送成功！${NC}"
        exit 0
    fi
    
    if try_batch_push; then
        echo -e "${GREEN}🎉 推送成功！${NC}"
        exit 0
    fi
    
    echo -e "${RED}❌ 所有方案都失败了${NC}"
    echo -e "${YELLOW}💡 建议稍后再试，或者使用: ./auto_push.sh --daemon${NC}"
    exit 1
}

# 运行主函数
main "$@"


