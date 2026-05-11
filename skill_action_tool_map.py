"""
Skill → Action → Tool Mapping

Maps: Skill Name → Schema.org Actions → Implementation Tool

Reference: https://schema.org/docs/full.html#action_tree
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


# Skill → Action → Tool
SKILL_ACTION_TOOL_MAP: Dict[str, Dict] = {
    # ===== WEB SKILLS =====
    "web_search": {
        "actions": ["SearchAction", "SeekToAction"],
        "tool": "browser_navigate",
        "description": "Search the web"
    },
    "web_scraping": {
        "actions": ["CheckAction", "DiscoverAction"],
        "tool": "tavily_tavily_extract",
        "description": "Extract content from URLs"
    },
    "web_crawl": {
        "actions": ["DiscoverAction", "SearchAction"],
        "tool": "tavily_tavily_crawl",
        "description": "Crawl websites"
    },
    
    # ===== BROWSER SKILLS =====
    "browser_navigate": {
        "actions": ["ViewAction", "NavigateAction"],
        "tool": "browser_navigate",
        "description": "Navigate to URL"
    },
    "browser_click": {
        "actions": ["InteractAction", "ClickAction"],
        "tool": "browser_click",
        "description": "Click element"
    },
    "browser_type": {
        "actions": ["FillAction", "InputAction"],
        "tool": "browser_type",
        "description": "Type text"
    },
    
    # ===== TERMINAL SKILLS =====
    "terminal_execute": {
        "actions": ["ExecuteAction", "RunAction"],
        "tool": "terminal",
        "description": "Execute shell command"
    },
    "file_editor": {
        "actions": ["WriteAction", "UpdateAction", "EditAction"],
        "tool": "file_editor",
        "description": "Edit files"
    },
    
    # ===== API SKILLS =====
    "api_call": {
        "actions": ["InvokeAction", "CallAction"],
        "tool": "default_api_call",
        "description": "Call REST API"
    },
    "graphql_query": {
        "actions": ["QueryAction", "SearchAction"],
        "tool": "graphql_client",
        "description": "Query GraphQL"
    },
    
    # ===== GIT SKILLS =====
    "git_clone": {
        "actions": ["CloneAction", "CopyAction"],
        "tool": "terminal (git clone)",
        "description": "Clone repository"
    },
    "git_commit": {
        "actions": ["UpdateAction", "AddAction"],
        "tool": "terminal (git commit)",
        "description": "Commit changes"
    },
    "git_push": {
        "actions": ["SendAction", "TransferAction"],
        "tool": "terminal (git push)",
        "description": "Push to remote"
    },
    
    # ===== DEVOPS SKILLS =====
    "docker_build": {
        "actions": ["BuildAction", "CreateAction"],
        "tool": "docker build",
        "description": "Build Docker image"
    },
    "docker_run": {
        "actions": ["RunAction", "ActivateAction"],
        "tool": "docker run",
        "description": "Run container"
    },
    "kubernetes_deploy": {
        "actions": ["DeployAction", "ActivateAction"],
        "tool": "kubectl apply",
        "description": "Deploy to K8s"
    },
    
    # ===== CLOUD SKILLS =====
    "aws_deploy": {
        "actions": ["DeployAction", "ActivateAction"],
        "tool": "aws_cli",
        "description": "Deploy to AWS"
    },
    "vercel_deploy": {
        "actions": ["DeployAction", "PublishAction"],
        "tool": "vercel deploy",
        "description": "Deploy to Vercel"
    },
    
    # ===== DATABASE SKILLS =====
    "db_query": {
        "actions": ["QueryAction", "SearchAction"],
        "tool": "sql_client",
        "description": "Query database"
    },
    "db_migrate": {
        "actions": ["UpdateAction", "MigrateAction"],
        "tool": "alembic",
        "description": "Run migrations"
    },
    
    # ===== CODE SKILLS =====
    "code_review": {
        "actions": ["ReviewAction", "AssessAction"],
        "tool": "github_pr_review",
        "description": "Review pull request"
    },
    "code_test": {
        "actions": ["TestAction", "AssessAction"],
        "tool": "pytest",
        "description": "Run tests"
    },
    "code_lint": {
        "actions": ["CheckAction", "AssessAction"],
        "tool": "ruff/black",
        "description": "Lint code"
    },
    
    # ===== AI/ML SKILLS =====
    "llm_complete": {
        "actions": ["CompleteAction", "GenerateAction"],
        "tool": "openai_client",
        "description": "LLM text completion"
    },
    "embedding_create": {
        "actions": ["CreateAction", "EmbedAction"],
        "tool": "sentence_transformers",
        "description": "Create embeddings"
    },
    
    # ===== AGENT SKILLS =====
    "agent_delegate": {
        "actions": ["DelegateAction", "AssignAction"],
        "tool": "openhands_sdk",
        "description": "Delegate to sub-agent"
    },
    "agent_create": {
        "actions": ["CreateAction", "GenerateAction"],
        "tool": "agent-creator",
        "description": "Create agent"
    },
    
    # ===== COMMUNICATION SKILLS =====
    "slack_message": {
        "actions": ["SendAction", "MessageAction"],
        "tool": "discord (Slack webhook)",
        "description": "Send Slack message"
    },
    "github_issue": {
        "actions": ["CreateAction", "ReportAction"],
        "tool": "github (Issues API)",
        "description": "Create GitHub issue"
    },
    "linear_ticket": {
        "actions": ["CreateAction", "TrackAction"],
        "tool": "linear (API)",
        "description": "Create Linear ticket"
    },
    
    # ===== FILE SKILLS =====
    "file_read": {
        "actions": ["ReadAction", "GetAction"],
        "tool": "file_editor (view)",
        "description": "Read file"
    },
    "file_write": {
        "actions": ["WriteAction", "CreateAction"],
        "tool": "file_editor (create)",
        "description": "Write file"
    },
    "file_delete": {
        "actions": ["DeleteAction", "RemoveAction"],
        "tool": "terminal (rm)",
        "description": "Delete file"
    },
    
    # ===== CALENDAR SKILLS =====
    "calendar_create": {
        "actions": ["CreateAction", "ScheduleAction"],
        "tool": "google_cal_api",
        "description": "Create calendar event"
    },
    "calendar_find": {
        "actions": ["FindAction", "SearchAction"],
        "tool": "google_cal_api",
        "description": "Find calendar events"
    },
    
    # ===== EMAIL SKILLS =====
    "email_send": {
        "actions": ["SendAction", "CommunicateAction"],
        "tool": "smtp_client",
        "description": "Send email"
    },
    
    # ===== PAYMENT SKILLS =====
    "payment_process": {
        "actions": ["PayAction", "ProcessAction"],
        "tool": "stripe_api",
        "description": "Process payment"
    },
    
    # ===== MEDIA SKILLS =====
    "image_generate": {
        "actions": ["GenerateAction", "CreateAction"],
        "tool": "dalle_client",
        "description": "Generate image"
    },
    "video_generate": {
        "actions": ["GenerateAction", "CreateAction"],
        "tool": "runway_client",
        "description": "Generate video"
    },
    "audio_transcribe": {
        "actions": ["TranscribeAction", "ConvertAction"],
        "tool": "whisper",
        "description": "Transcribe audio"
    },
    "pdf_create": {
        "actions": ["CreateAction", "GenerateAction"],
        "tool": "pdflatex",
        "description": "Create PDF"
    },
    
    # ===== SECRETS SKILLS =====
    "secrets_get": {
        "actions": ["GetAction", "ReadAction"],
        "tool": "CUSTOM_SECRETS",
        "description": "Get secret value"
    },
    
    # ===== SKILL REGISTRY SKILLS =====
    "skill_add": {
        "actions": ["AddAction", "RegisterAction"],
        "tool": "add-skill",
        "description": "Add external skill"
    },
    "skill_invoke": {
        "actions": ["InvokeAction", "ExecuteAction"],
        "tool": "invoke_skill",
        "description": "Invoke skill"
    },
}


class SkillActionMapper:
    """Maps Skill → Action → Tool"""
    
    def __init__(self):
        self.map = SKILL_ACTION_TOOL_MAP
    
    def get_tool(self, skill: str) -> Optional[str]:
        if skill in self.map:
            return self.map[skill]["tool"]
        return None
    
    def get_actions(self, skill: str) -> List[str]:
        if skill in self.map:
            return self.map[skill]["actions"]
        return []
    
    def list_skills(self) -> List[str]:
        return list(self.map.keys())
    
    def stats(self) -> dict:
        return {"total_skills": len(self.map)}


def main():
    mapper = SkillActionMapper()
    
    print("=== Skill → Action → Tool Mapping ===")
    print(f"Total Skills: {mapper.stats()['total_skills']}")
    print(f"\nExample Mappings:")
    print(f"  web_search -> {mapper.get_tool('web_search')}")
    print(f"  terminal_execute -> {mapper.get_tool('terminal_execute')}")
    print(f"  code_review -> {mapper.get_tool('code_review')}")
    print(f"  agent_delegate -> {mapper.get_tool('agent_delegate')}")


if __name__ == "__main__":
    main()

"""
Complete Mapping:
- 38 Skills
- → Schema.org Actions
- → Implementation Tools

Reference: https://schema.org/docs/full.html#action_tree
"""