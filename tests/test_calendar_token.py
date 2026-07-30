import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from services import send_invite


class CalendarTokenTests(unittest.TestCase):
    def test_inline_env_token_is_persisted_to_a_real_token_file(self):
        token_payload = {"token": "abc123", "refresh_token": "refresh-123"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            with patch.object(send_invite, "BASE_DIR", tmp_path), patch.dict(
                os.environ,
                {"GOOGLE_CALENDER_TOKEN": json.dumps(token_payload)},
                clear=False,
            ):
                resolved_path = send_invite.resolve_token_file()

            self.assertEqual(resolved_path, tmp_path / "token.json")
            self.assertTrue(resolved_path.exists())
            self.assertEqual(json.loads(resolved_path.read_text(encoding="utf-8")), token_payload)


if __name__ == "__main__":
    unittest.main()
