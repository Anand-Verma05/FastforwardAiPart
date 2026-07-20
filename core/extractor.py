#isme i want kya kya hua ha kya krna hai kya decisions hai and kya questiosn hai

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPormptTemplate
from langchain_core.output_parsers import StrOutputParser
from lanchain_core.runnables import RunnablePassthrough, RunnableLambda
import os

