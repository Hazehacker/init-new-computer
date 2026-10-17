"""Exercise configuration preservation and skill installation in disposable folders."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "init-new-computer"


class HelpersTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="init-computer-test-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def block(self, target, content, block_id="sdkman"):
        return subprocess.run(
            ["/bin/zsh", str(SKILL / "scripts" / "managed-block.zsh"),
             str(target), block_id, str(content), str(self.base / "backups")],
            capture_output=True, text=True,
        )

    def test_managed_block_preserves_user_lines_and_is_repeatable(self):
        target = self.base / ".zshrc"
        original = "export MY_SETTING=keep\n# user's comment\n"
        target.write_text(original)
        target.chmod(0o640)
        content = self.base / "sdkman.txt"
        content.write_text('export SDKMAN_DIR="$HOME/.sdkman"\n')
        result = self.block(target, content)
        self.assertEqual(result.returncode, 0, result.stderr)
        once = target.read_bytes()
        self.assertTrue(once.startswith(original.encode()))
        self.assertEqual(target.stat().st_mode & 0o777, 0o640)
        snapshots = list((self.base / "backups").iterdir())
        self.assertEqual(len(snapshots), 1)
        self.assertEqual(snapshots[0].read_text(), original)
        result = self.block(target, content)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(target.read_bytes(), once)
        self.assertEqual(len(list((self.base / "backups").iterdir())), 1)

    def test_managed_block_replaces_in_place_without_changing_shell_order(self):
        target = self.base / ".zshrc"
        target.write_text("before\n# BEGIN init-new-computer:sdkman\nold\n"
                          "# END init-new-computer:sdkman\nafter\n")
        content = self.base / "content"
        content.write_text("new\n")
        result = self.block(target, content)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(target.read_text(),
                         "before\n# BEGIN init-new-computer:sdkman\n"
                         "new\n# END init-new-computer:sdkman\nafter\n")

    def test_multiple_blocks_keep_their_order_across_updates(self):
        target = self.base / ".zprofile"
        target.write_text("# BEGIN init-new-computer:brew\nold brew\n"
                          "# END init-new-computer:brew\nuser setting\n"
                          "# BEGIN init-new-computer:locale\nold locale\n"
                          "# END init-new-computer:locale\n")
        brew_content = self.base / "brew"
        brew_content.write_text("new brew\n")
        locale_content = self.base / "locale"
        locale_content.write_text("new locale\n")
        self.assertEqual(self.block(target, brew_content, "brew").returncode, 0)
        self.assertEqual(self.block(target, locale_content, "locale").returncode, 0)
        expected = ("# BEGIN init-new-computer:brew\nnew brew\n"
                    "# END init-new-computer:brew\nuser setting\n"
                    "# BEGIN init-new-computer:locale\nnew locale\n"
                    "# END init-new-computer:locale\n")
        self.assertEqual(target.read_text(), expected)
        self.assertEqual(self.block(target, brew_content, "brew").returncode, 0)
        self.assertEqual(self.block(target, locale_content, "locale").returncode, 0)
        self.assertEqual(target.read_text(), expected)

    def test_unterminated_block_is_rejected_without_truncation(self):
        target = self.base / ".zshrc"
        original = "before\n# BEGIN init-new-computer:sdkman\nuser content\n"
        target.write_text(original)
        content = self.base / "content"
        content.write_text("new\n")
        result = self.block(target, content)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target.read_text(), original)

    def test_symlink_is_not_replaced(self):
        actual = self.base / "dotfiles"
        actual.write_text("keep\n")
        target = self.base / ".zshrc"
        target.symlink_to(actual)
        content = self.base / "content"
        content.write_text("new\n")
        result = self.block(target, content)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(target.is_symlink())
        self.assertEqual(actual.read_text(), "keep\n")

    def test_inventory_does_not_print_alias_credentials(self):
        (self.base / ".zshenv").write_text(
            "alias git='GIT_TOKEN=synthetic-test-value /usr/bin/git'\n"
        )
        result = subprocess.run(
            ["/bin/zsh", str(SKILL / "scripts" / "inventory.zsh")],
            env={**os.environ, "ZDOTDIR": str(self.base)},
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("synthetic-test-value", result.stdout)
        self.assertNotIn("GIT_TOKEN", result.stdout)

    def install(self):
        return subprocess.run(
            ["/bin/zsh", str(ROOT / "scripts" / "install-skill.zsh"),
             str(self.base / "installed-skills")],
            capture_output=True, text=True,
        )

    def test_install_is_self_contained_and_repeatable(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        installed = self.base / "installed-skills" / "init-new-computer"
        self.assertEqual((installed / "SKILL.md").read_bytes(),
                         (SKILL / "SKILL.md").read_bytes())
        self.assertTrue((installed / "references" / "macos.md").is_file())
        self.assertFalse(installed.is_symlink())
        self.assertEqual(self.install().returncode, 0)

    def test_install_preserves_an_existing_customized_skill(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = self.base / "installed-skills" / "init-new-computer" / "SKILL.md"
        manifest.write_text("local customization\n")
        self.assertNotEqual(self.install().returncode, 0)
        self.assertEqual(manifest.read_text(), "local customization\n")

    def test_skill_tracks_current_ai_workspace_tools(self):
        software = (SKILL / "references" / "software.md").read_text()
        migration = (SKILL / "references" /
                     "development-and-migration.md").read_text()
        combined = software + migration
        required = (
            "grill-with-docs",
            "Code-like-me",
            "https://github.com/Hazehacker/code-like-me",
            "Teach",
            "https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff",
            "https://github.com/dietrichgebert/ponytail",
            "https://github.com/study8677/repobrain",
            "https://github.com/alibaba/open-code-review",
        )
        for value in required:
            with self.subTest(value=value):
                self.assertIn(value, combined)
        self.assertNotIn("、grill-me", software.lower())

    def test_skill_tracks_wechat_and_csu_wifi_acceptance(self):
        migration = (SKILL / "references" /
                     "development-and-migration.md").read_text()
        recovery = (SKILL / "references" / "recovery.md").read_text()
        self.assertIn("关闭语音输入", migration)
        self.assertIn("portal.csu.edu.cn", recovery)
        self.assertIn("认证后", recovery)
        self.assertIn("恢复", recovery)


if __name__ == "__main__":
    unittest.main()
