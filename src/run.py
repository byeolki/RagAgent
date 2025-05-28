import os
from agent import Agent
from utils import generate_id

def main():
    chat_id = generate_id()
    agent = Agent(chat_id)
    while 1:
        question = input("Question input: ")
        question_id = generate_id()
        print(f"ChatID: {chat_id}, QuestionID: {question_id}")
        if question == "exit":
            return
        response = agent.handle_query(question_id, question)
        print(response)

if __name__ == "__main__":
    main()
