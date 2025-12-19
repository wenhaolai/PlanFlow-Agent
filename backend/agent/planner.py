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
from agent.prompts import PLANNER_SYSTEM_PROMPT_TEMPLATE, REPLANNER_SYSTEM_PROMPT_TEMPLATE

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
        """
        根据执行反馈重规划任务
        :param current_plan: 当前计划
        :param history: 执行历史记录
        :return: 新的计划
        """
        logger.info(f"正在根据反馈调整计划: {current_plan.original_goal}")
        if history is None:
            history = []

        # 1. 准备上下文
        tool_list_str = "\n".join([f"- {name}: {func.__doc__}" for name, func in self.tools.items()])
        
        # 序列化当前计划和历史 (兼容 Pydantic v1/v2)
        try:
            current_plan_str = current_plan.model_dump_json()
            history_str = json.dumps([h.model_dump() for h in history], ensure_ascii=False)
        except AttributeError:
            current_plan_str = current_plan.json()
            history_str = json.dumps([h.dict() for h in history], ensure_ascii=False)

        # 2. 填充 Prompt
        system_prompt = Template(REPLANNER_SYSTEM_PROMPT_TEMPLATE).safe_substitute(
            tool_list=tool_list_str,
            current_plan=current_plan_str,
            execution_history=history_str
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请根据执行情况调整计划。目标：{current_plan.original_goal}"}
        ]

        try:
            response = self._call_llm(messages)
            print(f"重规划调用得到的计划JSON格式：{response}")

            plan_data = self._parse_json_response(response)

            if plan_data.get("final_answer"):
                return Plan(
                    steps=current_plan.steps,
                    original_goal=current_plan.original_goal,
                    final_answer=plan_data.get("final_answer")
                )
            
            new_steps = []
            # 建立旧步骤的查找表 (id -> step)
            old_steps_map = {s.id: s for s in current_plan.steps}

            for step_data in plan_data.get("steps", []):
                step_id = step_data["id"]
                
                # 默认状态为 PENDING
                status = StepStatus.PENDING
                
                # 如果是已有步骤，保留其状态
                if step_id in old_steps_map:
                    status = old_steps_map[step_id].status
                
                new_steps.append(Step(
                    id=step_id,
                    description=step_data["description"],
                    status=status,
                    action_type=step_data["action_type"],
                    tool_name=step_data.get("tool_name"),
                    tool_args=step_data.get("tool_args")
                ))

            print(f"重规划后的steps为：{new_steps}")
            
            return Plan(
                steps=new_steps, 
                original_goal=current_plan.original_goal
            )

        except Exception as e:
            logger.error(f"重规划失败: {e}")
            return current_plan

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