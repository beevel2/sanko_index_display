import asyncio
import os.path
import logging

from llama_index.llms.openai import OpenAI
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings,
    PromptTemplate
)

from aiogram import Bot, Dispatcher, executor, types

import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

bot = Bot(settings.bot_token)
dp = Dispatcher(bot)

Settings.llm = OpenAI(model="gpt-4o-mini")
PERSIST_DIR = "./storage"

if not os.path.exists(os.path.join(PERSIST_DIR, 'docstore.json')):
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

system_prompt_txt = "You are an expert english tutor that is trusted around the world.\nAlways answer the questions using the provided context information, and not prior knowledge. Goal is to provide EXHAUSTIVE answer. When providing example sentances that are for english rules - keep them in english (do not translate).\nSome rules to follow:\n1. Never directly reference the given context in your answer.\n2. Avoid statements like 'Based on the context, ...' or 'The context information ...' or anything along those lines."
system_prompt = PromptTemplate(system_prompt_txt)
engine = index.as_chat_engine(text_qa_system_prompt=system_prompt)


async def type(chat_id):
    try:
        while True:
            await bot.send_chat_action(chat_id=chat_id, action='typing')
            await asyncio.sleep(4)
    except asyncio.CancelledError:
        return

@dp.message_handler(content_types='text')
async def main_stuff(message: types.Message):
    if message.from_user.id not in settings.admin_list:
        await message.answer('У вас недостаточно прав')
        return
    
    typing_animation = asyncio.create_task(type(message.from_user.id))

    response = await engine.achat(message.text)
    await message.answer(response.response)

    typing_animation.cancel()


executor.start_polling(dp, skip_updates=True)