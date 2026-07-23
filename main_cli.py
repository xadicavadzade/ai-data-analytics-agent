import asyncio

from app.models.state import AgentState
from app.builder import create_agent


async def main():

    agent = create_agent()

    print("Welcome SQL Agent :)")
    print("Type 'x' to exit.")

    while True:

        question = input(">> ")

        if question.lower() == "x":
            break

        state = AgentState(
            question=question,
            database_path="data/sales.db"
        )

        result = await agent.run(state)


        print(result.insight)


if __name__ == "__main__":
    asyncio.run(main())