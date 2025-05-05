import os
from agent import ToolSelector, AnswerGenerator
from utils import id_generator

def main():
    chat_id = id_generator(1, 10000, os.listdir("./data/chat"))*10000
    tool_selector = ToolSelector(chat_id)
    print("loaded tool_selector")
    answer_generator = AnswerGenerator(chat_id)
    print("loaded answer_generator")
    print(chat_id)
    while 1:
        question = input()
        if question == "exit": 
            print("대화가 종료되었습니다.")
            return
        question_id = chat_id+id_generator(1, 9999, os.listdir(f"./data/chat/{chat_id}/cache"))
        data = tool_selector.input_question(question_id, question)
        response = answer_generator.answer_generate(question_id, data)
        print(response)

if __name__ == "__main__":
    main()