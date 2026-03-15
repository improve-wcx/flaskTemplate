# Project Makefile

.PHONY: help protobuf protobuf-clean protobuf-regenerate protobuf-install-deps protobuf-check

# 默认目标
help:
	@echo "可用命令:"
	@echo ""
	@echo "Protocol Buffers:"
	@echo "  make protobuf              - 生成 Protocol Buffers 代码"
	@echo "  make protobuf-clean        - 清理生成的代码"
	@echo "  make protobuf-regenerate   - 重新生成代码"
	@echo "  make protobuf-install-deps - 安装 protobuf 依赖"
	@echo "  make protobuf-check        - 检查 protobuf 环境"
	@echo ""

# 生成 protobuf 代码
protobuf:
	@echo "生成 Protocol Buffers 代码..."
	@./scripts/generate_protobuf.sh

# 清理生成的 protobuf 代码
protobuf-clean:
	@echo "清理生成的 Protocol Buffers 代码..."
	@rm -rf app/proto/*.py
	@rm -rf app/proto/*.pyi
	@rm -rf app/proto/*.pyi.mypy
	@echo "清理完成!"

# 重新生成 protobuf 代码
protobuf-regenerate: protobuf-clean protobuf

# 安装 protobuf 依赖
protobuf-install-deps:
	@echo "安装 Protocol Buffers 依赖..."
	@pip install -r requirements.txt
	@echo "依赖安装完成!"

# 检查 protoc 是否安装
protobuf-check:
	@echo "检查 Protocol Buffers 环境..."
	@if command -v protoc > /dev/null; then \
		echo "✓ protoc 已安装：$$(protoc --version)"; \
	else \
		echo "✗ protoc 未安装"; \
		echo "请运行：sudo apt-get install protobuf-compiler (Ubuntu/Debian)"; \
		echo "或：brew install protobuf (macOS)"; \
		exit 1; \
	fi
	@if python3 -c "import grpc_tools" 2>/dev/null; then \
		echo "✓ grpcio-tools 已安装"; \
	else \
		echo "✗ grpcio-tools 未安装"; \
		echo "请运行：pip install grpcio-tools"; \
		exit 1; \
	fi
	@echo "环境检查完成!"
