import os
from openai import OpenAI
import json

if len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "llama-3.3-70b-versatile"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
else:
    OPENAI_API_KEY = os.getenv('OPENAI_KEY')
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = (
        """You are a seasoned content writer for a YouTube Shorts channel, specializing in facts videos. 
        Your facts shorts are concise, each lasting less than 50 seconds (approximately 140 words). 
        They are incredibly engaging and original. When a user requests a specific type of facts short, you will create it.

        For instance, if the user asks for:
        Weird facts
        You would produce content like this:

        Weird facts you don't know:
        - Bananas are berries, but strawberries aren't.
        - A single cloud can weigh over a million pounds.
        - There's a species of jellyfish that is biologically immortal.
        - Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.
        - The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.
        - Octopuses have three hearts and blue blood.

        You are now tasked with creating the best short script based on the user's requested type of 'facts'.

        Keep it brief, highly interesting, and unique.

        Stictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

        # Output
        {"script": "Here is the script ..."}

        Please output JSON in one line with only double quotes ("), and do not escape single quotes (') at all. Only newline characters should be escaped as \\n.
    """
    )

    # response = client.chat.completions.create(
    #         model=model,
    #         messages=[
    #             {"role": "system", "content": prompt},
    #             {"role": "user", "content": topic}
    #         ]
    #     )
    # content = response.choices[0].message.content
    # try:
    #     script = json.loads(content)["script"]
    # except Exception as e:
    #     json_start_index = content.find('{')
    #     json_end_index = content.rfind('}')
    #     print(content)
    #     content = content[json_start_index:json_end_index+1]
    #     script = json.loads(content)["script"]
    # return script

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic}
        ]
    )
    content = response.choices[0].message.content
    content = content.replace("\\'", "'")
    print("원본 content:", repr(content))

    script = ""
    try:
        script = json.loads(content)["script"]
    except Exception as e:
        print(f"JSON parsing error: {e}")
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        if json_start_index != -1 and json_end_index != -1:
            partial_json = content[json_start_index:json_end_index+1]
            # 개행 문자 escape 처리
            partial_json = partial_json.replace('\r\n', '\\n').replace('\n', '\\n')
            try:
                script = json.loads(partial_json)["script"]
            except Exception as inner_e:
                print(f"JSON 재파싱 실패: {inner_e}")
                print("partial_json:", repr(partial_json))
                script = "No valid script generated."
        else:
            print("JSON 구조 감지 실패")
            script = "No valid script generated."
    return script

    # try:
    #     script = json.loads(content)["script"]
    # except Exception as e:
    #     print(f"JSON parsing error: {e}")
    #     print("원본 content:", repr(content))
    #     json_start_index = content.find('{')
    #     json_end_index = content.rfind('}')
    #     if json_start_index != -1 and json_end_index != -1:
    #         partial_json = content[json_start_index:json_end_index+1]
    #         import re
    #         partial_json = re.sub(r'(?<!\\)\n', r'\\n', partial_json)
    #         try:
    #             script = json.loads(partial_json)["script"]
    #         except Exception as inner_e:
    #             print(f"JSON 재파싱 실패: {inner_e}")
    #             print("partial_json:", repr(partial_json))
    #             script = "No valid script generated."
    #     else:
    #         print("JSON 구조 감지 실패")
    #         script = "No valid script generated."