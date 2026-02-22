"""
Command Line Interface for AI Agent Framework
"""
import argparse
import asyncio
import json
import sys
import uuid
from typing import List
from .core import InformationGatheringAgent
from .modules import WhoisModule, DNSModule, PortScanModule, GitHubSearchModule, WebAnalyzerModule
from .config import config_manager
from .storage import storage

def create_agent_with_modules(modules: List[str]) -> InformationGatheringAgent:
    """Create an agent with specified modules"""
    agent = InformationGatheringAgent()
    
    # Register available modules
    available_modules = {
        "whois": WhoisModule(),
        "dns": DNSModule(),
        "port_scan": PortScanModule(),
        "github_search": GitHubSearchModule(),
        "web_analyzer": WebAnalyzerModule()
    }
    
    # Register requested modules
    for module_name in modules:
        if module_name in available_modules:
            agent.register_module(module_name, available_modules[module_name])
        else:
            print(f"Warning: Unknown module '{module_name}'")
    
    return agent


async def run_scan(target: str, modules: List[str], task_id: str = None) -> dict:
    """Run a scan with the agent"""
    if task_id is None:
        task_id = str(uuid.uuid4())
    
    # Create task record
    storage.create_task(task_id, target, modules)
    storage.update_task_status(task_id, "running")
    
    try:
        # Create agent and run scan
        agent = create_agent_with_modules(modules)
        task = {"target": target, "modules": modules}
        results = await agent.execute(task)
        
        # Save results to storage
        for module_name, result in results.items():
            storage.save_result(task_id, target, module_name, result)
        
        # Update task status
        storage.update_task_status(task_id, "completed")
        
        return results
    except Exception as e:
        storage.update_task_status(task_id, "failed")
        raise


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="AI Agent Framework CLI")
    parser.add_argument("--target", "-t", help="Target to scan")
    parser.add_argument("--modules", "-m", help="Comma-separated list of modules to run")
    parser.add_argument("--list-modules", "-l", action="store_true", help="List available modules")
    parser.add_argument("--task-id", "-i", help="Task ID for this scan")
    parser.add_argument("--export", "-e", help="Export results to file")
    parser.add_argument("--format", "-f", default="json", help="Export format (json, txt)")
    
    args = parser.parse_args()
    
    if args.list_modules:
        print("Available modules:")
        print("  whois        - WHOIS lookup")
        print("  dns          - DNS resolution")
        print("  port_scan    - Port scanning")
        print("  github_search - GitHub code search")
        print("  web_analyzer - Web technology analysis")
        return
    
    if not args.target:
        print("Error: Target is required")
        parser.print_help()
        sys.exit(1)
    
    # Determine modules to run
    if args.modules:
        modules = [m.strip() for m in args.modules.split(",")]
    else:
        # Run all enabled modules
        modules = config_manager.get_enabled_modules()
    
    if not modules:
        print("Error: No modules specified or enabled")
        sys.exit(1)
    
    # Run the scan
    try:
        print(f"Starting scan for {args.target} with modules: {', '.join(modules)}")
        results = asyncio.run(run_scan(args.target, modules, args.task_id))
        
        # Display results
        print("\nScan Results:")
        print("=" * 50)
        for module_name, result in results.items():
            print(f"\n{module_name.upper()} Module:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Export if requested
        if args.export and args.task_id:
            storage.export_results(args.task_id, args.export, args.format)
            print(f"\nResults exported to {args.export}")
            
    except Exception as e:
        print(f"Error running scan: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
