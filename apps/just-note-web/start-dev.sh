#!/bin/bash
# 记一下 Web App - 开发环境启动脚本

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "======================================"
echo "  记一下 Web App - 开发环境"
echo "======================================"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 启动后端
echo "🚀 启动后端服务器..."
cd backend

if [ ! -d "venv" ]; then
    echo "  创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate

if [ ! -f "venv/bin/uvicorn" ]; then
    echo "  安装依赖..."
    pip install -r requirements.txt -q
fi

echo "  启动 API 服务器 (http://localhost:8000)..."
python app/main.py &
BACKEND_PID=$!

cd ..

# 等待后端启动
sleep 2

# 启动前端
echo "🚀 启动前端开发服务器..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "  安装依赖..."
    npm install
fi

echo "  启动开发服务器 (http://localhost:3000)..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "======================================"
echo "  ✅ 开发环境已启动！"
echo "======================================"
echo ""
echo "  前端：http://localhost:3000"
echo "  后端：http://localhost:8000"
echo "  API 文档：http://localhost:8000/docs"
echo ""
echo "  按 Ctrl+C 停止所有服务"
echo "======================================"
echo ""

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo '✅ 已停止所有服务'; exit 0" INT

# 保持脚本运行
wait
