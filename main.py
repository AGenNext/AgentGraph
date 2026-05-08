"""Main entry point for Multi-Agent Content Writing Team."""

import asyncio
import argparse
from typing import Optional

from config import AppConfig
from agents import (
    OpenAIAgent,
    SalesforceAgent,
    MicrosoftAgent,
    GoogleAgent,
    TeamCoordinator,
)
from orchestrator.langgraph_workflow import run_team_workflow
from core import ContentRouter, ResponseAggregator, QualityScorer, ResultSynthesizer
from a2a import get_agent_card, get_all_agent_cards


def print_header(title: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_team_cards() -> None:
    """Print available team agent cards."""
    print_header("Multi-Agent Team - Available Agents")
    
    for card in get_all_agent_cards():
        print(f"\n📋 {card.name}")
        print(f"   ID: {card.agentId}")
        print(f"   Description: {card.description}")
        print(f"   Capabilities:")
        for cap in card.capabilities:
            print(f"     - {cap.name}: {cap.description}")
        print(f"   Skills:")
        for skill in card.skills:
            print(f"     - {skill.name}")


def demo_single_agent(
    agent_type: str = "openai",
    topic: str = "AI Content Writing",
    content_type: str = "blog",
) -> None:
    """Demo a single agent."""
    
    print_header(f"Demo: {agent_type.title()} Agent")
    print(f"Topic: {topic}")
    print(f"Content Type: {content_type}")
    
    # Select agent
    agents_map = {
        "openai": OpenAIAgent(),
        "salesforce": SalesforceAgent(),
        "microsoft": MicrosoftAgent(),
        "google": GoogleAgent(),
    }
    
    agent = agents_map.get(agent_type.lower())
    if not agent:
        print(f"Unknown agent type: {agent_type}")
        return
    
    # Generate content
    from agents.base_agent import ContentRequest
    request = ContentRequest(
        topic=topic,
        content_type=content_type,
        style="professional",
        length="medium",
    )
    
    result = agent._generate_content(request)
    
    print(f"\n--- Generated Content ---")
    print(result.content[:1000])
    print(f"\n[...continued...]")
    
    print(f"\n--- Metadata ---")
    print(f"Agent: {result.agent_id}")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Provider: {result.metadata.get('provider', 'N/A')}")


def demo_team_collaboration(
    topic: str = "AI Content Writing",
    content_type: str = "blog",
) -> None:
    """Demo multi-agent team collaboration."""
    
    print_header("Multi-Agent Team Collaboration")
    print(f"Topic: {topic}")
    print(f"Content Type: {content_type}")
    
    # Use LangGraph workflow
    result = run_team_workflow(topic, content_type)
    
    print(f"\n--- Team Generated Content ---")
    print(result["content"][:1500])
    print(f"\n[...continued...]")
    
    print(f"\n--- Team Stats ---")
    print(f"Quality Score: {result['quality_score']:.2f}")
    print(f"Multi-Agent: {result['team_used']}")
    if result.get("errors"):
        print(f"Errors: {result['errors']}")


def demo_a2a_delegation() -> None:
    """Demo A2A protocol delegation."""
    
    print_header("A2A Protocol - Task Delegation")
    
    # Get agent cards
    print("\n📡 Agent Cards:")
    
    for card in get_all_agent_cards():
        print(f"\n  {card.name} ({card.agentId})")
        print(f"    URL: {card.url}")
        print(f"    Capabilities: {[c.name for c in card.capabilities]}")
    
    # Demo delegation
    print("\n📨 Delegation Example:")
    print("  Team Coordinator → OpenAI Agent: Generate blog post")
    print("  Team Coordinator → Salesforce Agent: Generate sales copy")
    print("  Team Coordinator → Google Agent: SEO optimization")
    
    # Use coordinator
    coordinator = TeamCoordinator()
    coordinator._setup_default_team()
    
    status = coordinator.get_team_status()
    print(f"\n  Team Status: {status['team_size']} members")
    for member in status["members"]:
        print(f"    - {member['id']}: {member['capabilities']}")


def interactive_mode() -> None:
    """Run interactive content generation mode."""
    
    print_header("Interactive Content Generation")
    print("Enter your content request (topic, content_type, style)")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            topic = input("Topic: ").strip()
            if topic.lower() == "quit":
                break
            
            content_type = input("Content Type (blog/sales/tech/seo/comprehensive): ").strip() or "blog"
            style = input("Style (professional/casual/technical): ").strip() or "professional"
            
            print("\nGenerating content with multi-agent team...\n")
            
            result = run_team_workflow(topic, content_type, style)
            
            print(f"--- Generated Content ---")
            print(result["content"][:800])
            print("[...]\n")
            
            print(f"Quality: {result['quality_score']:.2f} | Team: {result['team_used']}\n")
            
        except (KeyboardInterrupt, EOFError):
            break
    
    print("\nGoodbye!")


def main():
    """Main entry point."""
    
    parser = argparse.ArgumentParser(description="Multi-Agent Content Writing Team")
    parser.add_argument(
        "--mode",
        choices=["demo", "team", "a2a", "interactive", "cards"],
        default="cards",
        help="Operation mode",
    )
    parser.add_argument("--agent", default="openai", help="Agent type for demo")
    parser.add_argument("--topic", default="AI Content Writing", help="Content topic")
    parser.add_argument("--content-type", default="blog", help="Content type")
    
    args = parser.parse_args()
    
    if args.mode == "cards":
        print_team_cards()
    
    elif args.mode == "demo":
        demo_single_agent(args.agent, args.topic, args.content_type)
    
    elif args.mode == "team":
        demo_team_collaboration(args.topic, args.content_type)
    
    elif args.mode == "a2a":
        demo_a2a_delegation()
    
    elif args.mode == "interactive":
        interactive_mode()
    
    else:
        print(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    main()