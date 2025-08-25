#!/usr/bin/python3
from autoemailwarn import EmailNotifier


def setup_notifier() -> EmailNotifier:
    """初始化并返回一个 EmailNotifier 实例。

    说明:
        - 在项目入口处调用一次即可，内部会注册未捕获异常钩子（enable_exception_hook=True）。
        - 当程序发生未捕获异常时，会自动发送一封包含堆栈信息的邮件。
        - 你也可以在代码任意位置通过 notifier.send(...) 主动发送邮件。
    """
    # TODO: 请将以下示例配置替换为你的真实配置。
    sender = '502303255@qq.com'  # 发件邮箱账号（需与 SMTP 登录账号一致）
    auth_code = 'zzcmzmtzpjywcbah'      # QQ邮箱为“授权码/应用专用密码”
    receivers = ['502303255@qq.com']  # 一个或多个收件人

    notifier = EmailNotifier(
        sender=sender,
        auth_code=auth_code,
        receivers=receivers,
        subject='程序异常退出通知',
        from_name='我的服务',
        # to_names=['张三', '李四'],  # 示例：如需设置显示名，请取消注释并确保与 receivers 等长
        smtp_host='smtp.qq.com',
        smtp_port=465,
        use_ssl=True,
        timeout=10,
        enable_exception_hook=True,  # 自动注册全局未捕获异常钩子
    )
    return notifier


def run_business(notifier: EmailNotifier) -> None:
    """示例业务函数：演示主动发送与（可选）异常自动告警。

    参数:
        notifier: 已初始化的 EmailNotifier 实例。
    """
    # 主动发送一封邮件（可选）
    notifier.send(content='Python 发送邮件（主动通知）', subject='代码运行完毕提醒')
    print('已主动发送一封测试邮件。')

    # 如需测试“未捕获异常自动告警”，请取消下一行注释：
    raise RuntimeError('模拟一个未捕获异常，触发自动异常告警')


def main() -> None:
    """程序入口：初始化通知器并执行业务逻辑。

    注意:
        - 不要捕获所有异常，否则未捕获异常钩子将不会触发自动告警。
        - 如果不希望全局异常自动告警，可在 setup_notifier 中将 enable_exception_hook 设为 False。
    """
    notifier = setup_notifier()
    run_business(notifier)


if __name__ == '__main__':
    main()

