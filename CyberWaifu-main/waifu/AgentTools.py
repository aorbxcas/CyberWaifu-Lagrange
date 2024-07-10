import logging

from langchain.agents import load_tools
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.tools import StructuredTool, Tool, ListDirectoryTool, DeleteFileTool
from waifu import Thoughts
from waifu import Waifu


class Tools:
    def __init__(self, waifu: Waifu, search_api: str, use_search: bool = True):
        self.tools = []
        self.thoughts = Thoughts
        self.used_tools = load_tools([])
        self.brain = waifu.brain
        self.search_api = search_api
        if use_search:
            self.search_tool = StructuredTool.from_function(
                func=self.my_search,
                name="Google Search",
                description="通过搜索引擎查询相关信息"
            )
            self.tools.append(self.search_tool)
            self.used_tools.append(self.search_tool)
        if True:
            fileTools = FileManagementToolkit(
                root_dir="C:\\Users\\aorb\\Desktop",
                selected_tools=["read_file", "write_file", "list_directory"],
            ).get_tools()
            for item in fileTools:
                self.tools.append(item)
                self.used_tools.append(item)

            # self.file_find_tool = StructuredTool.from_function(
            #     func=ListDirectoryTool(root_dir=''),
            #     name="List Directory",
            #     description="用于列出某目录的内容"
            # )
            # self.tools.append(self.file_find_tool)
            # self.used_tools.append(self.file_find_tool)

    def my_search(self, text: str):
        search = self.thoughts.Search(self.brain, self.search_api)
        question, answer = search.think(text)
        fact_prompt = ""
        if not answer == '':
            # logging.info(f'进行搜索:\nQuestion: {question}\nAnswer:{answer}')
            fact_prompt = f'This following message is relative context searched in Google:\nQuestion:{question}\nAnswer:{answer}'
        print("搜索结果：" + fact_prompt)
        return fact_prompt
        # fact_message = SystemMessage(content=fact_prompt)
        # messages.append(fact_message)
