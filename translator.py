import mygpt


def translate(to_language, data):
    instruction = f'Translate the query into the language {to_language}.'
    return mygpt.ask(f"@@SYSTEM {instruction} @@QUESTION {data}")

def run():
    # Get user input for the language
    to_language = input("Enter the language you want to translate to: ")
    
    # Get user input for the text to translate
    data = input("Enter the text you want to translate: ")
    
    # Translate and print the result
    translated_text = translate(to_language, data)
    print("Translated text:", translated_text)
    
if __name__ == '__main__':
    run()

