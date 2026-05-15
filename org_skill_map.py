"""
Organization → Skill Mapping

Maps: Organization Type → Required Skills → Tools

Reference: https://schema.org/Organization
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


# Organization Type → Required Skills
ORG_SKILL_MAP: Dict[str, Dict] = {
    # ===== TECH COMPANIES =====
    "tech_startup": {
        "required_skills": [
            "python_code", "javascript_code", "git_clone", "git_commit",
            "db_query", "docker_build", "docker_run", "api_call",
            "terminal_execute", "file_editor"
        ],
        "tools": ["python", "node", "docker", "sql", "git"],
        "description": "Technology startup"
    },
    "faang": {
        "required_skills": [
            "python_code", "java_code", "system_design", "sql_query",
            "code_review", "code_test", "docker_ops", "git_push",
            "terminal_execute", "file_editor"
        ],
        "tools": ["java", "python", "docker", "git", "junit"],
        "description": "FAANG company"
    },
    "saas_company": {
        "required_skills": [
            "python_code", "javascript_code", "surrealdb_admin",
            "docker_build", "cicd_pipeline", "api_call",
            "terminal_execute", "file_editor"
        ],
        "tools": ["python", "surrealdb", "docker", "github_actions"],
        "description": "SaaS business"
    },
    "consulting_firm": {
        "required_skills": [
            "python_code", "sql_query", "data_analysis",
            "jupyter_notebook", "terminal_execute"
        ],
        "tools": ["python", "jupyter", "pandas"],
        "description": "Tech consulting"
    },
    
    # ===== FINANCIAL SERVICES =====
    "fintech": {
        "required_skills": [
            "python_code", "java_code", "surrealdb_admin",
            "security_code", "api_call", "terminal_execute",
            "code_review"
        ],
        "tools": ["java", "python", "surrealdb", "vault"],
        "description": "Financial technology"
    },
    "bank": {
        "required_skills": [
            "java_code", "cobol_legacy", "db2_admin",
            "api_call", "terminal_execute", "code_review"
        ],
        "tools": ["java", "db2", "cobol"],
        "description": "Traditional bank"
    },
    "hedge_fund": {
        "required_skills": [
            "python_code", "quantitative_analysis", "sql_query",
            "machine_learning", "jupyter_notebook"
        ],
        "tools": ["python", "jupyter", "numpy", "pandas"],
        "description": "Hedge fund"
    },
    "crypto_company": {
        "required_skills": [
            "solidity_code", "web3_dev", "smart_contract_audit",
            "security_code", "terminal_execute"
        ],
        "tools": ["solidity", "hardhat", "ethers"],
        "description": "Cryptocurrency company"
    },
    
    # ===== ECOMMERCE =====
    "ecommerce": {
        "required_skills": [
            "javascript_code", "python_code", "mysql_admin",
            "redis_admin", "cdn_config", "api_call",
            "terminal_execute"
        ],
        "tools": ["node", "python", "redis", "cloudflare"],
        "description": "E-commerce platform"
    },
    "marketplace": {
        "required_skills": [
            "python_code", "javascript_code", "surrealdb_admin",
            "payment_process", "search_functionality",
            "terminal_execute"
        ],
        "tools": ["python", "surrealdb", "stripe"],
        "description": "Online marketplace"
    },
    
    # ===== HEALTHCARE =====
    "healthtech": {
        "required_skills": [
            "python_code", "hl7_integration", "mysql_admin",
            "hipaa_compliance", "api_call", "terminal_execute",
            "code_review"
        ],
        "tools": ["python", "mysql", "hl7"],
        "description": "Healthcare technology"
    },
    "pharma": {
        "required_skills": [
            "python_code", "data_analysis", "ml_engineering",
            "jupyter_notebook", "terminal_execute"
        ],
        "tools": ["python", "jupyter", "scikit"],
        "description": "Pharmaceutical company"
    },
    "healthcare_provider": {
        "required_skills": [
            "emr_system", "hl7_integration", "db_query",
            "terminal_execute"
        ],
        "tools": ["epic", "cerner", "sql"],
        "description": "Healthcare provider"
    },
    
    # ===== EDUCATION =====
    "edtech": {
        "required_skills": [
            "python_code", "javascript_code", "video_upload",
            "lms_config", "terminal_execute"
        ],
        "tools": ["python", "node", "moodle"],
        "description": "Education technology"
    },
    "university": {
        "required_skills": [
            "research_computing", "jupyter_notebook", "latex_write",
            "terminal_execute"
        ],
        "tools": ["jupyter", "latex", "r"],
        "description": "University/Research"
    },
    "bootcamp": {
        "required_skills": [
            "python_code", "javascript_code", "teaching",
            "terminal_execute", "file_editor"
        ],
        "tools": ["python", "node", "jupyter"],
        "description": "Coding bootcamp"
    },
    
    # ===== MEDIA & ENTERTAINMENT =====
    "streaming_service": {
        "required_skills": [
            "video_encoding", "cdn_config", "python_code",
            "content_cdn", "terminal_execute"
        ],
        "tools": ["ffmpeg", "aws", "cloudfront"],
        "description": "Streaming media"
    },
    "game_studio": {
        "required_skills": [
            "unreal_engine", "unity_dev", "c_plus_plus",
            "shader_programming", "terminal_execute"
        ],
        "tools": ["unreal", "unity", "c++"],
        "description": "Game development studio"
    },
    "social_media": {
        "required_skills": [
            "python_code", "javascript_code", "recommendation_system",
            "kafka_stream", "terminal_execute"
        ],
        "tools": ["python", "kafka", "spark"],
        "description": "Social media platform"
    },
    "news_media": {
        "required_skills": [
            "cms_management", "javascript_code",
            "terminal_execute", "file_editor"
        ],
        "tools": ["wordpress", "drupal"],
        "description": "News organization"
    },
    
    # ===== LOGISTICS =====
    "logistics": {
        "required_skills": [
            "python_code", "mapping_api", "surrealdb_admin",
            "api_call", "terminal_execute"
        ],
        "tools": ["python", "postgis", "aws"],
        "description": "Logistics company"
    },
    "delivery_service": {
        "required_skills": [
            "route_optimization", "python_code",
            "mobile_dev", "gps_integration"
        ],
        "tools": ["python", "react_native"],
        "description": "Delivery service"
    },
    "supply_chain": {
        "required_skills": [
            "erp_system", "db_query", "python_code",
            "terminal_execute"
        ],
        "tools": ["sap", "oracle", "sql"],
        "description": "Supply chain company"
    },
    
    # ===== MANUFACTURING =====
    "manufacturing": {
        "required_skills": [
            "cad_design", "cnc_programming", "plc_programming",
            "terminal_execute"
        ],
        "tools": ["autocad", "solidworks"],
        "description": "Manufacturing company"
    },
    "robotics": {
        "required_skills": [
            "ros_dev", "c_plus_plus", "python_code",
            "embedded_systems", "terminal_execute"
        ],
        "tools": ["ros", "c++", "arduino"],
        "description": "Robotics company"
    },
    "automotive": {
        "required_skills": [
            "automotive_dev", "can_bus", "adas_development",
            "terminal_execute"
        ],
        "tools": ["autosar", "canalyzer"],
        "description": "Automotive OEM"
    },
    
    # ===== GOVERNMENT =====
    "government": {
        "required_skills": [
            "java_code", "db_query", "security_compliance",
            "terminal_execute", "code_review"
        ],
        "tools": ["java", "oracle", "splunk"],
        "description": "Government agency"
    },
    "defense": {
        "required_skills": [
            "security_clearance", "c_plus_plus", "ada_language",
            "terminal_execute"
        ],
        "tools": ["ada", "c++", "matlab"],
        "description": "Defense contractor"
    },
    "nonprofit": {
        "required_skills": [
            "python_code", "crm_system", "donation_tracking",
            "terminal_execute"
        ],
        "tools": ["salesforce", "python"],
        "description": "Nonprofit organization"
    },
    
    # ===== RETAIL =====
    "retail_chain": {
        "required_skills": [
            "pos_system", "inventory_mgmt", "python_code",
            "terminal_execute"
        ],
        "tools": ["sap", "oracle"],
        "description": "Retail chain"
    },
    "grocery": {
        "required_skills": [
            "inventory_system", "cold_chain_monitor",
            "terminal_execute"
        ],
        "tools": ["sap", "iot"],
        "description": "Grocery retailer"
    },
    
    # ===== ENERGY =====
    "utility": {
        "required_skills": [
            "scada_system", "grid_management", "python_code",
            "terminal_execute"
        ],
        "tools": ["python", "scada"],
        "description": "Utility company"
    },
    "oil_gas": {
        "required_skills": [
            " geospatial", "seismic_analysis", "python_code",
            "terminal_execute"
        ],
        "tools": ["petrel", "python"],
        "description": "Oil & gas company"
    },
    "renewable_energy": {
        "required_skills": [
            "solar_monitoring", "wind_analysis",
            "python_code", "terminal_execute"
        ],
        "tools": ["python", "iot"],
        "description": "Renewable energy"
    },
    
    # ===== TELECOMMUNICATIONS =====
    "telecom": {
        "required_skills": [
            "network_infrastructure", "5g_development",
            "python_code", "terminal_execute"
        ],
        "tools": ["cisco", "python"],
        "description": "Telecommunications"
    },
    "isp": {
        "required_skills": [
            "network_admin", "dns_config", "bandwidth_mgmt",
            "terminal_execute"
        ],
        "tools": ["bind", "cisco"],
        "description": "Internet service provider"
    },
    
    # ===== REAL ESTATE =====
    "real_estate": {
        "required_skills": [
            "property_mgmt", "python_code", "ml_for_real_estate",
            "terminal_execute"
        ],
        "tools": ["salesforce", "python"],
        "description": "Real estate company"
    },
    "construction": {
        "required_skills": [
            "cad_design", "project_mgmt", "python_code",
            "terminal_execute"
        ],
        "tools": ["autocad", "primavera"],
        "description": "Construction company"
    },
    
    # ===== LEGAL =====
    "law_firm": {
        "required_skills": [
            "legal_research", "document_mgmt", "python_code",
            "terminal_execute"
        ],
        "tools": ["clio", "python"],
        "description": "Law firm"
    },
    "legal_tech": {
        "required_skills": [
            "nlp_for_legal", "document_classification",
            "python_code", "terminal_execute"
        ],
        "tools": ["python", "transformers"],
        "description": "Legal technology"
    },
    
    # ===== AGENCIES =====
    "marketing_agency": {
        "required_skills": [
            "seo_optimization", "advertising_api", "analytics",
            "terminal_execute"
        ],
        "tools": ["ga4", "google_ads"],
        "description": "Marketing agency"
    },
    "recruitment": {
        "required_skills": [
            "ats_system", "python_code", "linkedin_api",
            "terminal_execute"
        ],
        "tools": ["workday", "linkedin"],
        "description": "Recruitment agency"
    },
    "staffing": {
        "required_skills": [
            "crm_system", "scheduling_mgmt",
            "terminal_execute"
        ],
        "tools": ["salesforce"],
        "description": "Staffing company"
    },
    
    # ===== STARTUP STAGES =====
    "pre_seed_startup": {
        "required_skills": [
            "mvp_development", "python_code", "javascript_code",
            "terminal_execute", "file_editor"
        ],
        "tools": ["python", "node", "vercel"],
        "description": "Pre-seed startup"
    },
    "series_a_startup": {
        "required_skills": [
            "product_dev", "python_code", "surrealdb_admin",
            "docker_ops", "cicd_pipeline"
        ],
        "tools": ["python", "docker", "k8s"],
        "description": "Series A startup"
    },
    "ipo_ready": {
        "required_skills": [
            "sox_compliance", "security_audit", "code_review",
            "terminal_execute", "code_editor"
        ],
        "tools": ["vault", "splunk"],
        "description": "IPO-ready company"
    },
}


class OrgSkillMapper:
    """Maps Organization Type → Skills → Tools"""
    
    def __init__(self):
        self.map = ORG_SKILL_MAP
    
    def get_skills(self, org_type: str) -> List[str]:
        if org_type in self.map:
            return self.map[org_type]["required_skills"]
        return []
    
    def get_tools(self, org_type: str) -> List[str]:
        if org_type in self.map:
            return self.map[org_type]["tools"]
        return []
    
    def list_orgs(self) -> List[str]:
        return list(self.map.keys())
    
    def stats(self) -> dict:
        return {"total_orgs": len(self.map)}


def main():
    mapper = OrgSkillMapper()
    
    print("=== Organization → Skill → Tool Mapping ===")
    print(f"Total Organizations: {mapper.stats()['total_orgs']}")
    print(f"\nExamples:")
    print(f"  tech_startup -> {mapper.get_skills('tech_startup')[:3]}...")
    print(f"  fintech -> {mapper.get_skills('fintech')[:3]}...")
    print(f"  healthcare -> {mapper.get_skills('healthtech')[:3]}...")


if __name__ == "__main__":
    main()

"""
Complete Mapping:
- 40+ Organization Types
- → Required Skills
- → Tools

Reference: https://schema.org/Organization
"""
