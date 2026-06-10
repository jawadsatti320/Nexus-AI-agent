import os
import uuid
from typing import AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are Nexus, an advanced AI agent built to solve complex real-world tasks.

You have access to powerful tools:
- web_search: Search the internet for current information
- code_executor: Write and execute Python code
- file_reader: Read and analyze uploaded documents
- calculator: Perform precise mathematical calculations
- database_query: Query structured data

Always use tools when they help give better answers.
Think step by step. Explain what tool you are using and why.
Provide clear, structured responses."""


class NexusAgent:
    def __init__(self, tools: list):
        self.tools = tools
        self.conversations: dict = {}
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL_NAME", "gpt-4o"),
            temperature=0.1,
            streaming=True,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

    def _get_or_create_executor(self, conversation_id: str) -> AgentExecutor:
        if conversation_id not in self.conversations:
            memory = ConversationBufferWindowMemory(
                memory_key="chat_history",
                return_messages=True,
                k=10
            )
            agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
            executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                memory=memory,
                verbose=True,
                max_iterations=5,
                handle_parsing_errors=True,
                return_intermediate_steps=True
            )
            self.conversations[conversation_id] = executor
        return self.conversations[conversation_id]

    async def run(self, message: str, conversation_id: str = None) -> dict:
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        executor = self._get_or_create_executor(conversation_id)
        result = await executor.ainvoke({"input": message})
        tool_calls = []
        for step in result.get("intermediate_steps", []):
            action, observation = step
            tool_calls.append({
                "tool": action.tool,
                "input": action.tool_input,
                "output": str(observation)
            })
        return {
            "response": result["output"],
            "tool_calls": tool_calls,
            "conversation_id": conversation_id,
            "tokens_used": 0
        }

    async def run_stream(self, message: str, conversation_id: str = None) -> AsyncGenerator:
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        executor = self._get_or_create_executor(conversation_id)
        yield {"type": "start", "conversation_id": conversation_id}
        async for event in executor.astream_events({"input": message}, version="v1"):
            kind = event["event"]
            if kind == "on_tool_start":
                yield {"type": "tool_call", "tool": event["name"], "input": event["data"].get("input", {})}
            elif kind == "on_tool_end":
                yield {"type": "tool_result", "tool": event["name"], "output": str(event["data"].get("output", ""))[:500]}
            elif kind == "on_llm_stream":
                chunk = event["data"].get("chunk")
                if chunk and hasattr(chunk, "content") and chunk.content:
                    yield {"type": "token", "content": chunk.content}
        yield {"type": "end"}

    def clear_conversation(self, conversation_id: str):
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]

    def get_tool_names(self) -> list:
        return [t.name for t in self.tools]
