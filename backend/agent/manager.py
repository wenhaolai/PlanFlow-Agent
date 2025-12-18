"""
Agent 主程序，负责管理和协调各个组件的工作。
"""
from typing import List

from agent.executor import Executor
from agent.planner import Planner
from agent.schema import AgentState, StepStatus, StepRecord
from agent.tools import web_search

class AgentManager:
    def __init__(self, max_steps: int):
        self.tools = [web_search]

        self.planner = Planner(tools=self.tools)
        self.executor = Executor(tools=self.tools)

        self.max_steps = max_steps

    def run(self, problem: str) -> AgentState:
        plan = self.planner.create_initial_plan(problem)

        agent_state = AgentState(
            problem=problem,
            current_plan=plan,
            history=[]
        )

        step_count = 0

        # 2. 主执行循环
        while not agent_state.is_task_completed():
            if step_count >= self.max_steps:
                break

            next_step = agent_state.current_plan.next_step()
            if not next_step:
                # 没有可执行步骤，但也没 final_answer → 交给 replanner
                self.planner.refine_plan(current_plan=plan, history=agent_state.history)
                step_count += 1
                continue

            # 3. 执行单步
            result = self.executor.execute_step(step=next_step, history=agent_state.history)
            print(f"In Manage, success executing step {next_step.id}, result is {result.raw_output}")

            # 4. 更新 step 状态
            if result.is_success:
                next_step.status = StepStatus.COMPLETED
            else:
                next_step.status = StepStatus.FAILED
                agent_state.last_error = result.error_message

            # 5. 记录历史
            agent_state.history.append(
                StepRecord(step=next_step, result=result)
            )

            # 6. 是否完成？
            if agent_state.current_plan.final_answer:
                break

            # 7. 交给 Replanner 判断是否需要调整计划
            self.planner.refine_plan(current_plan=plan, history=agent_state.history)

            step_count += 1

        return agent_state

if __name__ == "__main__":
    agent = AgentManager(max_steps=10)
    agent_status = agent.run(problem="今年f1冠军得主的家乡在哪里？")
    print(agent_status)