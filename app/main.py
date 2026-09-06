from app.agent.react_loop import ReActAgent


def main():

    print("====================================")
    print("     GOVERNMENT SCHEME TRACKER")
    print("====================================")

    print("\nAsk me about government schemes.")
    print("You can describe your situation naturally.")
    print("Type 'exit' to quit.")

    agent = ReActAgent()

    while True:

        user_query = input("\nYou:\n> ")

        if user_query.lower() == "exit":
            print("\nGoodbye!")
            break

        answer = agent.run(
            user_query,
            {}
        )

        print("\nAgent:")
        print(answer)


if __name__ == "__main__":
    main()