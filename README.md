# AutoEmailWarn / 邮件告警与通知工具
[![PyPI version](https://img.shields.io/pypi/v/autoemailwarn.svg)](https://pypi.org/project/autoemailwarn/) [![Python versions](https://img.shields.io/pypi/pyversions/autoemailwarn.svg)](https://pypi.org/project/autoemailwarn/) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE) [![Downloads](https://static.pepy.tech/badge/autoemailwarn)](https://pepy.tech/project/autoemailwarn)

A lightweight Python helper to send emails and automatically notify on uncaught exceptions. Suitable for scripts, services, batch jobs, and long-running processes.

一个轻量的 Python 邮件工具，支持主动发送邮件，并可在程序发生未捕获异常时自动告警。适用于脚本、服务、批处理任务以及长时间运行的进程。

---

## Features | 功能特性
- Send plain text emails with minimal code
- Global exception notifications via sys.excepthook
- Class-style notifier similar to logger (EmailNotifier)
- Environment variable based configuration
- RFC-compliant headers (From/To) with proper display name encoding

- 纯文本邮件快速发送
- 通过 sys.excepthook 实现全局异常自动告警
- 类似 logger 的告警器类（EmailNotifier），入口处一次初始化即可
- 支持通过环境变量启用与配置
- From/To 头部合法构造，显示名编码符合 RFC 规范

---

## Requirements | 运行环境
- Python >= 3.8
- Works on Windows/macOS/Linux
- If using QQ Mail: enable SMTP service and use an app-specific password (authorization code)

- Python >= 3.8
- 支持 Windows/macOS/Linux
- QQ 邮箱用户：需开启“SMTP服务”，并使用授权码作为密码

---

## Installation | 安装
You can install from PyPI or from local source.

你可以通过 PyPI 安装，或从本地源码安装。

- Option A: Install from PyPI (recommended)
  - 通过 PyPI 安装（推荐）

```
pip install autoemailearn
```

- Option B: Install from source (PEP 517)
  - 源码直接安装（PEP 517）

```
# In project root 在项目根目录
pip install .
```

- Option C: Build then install
  - 先构建，再安装

```
pip install build
python -m build
pip install dist/*.whl
```

---

## Quick Start | 快速开始
### 1) Send a simple email | 发送一封简单邮件
```python
from autoemailwarn import EmailSender

# 函数示例：发送纯文本邮件
# Function example: send a plain text email
sender = "your_account@qq.com"              # 发件人（需与登录账号一致）
auth_code = "your_smtp_app_password"       # 授权码/应用专用密码
receivers = ["to1@example.com", "to2@example.com"]

mailer = EmailSender(sender=sender, auth_code=auth_code)
mailer.send_text(
    receivers=receivers,
    subject="Job Finished",
    content="The job is done.",
    from_name="My Service",
    # to_names=["Zhang San", "Li Si"],  # 可选：若使用，必须与 receivers 等长
)
```

### 2) Global exception notification | 全局异常自动告警
Use EmailNotifier at your entry point. It registers a global exception hook to send stack-trace emails on uncaught exceptions.

在入口处初始化 EmailNotifier，它会注册未捕获异常钩子，程序出现未捕获异常时自动发送包含堆栈的邮件。

```python
from autoemailwarn import EmailNotifier

# 程序入口（例如 main.py）
# Program entry (e.g., main.py)

def main() -> None:
    # 初始化一次即可 Initialize once
    notifier = EmailNotifier(
        sender="your_account@qq.com",
        auth_code="your_smtp_app_password",
        receivers=["to@example.com"],
        subject="程序异常退出通知",      # 默认主题，可覆盖
        from_name="我的服务",            # 可选显示名
        # to_names=["张三"],            # 可选：若使用，必须与 receivers 等长
        smtp_host="smtp.qq.com",
        smtp_port=465,
        use_ssl=True,
        timeout=10,
        enable_exception_hook=True,    # 注册未捕获异常钩子
    )

    # 主动发送一封通知（可选）
    notifier.send("启动成功", subject="启动提醒")

    # 故意触发一个未捕获异常（测试自动告警）
    raise RuntimeError("测试：自动异常告警")

if __name__ == "__main__":
    main()
```

### 3) Enable via environment variables | 通过环境变量启用
You can enable exception notifications without hardcoding credentials.

无需在代码中硬编码账号信息，可通过环境变量启用异常告警。

```python
from autoemailwarn import enable_exception_email_from_env

def main() -> None:
    # 读取环境变量并启用异常自动告警 Enable via env vars
    enable_exception_email_from_env()  
    # Your business logic 你的业务逻辑
    ...
```

PowerShell example (Windows):
PowerShell 示例（Windows）：
```
$env:AUTOEMAILWARN_ENABLE="1"
$env:AUTOEMAILWARN_SENDER="your_account@qq.com"
$env:AUTOEMAILWARN_AUTH_CODE="your_smtp_app_password"
$env:AUTOEMAILWARN_RECEIVERS="to1@example.com,to2@example.com"
$env:AUTOEMAILWARN_SUBJECT="程序异常退出通知"
$env:AUTOEMAILWARN_FROM_NAME="我的服务"
$env:AUTOEMAILWARN_TO_NAMES="张三,李四"  # 可选：若使用，数量必须与 RECEIVERS 对齐
$env:AUTOEMAILWARN_SMTP_HOST="smtp.qq.com"
$env:AUTOEMAILWARN_SMTP_PORT="465"
$env:AUTOEMAILWARN_USE_SSL="1"
$env:AUTOEMAILWARN_TIMEOUT="10"
```

---

## API Overview | API 概览
- EmailSender
  - send_text(receivers, subject, content, from_name=None, to_names=None)
- EmailNotifier
  - __init__(..., enable_exception_hook=True)
  - send(content, subject=None, receivers=None, from_name=None, to_names=None)
  - notify_exception(exc_info=None, subject=None, extra=None)
  - enable_exception_hook() / disable_exception_hook()
- enable_exception_email(...)
- enable_exception_email_from_env(prefix="AUTOEMAILWARN_")

参数说明（部分要点）：
- sender: 发件邮箱；必须与 SMTP 登录账号一致。
- auth_code: 授权码/应用专用密码（QQ 邮箱需要先开启 SMTP 服务）。
- receivers: 收件人列表。
- from_name/to_names: 显示名；如使用 to_names，长度必须与 receivers 一致，否则请置为 None 或不要传入。
- smtp_host/smtp_port/use_ssl/timeout: SMTP 服务器配置。

---

## Best Practices | 最佳实践
- Initialize EmailNotifier once at your application entry (like a logger)
- Avoid catching all exceptions globally if you want uncaught exception notifications to work
- Do not include angle brackets in from_name/to_names; only display name is needed
- Never commit credentials; prefer environment variables or secret managers

- 在应用入口处初始化一次 EmailNotifier（类似 logger）
- 若需要自动异常告警，不要在最外层捕获并吞掉所有异常
- from_name/to_names 中不要包含尖括号，仅放显示名
- 不要提交账号与授权码到仓库，推荐使用环境变量或密钥管理方案

---

## Troubleshooting | 故障排查
- 550 or header errors: ensure sender equals your login account; our library builds RFC-compliant From/To headers and encodes display names properly
- to_names length mismatch: if provided, it must match receivers length (or set to None)
- Connection issues: check firewall/proxy; try SSL(465) or STARTTLS(587) as appropriate
- QQ Mail: enable SMTP service and use authorization code instead of the login password

- 550 或头部错误：确保 sender 与登录账号一致；库内部已按 RFC 构造 From/To 并正确编码显示名
- to_names 数量不一致：若使用，长度必须与 receivers 完全一致（或置为 None）
- 连接异常：检查防火墙/代理；根据需要尝试 SSL(465) 或 STARTTLS(587)
- QQ 邮箱：请先开启 SMTP 服务，并使用授权码而非登录密码

---

## Project Structure | 项目结构（简要）
```
autoemailwarn/
  ├─ __init__.py
  ├─ email_sender.py        # 发送纯文本邮件的核心
  └─ crash_notifier.py      # 异常告警 & EmailNotifier
main.py                      # 示例入口（基于 EmailNotifier）
pyproject.toml               # 构建配置（setuptools backend）
```
