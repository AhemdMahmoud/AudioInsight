from langdetect import detect
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os

# Set your API key
api_key = "U5QUXeaOzkeyBeQFkSKX23Qh5AQGfnni"
client = MistralClient(api_key=api_key)
model = "mistral-large-latest"

def summarize_text(text):
    word_limit = 150
    detected_language = detect(text)
    title = text.split('\n')[0]

    if detected_language == "ar":
        language_instruction_text = f"الرجاء تلخيص النص التالي بشكل موجز مع الحفاظ على الأفكار الرئيسية والتفاصيل الهامة. تأكد من أن الملخص واضح ومتماسك ولا يتجاوز  كلمه"

        language_instruction_title = """
        الرجاء تلخيص عنوان النص التالي بشكل إبداعي وجذاب. يجب أن يكون العنوان موجزًا ولكنه يلفت الأنظار ويعكس جوهر الموضوع بشكل مبتكر. تأكد من أن العنوان يعبر عن أهمية الموضوع بطريقة تثير الفضول وتلفت الانتباه للقارئ, اجعل العنوان متوازنًا بين الإبداع والوضوح.
        """

    else:
        language_instruction_text = f"Please summarize the following text concisely while preserving the key ideas and essential details. Ensure the summary is clear, coherent, and does not exceed {word_limit} words or {word_limit / len(text.split()) * 100}% of the original text's length. Focus on maintaining the central themes , Make sure the summary has a smooth flow between the ideas while staying concise and informative. Here's the text:"

        language_instruction_title = "Please summarize the title of the following text in a creative and engaging manner. The title should be concise yet attention-grabbing and reflect the core essence of the subject in an innovative way. Ensure the title conveys the importance of the topic in a way that sparks curiosity and captures the reader's attention. Make the title a balance between creativity and clarity."


    title_response = client.chat(
        model=model,
        messages=[
            ChatMessage(role="user", content=f"{language_instruction_title}\n\n{title}")
        ]
    )

    text_response = client.chat(
        model=model,
        messages=[
            ChatMessage(role="user", content=f"{language_instruction_text}\n\n{text}")
        ]
    )

    return title_response, text_response

