import disnake.ext
from disnake.ext import commands
import requests
from datetime import datetime
from token import discordtoken

# Define o prefixo utilizado nos comandos
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print("Estou pronta!")

# Função para obter dados de uma criptomoeda
async def get_crypto_data(coin):
    api_url = f"https://api.coingecko.com/api/v3/coins/{coin}"
    crypto = requests.get(api_url)
    crypto_data = crypto.json()
    crypto_price = crypto_data["market_data"]["current_price"]["usd"]
    crypto_val = crypto_data["market_data"]["price_change_percentage_24h"]
    crypto_logo = crypto_data["image"]["small"]

    market_feeling = requests.get("https://api.alternative.me/fng/?limit=1")
    feeling_data = market_feeling.json()
    market_feeling = feeling_data["data"][0]["value_classification"]

    return crypto_price, crypto_val, crypto_logo, market_feeling

# Função para traduzir o sentimento do mercado
async def translate_market_sentiment(sentiment):
    if sentiment == "Fear":
        translated_sentiment = "Medo"
    elif sentiment == "Greed":
        translated_sentiment = "Otimista"
    else:
        translated_sentiment = sentiment
    return translated_sentiment


# Comandos [interações]
@bot.slash_command(name="cripto", description="[interações] Exibe informações sobre uma criptomoeda.")
async def cripto(interaction, coin: str):
    crypto_price, crypto_val, crypto_logo, market_feeling = await get_crypto_data(coin)
    translated_sentiment = await translate_market_sentiment(market_feeling)

    embed = disnake.Embed(
        title=coin.capitalize(),
        color=10066431
    )
    embed.add_field(name="Preço: ", value=f"$ {crypto_price:.2f}", inline=True)
    format_crypto_val = "{:.2f}".format(crypto_val)
    embed.add_field(name="Variação % 24h: ", value=f"{format_crypto_val}%", inline=True)
    embed.add_field(name="Sentimento do Mercado: ", value=translated_sentiment, inline=False)

    current_date_and_time = datetime.now()
    custom_format = "%d/%m/%Y - %Hh%M"
    formatted_date_and_time = current_date_and_time.strftime(custom_format)
    embed.set_footer(text="Atualização: " + formatted_date_and_time)
    embed.set_thumbnail(url=crypto_logo)

    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="caiu", description="[interações] Tá caindooooo!")
async def caiu(interaction):
    embed = disnake.Embed(
        title="Tá caindooooo!",
        description="Putz, galera, o valor caiu mais que pamonha quente numa festa junina!\n"
                    "Mas calma lá, o Bitcoin é tipo um gato que sempre cai em pé. 🐱",
        color=16737637
    )
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="subiu", description="[interações] Tá subindoooo!")
async def subiu(interaction):
    embed = disnake.Embed(
        title="Tá subindoooo!",
        description="Olha só o Bitcoin decolando mais alto que foguete em dia de lançamento! 🚀\n"
                    "O Bitcoin é tipo o mestre do retorno triunfal, sempre dando a volta por cima. 👑",
        color=7328346
    )
    await interaction.response.send_message(embed=embed)


# Comandos [curiosidades]
@bot.slash_command(name="sobre", description="[Curiosidades] Oi? Okay, você pode saber um pouco sobre mim.")
async def sobre(interaction):
    embed = disnake.Embed(
        title="Yo! Aqui é a Kula! ❄️",
        description="Fui desenvolvida por um entusiasta de criptomoedas que estava de saco cheio de ficar acessando sites para ver as cotações atuais.\n"
                    "\nMeu criador: https://github.com/akrcarlos\n"
                    "\n||Data provided by CoinGecko and Alternative.me||",

        color=10066431
    )
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="pizza", description="[Curiosidades] Te conto um pouco sobre a história da pizza envolvendo Bitcoin.")
async def pizza(interaction):
    embed = disnake.Embed(
        title="Pizza e Bitcoin",
        description="Em 22 de maio de 2010, rolou o primeiro rolê do Bitcoin: Laszlo Hanyecz comprou duas pizzas por 10.000 Bitcoins! 🍕\n",
        color=16028700
    )
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="bitcoin", description="[Curiosidades] Te conto um pouco sobre o Bitcoin.")
async def bitcoin(interaction):
    embed = disnake.Embed(
        title="Sobre o Bitcoin",
        description="Bitcoin é tipo a estrela das criptos, criada por alguém misterioso chamado Satoshi Nakamoto em 2009. ✨\n"
                    "Funciona meio como um banco virtual, mas sem nenhum banco mandando. É famoso por seus altos e baixos, mas muita gente acredita que é o futuro do dinheiro online.",
        color=16028700
    )
    await interaction.response.send_message(embed=embed)


bot.run(discordtoken)
