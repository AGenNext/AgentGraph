"""
Course → Skill Mapping

Maps: Learning Course → Skill → Action → Tool

Reference: https://schema.org/Course
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


# Course → Skill Mapping
COURSE_SKILL_MAP: Dict[str, Dict] = {
    # ===== PROGRAMMING COURSES =====
    "python_basics": {
        "skill": "python_code",
        "level": "beginner",
        "actions": ["WriteAction", "CreateAction"],
        "tool": "file_editor",
        "description": "Learn Python basics"
    },
    "python_advanced": {
        "skill": "python_code",
        "level": "advanced",
        "actions": ["OptimizeAction", "RefactorAction"],
        "tool": "file_editor",
        "description": "Advanced Python patterns"
    },
    "javascript_course": {
        "skill": "javascript_code",
        "level": "intermediate",
        "actions": ["WriteAction", "CreateAction"],
        "tool": "file_editor",
        "description": "JavaScript programming"
    },
    "rust_course": {
        "skill": "rust_code",
        "level": "advanced",
        "actions": ["WriteAction", "BuildAction"],
        "tool": "terminal",
        "description": "Rust programming"
    },
    "go_course": {
        "skill": "go_code",
        "level": "intermediate",
        "actions": ["WriteAction", "BuildAction"],
        "tool": "terminal",
        "description": "Go programming"
    },
    "java_course": {
        "skill": "java_code",
        "level": "intermediate",
        "actions": ["WriteAction", "BuildAction"],
        "tool": "gradle/maven",
        "description": "Java programming"
    },
    
    # ===== WEB DEVELOPMENT COURSES =====
    "html_css_course": {
        "skill": "web_dev",
        "level": "beginner",
        "actions": ["WriteAction", "CreateAction"],
        "tool": "file_editor",
        "description": "HTML & CSS"
    },
    "react_course": {
        "skill": "react_dev",
        "level": "intermediate",
        "actions": ["CreateAction", "BuildAction"],
        "tool": "npm",
        "description": "React.js development"
    },
    "vue_course": {
        "skill": "vue_dev",
        "level": "intermediate",
        "actions": ["CreateAction", "BuildAction"],
        "tool": "npm",
        "description": "Vue.js development"
    },
    "angular_course": {
        "skill": "angular_dev",
        "level": "intermediate",
        "actions": ["CreateAction", "BuildAction"],
        "tool": "npm",
        "description": "Angular development"
    },
    "nextjs_course": {
        "skill": "nextjs_dev",
        "level": "intermediate",
        "actions": ["CreateAction", "DeployAction"],
        "tool": "vercel",
        "description": "Next.js development"
    },
    
    # ===== BACKEND COURSES =====
    "nodejs_course": {
        "skill": "nodejs_dev",
        "level": "intermediate",
        "actions": ["WriteAction", "RunAction"],
        "tool": "node",
        "description": "Node.js backend"
    },
    "django_course": {
        "skill": "django_dev",
        "level": "intermediate",
        "actions": ["WriteAction", "RunAction"],
        "tool": "python",
        "description": "Django full-stack"
    },
    "fastapi_course": {
        "skill": "fastapi_dev",
        "level": "intermediate",
        "actions": ["WriteAction", "RunAction"],
        "tool": "uvicorn",
        "description": "FastAPI REST APIs"
    },
    "flask_course": {
        "skill": "flask_dev",
        "level": "intermediate",
        "actions": ["WriteAction", "RunAction"],
        "tool": "flask",
        "description": "Flask micro-framework"
    },
    "spring_boot_course": {
        "skill": "spring_dev",
        "level": "advanced",
        "actions": ["WriteAction", "BuildAction"],
        "tool": "maven",
        "description": "Spring Boot Java"
    },
    
    # ===== DATABASE COURSES =====
    "sql_course": {
        "skill": "sql_query",
        "level": "beginner",
        "actions": ["QueryAction", "SearchAction"],
        "tool": "sql_client",
        "description": "SQL fundamentals"
    },
    "surrealdb_course": {
        "skill": "surrealdb_admin",
        "level": "intermediate",
        "actions": ["QueryAction", "ManageAction"],
        "tool": "psql",
        "description": "SurrealDB database"
    },
    "mongodb_course": {
        "skill": "mongodb_admin",
        "level": "intermediate",
        "actions": ["QueryAction", "ManageAction"],
        "tool": "mongosh",
        "description": "MongoDB NoSQL"
    },
    "redis_course": {
        "skill": "redis_admin",
        "level": "intermediate",
        "actions": ["QueryAction", "CacheAction"],
        "tool": "redis_cli",
        "description": "Redis in-memory"
    },
    
    # ===== DEVOPS COURSES =====
    "docker_course": {
        "skill": "docker_ops",
        "level": "intermediate",
        "actions": ["BuildAction", "RunAction"],
        "tool": "docker",
        "description": "Docker containerization"
    },
    "kubernetes_course": {
        "skill": "kubernetes_ops",
        "level": "advanced",
        "actions": ["DeployAction", "ScaleAction"],
        "tool": "kubectl",
        "description": "Kubernetes orchestration"
    },
    "terraform_course": {
        "skill": "terraform_iac",
        "level": "intermediate",
        "actions": ["ApplyAction", "PlanAction"],
        "tool": "terraform",
        "description": "Terraform IaC"
    },
    "ansible_course": {
        "skill": "ansible_config",
        "level": "intermediate",
        "actions": ["ApplyAction", "ConfigureAction"],
        "tool": "ansible",
        "description": "Ansible automation"
    },
    "ci_cd_course": {
        "skill": "cicd_pipeline",
        "level": "intermediate",
        "actions": ["BuildAction", "DeployAction"],
        "tool": "github_actions",
        "description": "CI/CD pipelines"
    },
    
    # ===== CLOUD COURSES =====
    "aws_course": {
        "skill": "aws_cloud",
        "level": "intermediate",
        "actions": ["DeployAction", "ConfigureAction"],
        "tool": "aws_cli",
        "description": "Amazon Web Services"
    },
    "gcp_course": {
        "skill": "gcp_cloud",
        "level": "intermediate",
        "actions": ["DeployAction", "ConfigureAction"],
        "tool": "gcloud",
        "description": "Google Cloud Platform"
    },
    "azure_course": {
        "skill": "azure_cloud",
        "level": "intermediate",
        "actions": ["DeployAction", "ConfigureAction"],
        "tool": "az",
        "description": "Microsoft Azure"
    },
    
    # ===== DATA SCIENCE COURSES =====
    "python_ds_course": {
        "skill": "data_science",
        "level": "intermediate",
        "actions": ["AnalyzeAction", "VisualizeAction"],
        "tool": "jupyter",
        "description": "Python data science"
    },
    "machine_learning_course": {
        "skill": "ml_engineering",
        "level": "advanced",
        "actions": ["TrainAction", "PredictAction"],
        "tool": "scikit_learn",
        "description": "Machine learning"
    },
    "deep_learning_course": {
        "skill": "dl_engineering",
        "level": "advanced",
        "actions": ["TrainAction", "PredictAction"],
        "tool": "pytorch/tensorflow",
        "description": "Deep learning"
    },
    "nlp_course": {
        "skill": "nlp_engineering",
        "level": "advanced",
        "actions": ["TrainAction", "PredictAction"],
        "tool": "transformers",
        "description": "NLP with transformers"
    },
    
    # ===== AI/AGENT COURSES =====
    "openai_api_course": {
        "skill": "llm_integration",
        "level": "intermediate",
        "actions": ["GenerateAction", "CompleteAction"],
        "tool": "openai",
        "description": "OpenAI API integration"
    },
    "langchain_course": {
        "skill": "langchain_dev",
        "level": "advanced",
        "actions": ["ChainAction", "ExecuteAction"],
        "tool": "langchain",
        "description": "LangChain framework"
    },
    "agent_course": {
        "skill": "agent_development",
        "level": "advanced",
        "actions": ["CreateAction", "DelegateAction"],
        "tool": "openhands_sdk",
        "description": "AI agent development"
    },
    "rag_course": {
        "skill": "rag_development",
        "level": "advanced",
        "actions": ["QueryAction", "SearchAction"],
        "tool": "langchain + chroma",
        "description": "RAG systems"
    },
    
    # ===== SECURITY COURSES =====
    "ethical_hacking_course": {
        "skill": "penetration_testing",
        "level": "advanced",
        "actions": ["ExploitAction", "AssessAction"],
        "tool": "metasploit",
        "description": "Ethical hacking"
    },
    "secure_coding_course": {
        "skill": "secure_coding",
        "level": "intermediate",
        "actions": ["ValidateAction", "SanitizeAction"],
        "tool": "bandit/semgrep",
        "description": "Secure coding practices"
    },
    
    # ===== MOBILE COURSES =====
    "react_native_course": {
        "skill": "mobile_dev",
        "level": "intermediate",
        "actions": ["BuildAction", "DeployAction"],
        "tool": "expo",
        "description": "React Native mobile"
    },
    "flutter_course": {
        "skill": "flutter_dev",
        "level": "intermediate",
        "actions": ["BuildAction", "DeployAction"],
        "tool": "flutter",
        "description": "Flutter mobile"
    },
    "swift_course": {
        "skill": "ios_dev",
        "level": "intermediate",
        "actions": ["BuildAction", "DeployAction"],
        "tool": "xcode",
        "description": "Swift iOS development"
    },
    "kotlin_course": {
        "skill": "android_dev",
        "level": "intermediate",
        "actions": ["BuildAction", "DeployAction"],
        "tool": "gradle",
        "description": "Kotlin Android"
    },
    
    # ===== BLOCKCHAIN COURSES =====
    "solidity_course": {
        "skill": "smart_contract_dev",
        "level": "advanced",
        "actions": ["WriteAction", "DeployAction"],
        "tool": "hardhat",
        "description": "Solidity smart contracts"
    },
    "web3_course": {
        "skill": "web3_dev",
        "level": "advanced",
        "actions": ["IntegrateAction", "DeployAction"],
        "tool": "ethers.js",
        "description": "Web3 development"
    },
}


class CourseSkillMapper:
    """Maps Course → Skill → Action → Tool"""
    
    def __init__(self):
        self.map = COURSE_SKILL_MAP
    
    def get_skill(self, course: str) -> Optional[str]:
        if course in self.map:
            return self.map[course]["skill"]
        return None
    
    def get_tool(self, course: str) -> Optional[str]:
        if course in self.map:
            return self.map[course]["tool"]
        return None
    
    def get_actions(self, course: str) -> List[str]:
        if course in self.map:
            return self.map[course]["actions"]
        return []
    
    def list_courses(self, level: str = None) -> List[str]:
        if level:
            return [c for c, m in self.map.items() if m.get("level") == level]
        return list(self.map.keys())
    
    def stats(self) -> dict:
        by_level = {}
        for course, meta in self.map.items():
            level = meta.get("level", "unknown")
            by_level[level] = by_level.get(level, 0) + 1
        return {"total_courses": len(self.map), "by_level": by_level}


def main():
    mapper = CourseSkillMapper()
    
    print("=== Course → Skill → Tool Mapping ===")
    print(f"Total Courses: {mapper.stats()['total_courses']}")
    print(f"\nBy Level:")
    for level, count in mapper.stats()["by_level"].items():
        print(f"  {level}: {count}")
    print(f"\nExample:")
    print(f"  python_basics -> {mapper.get_skill('python_basics')}")
    print(f"  docker_course -> {mapper.get_skill('docker_course')}")
    print(f"  agent_course -> {mapper.get_skill('agent_course')}")


if __name__ == "__main__":
    main()

"""
Complete Mapping:
- 50+ Courses
- → Skills
- → Actions
- → Tools

Reference: https://schema.org/Course
"""
