# 失败恢复与继续执行

## 通用恢复

先读错误并确认根因，记录原操作、部分成果、尝试次数和下一步。不因为单项失败停止整个初始化；继续所有不依赖它的项目。

同一根因最多尝试 3 次；只有来源、网络、权限或执行方式有具体变化时才重试。上限用尽或失败需要本人输入时将该项记为 blocked/failed，保留进度，不循环询问或盲目重试。后续用户提供新条件时，从记录的下一条操作恢复。

## 网络与下载

终端沙箱 DNS/网络失败时按当前宿主权限流程申请网络执行权限。现有代理可用于已授权的下载；不要关闭证书验证、修改系统 DNS/代理或改用未知镜像来绕过错误。

保存官方 URL、最终 CDN、版本、架构、预计长度及校验来源。URL 不能包含凭据。下载写入本次私有 downloads 目录，中断保留原文件。curl 示例的 URL/文件变量均由当前任务确定：

```sh
curl --fail --location --connect-timeout 20 --max-time 300 \
  --continue-at - --output "$artifact_path" "$official_url"
```

先检查服务器支持 Range/续传，重试保持同一版本/ETag。服务器不支持时不要破坏旧的部分文件；另用新临时文件重新下载并说明原因。如果用多个分段，必须验证每段 Content-Range、字节长度和同一 ETag，按正确顺序合并后验证整包 SHA-256。分段不得用已完成百分比代替完整校验。

从 Homebrew 元数据或厂商发布信息取得校验值；GUI app 再验证代码签名/系统架构并实际运行。不要移除 quarantine 或关闭 Gatekeeper。没有发布校验值时记录实际可用的官方来源、TLS 和签名证据，不编造校验值。

大下载通过当前工具的异步执行/短等待获取结果，保持有意义的进度说明，不安排未经用户要求的长期自动化。日志只保留必要摘要，成功后清理本次创建且已核对路径的临时包，不删除备份或用户已有文件。

## 常见条件

| 现象 | 根因检查与动作 |
| --- | --- |
| sudo 仍提示密码 | 授权可能绑定别的终端；让用户直接完成所需的官方管理员操作，同时继续独立项目 |
| SDKMAN 报 Bash 4 要求 | Mac Bash 3.2；检查官方支持后用 Zsh 执行，不增加不必要的新 Bash 依赖 |
| `sdk` command not found | 它是 shell function；检查 init 文件和 .zshrc，再以新交互 shell 验证 |
| Maven 使用其他 JDK | 查 PATH/JAVA_HOME/IDEA Maven 设置及 SDKMAN 默认值，保持用户项目要求 |
| Java/Maven 编码 US-ASCII | 查 `locale -a` 和继承的无效 C.UTF-8；条件修正并重新验证实际 encoding |
| Homebrew 提示系统支持有限 | 核对当前 Support Tiers；应用可走厂商受支持发行版，不为安装而自动升级/重启系统 |
| SSH 22 端口失败 | 针对 GitHub 可核对其官方 SSH over HTTPS 443 方案，保留主机密钥校验，避免全局改写 SSH 配置 |
| GUI 权限未授予 | 记录不能交互验证的设置/登录；完成可验证项目，告诉用户具体的权限/操作入口 |
| 付费软件/许可协议待确认 | 应用已安装与账户已激活分开记录，必要时交给本人完成最后步骤 |

SSH 443 的方案仅适用于明确的 GitHub 操作，参考 [GitHub 官方文档](https://docs.github.com/en/authentication/troubleshooting-ssh/using-ssh-over-the-https-port)，不能推广为其他云主机的默认设置。
