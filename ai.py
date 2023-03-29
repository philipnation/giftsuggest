import openai
openai.api_key = "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"
def text():
    prompt = input("ask now: ")
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2000
        )
        print(response["choices"][0]["text"])
    except openai.error.APIConnectionError:
        print("connection error try again")
    
def img():
    response = openai.Image.create(
    prompt='draw object with this desciption: dog playing chess',
    n=1,
    size="256x256",
    )
    return response["data"][0]["url"]

text()