from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.mysql import get_db
from services.UserService import get_current_user
from models.UserModel import User
from models.TasksModel import Task
from models.ChatModel import Chat
from schemas.ChatSchema import ChatRequest, ChatResponse
from agent.manager import AgentManager

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Handle Task
    if request.task_id:
        task = db.query(Task).filter(Task.id == request.task_id, Task.user_id == current_user.id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    else:
        # Create new task
        task = Task(
            user_id=current_user.id,
            title=request.message[:50] if len(request.message) > 50 else request.message
        )
        db.add(task)
        db.commit()
        db.refresh(task)

    # 2. Save User Message
    user_chat = Chat(
        task_id=task.id,
        role="user",
        content=request.message
    )
    db.add(user_chat)
    db.commit()

    # 3. Run Agent
    # Initialize AgentManager with a max step limit
    agent = AgentManager(max_steps=10)
    
    try:
        # Run the agent
        agent_state = agent.run(request.message)
        
        # Extract final answer
        final_answer = agent_state.current_plan.final_answer
        if not final_answer:
            final_answer = "抱歉，我无法完成您的请求，请稍后再试。"
            
    except Exception as e:
        # Handle any errors during agent execution
        print(f"Agent execution error: {e}")
        final_answer = f"处理请求时发生错误: {str(e)}"
        # We might want to return a partial state or just the error
        # For now, we'll construct a minimal state or just proceed
        # Since agent_state might not be defined if error happens early, we need to be careful.
        # But for this simple implementation, let's assume run() handles its own internal errors 
        # and returns a state with error info if possible. 
        # If it crashes, we catch it here.
        # To be safe, let's mock a state or re-raise if critical.
        # But let's stick to the happy path + basic error handling.
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")

    # 4. Save Assistant Message
    assistant_chat = Chat(
        task_id=task.id,
        role="assistant",
        content=final_answer
    )
    db.add(assistant_chat)
    db.commit()

    # 5. Return Response
    return ChatResponse(
        task_id=task.id,
        final_answer=final_answer
    )
