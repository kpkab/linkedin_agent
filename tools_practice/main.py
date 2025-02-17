import asyncio
from langchain_core.tools import StructuredTool

def multiply(x: int, y: int) -> int:
    """Multiplies two numbers."""
    return x * y

async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

multiply_tool = StructuredTool.from_function(
    func = multiply,
    croutine = amultiply,
)

async def main():
    print(multiply_tool.invoke({"x": 2, "y": 3}))  # Synchronous call
    print(await multiply_tool.ainvoke({"x": 2, "y": 3}))  # Asynchronous call


asyncio.run(main())