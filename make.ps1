# Windows Makefile (PowerShell)
# 使用方式：.\make.ps1 <target>

.PHONY: help install install-dev install-deps test run clean protobuf protobuf-clean

# 默认目标
help:
	@echo "=========================================="
	@echo "Flask 项目 - Windows 构建脚本"
	@echo "=========================================="
	@echo ""
	@echo "可用命令:"
	@echo "  .\make.ps1 install       - 安装生产依赖"
	@echo "  .\make.ps1 install-dev   - 安装开发依赖"
	@echo "  .\make.ps1 install-deps  - 自动检测平台并安装依赖"
	@echo "  .\make.ps1 test          - 运行所有测试"
	@echo "  .\make.ps1 run           - 启动开发服务器"
	@echo "  .\make.ps1 protobuf      - 生成 Protobuf 代码"
	@echo "  .\make.ps1 protobuf-clean- 清理 Protobuf 代码"
	@echo "  .\make.ps1 clean         - 清理所有临时文件"
	@echo ""

# 安装生产依赖
install:
	@echo "安装生产依赖..."
	@.\env\Scripts\Activate.ps1; pip install -r requirements\linux.txt

# 安装开发依赖
install-dev:
	@echo "安装开发依赖..."
	@.\env\Scripts\Activate.ps1; pip install -r requirements\windows.txt

# 自动检测平台并安装依赖
install-deps:
	@echo "自动检测平台并安装依赖..."
	@.\env\Scripts\Activate.ps1; python scripts\install_deps.py

# 运行测试
test:
	@echo "运行测试..."
	@.\env\Scripts\Activate.ps1; pytest tests/ -v

# 启动开发服务器
run:
	@echo "启动开发服务器..."
	@.\env\Scripts\Activate.ps1; python run.py

# 生成 Protobuf 代码
protobuf:
	@echo "生成 Protobuf 代码..."
	@.\env\Scripts\Activate.ps1; python scripts\generate_protobuf_win.py

# 清理 Protobuf 代码
protobuf-clean:
	@echo "清理 Protobuf 代码..."
	@Remove-Item -Recurse -Force app\proto\*_pb2.py -ErrorAction SilentlyContinue
	@Remove-Item -Recurse -Force app\proto\*_pb2.pyi -ErrorAction SilentlyContinue
	@echo "清理完成!"

# 清理所有临时文件
clean:
	@echo "清理临时文件..."
	@Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
	@Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
	@Remove-Item -Recurse -Force .coverage -ErrorAction SilentlyContinue
	@Remove-Item -Recurse -Force htmlcov -ErrorAction SilentlyContinue
	@Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
	@Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
	@echo "清理完成!"
