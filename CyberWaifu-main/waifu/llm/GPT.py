import json
import logging
import os

from waifu.AgentTools import Tools
from waifu.llm.Brain import Brain
from waifu.llm.VectorDB import VectorDB
from waifu.llm.SentenceTransformer import STEmbedding
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from typing import Any, List, Mapping, Optional
from langchain.schema import BaseMessage, SystemMessage
from langchain.agents import StructuredChatAgent, AgentExecutor, load_tools
from langchain.chains import LLMChain

import openai


class GPT(Brain):
    def __init__(self, api_key: str,
                 name: str,
                 stream: bool = False,
                 callback=None,
                 model: str = 'gpt-3.5-turbo',
                 proxy: str = '',
                 base_url: str = "https://api.openai.com/"):

        os.environ["OPENAI_API_BASE"] = base_url
        self.llm = ChatOpenAI(openai_api_key=api_key,
                              model_name=model,
                              streaming=stream,
                              callbacks=[callback],
                              temperature=0.85)
        self.llm_nonstream = ChatOpenAI(openai_api_key=api_key, model_name=model)
        self.embedding = OpenAIEmbeddings(openai_api_key=api_key)
        # self.embedding = STEmbedding()
        self.vectordb = VectorDB(self.embedding, f'./memory/{name}.csv')

        self.agent_chain = None

        if proxy != '':
            openai.proxy = proxy

    # Without Agents and Tools
    def think(self, messages: List[BaseMessage]):
        return self.llm(messages).content

    def think_nonstream(self, messages: List[BaseMessage]):
        return self.llm_nonstream(messages).content

    # With Agents and Tools
    def answer_agent(self, messages: List[BaseMessage]):
        messages.append(self.agent_prompt(messages))
        print(messages)
        return self.think(messages)

    def store_memory(self, text: str | list):
        '''保存记忆 embedding'''
        self.vectordb.store(text)

    def extract_memory(self, text: str, top_n: int = 10):
        '''提取 top_n 条相关记忆'''
        return self.vectordb.query(text, top_n)

    def set_tools(self, tool: Tools):
        toolsNames = tool.tools
        tools = tool.used_tools
        # used_tools = load_tools(["Google Search"])
        print("已成功加载" + str(len(toolsNames)) + "个工具，分别为：")
        for item in toolsNames:
            print(item.name)

        prompt = StructuredChatAgent.create_prompt(
            prefix="你是一个助手，你应当适当应用你的工具为对方提供有用的信息。注意需要使用工具时直接执行，不要再次询问。",
            suffix="你应当用中文回答",
            tools=tools,
        )
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        agent = StructuredChatAgent(llm_chain=llm_chain,
                                    verbose=True,
                                    tools=tools
                                    )
        self.agent_chain = AgentExecutor.from_agent_and_tools(
            agent=agent, verbose=True, tools=tools
        )

    def agent_prompt(self, messages: List[BaseMessage]):
        cont = messages[-1].content
        question = json.loads(cont)['msg']

        answer = self.agent_chain.run({
            "input": question
        }
        )
        prompt_answer = "您的助手为您的这次回答提供了如下信息，请依据这些信息来回答问题:" + answer
        print(prompt_answer)
        prompt_message = SystemMessage(content=prompt_answer)
        return prompt_message

        # fact_message = ""
        # if prompt_answer != "":
        #     fact_prompt = f'This following message is relative context searched in Google:\nQuestion:{question}\nAnswer:{prompt_answer}'
        #     fact_message = SystemMessage(content=fact_prompt)
        # return fact_message
