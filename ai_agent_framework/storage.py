"""
Storage System for AI Agent Framework
"""
import json
import sqlite3
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class Storage:
    """Storage system for agent results and configuration"""
    
    def __init__(self, db_path: str = "agent_data.db"):
        self.db_path = Path(db_path)
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    target TEXT NOT NULL,
                    module_name TEXT NOT NULL,
                    result TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE NOT NULL,
                    target TEXT NOT NULL,
                    modules TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed_at DATETIME
                )
            """)
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    def save_result(self, task_id: str, target: str, module_name: str, result: Dict[str, Any]):
        """Save a module result to the database"""
        try:
            result_json = json.dumps(result, ensure_ascii=False)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO results (task_id, target, module_name, result)
                    VALUES (?, ?, ?, ?)
                """, (task_id, target, module_name, result_json))
                conn.commit()
                
            logger.info(f"Saved result for task {task_id}, module {module_name}")
        except Exception as e:
            logger.error(f"Failed to save result: {str(e)}")
            raise
    
    def get_results(self, task_id: str) -> List[Dict[str, Any]]:
        """Retrieve all results for a task"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM results WHERE task_id = ? ORDER BY timestamp
                """, (task_id,))
                
                rows = cursor.fetchall()
                results = []
                for row in rows:
                    result = dict(row)
                    result["result"] = json.loads(result["result"])
                    results.append(result)
                
                return results
        except Exception as e:
            logger.error(f"Failed to retrieve results: {str(e)}")
            return []
    
    def create_task(self, task_id: str, target: str, modules: List[str]):
        """Create a new task record"""
        try:
            modules_json = json.dumps(modules, ensure_ascii=False)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO tasks (task_id, target, modules)
                    VALUES (?, ?, ?)
                """, (task_id, target, modules_json))
                conn.commit()
                
            logger.info(f"Created task {task_id} for target {target}")
        except Exception as e:
            logger.error(f"Failed to create task: {str(e)}")
            raise
    
    def update_task_status(self, task_id: str, status: str, completed_at: Optional[str] = None):
        """Update task status"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if completed_at:
                    cursor.execute("""
                        UPDATE tasks SET status = ?, completed_at = ? WHERE task_id = ?
                    """, (status, completed_at, task_id))
                else:
                    cursor.execute("""
                        UPDATE tasks SET status = ? WHERE task_id = ?
                    """, (status, task_id))
                
                conn.commit()
                logger.info(f"Updated task {task_id} status to {status}")
        except Exception as e:
            logger.error(f"Failed to update task status: {str(e)}")
            raise
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a task by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM tasks WHERE task_id = ?
                """, (task_id,))
                
                row = cursor.fetchone()
                if row:
                    task = dict(row)
                    task["modules"] = json.loads(task["modules"])
                    return task
                return None
        except Exception as e:
            logger.error(f"Failed to retrieve task: {str(e)}")
            return None
    
    def export_results(self, task_id: str, filepath: str, format: str = "json"):
        """Export results to a file"""
        results = self.get_results(task_id)
        
        if format.lower() == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        elif format.lower() == "txt":
            with open(filepath, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"Module: {result['module_name']}\n")
                    f.write(f"Timestamp: {result['timestamp']}\n")
                    f.write(json.dumps(result['result'], indent=2, ensure_ascii=False))
                    f.write("\n\n")
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        logger.info(f"Exported results for task {task_id} to {filepath}")


# Global storage instance
storage = Storage()
