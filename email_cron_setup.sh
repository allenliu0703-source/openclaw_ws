#!/bin/bash
# 邮件定时任务配置脚本

echo "📧 OpenClaw邮件定时任务配置"
echo "=" * 40

# 检查Python环境
echo "检查Python环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3未安装，请先安装Python3"
    exit 1
fi

# 检查必要的Python库
echo "检查Python库..."
python3 -c "import smtplib, email, json" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  缺少必要的Python库，正在安装..."
    pip3 install --user smtplib email-validator
fi

# 检查邮件脚本
echo "检查邮件脚本..."
if [ ! -f "/home/allen/.openclaw/workspace/simple_email_sender.py" ]; then
    echo "❌ 邮件发送脚本不存在"
    exit 1
fi

if [ ! -f "/home/allen/.openclaw/workspace/send_stock_report_email.py" ]; then
    echo "❌ 股票报告邮件脚本不存在"
    exit 1
fi

echo "✅ 所有脚本检查通过"

# 显示当前cron任务
echo -e "\n当前cron任务："
crontab -l 2>/dev/null || echo "暂无cron任务"

# 配置选项
echo -e "\n请选择定时任务配置："
echo "1. 每日上午9点发送股票报告"
echo "2. 每日上午8点和下午4点发送"
echo "3. 每周一上午9点发送"
echo "4. 自定义时间"
echo "5. 仅配置，不添加定时任务"

read -p "请输入选择 (1-5): " choice

case $choice in
    1)
        CRON_TIME="0 9 * * *"
        TASK_DESC="每日上午9点"
        ;;
    2)
        CRON_TIME="0 8,16 * * *"
        TASK_DESC="每日上午8点和下午4点"
        ;;
    3)
        CRON_TIME="0 9 * * 1"
        TASK_DESC="每周一上午9点"
        ;;
    4)
        read -p "请输入cron表达式 (如: 0 9 * * *): " CRON_TIME
        TASK_DESC="自定义时间: $CRON_TIME"
        ;;
    5)
        echo "跳过定时任务配置"
        CRON_TIME=""
        ;;
    *)
        echo "无效选择，使用默认：每日上午9点"
        CRON_TIME="0 9 * * *"
        TASK_DESC="每日上午9点"
        ;;
esac

if [ -n "$CRON_TIME" ]; then
    # 创建cron任务
    CRON_CMD="$CRON_TIME cd /home/allen/.openclaw/workspace && python3 send_stock_report_email.py daily"
    
    # 添加到crontab
    (crontab -l 2>/dev/null | grep -v "send_stock_report_email.py"; echo "$CRON_CMD") | crontab -
    
    echo -e "\n✅ 定时任务已添加："
    echo "   时间: $TASK_DESC"
    echo "   命令: $CRON_CMD"
fi

# 创建测试脚本
echo -e "\n创建测试脚本..."
cat > /home/allen/.openclaw/workspace/test_email_system.sh << 'EOF'
#!/bin/bash
# 邮件系统测试脚本

echo "📧 邮件系统测试"
echo "=" * 40

# 测试1: 检查配置
echo "1. 检查邮件配置..."
if [ -f ~/.openclaw/email_config.json ]; then
    echo "   ✅ 配置文件存在"
    python3 -c "import json; data=json.load(open('$HOME/.openclaw/email_config.json')); print('   邮箱:', data.get('username')); print('   SMTP服务器:', data.get('smtp_server'))"
else
    echo "   ❌ 配置文件不存在"
    echo "   运行: python3 simple_email_sender.py setup"
fi

# 测试2: 测试发送
echo -e "\n2. 测试邮件发送..."
read -p "   是否发送测试邮件？ (y/n): " send_test
if [ "$send_test" = "y" ]; then
    cd /home/allen/.openclaw/workspace
    python3 simple_email_sender.py test
fi

# 测试3: 测试股票报告
echo -e "\n3. 测试股票报告..."
read -p "   是否测试股票报告邮件？ (y/n): " send_stock
if [ "$send_stock" = "y" ]; then
    cd /home/allen/.openclaw/workspace
    python3 send_stock_report_email.py test
fi

echo -e "\n✅ 测试完成"
EOF

chmod +x /home/allen/.openclaw/workspace/test_email_system.sh

# 创建管理脚本
cat > /home/allen/.openclaw/workspace/manage_email_system.sh << 'EOF'
#!/bin/bash
# 邮件系统管理脚本

echo "📧 邮件系统管理"
echo "=" * 40

echo "请选择操作："
echo "1. 配置邮件账户"
echo "2. 发送测试邮件"
echo "3. 发送股票报告"
echo "4. 查看当前配置"
echo "5. 查看定时任务"
echo "6. 测试整个系统"
echo "7. 退出"

read -p "请输入选择 (1-7): " choice

case $choice in
    1)
        cd /home/allen/.openclaw/workspace
        python3 simple_email_sender.py setup
        ;;
    2)
        cd /home/allen/.openclaw/workspace
        python3 simple_email_sender.py test
        ;;
    3)
        cd /home/allen/.openclaw/workspace
        python3 send_stock_report_email.py daily
        ;;
    4)
        cd /home/allen/.openclaw/workspace
        python3 simple_email_sender.py config
        ;;
    5)
        echo "当前定时任务："
        crontab -l | grep -E "(send_stock|email)"
        ;;
    6)
        ./test_email_system.sh
        ;;
    7)
        echo "再见！"
        ;;
    *)
        echo "无效选择"
        ;;
esac
EOF

chmod +x /home/allen/.openclaw/workspace/manage_email_system.sh

# 显示总结
echo -e "\n🎉 邮件系统配置完成！"
echo "=" * 40
echo ""
echo "📁 创建的文件："
echo "  1. simple_email_sender.py      - 基础邮件发送脚本"
echo "  2. send_stock_report_email.py  - 股票报告邮件脚本"
echo "  3. test_email_system.sh        - 系统测试脚本"
echo "  4. manage_email_system.sh      - 系统管理脚本"
echo "  5. email_setup_guide.md        - 配置指南"
echo ""
echo "🚀 快速开始："
echo "  1. 首先运行配置向导："
echo "     cd /home/allen/.openclaw/workspace"
echo "     python3 simple_email_sender.py setup"
echo ""
echo "  2. 测试邮件发送："
echo "     python3 simple_email_sender.py test"
echo ""
echo "  3. 发送股票报告："
echo "     python3 send_stock_report_email.py daily"
echo ""
echo "  4. 管理邮件系统："
echo "     ./manage_email_system.sh"
echo ""
if [ -n "$CRON_TIME" ]; then
    echo "⏰ 定时任务："
    echo "  已配置 $TASK_DESC 自动发送股票报告"
    echo "  查看定时任务：crontab -l"
fi
echo ""
echo "💡 提示："
echo "  - 确保邮箱已开启SMTP服务"
echo "  - Gmail需要应用专用密码"
echo "  - QQ邮箱需要授权码"
echo "  - 首次使用建议先发送测试邮件"
echo ""
echo "📞 遇到问题？"
echo "  运行测试脚本：./test_email_system.sh"
echo "  或查看指南：cat email_setup_guide.md"

echo -e "\n✅ 所有配置完成！"