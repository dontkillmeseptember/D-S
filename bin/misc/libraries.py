import os
import json
import logging

from flask import Flask

from threading import Thread

from dataclasses import dataclass
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, utils, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove, BotCommand