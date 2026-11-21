"""Integration & unit tests cho vgit."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest import mock

from vgit import cli, config, error_translator, git_runner


class TestVGitFlow(unittest.TestCase):
    def setUp(self) -> None:
        self._orig_cwd = os.getcwd()
        self._tmpdir = tempfile.TemporaryDirectory()
        self.repo_dir = Path(self._tmpdir.name)
        os.chdir(self.repo_dir)

        # Dat user.name/email cuc bo trong env de test khong phu thuoc global config
        self._env_patch = mock.patch.dict(
            os.environ,
            {
                "GIT_AUTHOR_NAME": "Test User",
                "GIT_AUTHOR_EMAIL": "test@example.com",
                "GIT_COMMITTER_NAME": "Test User",
                "GIT_COMMITTER_EMAIL": "test@example.com",
            },
        )
        self._env_patch.start()

    def tearDown(self) -> None:
        self._env_patch.stop()
        os.chdir(self._orig_cwd)
        self._tmpdir.cleanup()

    def _run_cli(self, args: list[str]) -> tuple[int, str, str]:
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(args)
        return code, out.getvalue(), err.getvalue()

    def test_huongdan_and_version(self) -> None:
        code, out, _ = self._run_cli(["huongdan"])
        self.assertEqual(code, 0)
        self.assertIn("vgit batdau", out)

        code_v, out_v, _ = self._run_cli(["--version"])
        self.assertEqual(code_v, 0)
        self.assertIn("0.3.0", out_v)

    def test_help_works_before_git_check(self) -> None:
        with mock.patch("vgit.git_runner.is_git_installed", return_value=False):
            code, out, _ = self._run_cli(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("vgit batdau", out)

    def test_full_local_workflow(self) -> None:
        # 1. batdau
        with mock.patch("vgit.git_runner.ensure_git_identity", return_value=True):
            code, out, _ = self._run_cli(["batdau"])
        self.assertEqual(code, 0)
        self.assertTrue((self.repo_dir / ".git").exists())
        self.assertIn("git init", out)

        # 2. trangthai khi chua co thay doi
        code, out, _ = self._run_cli(["trangthai"])
        self.assertEqual(code, 0)
        self.assertIn("sạch sẽ", out)

        # 3. Tao file moi va xem trangthai
        (self.repo_dir / "hello.txt").write_text("xin chao", encoding="utf-8")
        code, out, _ = self._run_cli(["trangthai"])
        self.assertEqual(code, 0)
        self.assertIn("[File mới]", out)
        self.assertIn("hello.txt", out)

        # 4. luu
        with mock.patch("vgit.git_runner.ensure_git_identity", return_value=True):
            code, out, _ = self._run_cli(["luu", "them file hello"])
        self.assertEqual(code, 0)
        self.assertIn("Đã lưu thay đổi", out)
        self.assertIn("git commit -m", out)

        # 5. lichsu
        code, out, _ = self._run_cli(["lichsu"])
        self.assertEqual(code, 0)
        self.assertIn("them file hello", out)

        # 6. nhanh: tao nhanh moi
        with mock.patch("vgit.ui.ask_yes_no", return_value=True):
            code, out, _ = self._run_cli(["nhanh", "tinh-nang-moi"])
        self.assertEqual(code, 0)
        self.assertIn("tinh-nang-moi", out)
        self.assertEqual(git_runner.get_current_branch(), "tinh-nang-moi")

        # 7. sua file va quaylai
        (self.repo_dir / "hello.txt").write_text("bi hong", encoding="utf-8")
        with mock.patch("vgit.ui.ask_yes_no", return_value=True):
            code, out, _ = self._run_cli(["quaylai", "hello.txt"])
        self.assertEqual(code, 0)
        self.assertEqual((self.repo_dir / "hello.txt").read_text(encoding="utf-8"), "xin chao")

    def test_error_translation_not_a_repo(self) -> None:
        res = git_runner.GitResult(
            returncode=128,
            stdout="",
            stderr="fatal: not a git repository (or any of the parent directories): .git",
            cmd_str="git status",
        )
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            error_translator.translate_and_print_error(res)
        self.assertIn("chưa được khởi tạo Git", err.getvalue())
        self.assertIn("vgit batdau", out.getvalue())

    def test_bridge_config_toggle(self) -> None:
        with tempfile.TemporaryDirectory() as cfg_tmp:
            cfg_file = Path(cfg_tmp) / "config.json"
            with mock.patch("vgit.config.get_config_path", return_value=cfg_file):
                code, _, _ = self._run_cli(["caidat", "bridge", "tat"])
                self.assertEqual(code, 0)
                self.assertFalse(config.load_config()["bridge_mode"])

                code, _, _ = self._run_cli(["caidat", "bridge", "bat"])
                self.assertEqual(code, 0)
                self.assertTrue(config.load_config()["bridge_mode"])

    def test_add_diff_unstage_and_stash_flow(self) -> None:
        with mock.patch("vgit.git_runner.ensure_git_identity", return_value=True):
            code, _, _ = self._run_cli(["batdau"])
        self.assertEqual(code, 0)

        (self.repo_dir / "note.txt").write_text("noi dung", encoding="utf-8")
        code, out, _ = self._run_cli(["them", "note.txt"])
        self.assertEqual(code, 0)
        self.assertIn("Đã chọn note.txt", out)
        self.assertIn("git add", out)

        code, out, _ = self._run_cli(["thaydoi", "da-chon"])
        self.assertEqual(code, 0)
        self.assertIn("note.txt", out)

        code, out, _ = self._run_cli(["bothem", "note.txt"])
        self.assertEqual(code, 0)
        self.assertIn("Đã bỏ", out)

        with mock.patch("vgit.git_runner.ensure_git_identity", return_value=True):
            code, _, _ = self._run_cli(["luu", "mo dau"])
        self.assertEqual(code, 0)

        (self.repo_dir / "draft.txt").write_text("tam thoi", encoding="utf-8")
        code, out, _ = self._run_cli(["vat", "luu", "dang lam"])
        self.assertEqual(code, 0)
        self.assertIn("Đã tạm lưu", out)

        code, out, _ = self._run_cli(["vat", "lay"])
        self.assertEqual(code, 0)
        self.assertIn("Đã lấy lại", out)


if __name__ == "__main__":
    unittest.main()
