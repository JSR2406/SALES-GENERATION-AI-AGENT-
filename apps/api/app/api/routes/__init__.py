# app/api/routes/__init__.py
# This file intentionally imports submodules to make them accessible
# as attributes of the 'routes' package. This is required for
# unittest.mock.patch to resolve targets like "app.api.routes.auth.supabase".
# These imports are safe because they have already been loaded by the
# app's router.py before any tests execute.
import importlib, sys

def _lazy_export(name):
    full = f"app.api.routes.{name}"
    if full in sys.modules:
        globals()[name] = sys.modules[full]

for _mod in ("auth", "campaigns", "leads", "dashboard", "webhooks", "agent_logs"):
    _lazy_export(_mod)
