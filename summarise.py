import mygpt


def summarise(to_language, data):
    instruction = f'Could you provide a structured summary of the key points from the diabetes treatment clinical study consent form? Please include the purpose of the study, the procedures involved, any potential side effects, the benefits of participating, how privacy is handled, and the nature of voluntary participation. {to_language}.'
    return mygpt.ask(f"@@SYSTEM {instruction} @@QUESTION {data}")

def run():
    # Get user input for the language
    to_language = input("Enter the language you want to summarise to: ")
    
    # Get user input for the text to translate
    data = input("Enter the text you want to translate: ")
    
    # Translate and print the result
    translated_text = summarise(to_language, data)
    print("Translated text:", translated_text)
    
if __name__ == '__main__':
    run()

