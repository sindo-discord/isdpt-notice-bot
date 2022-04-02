import requests
from bs4 import BeautifulSoup
import asyncio
import discord
from .utils import Embeds_color

class isdpt_notice_crawler:
  # 클래스 변수
  channel = set()
  crawl_time = 60*60*3 # 3시간
  domain = "http://home.sejong.ac.kr/bbs/"
  
  def __init__(self, bot, channel):
    self.channel = channel
    self.bot = bot
    # 공지를 뿌릴 클래스 변수에 채널 추가..
    isdpt_notice_crawler.channel.add(channel)
  
  # 밀린 공지를 확인하는 함수
  async def check_notice(self, latest_message):
    # 마지막 공지가 없었다면 아무것도 하지 않음
    if len(latest_message) == 0:
      self.latest_post_title = ""
      return
    
    # 우선 마지막 올린 메시지의 번호를 가져온다.. ( embed에 넣어야 해서..)
    Index = int(latest_message[0].embeds[0].fields[0].value)
    
    # 이제 밀린 공지를 출력해야 한다..
    # 채팅에 남은 마지막 공지를 가져와서 이전글이 있는지 확인한다..
    req = requests.get(latest_message[0].embeds[0].url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find('table', {'class': 'text-list-board'})
    trs = tables.find_all('tr')
    tds = trs[0].find_all('td')
    
    prev_content = tds[0]
    
    # 가장 최근에 올린 공지사항 이름을 저장
    self.latest_post_title = prev_content.text.strip()
    prev_title = prev_content.text.strip()
    prev_a = prev_content.find('a')
    
    # prev_a가 있다면 이전(최신)글 링크가 있다는 것
    while prev_a:
      
      prev_url = prev_a["href"]
      prev_url = prev_url.replace('¤', "&curren")
      
      req = requests.get(isdpt_notice_crawler.domain + prev_url)
      html = req.text
      soup = BeautifulSoup(html, 'html.parser')
      
      # 현재 글 정보
      tables = soup.find('table', {'class': 'text-view-board'})
      trs = tables.find_all('tr')
      tds = trs[1].find_all('td')
      
      # 임베드 생성해서 채널에 전송
      Title = prev_title
      Url = prev_url
      Color = Embeds_color.Notice
      Author = tds[0].text.strip()
      Index += 1
      Date = tds[1].text.strip()
      embed = self.SetNoticeEmbed(Title=Title, Url=Url, Color=Color, Author=Author, Index=Index, Date=Date)
      await self.channel.send("새 공지사항이 올라왔습니다.", embed=embed)
      
      # 가장 최근에 올린 공지사항 이름을 저장
      self.latest_post_title = Title
      
      # 이전(최신) 글 불러오기
      tables = soup.find('table', {'class': 'text-list-board'})
      trs = tables.find_all('tr')
      tds = trs[0].find_all('td')
      
      prev_content = tds[0]
      
      prev_title = prev_content.text.strip()
      prev_a = prev_content.find('a')

  async def run(self):
    while True: 
      # 클랙스에 등록된 모든 채널에 새 공지사항을 뿌린다..
      for channel_iter in isdpt_notice_crawler.channel:
        print(f"send notice to [{channel_iter}]")
        embed = self.crawl()
        
        # 크롤링한 데이터와 봇이 가장 최근에 전송한 공지사항의 제목이 다르면 
        # 공지사항이 올라왔다고 가정하고 임베드 전송
        print(embed.title)
        print(self.latest_post_title)
        if embed.title != self.latest_post_title:
          await channel_iter.send("새 공지사항이 올라왔습니다.", embed=embed)
          self.latest_post_title = embed.title
        else:
          print("가장 최신글을 가져왔습니다")
        # await i.send(f"<t:{int(datetime.datetime.now().timestamp())}:D>")
        
      await asyncio.sleep(isdpt_notice_crawler.crawl_time)
  
  def SetNoticeEmbed(self, Title, Url, Color, Author, Index, Date):
    embed=discord.Embed(title=Title, url=isdpt_notice_crawler.domain + Url, color=Color)
    embed.set_author(name=Author)
    embed.set_thumbnail(url="https://i.ibb.co/DtCXwHw/1.jpg")
    embed.add_field(name="번호", value=Index, inline=True)
    embed.add_field(name="작성일", value=Date, inline=True)
    return embed
  
  def crawl(self):
    data = {
      "currentPage": 1,
      "wslID": "isdpt",
      "bbsid": 571,
      "searchField": "",
      "searchValue": ""
    }

    req = requests.post('http://home.sejong.ac.kr/bbs/bbslist.do', data=data)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find('table', {'class': 'text-board'})
    trs = tables.find_all('tr')
    tds = trs[1].find_all('td')
    
    Index = tds[0].text.strip()
    Title = tds[1].text.strip()
    
    # 공교롭게도 href의 `...&currentPage=...` 에서 &curren 이 entity code라서
    # beutifulesoup을 쓰면 `...¤tPage=...`` 가된다.
    # https://entitycode.com/#currency-content
    #
    # 일단은 강제로 replace 해줌
    Url = tds[1].find('a')["href"]
    Url = Url.replace('¤', "&curren")
    
    Author = tds[2].text.strip()
    Date = tds[3].text.strip()
  
    # 디스코드 embed 생성 후 반환
    return self.SetNoticeEmbed(Title=Title, Url=Url, Color=Embeds_color.Notice, Author=Author, Index=Index, Date=Date)