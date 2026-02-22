"""
Core AI Agent Framework Implementation
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.modules = {}
        self.results = {}
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent task"""
        pass
    
    def register_module(self, name: str, module):
        """Register a module with the agent"""
        self.modules[name] = module
        logger.info(f"Registered module '{name}' with agent '{self.name}'")
    
    def get_results(self) -> Dict[str, Any]:
        """Get all stored results"""
        return self.results


class InformationGatheringAgent(BaseAgent):
    """Main agent for information gathering tasks"""
    
    def __init__(self, name: str = "InformationGatherer"):
        super().__init__(name)
        logger.info(f"Initialized {self.name} agent")
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute information gathering task
        
        Args:
            task: Dictionary containing task details
                - target: Target to scan
                - modules: List of modules to use (optional)
        
        Returns:
            Dictionary with results from all modules
        """
        target = task.get("target")
        if not target:
            raise ValueError("Target is required for information gathering")
        
        modules_to_run = task.get("modules", list(self.modules.keys()))
        
        logger.info(f"Starting information gathering for {target}")
        logger.info(f"Modules to run: {modules_to_run}")
        
        # Clear previous results
        self.results.clear()
        
        # Create tasks for concurrent execution
        tasks = []
        for module_name in modules_to_run:
            if module_name in self.modules:
                task_coro = self._run_module(module_name, self.modules[module_name], target)
                tasks.append(task_coro)
            else:
                logger.warning(f"Module '{module_name}' not found")
        
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
        
        logger.info(f"Completed information gathering for {target}")
        return self.results
    
    async def _run_module(self, module_name: str, module, target: str):
        """Run a specific module and store results"""
        try:
            logger.info(f"Running module '{module_name}' for target '{target}'")
            result = await module.execute(target)
            self.results[module_name] = result
            logger.info(f"Completed module '{module_name}' for target '{target}'")
        except Exception as e:
            logger.error(f"Error in module '{module_name}' for target '{target}': {str(e)}")
            self.results[module_name] = {"error": str(e)}


class Module(ABC):
    """Base class for all modules"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def execute(self, target: str) -> Dict[str, Any]:
        """Execute the module for a given target"""
        pass


# Example implementation of a simple module
class ExampleModule(Module):
    """Example module implementation"""
    
    def __init__(self):
        super().__init__("example")
    
    async def execute(self, target: str) -> Dict[str, Any]:
        """Simple example execution"""
        await asyncio.sleep(0.1)  # Simulate async work
        return {
            "target": target,
            "module": self.name,
            "result": f"Processed {target} with {self.name} module"
        }
