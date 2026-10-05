# init-new-computer

把新 Mac 的初始化交给 AI：检查机器、备份配置、调整使用体验、安装开发和日常软件、迁移个人设置，最后用实际运行结果验收。

仓库提供一个自包含的 Agent Skill，适用于 Codex，也可放入 Claude Code 的技能目录。当前支持 macOS 的 Apple Silicon 和 Intel；其他操作系统先生成对应计划，不执行 Mac 命令。

## 安装和使用

在新电脑上已有 Git、Codex 或其他支持 Agent Skills 的 AI 工具后，可以直接告诉 AI：

> 从 https://github.com/Hazehacker/init-new-computer 安装 `skills/init-new-computer`，然后使用 `$init-new-computer` 初始化这台 Mac。先检查现状，已有的软件验证后跳过，按默认配置继续执行，把需要我处理的登录和授权集中列出来。

也可以手动安装：

```sh
git clone https://github.com/Hazehacker/init-new-computer.git
cd init-new-computer
zsh scripts/install-skill.zsh
```

默认复制到 `~/.agents/skills/init-new-computer`。脚本可重复执行，不覆盖内容不同的已有技能。安装到其他宿主时传入技能目录，例如：

```sh
zsh scripts/install-skill.zsh "$HOME/.claude/skills"
```

使用支持技能的工具时，输入：

> 使用 `$init-new-computer` 完整初始化这台 Mac，按默认个人 Java 开发配置执行。

> 使用 `$init-new-computer`，这次先生成计划。

> 使用 `$init-new-computer` 继续上次的初始化，检查本机进度记录后从未完成的项目开始。

也可以让 AI 直接读取本仓库的 `skills/init-new-computer/SKILL.md`。在 Codex 中，本地技能发现和 `$技能名` 的用法见[官方技能文档](https://learn.chatgpt.com/docs/build-skills)。

## 覆盖范围

| 阶段 | 内容 |
| --- | --- |
| 盘点与备份 | 系统、芯片、空间、电池、软件和工具；终端、Git、SSH、偏好备份 |
| 系统体验 | 触控板、输入法、功能键、Finder、Dock、常用快捷键 |
| 基础工具 | Homebrew、Git、SSH、Ghostty、VS Code、Zsh/PATH |
| Java 环境 | SDKMAN、Java 17、Maven、IDEA、项目 SDK 和编译内存 |
| 个人知识仓库 | `self-knowledge-system` 放入 `~/Documents/myproject`，并拉取 `tech-learning`、`my-resume`、`engineering-notes` 到对应目录 |
| 项目依赖 | Node/npm、MySQL、Redis、RabbitMQ、Docker、数据库客户端 |
| AI 工具 | Codex、Claude Code、CC-Switch、所需插件和技能 |
| 软件与迁移 | 飞书、Chrome、微信、输入法、QQ、会议、网盘、邮件、截图、Obsidian及个人配置 |
| 验收与备份 | 实际项目构建和本地启动、权限核对、Time Machine 和交接记录 |

软件清单是默认候选配置，AI 会根据你的目标、实际项目和已安装内容决定每一项的动作。当前版本和安装方法在运行时核对官方来源，不把某一次初始化的版本永久写死。

管理员密码、双重验证、许可证激活、硬件实测和未授权的系统重启需要你参与。缺少某项权限时，AI 记录具体原因、继续其他工作，不宣称整机初始化完成。

配置备份、日志、迁移文件和下载放在本机私有状态目录，默认 `~/Library/Application Support/init-new-computer/`，不上传到本仓库。

## 目录和检查

```text
skills/init-new-computer/
  SKILL.md                     AI 入口
  agents/openai.yaml           Codex 展示信息
  references/                  按阶段读取的说明
  assets/status-template.md    本机进度记录模板
  scripts/inventory.zsh        只读盘点
  scripts/managed-block.zsh    带备份的终端配置块更新
scripts/install-skill.zsh      复制技能到本机
tests/test_helpers.py          配置保留与重复执行测试
```

```sh
python3 -m unittest discover -s tests -v
zsh skills/init-new-computer/scripts/inventory.zsh
```

测试只在临时目录操作测试文件，不安装软件或修改真实系统设置。系统自动化的实际验证由 AI 在每台目标电脑上逐项完成。
