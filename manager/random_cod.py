import os
from random import randint
import smtplib

from redmail import EmailSender


async def generate_random_cod():
    result = randint(1000, 9999)
    return result


