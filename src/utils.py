# src.utils

import discord

class Embeds_color:
  Notice=0xff0000
  JobOpening=0x00ff00

def IsDM(ctx):
  if not ctx.message.guild:
    return 1
  return 0