# app/services/__init__.py
# Lazy-export submodules so patch targets like "app.services.agent_service.supabase"
# resolve correctly. Only exposes modules that are already loaded in sys.modules.
import sys

def _lazy_export(name):
    full = f"app.services.{name}"
    if full in sys.modules:
        globals()[name] = sys.modules[full]

for _mod in ("agent_service", "campaign_service", "email_service", "lead_service"):
    _lazy_export(_mod)
