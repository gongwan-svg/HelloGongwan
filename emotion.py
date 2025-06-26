#from functools import lru_cache

#@lru_cache(maxsize=64)#直接加上这个装饰器，时间会非常快
import json
def get_llm_response(client, *, system_prompt='', few_shot_prompt=None,#封装成函数
                     user_prompt='', model='deepseek-chat', temperature=0.2,
                     top_p=0.1, frequency_penalty=0, presence_penalty=0,
                     max_tokens=1024, stream=True):
    """获取大模型响应"""
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    if few_shot_prompt and isinstance(few_shot_prompt, list):
        messages += few_shot_prompt
    if user_prompt:
        messages.append({'role': 'user', 'content': user_prompt})
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        max_tokens=max_tokens,
        messages=messages,
        stream=True,
    )
    if not stream:
        return resp.choices[0].message.content
    return resp
    '''lru_cache()
def fib(n:int)->int:
    if n in{1,2}:
        return 1
    return fib(n-1)+fib(n-2)
for i in range(1,121):
    print(i,fib(i))'''