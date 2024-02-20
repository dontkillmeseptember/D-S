import os
import json
import logging
import requests
import random
import datetime
import asyncio
import re
import uvicorn

from fastapi import FastAPI, Request

from threading import Thread

from googletrans import Translator

from dataclasses import dataclass
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, utils, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove, BotCommand
from aiogram.bot.base import Union
from aiogram.utils.exceptions import RetryAfter

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
