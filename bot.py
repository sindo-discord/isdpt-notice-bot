import discord
from discord.ext import commands
import os

from src.utils import *
from src.crawl import *

bot = commands.Bot(command_prefix='!')
bot.remove_command("help")

@bot.event
async def on_ready():
  print("Bot is ready")
  print(f"Bot name : {bot.user.name}")
  print(f"Bot ID : {bot.user.id}")

  Game = discord.Game("게시글 감지")
  await bot.change_presence(status=discord.Status.online, activity=Game)

@bot.command()
async def notice(ctx):
  # 개인 DM은 무시
  if IsDM(ctx):
    return
  
  # 명령 메시지 삭제  
  await ctx.message.channel.purge(limit=1)
        
  # 크롤링 후 Embed로 올릴 채널정보..
  # 만약 공지할 채널이 많다면 DB나 csv에 저장해두고 한번에 읽어야하나
  channel = bot.get_channel(ctx.channel.id)
  
  # 해당 명령을 친 채널 -> 공지사항을 받을 위치
  # 그런데 해당 채널이 이미 클래스 변수에 있다면 무시
  if not channel in isdpt_notice_crawler.channel:
    crawler = isdpt_notice_crawler(bot=bot, channel=channel)
    await crawler.run()
  
# 크롤러 공지사항 알림 중지하기
@bot.command()
async def stop_notice(ctx):
  # 개인 DM은 무시
  if IsDM(ctx):
    return
  
  # 명령 메시지 삭제  
  await ctx.message.channel.purge(limit=1)
  
  channel = bot.get_channel(ctx.channel.id)
  try:
    isdpt_notice_crawler.channel.remove(channel)
  except KeyError:
    pass
  await ctx.send("공지를 받지 않습니다.", delete_after=3)

if __name__ == '__main__':
  try:
    # 로컬에서 테스트할 경우 config 내부에 토큰 저장
    # [주의] .gitignore에 config.py 추가
    import config
    TOKEN = config.TOKEN
  except:
    # 도커로 배포할 경우 환경변수로 토큰을 등록할 것임
    TOKEN = os.getenv("TOKEN")
    
  bot.run(TOKEN)