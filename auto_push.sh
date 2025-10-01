#!/bin/bash

# 自动推送脚本 - 每隔10分钟尝试推送到远程仓库
# 使用方法: ./auto_push.sh

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目目录
PROJECT_DIR="/home/ubuntu/PhotoEnhanceAI-web"

# 日志文件
LOG_FILE="/home/ubuntu/auto_push.log"

# 函数：记录日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 函数：尝试推送到GitHub
try_push() {
    log "${BLUE}开始尝试推送到GitHub...${NC}"
    
    # 进入项目目录
    cd "$PROJECT_DIR" || {
        log "${RED}错误: 无法进入项目目录 $PROJECT_DIR${NC}"
        return 1
    }
    
    # 设置GitHub URL
    git remote set-url origin "https://github.com/Rsers/PhotoEnhanceAI-web.git"
    
    # 检查是否有待推送的提交
    local ahead_count=$(git rev-list --count origin/main..HEAD 2>/dev/null)
    if [ "$ahead_count" -eq 0 ]; then
        log "${YELLOW}没有待推送的提交${NC}"
        return 0
    fi
    
    log "${BLUE}发现 $ahead_count 个待推送的提交${NC}"
    
    # 多次重试推送（最多5次）
    local retry_count=0
    local max_retries=5
    
    while [ $retry_count -lt $max_retries ]; do
        log "${BLUE}第 $((retry_count + 1)) 次尝试推送...${NC}"
        
        # 先尝试拉取远程更改
        log "${BLUE}同步远程更改...${NC}"
        if timeout 300 git pull origin main 2>&1 | tee -a "$LOG_FILE"; then
            log "${GREEN}✅ 远程更改同步成功${NC}"
        else
            log "${YELLOW}⚠️ 远程同步失败，继续尝试推送${NC}"
        fi
        
        # 使用timeout避免长时间卡住
        if timeout 300 git push origin main 2>&1 | tee -a "$LOG_FILE"; then
            log "${GREEN}✅ 推送成功！${NC}"
            
            # 推送标签
            if git tag -l | grep -q "v1.0"; then
                log "${BLUE}推送标签 v1.0...${NC}"
                if timeout 300 git push origin v1.0 2>&1 | tee -a "$LOG_FILE"; then
                    log "${GREEN}✅ 标签推送成功！${NC}"
                else
                    log "${YELLOW}⚠️ 标签推送失败，但主分支推送成功${NC}"
                fi
            fi
            
            return 0
        else
            log "${RED}❌ 第 $((retry_count + 1)) 次推送失败${NC}"
            retry_count=$((retry_count + 1))
            
            if [ $retry_count -lt $max_retries ]; then
                log "${YELLOW}等待30秒后重试...${NC}"
                sleep 30
            fi
        fi
    done
    
    log "${RED}❌ 达到最大重试次数，推送失败${NC}"
    return 1
}

# 函数：检查网络连接
check_network() {
    log "${BLUE}检查网络连接...${NC}"
    
    # 检查GitHub连接
    if ping -c 1 -W 5 github.com >/dev/null 2>&1; then
        log "${GREEN}✅ GitHub连接正常${NC}"
        return 0
    else
        log "${RED}❌ GitHub连接失败${NC}"
        return 1
    fi
}

# 函数：切换镜像源
switch_mirror() {
    local mirror_url="$1"
    log "${BLUE}切换到镜像源: $mirror_url${NC}"
    
    cd "$PROJECT_DIR" || return 1
    git remote set-url origin "$mirror_url"
    
    if try_push; then
        log "${GREEN}✅ 使用镜像源推送成功！${NC}"
        return 0
    else
        log "${RED}❌ 镜像源推送也失败${NC}"
        return 1
    fi
}

# 主函数
main() {
    log "${GREEN}🚀 启动自动推送脚本${NC}"
    log "${BLUE}项目目录: $PROJECT_DIR${NC}"
    log "${BLUE}日志文件: $LOG_FILE${NC}"
    log "${BLUE}检查间隔: 10分钟${NC}"
    
    # 创建日志文件
    touch "$LOG_FILE"
    
    local attempt=1
    local max_attempts=100  # 最多尝试100次（约16.7小时）
    
    while [ $attempt -le $max_attempts ]; do
        log "${YELLOW}=== 第 $attempt 次尝试 ===${NC}"
        
        # 检查网络连接
        if ! check_network; then
            log "${YELLOW}网络连接异常，等待10分钟后重试...${NC}"
            sleep 600
            ((attempt++))
            continue
        fi
        
        # 尝试推送
        if try_push; then
            log "${GREEN}🎉 推送成功！脚本结束${NC}"
            exit 0
        fi
        
        # 如果失败，尝试不同的镜像源
        log "${BLUE}尝试使用不同的镜像源...${NC}"
        
        # 镜像源列表
        local mirrors=(
            "https://ghproxy.com/https://github.com/Rsers/PhotoEnhanceAI-web.git"
            "https://github.com.cnpmjs.org/Rsers/PhotoEnhanceAI-web.git"
            "https://hub.fastgit.xyz/Rsers/PhotoEnhanceAI-web.git"
            "https://github.com/Rsers/PhotoEnhanceAI-web.git"
        )
        
        for mirror in "${mirrors[@]}"; do
            if switch_mirror "$mirror"; then
                log "${GREEN}🎉 使用镜像源推送成功！脚本结束${NC}"
                exit 0
            fi
        done
        
        # 恢复原始URL
        git remote set-url origin "https://github.com/Rsers/PhotoEnhanceAI-web.git"
        
        log "${YELLOW}所有尝试都失败了，等待10分钟后重试...${NC}"
        log "${BLUE}下次尝试时间: $(date -d '+10 minutes' '+%Y-%m-%d %H:%M:%S')${NC}"
        
        sleep 600  # 等待10分钟
        ((attempt++))
    done
    
    log "${RED}❌ 达到最大尝试次数，脚本结束${NC}"
    exit 1
}

# 信号处理：优雅退出
cleanup() {
    log "${YELLOW}收到退出信号，正在清理...${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 检查是否在后台运行
if [ "$1" = "--daemon" ]; then
    log "${BLUE}以守护进程模式运行${NC}"
    nohup "$0" >/dev/null 2>&1 &
    echo "脚本已在后台启动，PID: $!"
    echo "查看日志: tail -f $LOG_FILE"
    exit 0
fi

# 运行主函数
main "$@"
