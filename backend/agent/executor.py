"""
backend.agent.executor 的 Docstring
负责执行计划中的单步骤任务。
"""
import logging
import os
import json
from string import Template
from typing import Callable, List, Optional

from openai import OpenAI

from agent.schema import StepResult, Step, StepStatus, StepRecord
from agent.prompts import TOOL_ARGUMENT_PROMPT_TEMPLATE, LLM_EXECUTOR_PROMPT_TEMPLATE, FINAL_FALLBACK_SYSTEM_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

class Executor:
    def __init__(self, tools: List[Callable]):
        self.client = OpenAI(
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 示例URL
        )
        self.model = "qwen-plus"  # 示例模型

        # 加载可调用工具列表
        self.tools = { func.__name__: func for func in tools}

    def execute_step(self, step:Step, history:Optional[List[StepRecord]] = None) -> StepResult:
        if history is None:
            history = []
        # 1. 检查当前步骤状态
        if step.status != StepStatus.PENDING:
            return StepResult(
                is_success=False,
                error_message=f"Step {step.id} is not PENDING, currrent status is {step.status}"
            )
        # 2. 标记为RUNNING
        step.status = StepStatus.RUNNING

        print(f"Executing step {step.id}, action type is {step.action_type}")
        try:
            if step.action_type == "LLM":
                return self._execute_llm_step(step, history)
            elif step.action_type == "TOOL":
                return self._execute_tool_step(step, history)
            else:
                raise ValueError(f"Unknown action type {step.action_type}")
        except Exception as e:
            logger.error(f"Execution failed for step {step.id}: {e}")
            step.status = StepStatus.FAILED
            return StepResult(
                is_success=False,
                error_message=str(e)
            )

    def _execute_llm_step(self, step:Step, history: List[StepRecord]) -> StepResult:
        print(f"Executing step {step.id}, history is {history}")
        # 1. 准备 Prompt
        history_str = ""
        if history:
            history_str = "\n".join([f"Step {record.step.id}: {record.step.description}\nResult: {record.result.raw_output}" for record in history])
        else:
            history_str = "无"

        prompt = Template(LLM_EXECUTOR_PROMPT_TEMPLATE).safe_substitute(
            current_step=step.description,
            history=history_str
        )

        # 2. 调用 LLM
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "请执行当前步骤"}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"}
            )

            print(f"execute LLM response: {response}")

            content = response.choices[0].message.content
            result_json = json.loads(content)
            
            # 3. 解析结果
            # 简化逻辑：直接提取 content，若无则使用原始 JSON 字符串
            
            step.status = StepStatus.COMPLETED
            
            return StepResult(
                is_success=True,
                raw_output=result_json.get("content", content),
                structured_output=result_json
            )

        except Exception as e:
            step.status = StepStatus.FAILED
            logger.error(f"LLM execution failed: {e}")

            return StepResult(
                is_success=False,
                error_message=f"LLM execution failed: {str(e)}"
            )

    def _execute_tool_step(self, step:Step, history: List[StepRecord]) -> StepResult:
        print(f"Executing step {step.id}, history is {history}")
        tool_name = step.tool_name
        
        # 1. 验证工具是否存在
        if not tool_name:
            return StepResult(
                is_success=False,
                error_message=f"Tool name is missing for TOOL step {step.id}."
            )
            
        tool_func = self.tools.get(tool_name)
        if not tool_func:
            return StepResult(
                is_success=False,
                error_message=f"Tool '{tool_name}' not found."
            )

        # 2. 使用 LLM 生成参数
        try:
            history_str = ""
            if history:
                history_str = "\n".join([f"Step {record.step.id}: {record.step.description}\nResult: {record.result.raw_output}" for record in history])
            else:
                history_str = "无"

            prompt = Template(TOOL_ARGUMENT_PROMPT_TEMPLATE).safe_substitute(
                tool_name=tool_name,
                tool_doc=tool_func.__doc__,
                step_description=step.description,
                history=history_str
            )

            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": "请生成参数"}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            args_content = response.choices[0].message.content

            print(f"execute TOOL args: {args_content}")

            tool_args = json.loads(args_content)
            logger.info(f"LLM generated args for {tool_name}: {tool_args}")

        except Exception as e:
            logger.warning(f"Failed to generate args using LLM, falling back to planner args. Error: {e}")
            tool_args = step.tool_args or {}

        # 3. 执行工具
        try:
            logger.info(f"Executing tool {tool_name} with args: {tool_args}")
            print(f"Executing tool {tool_name} with args: {tool_args}")

            # 假设工具函数支持 **kwargs 传参
            result = tool_func(**tool_args)

            print(f"execute TOOL {tool_name} success for {step.id}, get result len: {len(result)}")
            step.status = StepStatus.COMPLETED

            return StepResult(
                is_success=True,
                raw_output=str(result),
                # 尝试将结果作为结构化数据，如果不是 dict/list 则为 None
                structured_output=result if isinstance(result, (dict, list)) else {"result": result},
                tool_name=tool_name
            )
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            step.status = StepStatus.FAILED
            return StepResult(
                is_success=False,
                error_message=f"Tool execution failed: {str(e)}",
                tool_name=tool_name
            )

    def summary_final(self, query: str, history: List[StepRecord]) -> StepResult:
        """
        当达到最大步数限制时，尝试根据历史记录生成最终答案
        """
        logger.info("Max steps reached, generating final summary.")
        
        history_str = ""
        if history:
            history_str = "\n".join([f"Step {record.step.id}: {record.step.description}\nResult: {record.result.raw_output}" for record in history])
        else:
            history_str = "无"

        prompt = Template(FINAL_FALLBACK_SYSTEM_PROMPT_TEMPLATE).safe_substitute(
            query=query,
            history=history_str
        )

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "请给出最终答案"}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            content = response.choices[0].message.content
            
            return StepResult(
                is_success=True,
                raw_output=content,
                structured_output={"final_answer": content}
            )
            
        except Exception as e:
            logger.error(f"Final summary failed: {e}")
            return StepResult(
                is_success=False,
                error_message=f"Final summary failed: {str(e)}"
            )
