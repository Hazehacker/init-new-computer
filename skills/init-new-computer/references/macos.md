# macOS 盘点与基础配置

## 1. 实际盘点与备份

运行 `zsh scripts/inventory.zsh`，按结果补充只读检查。`system_profiler` 的硬件/电池输出可能带序列号，不将完整输出上传或放进公开交接材料。软件更新只查询；是否升级大版本、何时重启根据用户授权和应用兼容性决定。

私有状态目录放在用户 Library/Application Support 下。备份 `.zshrc`、`.zprofile`、`.gitconfig`、实际要改的 SSH 配置及应用配置；如迁移已有密钥，保留目录 `700`、私钥 `600`。仅在本地保存。偏好域可以用 `defaults export` 留底，同时逐项记录改动前的原值及不存在的键。用户的 dotfiles 管理工具和符号链接优先。

外观、坏点、接口、摄像头、麦克风、Touch ID 和 Apple Diagnostics 分列为硬件实测。需要关机或重启的项目由用户在适当时间执行，不把旧机检查表的“正常”复制为本机结果。

## 2. 系统体验

完整默认配置为 Dock 保持现有位置并自动隐藏；Finder 显示路径栏和状态栏；标准 F1–F12；在用户不需要 Fn 切换输入法时将该操作关闭。可用以下命令，先备份原值，再按授权逐项执行并读回：

```sh
defaults write com.apple.dock autohide -bool true
defaults write com.apple.finder ShowPathbar -bool true
defaults write com.apple.finder ShowStatusBar -bool true
defaults write NSGlobalDomain com.apple.keyboard.fnState -bool true
defaults write NSGlobalDomain AppleFnUsageType -int 0
```

Dock 可通过 `killall Dock` 刷新。Finder 正在复制文件时不重启进程；保留当前窗口并通过界面检查，必要时记录重登后验收。`defaults read` 成功仅证明保存值，不能代替手势或输入法的实际交互验证。

用可用的电脑控制工具检查和设置轻点点击、双指右键、三指拖拽。调整指针速度和力度只依据用户偏好，不猜数值。保留已有微信输入法等选择，避免重复添加；检查快捷键冲突。Finder 侧边栏按文档整理：下载、用户目录、应用程序、文稿、磁盘/外置磁盘、隔空投送等；“最近使用”按用户习惯决定。Touch Bar 相关项只适用于带 Touch Bar 的机型。

若电脑控制权限缺失，读回可通过命令验证的项目，其余 GUI 项单独记录为未验证并继续其他工作。不要通过未经授权的替代方式操作 GUI。

## 3. Homebrew、Git 与终端

1. 查询 Command Line Tools 是否存在；缺失才安装。确认 Homebrew 是否已在 PATH 或标准目录：Apple Silicon `/opt/homebrew`，Intel `/usr/local`。执行当前 [官方安装流程](https://brew.sh/)，安装脚本先下载检查。不要因为缺 sudo 就改成非标准目录安装。
2. 当前进程用 `sudo -n -v` 判断授权；用户在别的终端运行 `sudo -v` 通常不能共享。需要认证时让用户在自己的终端完成官方安装，密码只在系统/终端提示中输入。不要反复重试同一个 sudo 失败，也不要修改 sudoers；继续 SDKMAN、可安装的应用及其他不依赖 Homebrew 的任务。
3. 在 `.zprofile` 中初始化当前芯片对应的 `brew shellenv`。缺失 Homebrew 时使用存在性条件保护，不能让每次开终端报错。已有初始化复用，不重复追加。
4. 从 Homebrew 或官方发行源安装 Ghostty、VS Code；已有应用先验证。添加 `code` 命令路径，保持用户原有 shell 和终端配置。字体大小 14 可作为新配置的候选，不覆盖已有字号和主题。
5. Git 姓名/邮箱优先迁移用户已有配置，缺失时集中询问，不把旧项目日志中的公司邮箱猜成本机身份。保留 SSH 密钥，检查权限和明确目标主机的认证；不要在尚未指定远程目标时连接文档中的所有云主机。

用新登录 shell 验证 `command -v brew git code` 和版本。系统 Git 可用时不因“必备软件”清单就重复安装。

## 4. SDKMAN、Java 17、Maven 与 IDEA

项目锁定的 JDK 发行版、版本和 Maven Wrapper 优先。否则 Java 17 通过 SDKMAN 统一管理，从当前 `sdk list java` 选择支持本机架构的补丁版本。Temurin 是可选默认发行版；文档明确要求 Oracle 特性或已安装 Oracle 时先核对，不静默替换。

macOS 自带 Bash 3.2，较新的 SDKMAN 安装器可能要求 Bash 4；SDKMAN 官方同时支持 Zsh，优先采用下面的形式，无需为了 SDKMAN 等待 Homebrew 安装新 Bash：

```sh
curl -fsSL 'https://get.sdkman.io?rcupdate=false' -o "$sdkman_installer"
# 阅读下载文件并确认来源/范围后执行：
zsh "$sdkman_installer"
```

`sdkman_installer` 指向本次私有下载目录内明确的文件；失败时检查日志和 `~/.sdkman/bin/sdkman-init.sh` 是否实际存在，不能把部分目录当成成功。

先检查已有 `.zshrc` 初始化。初次加入 SDKMAN 块时放在 shell 初始化末尾；更新现有块保持原位，不能移动用户设置而改变执行顺序。若确实需要调整布局，先检查后续内容并显式合并，再验证实际 shell 行为：

```sh
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$SDKMAN_DIR/bin/sdkman-init.sh" ]] && source "$SDKMAN_DIR/bin/sdkman-init.sh"
```

初始化后：

```sh
sdk version
sdk list java
# java17_candidate 必须来自实际列表，不能照抄旧补丁版本。
sdk install java "$java17_candidate"
sdk default java "$java17_candidate"
sdk install maven
```

现有项目有 Maven Wrapper 时以 wrapper 验证构建，不强行用全局最新 Maven。新登录 shell 中检查 `java -version`、`javac -version`、`mvn -v`，确保 Maven 使用同一个 Java 17。实际编译并运行一个临时中文 Java 示例。

若环境继承 `C.UTF-8` 而 `locale -a` 不包含该 locale，Java 17 可能使用 US-ASCII。核对本机支持的 UTF-8 locale，条件修正无效的 `LANG`/`LC_CTYPE`/`LC_ALL`，保留用户已有有效语言设置。用 `mvn -v` 验证 platform encoding 为 UTF-8，不能仅凭 export 成功判断。

IDEA 使用官方支持当前 macOS 的版本和对应架构。SDK 设置为实际 JDK17 路径，语言级别 17/SDK 默认；文档建议的共享编译进程堆为 2000 MB，这与 IDE 自身内存上限不同。主题和字体按用户偏好或明确迁移源恢复。优先 UI 配置；写配置文件时核对当前版本的文件结构并备份，XML 格式检查只能记为“预配置”，首次启动和实际项目构建后才能验证生效。

IDEA 首次登录、许可协议或付费功能由用户在应用内处理，之后继续核对 SDK 与编译结果。
