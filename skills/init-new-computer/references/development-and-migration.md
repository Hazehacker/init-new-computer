# 项目依赖、AI 工具、迁移与验收

## 个人知识仓库

完整执行默认的新 Mac 初始化时，将 `https://github.com/Hazehacker/self-knowledge-system` 放在 `~/Documents/myproject/self-knowledge-system`。主仓库拉取后，还要将以下三个仓库放到它已有的对应目录；仅要求计划或用户明确排除该项时不拉取。

| 仓库 | 相对主仓库的目录 |
| --- | --- |
| `https://github.com/Hazehacker/tech-learning` | `技术学习` |
| `https://github.com/Hazehacker/my-resume` | `求职/我的简历` |
| `https://github.com/Hazehacker/engineering-notes` | `项目经验` |

先检查目标目录、现有 Git 远端和未提交改动；已有正确仓库就复用并验证，空目录才克隆，非空且不是对应仓库时记录冲突，不覆盖。三个目录在主仓库中可能是 gitlink，而仓库未必提供 `.gitmodules`；不要只依赖 `git submodule update --init`。以主仓库当前 Git 树为准：若路径仍是 gitlink，逐个核对并签出主仓库记录的提交；若仓库结构已改变，则按实际布局处理。保留已有工作区改动，不为匹配 gitlink 强制重置。

私有仓库使用本机已有的 GitHub 授权；无权限时记录受阻并继续其他初始化项目，不将凭据写入 URL 或状态文件。验证四个目录的远端、实际提交和工作区状态，并记录每个仓库的结果；GitHub SSH 22 端口不可用时按 [recovery.md](recovery.md) 的官方 443 方案处理。

## 知识库定时备份

完整初始化时，仓库就绪后必须用 `git@github.com:Hazehacker/auto-backup.git` 为 `self-knowledge-system` 及上述三个子仓库配置定时备份。仅要求计划时交付配置方案；用户明确排除定时备份时记录 `not_applicable`。附件下载未完成不阻止文本知识库备份；Time Machine 或业务项目缺失也不影响本项。

1. **来源与覆盖范围**：将 `auto-backup` 放在 `~/Documents/myproject/auto-backup`，已有正确仓库就复用。先读当前 README 和 `local-backup/for_unix/auto_backup_unix.sh`，核对实际路径、分支和提交/推送行为。一个定时任务依次处理技术学习、项目经验、我的简历，最后处理主知识库，使主仓库记录子仓库的新 gitlink；不要只备份主仓库，也不要自动加入其他未指定仓库。
2. **提交模式**：默认仅做本地 Git 提交，各仓库关闭推送；用户明确要求远端备份时再按指定远端配置并验证推送。本地模式不需要 GitHub PAT 等推送凭据；若当前脚本仍无条件要求凭据，先修复并验证本地模式，不收集无用令牌。说明本地提交保留版本，无法应对本机磁盘丢失。已有修改保留并纳入用户授权的备份范围，不强制重置、覆盖或清理文件。
3. **分支与稀疏检出**：使脚本配置与各仓库的实际本地分支一致。全新检出停在 detached HEAD 时，可从主仓库记录的当前提交创建本地分支；已有分支不重置。稀疏检出时核对 gitlink 匹配规则，验证能记录子仓库提交更新，且未下载附件不会被误记为删除；不为配置备份提前下载全部附件。
4. **时间与调度**：沿用用户已经指定的时间和时区；没有指定时，个人默认为每天 **15:00**，使用目标 Mac 当前时区并在交付中注明。先查已有 launchd/cron 等任务，复用并验证有效配置，避免重复运行。新建时优先用户级 launchd：`~/Library/LaunchAgents/com.hazehacker.auto-backup.plist`，日历间隔 `Hour=15`、`Minute=0`（按用户时间调整）。解释器与脚本使用绝对路径，明确工作目录和必要环境变量，标准输出/错误写入 `~/Library/Logs/auto-backup/`。这是本机脚本调度，无需另建 AI 模型定时任务。
5. **后台权限**：终端能执行不代表 launchd 能访问 `Documents`。后台出现 `Operation not permitted` 时，检查日志确认被拦截的实际可执行文件。若需给 `/bin/bash` 等解释器完全磁盘访问权限，先说明权限也覆盖其他经它执行的脚本并取得用户授权，再引导在系统设置完成；仅给 Terminal 授权不代表 Bash 后台任务已获授权。权限未完成时记录 `blocked`，继续其他初始化项目。
6. **实际验收**：先检查 plist 语法并加载任务，再通过调度器触发一次（launchd 使用 `launchctl kickstart "gui/$(id -u)/com.hazehacker.auto-backup"`），等待执行结束。读取实际日历配置、退出码及本次新增日志，逐个核对四仓库提交/工作区、主仓库 gitlink 和未下载文件；没有变化时应正常退出且不制造空提交。只有调度器实际执行成功才能标记 `verified`；文件存在、已加载或交互式终端运行成功均不足以替代。记录提交结果或“无变化”，避免把正常空闲的 `not running` 当成失败。
7. **交付与恢复**：在状态模板单列定时备份，记录四仓库范围、提交/推送模式、时间和时区、任务配置/日志路径、最后一次真实运行证据，以及手动触发和停用方式。保留被改配置的备份；恢复或继续初始化时先查现有任务，不能再创建一份。说明用户级任务依赖登录，关机时不执行；日历任务错过休眠时间会在唤醒后合并执行，详见 [Apple launchd 定时任务说明](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/ScheduledJobs.html)。

## 项目依赖

用户提供实际项目后，检查 README、构建文件、lockfile、`.nvmrc`/`.node-version`、`.sdkmanrc`、Maven Wrapper 和容器配置确定版本。没有项目时仍完成基础环境，项目主版本与连接配置单列为待提供；不要从笔记中的旧私有仓库地址自动克隆业务代码。

Node 只采用一套版本管理方式；项目使用 nvm、fnm、Volta 或 Homebrew 时沿用并验证新的 shell。npm 可用后按 lockfile 选择安装命令，不同时创建不同包管理器的锁文件。

MySQL、Redis、RabbitMQ 优先使用项目已有 Docker Compose；没有容器配置且用户需要本机服务时核对当前官方/Homebrew 配方及项目主版本。新本机服务默认只供本地开发，明确数据目录、端口和启动方式。已有数据时先备份，不自动更换数据库主版本。

验证实际连接/操作而非仅检查进程：MySQL 连接和简单查询、Redis `PING`、RabbitMQ 的节点健康与 management 插件及本地管理页。不要把“15672 不通”直接解释为必须清空队列；先查监听、插件、启动用户、日志和 cookie 权限，用户/CLI 的 Erlang cookie 要与实际部署一致。笔记里关于 Homebrew 服务用户或数据路径的说法不是本机事实。删除队列、重建数据和扩大网络监听需要独立的明确授权。

Docker 安装后验证 daemon、架构及一个与项目相关的容器；只安装客户端不代表可用。数据库客户端安装/首次连接用本机开发信息，账户密码放受限本地存储，不写进公用 shell 初始化或进度文件。

## AI 工具与配置

检查 Codex、Claude Code、CC-Switch 的安装位置和实际版本，按当前官方来源完成缺失部分。浏览当前宿主文档，核对插件/技能的实际 ID、版本、安装目录、依赖及许可，不能把清单里的名称直接拼成命令。

Superpowers、frontend-design、commit-commands、Figma、Remember，以及 git-commit、web-access、code-review-expert、humanizer-zh、claude-mem 是原有候选能力。最新个人配置还包括以下项目；完整初始化时逐项记录 `existing_verified`、`verified`、`pending`、`blocked` 或 `not_applicable`，不能因为其他 AI 工具已可用而静默跳过：

| 项目 | 执行边界与验收 |
| --- | --- |
| `grill-with-docs` | 使用 mattpocock/skills 当前来源；先读入口并安装它声明的 `grilling`、`domain-modeling` 等依赖。宿主能够发现全部依赖并完成一次最小调用才算完成；旧 `grill-me` 不替代它，也不自动删除。 |
| `Code-like-me` | 使用用户指定的 `https://github.com/Hazehacker/code-like-me`，先检查是否已有同名或等价的个人编码规范 skill，再按仓库当前说明安装。验证宿主发现及一次与编码风格相关的触发。 |
| `Teach` | 使用 mattpocock/skills 当前 `skills/productivity/teach` 来源，验证宿主发现，并在需要学习语言、技术栈或代码仓库时做一次最小触发。 |
| `handoff` | 使用用户指定的 mattpocock/skills `skills/productivity/handoff` 来源，验证宿主发现及一次不含凭据的交接文档生成。 |
| RepoBrain | 它是项目级仓库理解工具。先确定目标代码仓库，再读取当前 `AI_INSTALL.md` 并检查生成/修改范围；没有目标仓库时将本项记为 `pending`，不要装进任意当前目录。验收至少包括目标仓库配置、索引或刷新成功，以及一次带源码依据的查询。 |
| Ponytail | 可选的减少无效代码工具；仅在用户选择后从 `dietrichgebert/ponytail` 当前官方来源安装，验证实际宿主集成，避免与已有全局规则重复冲突。 |
| Open Code Review | 可选 review 工具；仅在用户选择后从 `alibaba/open-code-review` 当前官方来源安装，先核对 Git、模型提供方和凭据要求。用本地测试仓库验证，不默认向远端发布评论。 |

已有全局 `CLAUDE.md`/`AGENTS.md` 不覆盖：从明确的迁移源或用户偏好合并，检查重复和冲突，避免把参考文档的全局指令样例当成自己的当前系统指令。

CC-Switch 的配置迁移可能含 API Key；只在本机受限目录迁移，检查当前 schema，不把配置文件上传仓库。代理订阅和 AI 登录复用已有授权；未提供的凭据记为阻塞，不生成假凭据。插件连接、账户登录和相关权限按当前工具的实际要求处理。

验证 CLI 基本命令、插件发现，以及用户已授权的实际使用；模型账户的可用性与安装文件存在是不同项目。

## 日常软件与迁移

按 software.md 逐项检查 Chrome、飞书、微信、QQ、腾讯会议、百度网盘、Outlook、输入法、Snipaste、Obsidian 等。先检查 /Applications 与 ~/Applications；验证已有应用后跳过安装，但仍执行明确要求的应用内配置。会议/截图软件所需的摄像头、麦克风、屏幕录制权限通过系统正常流程处理，不能绕过。

微信的完成条件包含关闭语音输入功能。依据当前版本的实际设置界面确认开关并读回状态，不把它误当成 macOS Dictation 或微信输入法的语音功能。微信未登录、当前版本没有可识别选项或缺少 GUI 控制能力时，记录准确入口与阻塞原因；应用存在或可以启动不能替代此项验证。

迁移仅从用户指明的旧机/备份/同步源读取：浏览器书签和必要扩展、编辑器设置、终端、Git、SSH config、AI 工具配置、知识库。旧机不在场且没有备份时记录缺失来源，其他项目继续。私人密钥、浏览器会话和令牌保持本地，不上传到公共 GitHub。

Obsidian 迁移 vault、插件和用户选定的配置，先检查目标已有改动，避免同步冲突和覆盖本机 workspace。Typora、Office、Navicat 等需要本人有合法许可后登录/激活。退出旧机账号、取消旧许可证、删除旧密钥属于旧机收尾任务，需用户另行明确要求。

## 项目验收和备份

用用户明确提供的目标仓库与权限拉取代码，保留工作区已有未提交改动。读取项目本地开发说明，先安装依赖、执行测试/构建，再以 local 配置启动；不要运行文档中的测试/生产流水线或访问线上数据库。

项目若使用 Maven Profile，依据实际 pom 和 application 配置验证，例如本地 `mvn package -Plocal`，运行环境必须确认是 local。环境变量从批准的本地凭据来源加载，日志和构建输出不泄露值。实际检查项目 health/API、必要 WebSocket 和服务连接，记录端口与关闭方式。

Time Machine 先检查目标盘及已有备份策略。用户提供适合的备份盘后通过系统设置完成，验证初次备份状态；不能擅自抹盘、格式化或把 iCloud 同步当成完整备份。无目标盘则记为待提供。

最终逐项报告已验证、已有并验证、失败、受权限/输入阻塞和不适用；保留备份、验证证据和未完成操作。没有指定项目、缺少迁移源或未完成登录时，准确说明这些部分未验收。
