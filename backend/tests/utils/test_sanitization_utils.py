import pytest

from app.utils.sanitization_utils import escape_like


@pytest.mark.unit
class TestSanitizationUtils:
    @pytest.mark.anyio
    async def test_escape_like__no_special_chars(self):
        s = "normalstring"
        assert escape_like(s) == "normalstring"

    @pytest.mark.anyio
    async def test_escape_like__with_percent(self):
        s = "100% sure"
        assert escape_like(s) == "100\\% sure"

    @pytest.mark.anyio
    async def test_escape_like__with_underscore(self):
        s = "user_name"
        assert escape_like(s) == "user\\_name"

    @pytest.mark.anyio
    async def test_escape_like__with_backslash(self):
        s = "C:\\path\\to\\file"
        assert escape_like(s) == "C:\\\\path\\\\to\\\\file"

    @pytest.mark.anyio
    async def test_escape_like__with_all_special_chars(self):
        s = "50% off_user\\name"
        assert escape_like(s) == "50\\% off\\_user\\\\name"

    @pytest.mark.anyio
    async def test_escape_like__non_string_input(self):
        non_string_input = 12345
        assert escape_like(non_string_input) == 12345
