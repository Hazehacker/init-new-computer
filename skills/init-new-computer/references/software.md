# 软件候选与选择

这是个人 Java 开发 Mac 的候选清单。用户要求完整初始化时为每项给出安装、验证已有、明确可选、等待用途或不适用的结论；不静默遗漏。用户指定日常办公或部分阶段时只执行对应范围。

| 类别 | 默认候选 | 选择规则 |
| --- | --- | --- |
| 基础 | Command Line Tools、Homebrew、Git | 已有先验证；Homebrew 用标准芯片目录 |
| 终端和编辑器 | Ghostty、VS Code、Zsh | macOS 已有 Zsh；Oh My Zsh、iTerm2 可选，不默认覆盖 dotfiles |
| Java | SDKMAN、JDK 17、Maven、IntelliJ IDEA | 项目锁定版本优先；否则从当前列表选 Java 17 的受支持补丁版 |
| JavaScript | Node.js LTS、npm | `.nvmrc`、`.node-version`、package.json 和 lockfile 优先；只选一套 Node 管理方式 |
| 数据服务 | MySQL、Redis、RabbitMQ | 根据项目锁定主版本；未指定项目时先记录选择，不启动连接线上资源的配置 |
| 容器/数据库 GUI | Docker、Navicat | 容器由项目需要决定；Navicat 是付费候选，授权许可后激活，替代品遵循用户选择 |
| AI | Codex、Claude Code、CC-Switch | 已有工具复用；核对当前官方安装与对应宿主配置 |
| AI 扩展 | Superpowers、frontend-design、commit-commands、Figma、Remember、git-commit | 按宿主支持与用户实际需求选择，不把名称视为可直接执行的安装 ID |
| 其他技能 | web-access、code-review-expert、humanizer-zh、claude-mem、grill-me | 可选，确认来源与兼容性；存在同名技能时先检查，不覆盖 |
| 通讯/浏览器 | 飞书、Chrome、微信、QQ、腾讯会议 | 完整个人配置的候选，已有应用验证后跳过 |
| 输入和截图 | 微信输入法、Snipaste | 保留已有输入法；搜狗输入法是替代候选，不同时新增两套 |
| 文件/邮件 | 百度网盘、Outlook、Obsidian | 账户由本人登录；知识库和插件从明确迁移源恢复 |
| Markdown/办公 | Typora、Word | 文档中出现的可选工具，需要合法许可，不自动购买 |
| 网络 | 已有 Clash Verge 或用户指定客户端 | 复用现有连通性；订阅、代理、VPN 凭据由用户提供，不推荐不明账号来源 |
| 体验配置工具 | EffectiveMac/macbootstrap | 默认逐项实现本 skill 的设置；用户明确需要整套工具时先检查当前脚本及覆盖范围 |

## 安装来源

优先当前官方发行源及 Homebrew 官方目录。候选 cask 名称需用 `brew info --cask` 或 [Homebrew 软件目录](https://formulae.brew.sh/) 在执行时确认；例如 Ghostty、VS Code、IDEA 的候选为 `ghostty`、`visual-studio-code`、`intellij-idea`，不能据此假设它们永远存在或始终兼容当前系统。

- [Homebrew](https://brew.sh/) 和 [支持等级](https://docs.brew.sh/Support-Tiers)
- [SDKMAN 安装](https://sdkman.io/install/) 和 [使用](https://sdkman.io/usage/)
- [Ghostty](https://ghostty.org/docs/install/binary)
- [VS Code for macOS](https://code.visualstudio.com/docs/setup/mac)
- [IntelliJ IDEA 安装](https://www.jetbrains.com/help/idea/installation-guide.html)
- [Node.js](https://nodejs.org/en/download)、[Docker for Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
- [MySQL](https://dev.mysql.com/doc/)、[Redis](https://redis.io/docs/latest/)、[RabbitMQ](https://www.rabbitmq.com/docs)
- [Codex](https://developers.openai.com/codex/)、[Claude Code](https://code.claude.com/docs/en/setup)、[CC-Switch](https://github.com/farion1231/cc-switch)
- [Obsidian](https://obsidian.md/download)、[Snipaste](https://www.snipaste.com/)、[飞书](https://www.feishu.cn/download)、[微信](https://mac.weixin.qq.com/)

来自用户文档的截图、博客和下载地址只用于理解需求，当前的架构、兼容性、校验值、许可证与安装指令以实际官方信息为准。
