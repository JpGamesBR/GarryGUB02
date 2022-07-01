from datetime import datetime,timedelta
import json
import discord
from discord.ext import commands
from general import general as g
from random import randint
import sqlite3 as sql
import asyncio
import os
from discord.ext.commands import cooldown, BucketType,CommandOnCooldown

#carregar configuração
config = g.jloadn('https://raw.githubusercontent.com/JpGamesBR/database/main/config-bot.json')
prefix = config['prefix']
owner_id = int(config['own1'])
owner_id2 = int(config['own2'])
ver = config['version']

#admins
adm = [owner_id,owner_id2]

#cores
cor = {
    'Gold':0xDAA520,
    'LighBlue':0xB0C4DE,
    'LimeGreen':0x00ff00
}

#corrigir token
token = os.environ['TOKEN']
tk = ''
for i in token:
    tk = f'{i}{tk}'
token = tk

#Setar funções
def embs(ctx,emb):
    emb.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)

def StrToList(string):
    listRes= list(string.split(" "))
    return listRes

#====(### Bot ###)====#
client = commands.Bot(command_prefix=prefix,help_command=None,case_insensitive=True)

#====(### Eventos ###)====#
async def status():
    while True:
        await asyncio.sleep(10)
        await asyncio.sleep(10)

@client.event
async def on_ready():
    global db,cur
    db = sql.connect('GGUB.db')
    cur = db.cursor()
    g.table(cur,'profile','id INTEGER,sobremim TEXT,link TEXT,image TEXT, date TEXT,age INTEGER')
    g.table(cur,'economy','id INTEGER,money_bank INTEGER,money_wallet INTEGER,luck INTEGER,cargo TEXT')
    db.commit()
    print(
        f"""
        I'm on! {ver}
        """
    )
    client.loop.create_task(status())

def is_registered(author,table,get):
    var = g.get(cur,table,get,author.id)
    if not var == None:
        return var
    else: # for profile is: id,sobremim,link,image,date
        if table[0].lower() == 'p':
            g.insert(cur,table,('id, sobremim,link,image,date,age',f'{author.id},"Hello! im new in this bot!","https://discord.com","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVDZqAeZfhfMxtDYqWX1y2mCIQZqSoY1NZ2Q&usqp=CAU","00/00/0000",0'))
            db.commit()
        elif table[0].lower() == 'e':
            cargo = 'user'
            g.insert(cur,table,('id, money_bank, money_wallet,luck,cargo',f'{author.id},0,0,1,"{cargo}"'))
            db.commit()
        return is_registered(author,table,get)

#====(### Comandos ###)====#
    #====(### Economy ###)====#

@client.command()
async def shop(ctx,item:str=None):
    shopl = g.jloadn('https://raw.githubusercontent.com/JpGamesBR/database/main/shopping.json')
    wtypes = ['wallet','carteira','wa','w',1]
    btypes = ['bank','banco','ba','b',2]
    if item in wtypes:
        item = 'wallet'
    elif item in btypes:
        item = 'bank'
    if item != None:
        total = ''
        emotes = []
        for i in shopl['SHOP']:
            prize = i['p']
            name = i['n']
            reaction = i['e']
            emotes.append(reaction)
            total = f'{total}\nItem: {name} Prize: {prize} React: {reaction}'
        emb = discord.Embed(
            title=f'Shop',
            description=f'Items for you:```\n{total}```',
            colour = cor['LimeGreen']
        )
        emb.set_thumbnail(url=ctx.author.avatar_url)
        embs(ctx,emb)
        emb_msg = await ctx.reply(embed=emb)
        for i in emotes:
            await emb_msg.add_reaction(i)
        while True:
            try:
                reaction,user = await client.wait_for("reaction_add",check=lambda reaction,user:user == ctx.author and reaction.emoji in emotes,timeout=60.0)
            except asyncio.TimeoutError:
                return print('test')
            else:
                if reaction.emoji == '🍀':
                    old_m = is_registered(ctx.author,'economy',f'money_{item}')[0]
                    luck = is_registered(ctx.author,'economy',f'luck')[0]
                    if old_m >= 10000:
                        g.update(cur,'economy',('luck',luck+1),('id',ctx.author.id))
                        g.update(cur,'economy',(f'money_{item}',old_m-10000),('id',ctx.author.id))
                        db.commit()
                        await ctx.send(f'<@{ctx.author.id}>, buy +1 of luck per 10000')
                    else:
                        await ctx.send(f'<@{ctx.author.id}>, need 10000 coins!')
                if reaction.emoji == '🕶':
                    old_m = is_registered(ctx.author,'economy',f'money_{item}')[0]
                    luck = is_registered(ctx.author,'economy',f'luck')[0]
                    cargos:list = is_registered(ctx.author,'economy','cargo')[0]
                    cargos:list = StrToList(cargos)
                    if old_m >=12500:
                        if not 'Beta1T' in cargos:
                            cargos.insert(0,'Beta1T')
                            g.update(cur,'economy',(f'money_{item}',old_m-12500),('id',ctx.author.id))
                            cargos = ' '.join(map(str,cargos))
                            g.update(cur,'economy',('luck',luck+5),('id',ctx.author.id))
                            g.update(cur,'economy',(f'cargo',f'"{cargos}"'),('id',ctx.author.id))
                            db.commit()
                            await ctx.send(f'<@{ctx.author.id}>, Buy Beta! +5 luck!')
                        else:
                            await ctx.reply(f'<@{ctx.author.id}>, you already have this!')
                if reaction.emoji == '🚗':
                    old_m = is_registered(ctx.author,'economy',f'money_{item}')[0]
                    cargos: list = is_registered(ctx.author,'economy','cargo')[0]
                    cargos: list = StrToList(cargos)
                    if old_m >= 1000:
                        print(cargos)
                        if not 'CarExtensionPack' in cargos:
                            cargos.insert(0,'CarExtensionPack')
                            g.update(cur,'economy',(f'money_{item}',old_m-1000),('id',ctx.author.id))
                            cargos = ' '.join(map(str,cargos))
                            print(cargos)
                            g.update(cur,'economy',(f'cargo',f'"{cargos}"'),('id',ctx.author.id))
                            db.commit()
                            await ctx.send(f'<@{ctx.author.id}>, buy pack extensions!')
                        else:
                            await ctx.send(f'<@{ctx.author.id}>, you already have this!')
                    else:
                        await ctx.send(f'<@{ctx.author.id}>, need 1000 coins!')
    else:
        await ctx.reply('Please item! (wallet/bank)')
@client.command()
async def get_money(ctx,oper,quantity:int):
    if ctx.author.id in adm:
        old_m = is_registered(ctx.author,'economy','money_bank')[0]
        if oper == '+': # add
            quantity = old_m + quantity
        elif oper == '=':
            quantity = quantity
        g.update(cur,'economy',('money_bank',quantity),('id',ctx.author.id))
        db.commit()

@client.command(aliases=['trabalhar'])
@cooldown(1,43200,BucketType.user)
async def work(ctx):
    luck = is_registered(ctx.author,'economy','luck')[0]
    old_w = is_registered(ctx.author,'economy','money_wallet')[0]
    works = ['Programmer','Attorney','Journalist','Baker','self-employed','Pilot','Cabby','Teacher','Mason','Chef']
    works = works[randint(0,len(works)-1)]
    money = randint(250,3750)
    if luck == 1:
        luck = 2
    money = money * round(luck//2)
    emb = discord.Embed(
        title=f'{ctx.author.name} you worked as: {works}',
        description = f'You worked as: {works}\nAnd get {money} of money\nNow you have: {old_w+money}',
        colour = cor['LimeGreen']
    )
    emb.set_thumbnail(url=ctx.author.avatar_url)
    embs(ctx,emb)
    g.update(cur,'economy',('money_wallet',old_w+money),('id',ctx.author.id))
    db.commit()
    await ctx.reply(embed=emb)

@work.error
async def work_error(ctx,error):
    if isinstance(error,CommandOnCooldown):
        time = str(timedelta(seconds=int(error.retry_after)))
        await ctx.reply(f'This command is now in cooldown!\nTry again n: {time} hours')

@client.command(aliases=['diario','reward','claim'])
@cooldown(1,43200,BucketType.user)
async def daily(ctx):
    var = randint(10,350)
    luck = is_registered(ctx.author,'economy','luck')[0]
    if luck == 1:
        luck = 2
    var = round(var * (luck//2))
    old_w = is_registered(ctx.author,'economy','money_wallet')[0 ]
    emb = discord.Embed(
        title = f'{ctx.author.name} your daily is now!',
        description = f'{ctx.author.name} has claimed: {var}\nfrom ``{old_w}`` of wallet you got money!\nTotal money: {old_w+var}',
        colour = cor['LimeGreen']
    )
    g.update(cur,'economy',('money_wallet',var+old_w),('id',ctx.author.id))
    db.commit()
    emb.set_thumbnail(url=ctx.author.avatar_url)
    embs(ctx,emb)
    await ctx.reply(embed=emb)

@daily.error
async def daily_error(ctx,error):
    if isinstance(error,CommandOnCooldown):
        time = str(timedelta(seconds=int(error.retry_after))) #error.retry_after:.2f
        await ctx.reply(f'this command is now in cooldown!\nTry again in: {time} hours')

@client.command()
async def clear_me(ctx, table):
    print(ctx.author.id)
    print(owner_id)
    if not ctx.author.id in adm:
        await ctx.reply('Only owner can use this')
        return
    else:
        g.delete(cur,table,('id',ctx.author.id))
        db.commit()
        await ctx.reply('All of these table has been deleted!')

@client.command(aliases=['sacar','with'])
async def withdraw(ctx,quantity:int):
    old_w = is_registered(ctx.author,'economy','money_wallet')[0]
    old_b = is_registered(ctx.author,'economy','money_bank')[0]
    if quantity > old_b:
        await ctx.reply('The quantiy is more of your have!')
        return
    elif quantity < 0:
        await ctx.reply('Negative numbers not is allowed!')
        return
    old_b -= quantity
    old_w += quantity
    g.update(cur,'economy',('money_wallet',old_w),('id',ctx.author.id))
    g.update(cur,'economy',('money_bank',old_b),('id',ctx.author.id))
    db.commit()
    await ctx.reply(f'You got in the wallet: {quantity}\nNow in the wallet you have: {old_w}\nIn the bank you have: {old_b}')

@client.command(aliases=['balance'])
async def bal(ctx,member:discord.Member=None):
    luck = is_registered(ctx.author,'economy','luck')[0]
    if member == None:
        member = ctx.author
    old_w = is_registered(member,'economy','money_wallet')[0]
    old_b = is_registered(member,'economy','money_bank')[0]
    cargos = is_registered(member,'economy','cargo')[0]
    cargos = StrToList(cargos)
    carg = ''
    for i in cargos:
        if i == 'CarExt0F':
            i = 'None'
        elif i == 'Beta0F':
            i = 'None'
        carg = f'{i}, {carg}'
    emb = discord.Embed(
        title = f'{ctx.author.name} Balance of: {member.name}',
        description = f'```lua\nBank: {old_b}\nWallet: {old_w}\nLuck: {luck}\nPositions: {carg}```',
        colour = cor['LimeGreen']
    )
    emb.set_thumbnail(url=member.avatar_url)
    embs(ctx,emb)
    await ctx.reply(embed=emb)

@client.command(aliases=['dep','depositar','bank','banco'])
async def deposit(ctx,quantity:int):
    old_w = is_registered(ctx.author,'economy','money_wallet')[0]
    old_b = is_registered(ctx.author,'economy','money_bank')[0]
    if quantity > old_w:
        await ctx.reply('The quantiy is more of your have!')
        return
    elif quantity < 0:
        await ctx.reply('Negative numbers not is allowed!')
        return
    old_b += quantity
    old_w -= quantity
    g.update(cur,'economy',('money_wallet',old_w),('id',ctx.author.id))
    g.update(cur,'economy',('money_bank',old_b),('id',ctx.author.id))
    db.commit()
    await ctx.reply(f'You deposited in the bank: {quantity}\nNow in the wallet you have: {old_w}\nIn the bank you have: {old_b}')

    #====(### Misc ###)====#
@client.command(aliases=['latencia','pong','latency'])
async def ping(ctx): # Ping
    emb = discord.Embed(
        title = '🏓Ping🏓',
        description = f'**The ping is: {round(client.latency*1000)}ms**',
        color = cor['Gold']
    )
    embs(ctx,emb)
    await ctx.reply(embed=emb)
    
@client.command(aliases=['falar','speak'])
async def say(ctx,*,text): # say
    await ctx.send(text) 

@client.command(aliases=['perfil','pro','user'])
async def profile(ctx,member:discord.Member=None): # Profile
    if member == None:
        member = ctx.author
    inf1 = is_registered(member,'profile','sobremim')[0] # get about-me
    inf2 = is_registered(member,'profile','link')[0] # get the optional link
    inf3 = is_registered(member,'profile','image')[0] # get the optional image
    inf4 = is_registered(member, 'profile','date')[0] # get the optional born date
    inf5: int = is_registered(member,'profile', 'age')[0] # get the optional age
    inf_b = is_registered(member,'economy','money_bank')[0] #get the money in the bank
    inf_w = is_registered(member,'economy', 'money_wallet')[0] # get the money in the wallet
    inf_l = is_registered(member,'economy','luck')[0] # get the luck
    
    emb = discord.Embed(
        title = f'profile of: {member.name}',
        colour = cor['LighBlue']
    )
    emb.set_thumbnail(url=member.avatar_url) # Set avatar image
    emb.set_image(url=inf3)
    emb.add_field(name=f'**About-me:**',value=f'{inf1}',inline=False) # set about-me
    emb.add_field(name=f'**User Link:**',value=f'Link: {inf2}',inline=False) # set the link
    emb.add_field(name= f'**Born in/Age:**',value=f'```lua\nBorn in: {inf4}\nAge: {inf5}```',inline=False) # set the born date
    emb.add_field(name=f'**Balance:**',value=f'```lua\nWallet Money: {inf_b}\nBank Money: {inf_w}\nLuck: {inf_l}```') # Set all the balance status

    await ctx.reply(content=f'<@{ctx.author.id}>',embed=emb)

@client.command(aliases=['about-me','sobremim','sobre'])
async def about(ctx,*,text): # about-me / sobremim
    about_old = is_registered(ctx.author,'profile','sobremim')[0] # get old about_me
    about_new = text # new about_me
    g.update(cur,'profile',('sobremim',f'"{about_new}"'),('id',ctx.author.id))
    db.commit()
    await ctx.reply(f'your about-me has been defined from: ``{about_old}`` to: ``{about_new}``')

@client.command(aliases=['myimg','myimage','img','set-image'])
async def imagem(ctx,*,text): # image
    image_new = text # new about_me
    g.update(cur,'profile',('image',f'"{image_new}"'),('id',ctx.author.id))
    db.commit()
    await ctx.reply(f'your image has been defined to: {image_new}')

@client.command(aliases=['date','myborn','mydate','borning','born'])
async def nasc(ctx,day:int,month: int,year: int): # age / nascimento
    year_act = int(datetime.now().year)
    age = year_act - year
    g.update(cur,'profile',('date',f'"{day}/{month}/{year}"'),('id',ctx.author.id))
    g.update(cur,'profile',('age',f'{age}'),('id',ctx.author.id))
    db.commit()
    await ctx.reply(f'your born date has been defined to: ``{day}/{month}/{year}``\nand your age has been defined to: ``{age}``')

@client.command(aliases=['mylink','link','myurl'])
async def url(ctx,url): # url
    url_old = is_registered(ctx.author,'profile','link')[0] # get old link
    url_new = url
    g.update(cur, 'profile',('link',f'"{url_new}"'),('id',ctx.author.id))
    db.commit()
    await ctx.reply(f'your link has been defined from: ``{url_old}`` to: ``{url_new}``')

@client.command(aliases=['calculator','calcular','calculadora','math'])
async def calc(ctx,num1:int,sig,num2:int): # calcular
    if sig == '+':
        res = num1 + num2
    elif sig == '-':
        res = num1 - num2
    elif sig == '*':
        res = num1 * num2
    elif sig == '/':
        res = num1 / num2
    elif sig == '//':
        res = num1 // num2
    elif sig == '**':
        res = num1 ** num2
    else:
        await ctx.reply('Incorrect use of this!')
        return
    await ctx.reply(f'{num1}{sig}{num2}\nThe result of the calc is:{res}')

@client.command(aliases=['foto','icon'])
async def avatar(ctx,member: discord.Member=None): # avatar
    if member == None:
        member = ctx.author
    emb = discord.Embed(
        title = f'{ctx.author.name} Avatar of: {member.name}!',
        url = member.avatar_url,
        colour = cor['Gold']

    )
    emb.set_image(url=member.avatar_url)
    embs(ctx,emb)
    await ctx.reply(embed=emb)

    #====(### Funny ###)====#
@client.command(aliases=['car'])
async def carro(ctx):
    cargos:list = is_registered(ctx.author,'economy','cargo')[0]
    gifs = ['https://c.tenor.com/Sf2-dHHOJDYAAAAd/car.gif','https://c.tenor.com/MOt9dY8XGc0AAAAd/nissan-car.gif','https://c.tenor.com/kOj7COh2MnEAAAAC/dodge-challenger.gif'] # Normal gifs 3/3
    cargos = StrToList(cargos)
    stat = ''
    if 'CarExt1' in cargos:
        gifs.append('https://www.icegif.com/wp-content/uploads/car-icegif-4.gif')
        gifs.append('https://c.tenor.com/NBHP0sc4CaUAAAAC/drift-cars.gif')
        gifs.append('https://i.gifer.com/7Uv0.gif') #with ext gifs 6/6
        stat = '👑'
    gifs = gifs[randint(0,len(gifs)-1)]
    emb = discord.Embed(
        title = f'{ctx.author.name} has racing with your car!{stat}',
        colour = cor['Gold']
    )
    emb.set_image(url=gifs)
    embs(ctx,emb)
    await ctx.reply(embed=emb)

@client.command(aliases=['mm'])
async def meme(ctx):
    mm = g.jloadn('https://raw.githubusercontent.com/JpGamesBR/database/main/memes-pt-br.json')
    mm = mm[randint(0,len(mm)-1)]
    emb = discord.Embed(
        title=f'{ctx.author.name} Memes for you!',
        colour = cor['Gold']
    )
    emb.set_image(url=mm)
    embs(ctx,emb)
    await ctx.reply(embed=emb)

@client.command(aliases=['slap','tapa'])
async def _slap(ctx,member:discord.Member=None): # tapa
    gifs = ['https://media4.giphy.com/media/hVg8ceHRDw0uVHcSb3/200.gif','https://c.tenor.com/SmVEuFYER5UAAAAC/tapa-anime-tapas.gif','https://www.intoxianime.com/wp-content/uploads/2017/04/tumblr_ooub8fIHkT1qz64n4o2_400.gif']
    gifs = gifs[randint(0,len(gifs)-1)]
    if member == None:
        await ctx.reply('User not mentioned!')
        return
    emb = discord.Embed(
        title = f'{ctx.author.name} give a sleep in {member.name}',
        colour = cor['Gold']
    )
    emb.set_image(url=gifs)
    embs(ctx,emb)
    await ctx.reply(embed=emb)

@client.command(aliases=['punch','soco','socar'])
async def _soco(ctx,member:discord.Member=None): # soco
    gifs = ['https://c.tenor.com/9ZuBn8MALR4AAAAC/itadori-soco.gif','https://i0.wp.com/media.giphy.com/media/arbHBoiUWUgmc/giphy.gif','https://pa1.narvii.com/6457/fba783d9bd0ad25e4e6c505b08b9ce48d6c8d1bb_hq.gif']
    gifs = gifs[randint(0,len(gifs)-1)]
    if member == None:
        await ctx.reply('user not mentioned!')
        return
    emb = discord.Embed(
        title = f'{ctx.author.name} give a punch in the face of {member.name}',
        colour = cor['Gold']
    )
    emb.set_image(url=gifs)
    embs(ctx,emb)
    await ctx.reply(embed=emb)

#Rodar
client.run(token)
