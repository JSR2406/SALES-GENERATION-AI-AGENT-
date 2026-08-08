"""
conftest.py — Session-scoped test configuration.

Permanently patches external dependencies (Supabase, cryptography)
at the sys.modules level before any test module is imported.
This ensures modules like app.core.supabase never attempt to
import the real supabase package (which may have C extension
incompatibilities on the host Python version).
"""
import sys
from unittest.mock import MagicMock, patch

# ── Permanent sys.modules patches ─────────────────────────────────────────────
# These must be registered before any app code is imported.

def _make_supabase_mock():
    mock = MagicMock()

    def table_side_effect(name):
        tbl = MagicMock()

        def chain(*args, **kwargs):
            return tbl

        tbl.select.side_effect = chain
        tbl.insert.side_effect = chain
        tbl.update.side_effect = chain
        tbl.delete.side_effect = chain
        tbl.eq.side_effect = chain
        tbl.order.side_effect = chain
        tbl.execute.return_value = MagicMock(data=[], count=0)
        return tbl

    mock.table.side_effect = table_side_effect
    return mock

_supabase_client = _make_supabase_mock()

# Patch supabase at sys.modules level permanently for this test session
_supabase_module_mock = MagicMock()
_supabase_module_mock.create_client = MagicMock(return_value=_supabase_client)
_supabase_module_mock.Client = MagicMock

sys.modules.setdefault("supabase", _supabase_module_mock)
sys.modules.setdefault("supabase_auth", MagicMock())
sys.modules.setdefault("supabase._async", MagicMock())
sys.modules.setdefault("supabase._async.auth_client", MagicMock())
sys.modules.setdefault("gotrue", MagicMock())

# ── Patch passlib to avoid bcrypt C-extension backend failures ─────────────────
# passlib 1.7 + bcrypt 4.x have an incompatibility that raises MissingBackendError
# in some test environments. We patch the CryptContext to use md5_crypt (pure Python)
# for testing purposes only.
from passlib.context import CryptContext as _CryptContext

class _TestCryptContext:
    """Lightweight stand-in for CryptContext that uses md5_crypt (pure Python)."""
    _ctx = _CryptContext(schemes=["md5_crypt"])

    def __init__(self, *args, **kwargs):
        pass

    def hash(self, secret, **kwargs):
        return self._ctx.hash(secret)

    def verify(self, secret, hash_val, **kwargs):
        try:
            return self._ctx.verify(secret, hash_val)
        except Exception:
            return False

# Patch both the security module's CryptContext reference and the class itself
import app.core.security as _security_mod
_security_mod.pwd_context = _TestCryptContext()
