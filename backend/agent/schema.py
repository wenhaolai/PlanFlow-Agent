from enum import Enum
from typing import List, Optional, Literal, Any, Dict
from pydantic import BaseModel, Field

class StepStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"

class Step(BaseModel):
    """
    Planner的最小执行单元
    Planner只负责生成执行步骤，不关心具体的执行结果
    """
    id: int = Field(..., description="步骤ID")
    description: str = Field(..., description="步骤描述")
    status: StepStatus = Field(StepStatus.PENDING, description="步骤的执行状态")

    action_type: Literal["LLM", "TOOL"]

    # 如果是调用工具，Planner可以建议使用的工具
    tool_name: str | None = None
    # 使用则点存储参数，避免反复序列化
    tool_args: Dict[str, Any] | None = None

class Plan(BaseModel):
    """
    当前计划执行视图
    1. Planner每次修改replan，要么修改steps，要么完全替换plan
    2. Manager只关心next_step()
    """
    steps: List[Step] = Field(..., description="执行步骤列表")
    original_goal: str = Field(..., description="原始目标")

    # 当前任务完成后，Planner会将最终答案填写再这里
    final_answer: Optional[str] = Field(None, description="最终答案")

    def next_step(self) -> Step | None:
        """
        获取当前需要执行的步骤。
        逻辑：按顺序查找第一个状态不是 COMPLETED 或 SKIPPED 的步骤。
        """
        for step in self.steps:
            if step.status not in [StepStatus.COMPLETED, StepStatus.SKIPPED]:
                return step
        return None

class StepResult(BaseModel):
    """
    每一步执行结果
    """
    is_success: bool

    # LLM/TOOL的原始输出
    raw_output: str | None = None

    # 结构化信息，如解析出的JSON
    structured_output: Dict[str, Any] | None = None

    error_message: str | None = None
    tool_name: str | None = None

class StepRecord(BaseModel):
    """
    历史执行记录
    记录每一步的执行结果，供后续分析和调整计划使用
    """
    step: Step
    result: StepResult

class AgentState(BaseModel):
    """
    AgentState
    Agent的整体状态视图，包含当前计划和历史记录, 可用于序列化保存
    """
    problem: str = Field(...)

    # 当前计划
    current_plan: Plan

    # 历史执行记录
    history: List[StepRecord] = Field(default_factory=list)

    def is_task_completed(self) -> bool:
        return self.current_plan.final_answer is not None

    