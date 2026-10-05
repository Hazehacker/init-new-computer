---
name: init-new-computer
description: Use when initializing a new Mac, setting up a macOS development and personal workspace, migrating settings to another Mac, or resuming incomplete computer setup. Also applies to 新电脑初始化、Mac 环境配置 and 迁移开发环境; not to wiping an old computer or deploying cloud infrastructure.
---

# 初始化新电脑

把用户指定的新 Mac 配置成可用的个人和开发工作环境，维护可以继续执行的本机进度。当前支持 macOS；检测到 Windows/Linux 时先提出对应计划，明确 Mac 脚本不适用。

## 先确定范围

读取用户提供的文档和当前目标，区分参考资料与当前授权。只要求计划时仅做只读盘点并交付计划；已要求执行时持续完成授权范围，不在每个阶段重新确认。用户已有计划时沿用，不重新规划已完成工作。

没有其他偏好时，以 [software.md](references/software.md) 的个人 Java 开发配置为候选。保留用户现有选择；项目依赖、付费产品和订阅需要明确用途。先集中询问影响配置的缺失信息，同时推进独立项目。个人知识仓库按下述固定位置处理；其他项目路径或迁移源未知时不要编造，记为待用户提供。

## 本机记录与备份

1. 用 `zsh scripts/inventory.zsh` 盘点实际机器，不拿旧机截图作为检测结果。
2. 在 `~/Library/Application Support/init-new-computer/` 建立权限为 `700` 的私有状态目录。用 [status-template.md](assets/status-template.md) 创建 `status.md`；继续任务时先读该文件，再检查已记录的结果是否仍成立。
3. 修改前在此目录备份相关文件和原值，记录不存在的配置项。备份终端、Git/SSH、偏好，以及实际会改动的应用配置。保持私钥权限；备份和迁移资料留在本机，日志不包含密码、令牌、私钥内容或带凭据的 URL。
4. 每完成一项就记录动作、版本/路径、验证命令与结果、下一步。状态使用 `verified`、`existing_verified`、`pending`、`blocked`、`failed`、`not_applicable`。失败记录尝试次数和下载进度；完成只以验证结果为依据。

## 按依赖推进

| 任务 | 读取的资料 | 关键验证 |
| --- | --- | --- |
| 系统、Finder、Dock、输入法与触控板 | [macos.md](references/macos.md) | 偏好读回；需要 GUI 的项目检查实际界面 |
| Homebrew、Git/SSH、终端、Java/IDEA | [macos.md](references/macos.md) | 新登录 shell；Java 编译；Maven JDK/UTF-8 |
| 个人知识仓库及三个子仓库 | [development-and-migration.md](references/development-and-migration.md) | 路径、远端、主仓库记录的提交及工作区状态 |
| 数据库、Node、容器、AI 工具、迁移 | [development-and-migration.md](references/development-and-migration.md) | 本地服务/工具可用；迁移后实际使用 |
| 软件候选、可选项和官方来源 | [software.md](references/software.md) | 安装架构、签名、命令/应用实际运行 |
| 下载中断、sudo、网络、UI 权限失败 | [recovery.md](references/recovery.md) | 根因、受影响项目、已做的有限重试 |

脚本路径均相对于本 skill 目录；先确定完整目录，再调用其解释器。脚本仅覆盖可重复的机械操作，其他工作用当前可用的文件、终端、官方连接器或电脑控制工具完成。

更新 `.zprofile`/`.zshrc` 时先处理已有初始化，避免再添加第二套。需要新增或更新本技能维护的内容时，将配置保存到临时内容文件，调用：

```sh
zsh scripts/managed-block.zsh "/absolute/path/.zshrc" sdkman "/absolute/path/content.txt" "/absolute/path/private-backups"
```

脚本在原位替换已有块，保留用户内容和执行顺序、备份原文件，重复执行无额外变化，并拒绝格式损坏的标记和符号链接。若 dotfiles 使用符号链接，先确定实际来源及管理方式，再按用户原有流程修改。

## 完成条件

执行完整计划，遇到阻塞继续不依赖该条件的项目。Java 17 由一个版本管理器维护；SDKMAN 在 Mac 上优先用 Zsh，避免 Bash 3.2 造成无谓的 Homebrew 依赖。已安装的软件先验证，失败再修复；不自动升级已有数据库或替换发行版。

文档中的离职清理、RabbitMQ 清空数据、云端部署和全局 AI 指令样例属于其他任务；不从参考文档扩大本次范围。参考中的明文凭据不复制到公共仓库或通用配置。

对安装命令和软件版本核对当前官方来源。保留部分下载并优先续传；完整校验与应用签名通过后才安装。重试按 [recovery.md](references/recovery.md) 的限制执行。

最终交付已验证结果、备份和本机状态路径，以及每个阻塞项的原因和准确下一步。项目构建/启动、GUI 首次设置、登录或备份未验证时分别列为未完成，不能以软件文件存在代替整机完成。
