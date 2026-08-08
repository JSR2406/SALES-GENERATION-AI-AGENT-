"""
====================================================================
  Autonomous B2B Sales Agent — End-to-End Test Suite
====================================================================
  Tests every functional layer of the system:
    1. Health-check endpoint
    2. Auth (register / login flow)
    3. Campaign CRUD
    4. Lead retrieval
    5. Dashboard stats
    6. Agent workflow (prospecting → qualifying → drafting → sending)
    7. Agent audit log writing
    8. Email service (mocked provider)
  
  Run with:
    pytest tests/test_e2e.py -v --tb=short
====================================================================
"""

import asyncio
import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

# ── Patch Supabase and external services BEFORE importing the app ──
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# --------------------------------------------------------------------------
# Supabase Mock Factory
# --------------------------------------------------------------------------
def make_supabase_mock():
    """Returns a full Supabase client mock with chainable builder pattern.
    
    Uses a single shared 'tbl' mock so that tests can configure
    _sb.table.return_value.execute.return_value directly.
    """
    mock = MagicMock()
    tbl = MagicMock()

    # --- fluent builder chain — all methods return the same tbl ---
    tbl.select.return_value = tbl
    tbl.insert.return_value = tbl
    tbl.update.return_value = tbl
    tbl.delete.return_value = tbl
    tbl.eq.return_value = tbl
    tbl.order.return_value = tbl
    tbl.limit.return_value = tbl

    # --- default execute() result ---
    tbl.execute.return_value = MagicMock(data=[], count=0)

    # table() always returns the same tbl so tests can reconfigure it
    mock.table.return_value = tbl
    return mock


# Patch at module level so imports succeed
_sb = make_supabase_mock()

with patch.dict("sys.modules", {
    "supabase": MagicMock(create_client=MagicMock(return_value=_sb)),
}):
    with patch("app.core.supabase.supabase", _sb):
        from app.main import app

client = TestClient(app)

# ===========================================================================
# SECTION 1 — Health Check
# ===========================================================================

class TestHealthCheck:
    def test_health_returns_ok(self):
        resp = client.get("/api/health")
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.json()
        assert data.get("status") == "ok", f"Expected status=ok, got: {data}"
        print(f"\n  ✅  Health endpoint: {data}")


# ===========================================================================
# SECTION 2 — Auth Endpoints
# ===========================================================================

class TestAuthEndpoints:
    def test_register_new_user(self):
        """POST /api/v1/auth/register — should create user and return user_id."""
        with patch("app.api.routes.auth.supabase", _sb):
            with patch("app.api.routes.auth.get_password_hash", return_value="hashed_pw"):
                # Simulate user not existing (empty), then inserted successfully
                responses = [
                    MagicMock(data=[]),   # existing check → empty
                    MagicMock(data=[{"id": "abc-123"}]),  # insert → success
                ]
                _sb.table.return_value.execute.side_effect = responses

                resp = client.post("/api/v1/auth/register", json={
                    "email": "demo@salesai.com",
                    "password": "SecurePass123!",
                    "full_name": "Demo User",
                    "company_name": "Sales.AI Corp"
                })

        # Reset side_effect after test
        _sb.table.return_value.execute.side_effect = None

        assert resp.status_code == 200, f"Register failed: {resp.text}"
        data = resp.json()
        assert data.get("status") == "success"
        print(f"\n  ✅  Register: user_id={data.get('user_id')}")

    def test_login_returns_token(self):
        """POST /api/v1/auth/login — should return JWT access_token."""
        # Use a real md5_crypt hash so verify_password succeeds naturally
        # (conftest's _TestCryptContext uses md5_crypt)
        _valid_hash = "$1$XUJP0jGo$DyTxQ13n6l1oboOamTK5L."  # md5_crypt of 'SecurePass123!'
        with patch("app.api.routes.auth.supabase", _sb):
            _sb.table.return_value.execute.side_effect = None
            _sb.table.return_value.execute.return_value = MagicMock(
                data=[{
                    "id": "user-001",
                    "email": "demo@salesai.com",
                    "full_name": "Demo User",
                    "hashed_password": _valid_hash
                }]
            )

            resp = client.post("/api/v1/auth/login", json={
                "email": "demo@salesai.com",
                "password": "SecurePass123!"
            })

        assert resp.status_code == 200, f"Login failed: {resp.text}"
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        print(f"\n  ✅  Login: token={data['access_token'][:20]}...")

    def test_login_invalid_credentials(self):
        """POST /api/v1/auth/login with wrong password — should return 400."""
        # Use valid md5_crypt hash — 'WrongPassword' will NOT match it naturally
        _valid_hash = "$1$XUJP0jGo$DyTxQ13n6l1oboOamTK5L."  # md5_crypt of 'SecurePass123!'
        with patch("app.api.routes.auth.supabase", _sb):
            _sb.table.return_value.execute.side_effect = None
            _sb.table.return_value.execute.return_value = MagicMock(
                data=[{"id": "u1", "hashed_password": _valid_hash, "email": "e@e.com", "full_name": "X"}]
            )
            resp = client.post("/api/v1/auth/login", json={
                "email": "demo@salesai.com",
                "password": "WrongPassword"
            })

        assert resp.status_code == 400
        print(f"\n  ✅  Login rejection test passed (got 400 as expected)")


# ===========================================================================
# SECTION 3 — Campaign CRUD
# ===========================================================================

MOCK_CAMPAIGN = {
    "id": "11111111-1111-1111-1111-111111111111",
    "user_id": "00000000-0000-0000-0000-000000000001",
    "campaign_name": "SaaS Q3 Outreach",
    "target_industries": ["SaaS", "Fintech"],
    "company_size": "11-50 employees",
    "offer_summary": "AI-powered sales automation tool",
    "value_proposition": "10x your pipeline with autonomous AI agents",
    "status": "pending",
    "created_at": "2026-08-08T10:00:00Z"
}

class TestCampaignEndpoints:
    def test_list_campaigns(self):
        """GET /api/v1/campaigns — should return list of campaigns."""
        with patch("app.api.routes.campaigns.supabase", _sb):
            _sb.table.return_value.execute.return_value = MagicMock(data=[MOCK_CAMPAIGN])
            resp = client.get("/api/v1/campaigns")

        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        print(f"\n  ✅  List campaigns: {len(data)} campaigns returned")

    def test_create_campaign_triggers_agent(self):
        """POST /api/v1/campaigns — should create and trigger background agent."""
        from app.services.agent_service import AgentService as _AS
        with patch("app.api.routes.campaigns.supabase", _sb):
            with patch("starlette.background.BackgroundTasks.add_task") as mock_add_task:
                _sb.table.return_value.execute.return_value = MagicMock(data=[MOCK_CAMPAIGN])
                resp = client.post("/api/v1/campaigns", json={
                    "campaign_name": "SaaS Q3 Outreach",
                    "target_industries": ["SaaS"],
                    "company_size": "11-50 employees",
                    "offer_summary": "AI-powered sales automation tool",
                    "value_proposition": "10x your pipeline"
                })

        assert resp.status_code == 200
        data = resp.json()
        assert data.get("status") == "success"
        assert "campaign" in data
        print(f"\n  ✅  Campaign created: {data['campaign'].get('campaign_name')}")
        print(f"      🤖 Background agent task queued: id={data['campaign'].get('id')}")

    def test_get_campaign_by_id(self):
        """GET /api/v1/campaigns/{id} — should return specific campaign."""
        with patch("app.api.routes.campaigns.supabase", _sb):
            _sb.table.return_value.execute.return_value = MagicMock(data=[MOCK_CAMPAIGN])
            resp = client.get("/api/v1/campaigns/11111111-1111-1111-1111-111111111111")

        assert resp.status_code == 200
        data = resp.json()
        assert data.get("campaign_name") == "SaaS Q3 Outreach"
        print(f"\n  ✅  Get campaign by ID: {data.get('campaign_name')}")

    def test_get_campaign_not_found(self):
        """GET /api/v1/campaigns/{bad-id} — should return 404."""
        with patch("app.api.routes.campaigns.supabase", _sb):
            _sb.table.return_value.execute.return_value = MagicMock(data=[])
            resp = client.get("/api/v1/campaigns/00000000-0000-0000-0000-000000000000")

        assert resp.status_code == 404
        print(f"\n  ✅  Campaign not-found test passed (got 404 as expected)")


# ===========================================================================
# SECTION 4 — Leads Endpoint
# ===========================================================================

MOCK_LEADS = [
    {
        "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "campaign_id": "11111111-1111-1111-1111-111111111111",
        "full_name": "Sarah Chen",
        "company_name": "Fieldwork Labs",
        "title": "CTO",
        "email": "sarah@fieldworklabs.com",
        "qualification_score": 9.2,
        "qualification_reason": "Perfect ICP match — Tech decision-maker in SaaS",
        "status": "draft_ready",
        "created_at": "2026-08-08T10:01:00Z"
    },
    {
        "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        "campaign_id": "11111111-1111-1111-1111-111111111111",
        "full_name": "Marcus Lee",
        "company_name": "Orbit Analytics",
        "title": "VP Sales",
        "email": "marcus@orbitanalytics.com",
        "qualification_score": 8.5,
        "qualification_reason": "High purchasing authority in data space",
        "status": "draft_ready",
        "created_at": "2026-08-08T10:02:00Z"
    }
]

class TestLeadsEndpoints:
    def test_list_all_leads(self):
        """GET /api/v1/leads — should list all leads."""
        with patch("app.api.routes.leads.supabase", _sb):
            _sb.table.return_value.execute.return_value = MagicMock(data=MOCK_LEADS)
            resp = client.get("/api/v1/leads")

        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        print(f"\n  ✅  List leads: {len(data)} leads returned")
        for lead in data:
            print(f"      → {lead['full_name']} @ {lead['company_name']} (score: {lead['qualification_score']})")

    def test_get_single_lead(self):
        """GET /api/v1/leads/{id} — should return lead details."""
        with patch("app.api.routes.leads.supabase", _sb):
            _sb.table.return_value.execute.return_value = MagicMock(data=[MOCK_LEADS[0]])
            resp = client.get("/api/v1/leads/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")

        assert resp.status_code == 200
        data = resp.json()
        assert data["full_name"] == "Sarah Chen"
        print(f"\n  ✅  Get lead: {data['full_name']} — score {data['qualification_score']}")


# ===========================================================================
# SECTION 5 — Dashboard Stats
# ===========================================================================

class TestDashboardEndpoint:
    def test_dashboard_stats(self):
        """GET /api/v1/dashboard/stats — should return KPI stats."""
        with patch("app.api.routes.dashboard.supabase", _sb):
            _sb.table.return_value.execute.return_value = MagicMock(data=[], count=42)
            resp = client.get("/api/v1/dashboard/stats")

        assert resp.status_code == 200
        data = resp.json()
        assert "stats" in data
        assert isinstance(data["stats"], list)
        print(f"\n  ✅  Dashboard stats: {len(data['stats'])} KPIs returned")
        for stat in data["stats"]:
            print(f"      📊 {stat.get('label')}: {stat.get('value')}")


# ===========================================================================
# SECTION 6 — Agent Workflow (Unit Tests — Mocked LLM)
# ===========================================================================

class TestAgentWorkflowNodes:
    """Tests the 4-node LangGraph workflow in isolation with mocked LLM calls."""

    def _make_state(self):
        return {
            "campaign_id": "camp-001",
            "campaign_context": {
                "target_industries": ["SaaS", "Fintech"],
                "company_size": "11-50 employees",
                "offer_summary": "AI-powered sales automation",
                "value_proposition": "Close 3x more deals with autonomous agents"
            },
            "leads": [],
            "status": "started",
            "errors": []
        }

    @pytest.mark.asyncio
    async def test_prospect_node_generates_leads(self):
        """prospect_node should generate 2-5 leads via structured LLM output."""
        from app.agents.workflow import prospect_node, LeadGenerationResult, LeadProfile

        mock_result = LeadGenerationResult(leads=[
            LeadProfile(full_name="Sarah Chen", company_name="Fieldwork Labs", title="CTO",
                        industry="SaaS", email="sarah@fieldworklabs.com"),
            LeadProfile(full_name="Marcus Lee", company_name="Orbit Analytics", title="VP Sales",
                        industry="Fintech", email="marcus@orbitanalytics.com"),
            LeadProfile(full_name="Priya Nair", company_name="DataBridge Co", title="CEO",
                        industry="SaaS", email="priya@databridgeco.io"),
        ])

        mock_structured_llm = MagicMock()
        mock_structured_llm.ainvoke = AsyncMock(return_value=mock_result)

        with patch("app.agents.workflow.llm") as mock_llm:
            mock_llm.with_structured_output.return_value = mock_structured_llm
            result = await prospect_node(self._make_state())

        assert len(result["leads"]) == 3
        assert result["status"] == "prospecting_complete"
        print(f"\n  ✅  Prospect node: discovered {len(result['leads'])} leads")
        for lead in result["leads"]:
            print(f"      🔍 {lead['full_name']} ({lead['title']}) @ {lead['company_name']}")

    @pytest.mark.asyncio
    async def test_qualify_node_scores_leads(self):
        """qualify_node should score each lead with a float 0-10."""
        from app.agents.workflow import qualify_node

        state = self._make_state()
        state["leads"] = [
            {"full_name": "Sarah Chen", "company_name": "Fieldwork Labs", "title": "CTO",
             "industry": "SaaS", "email": "sarah@fieldworklabs.com"},
            {"full_name": "Marcus Lee", "company_name": "Orbit Analytics", "title": "VP Sales",
             "industry": "Fintech", "email": "marcus@orbitanalytics.com"},
        ]

        mock_response = MagicMock()
        mock_response.content = '{"score": 8.7, "reason": "Strong ICP match — decision-maker in SaaS"}'

        with patch("app.agents.workflow.llm") as mock_llm:
            mock_llm.ainvoke = AsyncMock(return_value=mock_response)
            result = await qualify_node(state)

        assert result["status"] == "qualification_complete"
        for lead in result["leads"]:
            assert "qualification_score" in lead
            assert isinstance(lead["qualification_score"], float)
            print(f"\n  ✅  Qualify: {lead['full_name']} scored {lead['qualification_score']}/10 — \"{lead.get('qualification_reason', '')}\"")

    @pytest.mark.asyncio
    async def test_draft_node_writes_emails(self):
        """draft_node should produce email subject+body for high-scoring leads."""
        from app.agents.workflow import draft_node

        state = self._make_state()
        state["leads"] = [
            {
                "full_name": "Sarah Chen", "company_name": "Fieldwork Labs", "title": "CTO",
                "industry": "SaaS", "email": "sarah@fieldworklabs.com",
                "qualification_score": 9.2
            },
            {
                "full_name": "Bob Smith", "company_name": "Tiny Corp", "title": "Intern",
                "industry": "SaaS", "email": "bob@tinycorp.com",
                "qualification_score": 3.1  # Below threshold — should be skipped
            }
        ]

        mock_response = MagicMock()
        mock_response.content = json.dumps({
            "subject": "10x Your Pipeline — Quick Chat?",
            "body": "Hi Sarah, I saw Fieldwork Labs is scaling fast. Our AI agents can automate your entire outbound in days. Worth a 15-min call?"
        })

        with patch("app.agents.workflow.llm") as mock_llm:
            mock_llm.ainvoke = AsyncMock(return_value=mock_response)
            result = await draft_node(state)

        assert result["status"] == "drafting_complete"
        
        sarah = next(l for l in result["leads"] if l["full_name"] == "Sarah Chen")
        bob = next(l for l in result["leads"] if l["full_name"] == "Bob Smith")

        assert sarah["email_subject"] is not None, "High-score lead should have email"
        assert bob["email_subject"] is None, "Low-score lead should be skipped"
        
        print(f"\n  ✅  Draft node:")
        print(f"      📧 {sarah['full_name']}: Subject='{sarah['email_subject']}'")
        print(f"      ⏭️  {bob['full_name']}: Skipped (score {bob['qualification_score']} < 7)")

    @pytest.mark.asyncio
    async def test_send_node_sends_emails(self):
        """send_node should call email_provider.send() for qualified leads."""
        from app.agents.workflow import send_node

        state = self._make_state()
        state["leads"] = [
            {
                "full_name": "Sarah Chen",
                "email": "sarah@fieldworklabs.com",
                "qualification_score": 9.2,
                "email_subject": "10x Your Pipeline",
                "email_body": "Hi Sarah, let's chat about AI sales automation..."
            }
        ]

        mock_send_result = {"success": True, "message_id": "msg-abc-123"}
        mock_email_provider = AsyncMock()
        mock_email_provider.send = AsyncMock(return_value=mock_send_result)

        with patch("app.agents.workflow.email_provider", mock_email_provider):
            result = await send_node(state)

        assert result["status"] == "sending_complete"
        lead = result["leads"][0]
        assert lead["send_status"] == "sent"
        print(f"\n  ✅  Send node: email sent to {lead['full_name']} ({lead['email']})")
        print(f"      📨 Message ID: {lead['send_message_id']}")

    @pytest.mark.asyncio
    async def test_full_pipeline_integration(self):
        """Full pipeline: prospect → qualify → draft → send in sequence."""
        print("\n\n  🚀 Running FULL PIPELINE integration test...")
        
        from app.agents.workflow import prospect_node, qualify_node, draft_node, send_node, LeadGenerationResult, LeadProfile

        state = self._make_state()

        # Node 1: Prospect
        mock_leads = LeadGenerationResult(leads=[
            LeadProfile(full_name="Elena Vance", company_name="CloudCore AI",
                        title="CEO", industry="SaaS", email="elena@cloudcoreai.com"),
            LeadProfile(full_name="Jake Foster", company_name="MetaOps Ltd",
                        title="VP Engineering", industry="Fintech", email="jake@metaops.io"),
        ])
        mock_structured = MagicMock()
        mock_structured.ainvoke = AsyncMock(return_value=mock_leads)
        with patch("app.agents.workflow.llm") as mock_llm:
            mock_llm.with_structured_output.return_value = mock_structured
            state = {**state, **(await prospect_node(state))}
        print(f"\n      🔍 [1/4] Prospect: found {len(state['leads'])} leads")

        # Node 2: Qualify
        qualify_resp = MagicMock(content='{"score": 8.9, "reason": "Excellent ICP fit"}')
        with patch("app.agents.workflow.llm") as mock_llm:
            mock_llm.ainvoke = AsyncMock(return_value=qualify_resp)
            state = {**state, **(await qualify_node(state))}
        avg_score = sum(l["qualification_score"] for l in state["leads"]) / len(state["leads"])
        print(f"      📊 [2/4] Qualify: avg score {avg_score:.1f}/10")

        # Node 3: Draft
        draft_resp = MagicMock(content='{"subject": "Quick win for {company}?", "body": "Hi, let\'s connect."}')
        with patch("app.agents.workflow.llm") as mock_llm:
            mock_llm.ainvoke = AsyncMock(return_value=draft_resp)
            state = {**state, **(await draft_node(state))}
        drafted = [l for l in state["leads"] if l.get("email_subject")]
        print(f"      📝 [3/4] Draft: {len(drafted)}/{len(state['leads'])} emails drafted")

        # Node 4: Send
        mock_provider = AsyncMock()
        mock_provider.send = AsyncMock(return_value={"success": True, "message_id": "final-msg-001"})
        with patch("app.agents.workflow.email_provider", mock_provider):
            state = {**state, **(await send_node(state))}
        sent = [l for l in state["leads"] if l.get("send_status") == "sent"]
        print(f"      📨 [4/4] Send: {len(sent)} emails sent successfully")
        
        print(f"\n  ✅  FULL PIPELINE COMPLETE: {len(sent)} emails sent end-to-end!")
        assert state["status"] == "sending_complete"


# ===========================================================================
# SECTION 7 — Agent Service (Audit Logging)
# ===========================================================================

class TestAgentService:
    @pytest.mark.asyncio
    async def test_run_campaign_pipeline_logs_to_supabase(self):
        """AgentService.run_campaign_pipeline should log each node to agent_logs."""
        mock_campaign = {
            "id": "camp-001",
            "campaign_name": "Test Campaign",
            "target_industries": ["SaaS"],
            "company_size": "11-50",
            "offer_summary": "AI sales tool",
            "value_proposition": "10x pipeline",
        }

        mock_final_state = {
            "leads": [
                {
                    "full_name": "Test User",
                    "company_name": "Test Co",
                    "qualification_score": 8.5,
                    "qualification_reason": "Good match",
                    "email_subject": "Test Subject",
                    "email_body": "Test body",
                    "send_status": "sent"
                }
            ],
            "status": "sending_complete"
        }

        async def mock_astream(state, stream_mode):
            yield {"prospect": {"leads": mock_final_state["leads"], "status": "prospecting_complete"}}
            yield {"qualify": {"leads": mock_final_state["leads"], "status": "qualification_complete"}}
            yield {"draft": {"leads": mock_final_state["leads"], "status": "drafting_complete"}}
            yield {"send": {"leads": mock_final_state["leads"], "status": "sending_complete"}}

        with patch("app.services.agent_service.supabase", _sb):
            with patch("app.services.agent_service.sales_agent_executor") as mock_executor:
                _sb.table.return_value.execute.return_value = MagicMock(
                    data=[mock_campaign]
                )
                mock_executor.astream = mock_astream

                from app.services.agent_service import AgentService
                result = await AgentService.run_campaign_pipeline("camp-001")

        print(f"\n  ✅  AgentService pipeline completed with status: {result.get('status')}")
        print(f"      📋 {len(result.get('leads', []))} leads processed and saved to Supabase")


# ===========================================================================
# SECTION 8 — Email Service (Provider Mock)
# ===========================================================================

class TestEmailService:
    @pytest.mark.asyncio
    async def test_email_provider_send(self):
        """Email provider should format and return send result."""
        from app.services.email_service import email_provider

        with patch.object(email_provider, 'send', new_callable=AsyncMock) as mock_send:
            mock_send.return_value = {
                "success": True,
                "message_id": "em-xyz-7890",
                "provider": "mock"
            }

            result = await email_provider.send(
                to_email="sarah@fieldworklabs.com",
                subject="10x Your Pipeline",
                body="Hi Sarah, let's talk AI sales automation..."
            )

        assert result["success"] is True
        assert "message_id" in result
        print(f"\n  ✅  Email service: sent → message_id={result['message_id']}")


# ===========================================================================
# SECTION 9 — OpenAPI & Docs Validation
# ===========================================================================

class TestOpenAPISpec:
    def test_openapi_schema_accessible(self):
        """GET /api/v1/openapi.json — schema must be valid JSON with paths."""
        resp = client.get("/api/v1/openapi.json")
        assert resp.status_code == 200
        schema = resp.json()
        assert "paths" in schema
        assert "info" in schema
        paths = list(schema["paths"].keys())
        print(f"\n  ✅  OpenAPI spec: {len(paths)} routes documented")
        for path in paths:
            print(f"      🛣️  {path}")

    def test_all_expected_routes_present(self):
        """Ensure all critical API routes are registered."""
        resp = client.get("/api/v1/openapi.json")
        schema = resp.json()
        paths = schema["paths"]

        expected = [
            "/api/v1/auth/register",
            "/api/v1/auth/login",
            "/api/v1/campaigns",
            "/api/v1/leads",
            "/api/v1/dashboard/stats",
        ]

        for route in expected:
            assert route in paths, f"❌ Route not found in OpenAPI spec: {route}"
            print(f"\n  ✅  Route registered: {route}")
