from app.ai.llm_client import LLMClient


def main():
    print("Starting test...")

    client = LLMClient()

    print("Client created.")

    response = client.generate(
        "Respond with exactly: Hello from GPT!"
    )

    print("Response received.")
    print(repr(response))


if __name__ == "__main__":
    main()