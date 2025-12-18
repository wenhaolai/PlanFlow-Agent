"""
planner负责初步的任务规划和分解。
replanner负责在任务执行过程中根据反馈进行动态调整。
"""
import json
import logging
import os
from string import Template
from typing import List, Optional, Dict, Any, Callable
from openai import OpenAI

from agent.schema import StepStatus, Step, Plan, StepRecord
# from core.config import settings
# from schema import Plan, Step
from agent.prompts import PLANNER_SYSTEM_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

class Planner:
    def __init__(self, tools: Optional[List[Callable]] = None):
        # 初始化LLM客户端
        # 这里假设使用OpenAI兼容的接口，你可以根据实际情况调整
        self.client = OpenAI(
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1" # 示例URL
        )
        self.model = "qwen-plus" # 示例模型

        # 加载可调用工具列表
        self.tools = {func.__name__: func for func in tools}

    def create_initial_plan(self, goal: str) -> Plan:
        """
        根据用户目标创建初始计划
        :param goal: 用户输入的原始目标
        :return: 包含步骤列表的Plan对象
        """
        logger.info(f"正在为目标创建初始计划: {goal}")
        
        # 1. 准备工具描述
        tool_list_str = "\n".join([f"- {name}: {func.__doc__}" for name, func in self.tools.items()])
        
        # 2. 填充 Prompt
        system_prompt = Template(PLANNER_SYSTEM_PROMPT_TEMPLATE).safe_substitute(
            tool_list=tool_list_str
        )

        messages = [
            {"role":"system", "content": system_prompt},
            {"role":"user", "content": goal}
        ]
        try:
            response = self._call_llm(messages)
            print(f"初次调用得到的计划JSON格式：{response}")

            plan_data = self._parse_json_response(response)
            
            steps = []
            for step_data in plan_data.get("steps", []):
                steps.append(Step(
                    id=step_data["id"],
                    description=step_data["description"],
                    status=StepStatus.PENDING,
                    action_type=step_data["action_type"],
                    tool_name=step_data.get("tool_name"),
                    tool_args=step_data.get("tool_args")
                ))

            print(f"转化后的steps为：{steps}")

            return Plan(steps=steps, original_goal=goal)
            
        except Exception as e:
            logger.error(f"创建初始计划失败: {e}")
            # 发生错误时返回一个简单的单步计划作为兜底
            return Plan(
                steps=[Step(id=1, description=f"直接尝试解决问题: {goal}", status="pending")],
                original_goal=goal
            )

    def refine_plan(self, current_plan: Plan, history:Optional[List[StepRecord]] = None) -> Plan:
        ...

    def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        """调用LLM的辅助函数"""
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"} # 强制JSON输出
        )
        return completion.choices[0].message.content

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """解析JSON响应的辅助函数"""
        try:
            # 清理可能的Markdown标记
            cleaned_response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            logger.error(f"JSON解析失败: {response}")
            raise




if __name__ == "__main__":
    planner = Planner()
    planner.create_initial_plan("今天北京的天气适合进行户外运动吗？")