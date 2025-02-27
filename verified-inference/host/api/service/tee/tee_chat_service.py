from typing import AsyncGenerator

async def execute(enclave_name: str) -> AsyncGenerator[str, None]:
    # Split the test message into chunks
    chunks = ["this ", "is ", "a ", "test"]
    for chunk in chunks:
        # Format as SSE data
        yield f"data: {chunk}\n\n"
    yield "data: [DONE]\n\n" 