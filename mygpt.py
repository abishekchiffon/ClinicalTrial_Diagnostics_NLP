import re
import openai
import time

#openai.api_key = ""

class MyGPT:
    MODELS_ARRAY = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k", "gpt-4-1106-preview"]
    MODEL_DEFAULT = "gpt-3.5-turbo-16k"
    #MODEL_DEFAULT = "gpt-4"
    TEMPERATURE_DEFAULT = 0.2
    TOP_P_DEFAULT = 0.1
    MAX_TOKENS_DEFAULT = 32000
    N_DEFAULT = 1
    FREQUENCY_PENALTY_DEFAULT = 0.0
    PRESENCE_PENALTY_DEFAULT = 0.0
    TEMPERATURE_MAX = 2.0
    TOP_P_MAX = 1.0
    MAX_TOKENS_MAX = 32000
    N_MAX = 10
    FREQUENCY_PENALTY_MAX = 2.0
    PRESENCE_PENALTY_MAX = 2.0
    TEMPERATURE_MIN = 0.0
    TOP_P_MIN = 0.0
    MAX_TOKENS_MIN = 0
    N_MIN = 1
    FREQUENCY_PENALTY_MIN = -2.0
    PRESENCE_PENALTY_MIN = -2.0
    
    def __init__(self, raw_settings):
        self.raw_settings = raw_settings
        self.model = MyGPT.MODEL_DEFAULT
        self.temperature = MyGPT.TEMPERATURE_DEFAULT
        self.top_p = MyGPT.TOP_P_DEFAULT
        self.max_tokens = MyGPT.MAX_TOKENS_DEFAULT
        self.n = MyGPT.N_DEFAULT
        self.frequency_penalty = MyGPT.FREQUENCY_PENALTY_DEFAULT
        self.presence_penalty = MyGPT.PRESENCE_PENALTY_DEFAULT
        self.messages = []
        self.settings_array = self._to_settings_array(self._to_raw_settings_array(raw_settings))
        self._set_settings(self.settings_array)
        #print(raw_settings)

    # def ask(self):
    #     output = self.raw_settings
    #     try:
    #         self.response = self.chat_completion()
    #         self.answers = self._to_answers(self.response)
    #         self.answer = self.answers[0]
    #         for answer in self.answers:
    #             output += f"\n\n@@ANSWER\n{answer}"
    #         output += f"\n\n@@QUESTION\n"
    #         return output
    #     except Exception as e:
    #         output += "\n\n" + str(e)
    #         return output

    # def ask(self):
    #     output = self.raw_settings
    #     attempts = 0
    #     max_attempts = 100
    #     sleep_seconds = 1

    #     while attempts < max_attempts:
    #         try:
    #             self.response = self.chat_completion()
    #             self.answers = self._to_answers(self.response)
    #             self.answer = self.answers[0]
    #             for answer in self.answers:
    #                 output += f"\n\n@@ANSWER\n{answer}"
    #             output += f"\n\n@@QUESTION\n"
    #             return output
    #         except Exception as e:
    #             attempts += 1
    #             print(str(e))
    #             if attempts == max_attempts - 1:
    #                 self.model = "gpt-3.5-turbo-16k"
    #             if attempts == max_attempts:
    #                 output += "\n\n" + str(e)
    #                 return output

    def ask(self):
        output = self.raw_settings
        attempts = 0
        max_attempts = 60
        sleep_seconds = 5

        while attempts < max_attempts:
            try:
                self.response = self.chat_completion()
                self.answers = self._to_answers(self.response)
                self.answer = self.answers[0]
                for answer in self.answers:
                    output += f"\n\n@@ANSWER\n{answer}"
                output += f"\n\n@@QUESTION\n"
                return output
            except Exception as e:
                attempts += 1
                print(str(e))
                print("Failed GPT Call.  Retry in " + str(sleep_seconds) + ". Attempts remaining: " + str(max_attempts - attempts))
                time.sleep(sleep_seconds)
                if attempts == max_attempts - 1:
                    self.model = "gpt-3.5-turbo-16k"
                if attempts == max_attempts:
                    output += "\n\n" + str(e)
                    return output

    def chat_completion(self):
        print(f"Called {self.model} with tokens: " + str(len(self.raw_settings)/4))
        return openai.ChatCompletion.create(messages = self.messages, 
                                                model = self.model, 
                                                temperature = self.temperature,
                                                top_p = self.top_p,
                                                frequency_penalty = self.frequency_penalty,
                                                max_tokens = min(self.max_tokens, self._calculate_max_token_for_answer(self.messages, self.model)),
                                                n = self.n,
                                                presence_penalty = self.presence_penalty)

    def _to_raw_settings_array(self, raw_settings):
        pattern = r"@@(\w+)(.*?)(?=(@@|$))"
        matches = re.findall(pattern, raw_settings, re.DOTALL)
        return [(match[0], match[1]) for match in matches]
    
    def _to_int(self, raw_string, default_value):
        match = re.search(r"(-?\d+)", raw_string)
        if match:
            return int(match.group(1))
        else:
            return int(default_value)
    
    def _to_float(self, raw_string, default_value):
        match = re.search(r"(-?\d*\.\d+|-?\d+)", raw_string)
        if match:
            return float(match.group(1))
        else:
            return float(default_value)
        
    def _to_model(self, raw_string, default_value):
        self.MODELS_ARRAY.sort(key=len, reverse=True)
        for pattern in self.MODELS_ARRAY:
            if re.search(pattern, raw_string):
                return pattern
        return default_value

    def _clamp(self, value, minimum, maximum):
        return max(minimum, min(value, maximum))

    def _get_last_value_of_key(self, key, settings_array):
        for t in reversed(settings_array):
            if t[0] == key:
                return t[1]
        return None

    def _set_settings(self, settings_array):
        self.model = self._get_last_value_of_key("model", settings_array) or self.model
        self.temperature = self._get_last_value_of_key("temperature", settings_array) or self.temperature
        self.top_p = self._get_last_value_of_key("top_p", settings_array) or self.top_p
        self.max_tokens = self._get_last_value_of_key("max_tokens", settings_array) or self.max_tokens
        self.n = self._get_last_value_of_key("n", settings_array) or self.n
        self.frequency_penalty = self._get_last_value_of_key("frequency_penalty", settings_array) or self.frequency_penalty
        self.presence_penalty = self._get_last_value_of_key("presence_penalty", settings_array) or self.presence_penalty
        self.messages = self._to_messages(settings_array)

    def _to_settings_array(self, raw_settings_array):
        settings_array = []
        for x in raw_settings_array:
            key = x[0].lower()
            value = x[1]
            if key == "model":
                value = self._to_model(value, self.MODEL_DEFAULT)
                settings_array.append((key, value))
            elif key == "temperature":
                value = self._to_float(value, self.TEMPERATURE_DEFAULT)
                value = self._clamp(value, self.TEMPERATURE_MIN, self.TEMPERATURE_MAX)
                settings_array.append((key, value))
            elif key == "top_p":
                value = self._to_float(value, self.TOP_P_DEFAULT)
                value = self._clamp(value, self.TOP_P_MIN, self.TOP_P_MAX)
                settings_array.append((key, value))
            elif key == "max_tokens":
                value = self._to_int(value, self.MAX_TOKENS_DEFAULT)
                value = self._clamp(value, self.MAX_TOKENS_MIN, self.MAX_TOKENS_MAX)
                settings_array.append((key, value))
            elif key == "n":
                value = self._to_int(value, self.N_DEFAULT)
                value = self._clamp(value, self.N_MIN, self.N_MAX)
                settings_array.append((key, value))
            elif key == "frequency_penalty":
                value = self._to_float(value, self.FREQUENCY_PENALTY_DEFAULT)
                value = self._clamp(value, self.FREQUENCY_PENALTY_MIN, self.FREQUENCY_PENALTY_MAX)
                settings_array.append((key, value))
            elif key == "presence_penalty":
                value = self._to_float(value, self.PRESENCE_PENALTY_DEFAULT)
                value = self._clamp(value, self.PRESENCE_PENALTY_MIN, self.PRESENCE_PENALTY_MAX)
                settings_array.append((key, value))
            else:
                settings_array.append((key, value))
        return settings_array
    
    def _to_messages(self, settings_array):
        roles = {
            "system": "system",
            "user": "user",
            "assistant": "assistant",
            "question": "user",
            "answer": "assistant"
        }
        messages = []
        for x in settings_array:
            if x[0] in roles:
                messages.append({
                    "role": roles[x[0]],
                    "content": x[1]
                })
        return messages

    def _to_answers(self, response):
        return [choice["message"]["content"] for choice in response["choices"]]

    def _estimate_tokens(self, messages):
        characters = sum(len(message['content']) for message in messages)
        return int(characters / 4)
    
    def _calculate_max_token_for_answer(self, messages, model):
        model_max_token = [
            {"model": "gpt-3.5-turbo", "max_token": 4097},
            {"model": "gpt-3.5-turbo-16k", "max_token": 16385},
            {"model": "gpt-4", "max_token": 8192},
            {"model": "gpt-4-32k", "max_token": 32768},
            {"model": "gpt-4-1106-preview", "max_token": 32768},
        ]
        model_max_token = {"gpt-3.5-turbo": 4097, "gpt-3.5-turbo-16k": 16385, "gpt-4": 8192, "gpt-4-32k": 32768, "gpt-4-1106-preview": 4097}
        total_max_token = model_max_token[model]
        messages_token = self._estimate_tokens(messages)
        return int(total_max_token * 0.9 - messages_token * 1.2)
    

def ask(query):
    gpt = MyGPT(query)
    gpt.ask()
    return gpt.answer