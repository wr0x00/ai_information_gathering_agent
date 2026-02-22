import argparse
import asyncio
import sys
import os
from typing import List
from agent import InformationGatheringAgent
from storage import ResultsStorage
from config import module_config
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class InformationGatheringCLI:
    """信息收集代理的命令行界面"""
    
    def __init__(self):
        self.agent = InformationGatheringAgent()
        self.storage = ResultsStorage()
    
    def parse_arguments(self) -> argparse.Namespace:
        """解析命令行参数"""
        parser = argparse.ArgumentParser(
            description="AI信息收集代理",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例:
  python cli.py -t example.com
  python cli.py -t example.com -m whois domain
  python cli.py -t example.com --list-modules
  python cli.py --list-results
            """
        )
        
        parser.add_argument(
            "-t", "--target",
            help="要扫描的目标域名或IP地址"
        )
        
        parser.add_argument(
            "-m", "--modules",
            nargs="+",
            help="要运行的特定模块（默认：所有启用的模块）"
        )
        
        parser.add_argument(
            "--list-modules",
            action="store_true",
            help="列出所有可用模块"
        )
        
        parser.add_argument(
            "--list-results",
            action="store_true",
            help="列出所有保存的扫描结果"
        )
        
        parser.add_argument(
            "--load-result",
            help="加载并显示保存的结果文件"
        )
        
        parser.add_argument(
            "-o", "--output",
            choices=["json", "text"],
            default="text",
            help="结果的输出格式（默认：text）"
        )
        
        parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="启用详细日志记录"
        )
        
        return parser.parse_args()
    
    def list_modules(self):
        """列出所有可用模块"""
        print("可用模块:")
        print("-" * 30)
        
        modules = {
            "whois": "WHOIS信息收集",
            "domain": "域名信息和子域名枚举",
            "port": "端口扫描和C段分析",
            "sensitive": "敏感信息发现",
            "github": "GitHub代码和信息搜索"
        }
        
        for module_name, description in modules.items():
            status = "已启用" if module_name in module_config.get_enabled_modules() else "已禁用"
            print(f"{module_name:<12} | {status:<10} | {description}")
    
    def list_results(self):
        """列出所有保存的扫描结果"""
        results = self.storage.list_saved_results()
        
        if not results:
            print("未找到保存的结果。")
            return
        
        print("保存的结果:")
        print("-" * 60)
        print(f"{'文件名':<30} {'修改时间':<20}")
        print("-" * 60)
        
        for result in results:
            filename = result["filename"]
            modified = result["modified"].split("T")[0]  # 仅日期部分
            print(f"{filename:<30} {modified:<20}")
    
    async def load_and_display_result(self, filepath: str):
        """加载并显示保存的结果文件"""
        try:
            if not os.path.exists(filepath):
                # 尝试在输出目录中查找
                filepath = os.path.join(self.storage.output_dir, filepath)
                if not os.path.exists(filepath):
                    print(f"未找到结果文件: {filepath}")
                    return
            
            results = await self.storage.load_results(filepath)
            target = results.get("target", "未知")
            timestamp = results.get("scan_timestamp", "未知")
            
            print(f"\n已加载 {target} 的结果（扫描时间 {timestamp}）")
            print("=" * 60)
            
            # 显示摘要
            result_data = results.get("results", {})
            for module_name, module_results in result_data.items():
                if "error" in module_results:
                    print(f"{module_name}: 错误 - {module_results['error']}")
                else:
                    print(f"{module_name}: 成功完成")
            
        except Exception as e:
            print(f"加载结果时出错: {str(e)}")
    
    async def run_scan(self, target: str, modules: List[str] = None, output_format: str = "text"):
        """对目标运行扫描"""
        if not target:
            print("错误: 需要目标。使用 -t/--target 指定目标。")
            return
        
        print(f"开始对 {target} 进行信息收集")
        
        try:
            # 运行扫描
            if modules:
                results = await self.agent.run_specific_modules(target, modules)
            else:
                results = await self.agent.run_scan(target)
            
            # 保存结果
            if output_format == "json":
                filepath = await self.storage.save_results(target, results)
                print(f"结果已保存到: {filepath}")
            else:
                filepath = await self.storage.save_results_as_text(target, results)
                print(f"结果已保存到: {filepath}")
            
            # 显示摘要
            print("\n扫描摘要:")
            print("-" * 30)
            for module_name, module_results in results.items():
                if "error" in module_results:
                    print(f"{module_name}: 错误 - {module_results['error']}")
                else:
                    print(f"{module_name}: 成功完成")
            
            print(f"\n完整结果已保存到: {filepath}")
            
        except Exception as e:
            print(f"扫描过程中出错: {str(e)}")
            logger.error(f"扫描 {target} 时出错: {str(e)}")
    
    async def run(self):
        """运行CLI应用程序"""
        args = self.parse_arguments()
        
        # 设置日志级别
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # 处理不同的命令模式
        if args.list_modules:
            self.list_modules()
            return
        
        if args.list_results:
            self.list_results()
            return
        
        if args.load_result:
            await self.load_and_display_result(args.load_result)
            return
        
        # 运行扫描
        await self.run_scan(args.target, args.modules, args.output)


def main():
    """CLI的主入口点"""
    cli = InformationGatheringCLI()
    try:
        asyncio.run(cli.run())
    except KeyboardInterrupt:
        print("\n扫描被用户中断。")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
