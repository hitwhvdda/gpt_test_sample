from openai import OpenAI
import os
import sys

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="your key",
    base_url="https://api.chatanywhere.tech/v1"
)
# vulnerabilty dir
vullist = ['Int_Overflow','memory_leak','OS_Command_Injection','use_after_free']
#vullist = ['use_after_free']
datadir = '/home/ao_ding/GPT_VUL/data/'
gptoutdir = '/home/ao_ding/GPT_VUL/gpt_output/'


def gpt_35_api_stream(messages: list):
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

if __name__ == '__main__':
    prompt = "Please test the following code for vulnerabilities, give the type of vulnerability and the location of the vulnerability and give the fixed code:\n"
    for vul in vullist:
        workdir = datadir + vul
        os.chdir(workdir)
        filenamelist = os.listdir()
        for filename in filenamelist:
            file_path = workdir + '/' + filename 
            with open(file_path, 'r') as file:
                file_content = file.read()
            gpt_input = prompt + file_content
            #print(gpt_input)
            out_filename = filename.split('.')[0] + '.txt'
            with open(gptoutdir + vul + '/' + out_filename, 'w') as f:
                sys.stdout = f
                messages = [{'role': 'user','content': gpt_input},]
                gpt_35_api_stream(messages)
            
            sys.stdout = sys.__stdout__
            print("analysis" + filename + "success!")