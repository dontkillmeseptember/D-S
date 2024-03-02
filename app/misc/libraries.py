import os
import json
import logging
import requests
import random
import datetime
import asyncio
import re
import uvicorn

from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.responses import HTMLResponse

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

from fastui import FastUI, AnyComponent, prebuilt_html, components as comps
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, AuthEvent
from fastui.forms import fastui_form

from pydantic import BaseModel, Field, EmailStr, SecretStr

from typing import Annotated, Any, Self
