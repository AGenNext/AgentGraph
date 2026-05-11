"""
Skills Database - SFIA Framework

Skills using SFIA (Skills Framework for the Information Age):
- SFIA 7 skill categories
- Skill levels
- Skill definitions
- Proficiency assessment

Reference:
- SFIA Framework: https://www.sfia-online.org/
- UK IT industry skills framework
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# =============================================================================
# SFIA CATEGORIES
# =============================================================================

class SFIACategory(Enum):
    """SFIA 7 Categories"""
    Strategy_Architecture = "Strategy & Architecture"
    Change_Transformation = "Change & Transformation"
    Development_Implementation = "Development & Implementation"
    Service_Management = "Service Management"
    Client_Stakeholder = "Client Stakeholder"
    Information_Risk = "Information Risk"
    Security = "Security"
    Continual_Improvement = "Continual Improvement"
    Talent_People = "Talent & People"
    Technical_Worthy = "Technical Worthy"


class SFIALevel(Enum):
    """SFIA 7 Levels"""
    Follow = 1  # Follow
    Assist = 2  # Assist
    Apply = 3  # Apply
    Enable = 4  # Enable
    Ensure_Advise = 5  # Ensure/Advise
    Initiate_Influence = 6  # Initiate/Influence
    Set_Lead = 7  # Set/Lead


# =============================================================================
# SKILL
# =============================================================================

@dataclass
class Skill:
    """SFIA Skill"""
    code: str  # e.g., "SKTY"
    name: str
    
    category: SFIACategory
    
    definition: str = ""
    
    scope: str = ""  # What the skill covers
    
    key_areas: List[str] = field(default_factory=list)
    
    behaviours: List[str] = field(default_factory=list)  # Level indicators
    
    # Related
    related_skills: List[str] = field(default_factory=list)
    
    # Generic skills flag
    generic: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "code": self.code,
            "name": self.name,
            "category": self.category.value,
            "level": SFIALevel.Enable.name
        }


@dataclass
class SkillLevel:
    """Skill proficiency level"""
    skill_code: str
    person_id: str
    
    level: SFIALevel
    
    assessed_on: datetime = field(default_factory=datetime.now)
    
    assessor: str = ""
    
    expires_on: Optional[datetime] = None
    
    evidence: str = ""
    
    notes: str = ""


# =============================================================================
# SFIA SKILLS
# =============================================================================

class SFIASkills:
    """SFIA Skills Catalog"""
    
    # Strategy & Architecture
    SKILLS_ARCHITECTURE = {
        "ARIT": Skill(
            "ARIT", "Information Systems Architecture",
            SFIACategory.Strategy_Architecture,
            "The design and specification of the overall logical and physical structure and functionality of the information system(s) within and across organisation boundaries.",
            key_areas=["System structure", "Data architecture", "Application architecture", "Technology architecture"],
            related_skills=["ARCH", "ANLY"]
        ),
        "ARCH": Skill(
            "ARCH", "Architecture Definition",
            SFIACategory.Strategy_Architecture,
            "The process of identifying, documenting and maintaining the architecture of an automated system or a set of systems.",
            key_areas=["Business architecture", "Data architecture", "Application architecture", "Technology architecture"],
        ),
        "BPRE": Skill(
            "BPRE", "Business Process Engineering",
            SFIACategory.Strategy_Architecture,
            "The analysis and redesign of existing business processes within the organisation to make them more effective and efficient.",
            key_areas=["Process analysis", "Process design", "Process modeling", "Process improvement"],
        ),
        "ITSP": Skill(
            "ITSP", "IT Strategy",
            SFIACategory.Strategy_Architecture,
            "The creation and communication of a high-level ICT strategy aligned with the business strategy.",
            key_areas=["Strategy development", "Technology planning", "Roadmap creation"],
        ),
    }
    
    # Change & Transformation
    SKILLS_CHANGE = {
        "CHMG": Skill(
            "CHMG", "Change Management",
            SFIACategory.Change_Transformation,
            "The management of organizational transition, including stakeholder management, communication and training.",
            key_areas=["Change planning", "Stakeholder engagement", "Training", "Communication"],
        ),
        "PROF": Skill(
            "PROF", "Organisational Change",
            SFIACategory.Change_Transformation,
            "The diagnosis, planning and implementation of organisational change.",
            key_areas=["Change diagnosis", "Change planning", "Change implementation"],
        ),
        "RELM": Skill(
            "RELM", "Release Management",
            SFIACategory.Change_Transformation,
            "The management of the processes, systems and functions to package, build, test and deploy changes.",
            key_areas=["Release planning", "Build management", "Deployment"],
        ),
    }
    
    # Development & Implementation
    SKILLS_DEV = {
        "ANLY": Skill(
            "ANLY", "Analysis",
            SFIACategory.Development_Implementation,
            "The systematic examination of information to determine its nature, structure and relationships.",
            key_areas=["Requirements analysis", "Data analysis", "Process analysis"],
        ),
        "DESN": Skill(
            "DESN", "Design",
            SFIACategory.Development_Implementation,
            "The creation and specification of the abstract and detailed design of a system or solution.",
            key_areas=["System design", "Component design", "Interface design"],
        ),
        "PROG": Skill(
            "PROG", "Programming",
            SFIACategory.Development_Implementation,
            "The conception, creation, production, construction and testing of executable programs.",
            key_areas=["Code development", "Testing", "Debugging", "Documentation"],
        ),
        "TEST": Skill(
            "TEST", "Testing",
            SFIACategory.Development_Implementation,
            "The systematic evaluation of a system or system component to detect faults.",
            key_areas=["Test planning", "Test execution", "Test automation"],
        ),
        "DBMS": Skill(
            "DBMS", "Database/DS Management",
            SFIACategory.Development_Implementation,
            "The definition, design, creation and maintenance of databases and data warehouses.",
            key_areas=["Database design", "Data modeling", "Query optimization"],
        ),
        "WEBD": Skill(
            "WEBD", "Web Development",
            SFIACategory.Development_Implementation,
            "The design, development and management of web sites, applications and services.",
            key_areas=["HTML/CSS", "JavaScript", "Web frameworks", "API development"],
        ),
        "API": Skill(
            "API", "API Development",
            SFIACategory.Development_Implementation,
            "The design and development of application programming interfaces.",
            key_areas=["API design", "REST/GraphQL", "Documentation"],
        ),
        "CLOUD": Skill(
            "CLOUD", "Cloud Computing",
            SFIACategory.Development_Implementation,
            "The design, development and management of cloud-based solutions.",
            key_areas=["Cloud architecture", "Serverless", "Containerization", "DevOps"],
        ),
    }
    
    # Service Management
    SKILLS_SERVICE = {
        "ITOP": Skill(
            "ITOP", "IT Operations",
            SFIACategory.Service_Management,
            "The delivery of operational ICT services aligned to business requirements.",
            key_areas=["Incident management", "Problem management", "Service desk"],
        ),
        "SVMG": Skill(
            "SVMG", "Service Level Management",
            SFIACategory.Service_Management,
            "The definition, agreement and management of service levels.",
            key_areas=["SLA definition", "Performance monitoring", "Reporting"],
        ),
        "SUP": Skill(
            "SUP", "Support",
            SFIACategory.Service_Management,
            "The timely and effective support for ICT services and their users.",
            key_areas=["User support", "Troubleshooting", "Knowledge management"],
        ),
        "NETW": Skill(
            "NETW", "Network Support",
            SFIACategory.Service_Management,
            "The support of network systems and services.",
            key_areas=["Network monitoring", "Troubleshooting", "Configuration"],
        ),
    }
    
    # Client Stakeholder
    SKILLS_CLIENT = {
        "BSCN": Skill(
            "BSCN", "Business Consultation",
            SFIACategory.Client_Stakeholder,
            "The provision of advice to the business on the effective use of ICT.",
            key_areas=["Advisory", "Requirements gathering", "Solution proposal"],
        ),
        "CUST": Skill(
            "CUST", "Customer Service",
            SFIACategory.Client_Stakeholder,
            "The provision of high-quality customer service.",
            key_areas=["Communication", "Problem resolution", "Relationship management"],
        ),
        "SALES": Skill(
            "SALES", "Sales",
            SFIACategory.Client_Stakeholder,
            "The generation and management of sales opportunities.",
            key_areas=["Lead generation", "Negotiation", "Account management"],
        ),
        "MKTG": Skill(
            "MKTG", "Marketing",
            SFIACategory.Client_Stakeholder,
            "The promotion and sale of products and services.",
            key_areas=["Digital marketing", "Content", "Campaign management"],
        ),
    }
    
    # Information Risk
    SKILLS_RISK = {
        "IRIS": Skill(
            "IRIS", "Information Security",
            SFIACategory.Information_Risk,
            "The identification, assessment and management of information security risks.",
            key_areas=["Risk assessment", "Controls", "Compliance"],
        ),
        "INRM": Skill(
            "INRM", "Information Management",
            SFIACategory.Information_Risk,
            "The management of information throughout its lifecycle.",
            key_areas=["Data governance", "Data quality", "Retention"],
        ),
        "PRIV": Skill(
            "PRIV", "Data Privacy",
            SFIACategory.Information_Risk,
            "The protection of personal data and privacy.",
            key_areas=["Privacy compliance", "Data protection", "GDPR"],
        ),
    }
    
    # Security
    SKILLS_SECURITY = {
        "SCER": Skill(
            "SCER", "Security Testing",
            SFIACategory.Security,
            "The systematic evaluation of system security.",
            key_areas=["Penetration testing", "Vulnerability assessment", "Code review"],
        ),
        "SCTY": Skill(
            "SCTY", "Cyber Security",
            SFIACategory.Security,
            "The protection of systems and information from cyber threats.",
            key_areas=["Threat detection", "Incident response", "Security hardening"],
        ),
        "SGEM": Skill(
            "SGEM", "Security Engineering",
            SFIACategory.Security,
            "The design and implementation of security systems.",
            key_areas=["Security architecture", "Encryption", "Authentication"],
        ),
    }
    
    # Technical Worthy
    SKILLS_TECHNICAL = {
        "TECH": Skill(
            "TECH", "Technical Research",
            SFIACategory.Technical_Worthy,
            "The investigation and evaluation of technical solutions.",
            key_areas=["Research", "Evaluation", "Proof of concept"],
        ),
        "HAUD": Skill(
            "HAUD", "Hardware Audit",
            SFIACategory.Technical_Worthy,
            "The audit and review of hardware assets.",
            key_areas=["Asset tracking", "Inventory", "Compliance"],
        ),
        "AUDT": Skill(
            "AUDT", "Technical Audit",
            SFIACategory.Technical_Worthy,
            "The independent assessment of technical compliance.",
            key_areas=["Compliance checking", "Process audit", "Reporting"],
        ),
    }
    
    # Continual Improvement
    SKILLS_IMPROVEMENT = {
        "CIPR": Skill(
            "CIPR", "Continual Improvement",
            SFIACategory.Continual_Improvement,
            "The systematic approach to improving products, services and processes.",
            key_areas=["Process improvement", "Lean", "Six Sigma"],
        ),
        "QUAL": Skill(
            "QUAL", "Quality Assurance",
            SFIACategory.Continual_Improvement,
            "The systematic approach to ensuring quality in processes and products.",
            key_areas=["Testing", "Standards", "Process compliance"],
        ),
    }
    
    # Talent & People
    SKILLS_TALENT = {
        "HCMD": Skill(
            "HCMD", "Human Capital Management",
            SFIACategory.Talent_People,
            "The management of an organisation's human resources.",
            key_areas=["Recruitment", "Development", "Performance management"],
        ),
        "COAC": Skill(
            "COAC", "Capability Assessment",
            SFIACategory.Talent_People,
            "The assessment of individual and team capabilities.",
            key_areas=["Skill assessment", "Gap analysis", "Development planning"],
        ),
        "TRAIN": Skill(
            "TRAIN", "Learning & Development",
            SFIACategory.Talent_People,
            "The planning and delivery of learning and development activities.",
            key_areas=["Training design", "Delivery", "Evaluation"],
        ),
    }
    
    @classmethod
    def all_skills(cls) -> Dict[str, Skill]:
        """Get all skills"""
        all_s = {}
        
        for category in [
            cls.SKILLS_ARCHITECTURE,
            cls.SKILLS_CHANGE,
            cls.SKILLS_DEV,
            cls.SKILLS_SERVICE,
            cls.SKILLS_CLIENT,
            cls.SKILLS_RISK,
            cls.SKILLS_SECURITY,
            cls.SKILLS_TECHNICAL,
            cls.SKILLS_IMPROVEMENT,
            cls.SKILLS_TALENT,
        ]:
            all_s.update(category)
        
        return all_s
    
    @classmethod
    def skills_by_category(cls) -> Dict[SFIACategory, List[Skill]]:
        """Get skills grouped by category"""
        result = {}
        
        for skill in cls.all_skills().values():
            if skill.category not in result:
                result[skill.category] = []
            result[skill.category].append(skill)
        
        return result


# =============================================================================
# SKILL DATABASE
# =============================================================================

class SkillsDatabase:
    """Skills database"""
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.proficiencies: Dict[str, SkillLevel] = {}
        
        # Load SFIA skills
        for code, skill in SFIASkills.all_skills().items():
            self.skills[code] = skill
    
    def get_skill(self, code: str) -> Optional[Skill]:
        return self.skills.get(code)
    
    def get_skill_by_name(self, name: str) -> Optional[Skill]:
        name_lower = name.lower()
        for skill in self.skills.values():
            if name_lower in skill.name.lower():
                return skill
        return None
    
    def get_skills_by_category(
        self,
        category: SFIACategory
    ) -> List[Skill]:
        return [
            s for s in self.skills.values()
            if s.category == category
        ]
    
    def search_skills(
        self,
        query: str = None,
        category: SFIACategory = None,
        generic_only: bool = False
    ) -> List[Skill]:
        results = list(self.skills.values())
        
        if query:
            q = query.lower()
            results = [
                s for s in results
                if q in s.name.lower() or q in s.definition.lower()
            ]
        
        if category:
            results = [s for s in results if s.category == category]
        
        if generic_only:
            results = [s for s in results if s.generic]
        
        return results
    
    def add_proficiency(
        self,
        skill_code: str,
        person_id: str,
        level: SFIALevel,
        assessor: str = ""
    ) -> SkillLevel:
        proficiency = SkillLevel(
            skill_code=skill_code,
            person_id=person_id,
            level=level,
            assessor=assessor
        )
        
        key = f"{person_id}_{skill_code}"
        self.proficiencies[key] = proficiency
        
        return proficiency
    
    def get_proficiency(
        self,
        person_id: str,
        skill_code: str
    ) -> Optional[SkillLevel]:
        key = f"{person_id}_{skill_code}"
        return self.proficiencies.get(key)
    
    def get_person_skills(
        self,
        person_id: str,
        min_level: SFIALevel = None
    ) -> List[Skill]:
        results = []
        
        prefix = f"{person_id}_"
        
        for key, prof in self.proficiencies.items():
            if key.startswith(prefix):
                if min_level and prof.level.value < min_level.value:
                    continue
                skill = self.skills.get(prof.skill_code)
                if skill:
                    results.append(skill)
        
        return results
    
    def get_skill_gap(
        self,
        person_id: str,
        required_skills: List[str]
    ) -> Dict[str, Skill]:
        gaps = {}
        
        person_skills = self.get_person_skills(person_id)
        person_skill_codes = {s.code for s in person_skills}
        
        for code in required_skills:
            if code not in person_skill_codes:
                skill = self.skills.get(code)
                if skill:
                    gaps[code] = skill
        
        return gaps
    
    def get_available_levels(self) -> List[str]:
        return [
            f"Level {l.value}: {l.name}"
            for l in SFIALevel
        ]
    
    def stats(self) -> Dict:
        return {
            "total_skills": len(self.skills),
            "skills_by_category": {
                cat.value: len(skills)
                for cat, skills in SFIASkills.skills_by_category().items()
            },
            "total_proficiencies": len(self.proficiencies)
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Skills Database - SFIA Framework")
    print("=" * 50)
    
    db = SkillsDatabase()
    
    print(f"\nTotal SFIA skills: {len(db.skills)}")
    
    # Stats
    stats = db.stats()
    print(f"\nSkills by category:")
    for cat, count in stats["skills_by_category"].items():
        print(f"  {cat}: {count}")
    
    # Search
    print("\nSearch 'Development':")
    results = db.search_skills("development")
    for s in results[:5]:
        print(f"  [{s.code}] {s.name}")
    
    # Get by category
    print("\nDevelopment & Implementation skills:")
    skills = db.get_skills_by_category(SFIACategory.Development_Implementation)
    for s in skills[:5]:
        print(f"  [{s.code}] {s.name}")
    
    # Add proficiency
    prof = db.add_proficiency("PROG", "person1", SFIALevel.Enable)
    print(f"\nProficiency added: {prof.skill_code} at Level {prof.level.value}")
    
    # Get person skills
    person_skills = db.get_person_skills("person1", min_level=SFIALevel.Apply)
    print(f"\nPerson skills: {len(person_skills)}")
    
    # Available levels
    print("\nSFIA Levels:")
    for level in db.get_available_levels():
        print(f"  {level}")


if __name__ == "__main__":
    main()


"""
Skills Database Usage

    db = SkillsDatabase()
    
    # Get skill
    skill = db.get_skill("PROG")
    skill = db.get_skill_by_name("Programming")
    
    # Search
    skills = db.search_skills("security")
    skills = db.get_skills_by_category(SFIACategory.Security)
    
    # Proficiency
    prof = db.add_proficiency("PROG", "person1", SFIALevel.Enable)
    proficiency = db.get_proficiency("person1", "PROG")
    person_skills = db.get_person_skills("person1")
    
    # Gaps
    gaps = db.get_skill_gap("person1", ["PROG", "TEST", "ANLY"])
    
    # Stats
    stats = db.stats()
    
    # Available levels
    levels = db.get_available_levels()
"""