import discord
from discord.ext import commands
import utils

# Botのアクセストークン
TOKEN = ''

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='./', intents=intents)

# オンラインか確認するコマンド
@bot.command()
async def active(ctx):
    await ctx.send('Poker Manager is active!')


# pt割り当て一覧を呼び出すコマンド
@bot.command()
async def rate(ctx, player, stack):
    rate = utils.pt_rate(int(player), int(stack))
    for i in range(len(rate)):
        await ctx.send('No.' + str(i+1) + ' +' + str(rate[i]) + 'pt')


# ptを確認するコマンド
@bot.command()
async def pt(ctx, name):
    data = utils.json_load()
    name = utils.key_to_value(data['name'], name)
    if not utils.value_check(data['name'], name):
        await ctx.send(utils.value_to_key(data['name'], name) + ' has ' + str(data['point'][name]) + ' point')
        if (data['medal'][name][0] >= 1 or data['medal'][name][1] >= 1 or data['medal'][name][2] >= 1):
            medals = ''
            for i in range(data['medal'][name][0]):
                medals += ':first_place:'
            for i in range(data['medal'][name][1]):
                medals += ':second_place:'
            for i in range(data['medal'][name][2]):
                medals += ':third_place:'
            await ctx.send('medals: ' + medals)
    else:
        await ctx.send(name + ' is not linked')


# ptのランキングを確認するコマンド
@bot.command()
async def ranking(ctx, num):
    data = utils.json_load()
    ranking = list(sorted(data['point'].items(), key=lambda x:x[1], reverse=True))
    for i in range(min(10, int(num))):
        await ctx.send(utils.value_to_key(data['name'], ranking[i][0]) + ' ' + str(ranking[i][1]) + 'pt')


# バックアップするコマンド
@bot.command()
@commands.has_role("Promoter")
async def backup(ctx):
    data = utils.json_load()
    utils.json_backup(data)
    await ctx.send('Successful!')


# Discordユーザーを紐付けるコマンド
@bot.command()
@commands.has_role("Promoter")
async def link(ctx, name, user):
    data = utils.json_load()
    if utils.key_check(data['name'], user):
        data['name'][user] = name
        await ctx.send(user + ' is linked to ' + name)
    else:
        await ctx.send(user + ' is linked yet')
    if utils.key_check(data['point'], name):
        data['point'][name] = 0
        data['medal'][name] = [0, 0, 0]
    utils.json_write(data)


# 固有名を定義するコマンド
@bot.command()
@commands.has_role("Promoter")
async def define(ctx, name):
    data = utils.json_load()
    if utils.key_check(data['point'], name):
        data['point'][name] = 0
        data['medal'][name] = [0, 0, 0]
        await ctx.send('Successful!')
    else: 
        await ctx.send(name + ' is defined yet')
    utils.json_write(data)


# ptを増減させるコマンド
@bot.command()
@commands.has_role("Promoter")
async def manage(ctx, name, value):
    data = utils.json_load()
    name = utils.key_to_value(data['name'], name)
    if not utils.key_check(data['point'], name):
        point = data['point'][name] + int(value)
        data['point'][name] = point
        await ctx.send('Successful!')
    else:
        await ctx.send(name + ' is not linked')
    utils.json_write(data)


# メダルを増減させるコマンド
@bot.command()
@commands.has_role("Promoter")
async def medal(ctx, name, value1, value2, value3):
    data = utils.json_load()
    name = utils.key_to_value(data['name'], name)
    if not utils.key_check(data['medal'], name):
        gold = data['medal'][name][0] + int(value1)
        silver = data['medal'][name][1] + int(value2)
        bronze = data['medal'][name][2] + int(value3)
        data['medal'][name] = [gold, silver, bronze]
        await ctx.send('Successful!')
    else:
        await ctx.send(name + ' is not linked')
    utils.json_write(data)


# 結果を入力するとptを加算するコマンド
@bot.command()
@commands.has_role("Promoter")
async def result(ctx, player, stack, *names):
    rate = utils.pt_rate(int(player), int(stack))
    if (len(names) >= len(rate) and len(names) >= 3):
        data = utils.json_load()
        for i in range(max(len(rate), 3)):
            name = utils.key_to_value(data['name'], names[i])
            if not utils.key_check(data['point'], name):
                if i < len(rate):
                    point = data['point'][name] + rate[i]
                    data['point'][name] = point
                if i < 3:
                    gold = data['medal'][name][0]
                    silver = data['medal'][name][1]
                    bronze = data['medal'][name][2]
                    if i == 0:
                        gold += 1
                    if i == 1:
                        silver += 1
                    if i == 2:
                        bronze += 1
                    data['medal'][name] = [gold, silver, bronze]
                await ctx.send('Successful!')
            else:
                await ctx.send(name + ' is not linked')
        utils.json_write(data)
    else:
        await ctx.send('Result is not enough')


# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)
