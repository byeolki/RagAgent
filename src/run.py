import os
from agent import Agent
from utils import id_generator, Logger

def main():
    chat_id = id_generator()
    agent = Agent(chat_id)
    while 1:
        question = input("Question input: ")
        question_id = id_generator()
        logger = Logger(chat_id, question_id)
        logger.info(f"chat_id: {chat_id}, question_id: {question_id}")
        logger.info("Loaded agent")
        if question == "exit": 
            logger.info("Finish Process.")
            return
        data = agent.input_question(question_id, question, logger)
        response = agent.answer_generate(question_id, data, logger)
        logger.info(response)

if __name__ == "__main__":
    main()