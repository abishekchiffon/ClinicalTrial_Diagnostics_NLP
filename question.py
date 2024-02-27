import mygpt


def question(to_language, data, question):
    #template = f"Here is the text: [{data}] \
    #   Based on the above context, Could you answer the following question based on the text provided in {to_language} - [{question}]? : "
    template = f"Please carefully analyze the following text: [{data}]. Based on your analysis, formulate a response to this question: [{question}]. Your response should directly address the question by leveraging insights from the provided text. Importantly, present your answer in {to_language} language. This task involves two key steps: understanding and interpreting the text, and then crafting an answer that both reflects this understanding and is expressed in the specified language."
    instruction = f'{template}'
    print(template)
    return mygpt.ask(f"@@SYSTEM {instruction} @@QUESTION {data}")

def run():
    # Get user input for the language
    to_language = input("Enter the language you want to summarise to: ")
    
    # Get user input for the text to translate
    data = input("Enter the text you want to translate: ")
    
    # Translate and print the result
    translated_text = question(to_language, data, question)
    print("Translated text:", translated_text)
    
if __name__ == '__main__':
    run()

