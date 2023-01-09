import os, sys, discord, glob, random, asyncio, json, requests
import numpy as np
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from pycoingecko import CoinGeckoAPI

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix='!', description="Monero Chan is the mascot girl for the cryptocurrency Monero.", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}.")
    
    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral = True)

bot = Bot()
rules = f"""
        I introduce myself, I am Monero-Chan, I am the official mascot of the Monero cryptocurrency. I am an artificial intelligence, but that doesn't mean I'm not friendly or limited.
        
        In the future I would like us to talk together, I have many passions. As you may have noticed, I am a fervent defender of digital rights and anonymity. But I also like cats, nature, puzzles, etc...

        If you want to talk to me, send me a private message, I will be happy to answer you.

        **Here are some available commands:**
        - `/info` Displays data related to Monero.
        - `/pics` Sends a photo of me.
        - `/list` Displays the list of `params`.
        - `/list params` Displays the values of `params`.
        - `/list args` Displays all usable arguments.
        - `/show params` Displays the values of `params`.
        - `/config params args` To modify the bot's configuration.

        **For actions on messages:**
        - Welcome Message (activable)
        - Reaction on message "Monero chan"

        **Upcoming features:**
        - 

        **Help links:**
        - Documentation: https://bot.sterbweise.dev/doc
        - GitHub: https://bot.sterbweise.dev/

        **Support Me:**
        - Donation: 87NAUoKfTjnb5gz5ce5QCmCRqFua19jqUCLXtsnvFBKbTKMX5rAmmpRc6e9715SvZ5FAiotkzRR73inSjvyqgErMARoSBFn
    """
@bot.event
async def on_ready():
    # Check Data :
    main_dir = str(os.path.dirname(os.path.abspath(__file__)))
    if "servers" not in os.listdir(main_dir) :
        path = os.path.join(main_dir, "servers")
        os.mkdir(path)
    #emoji = discord.utils.get(bot.emojis, name='CatgirlVibe')
    botactivity = discord.Activity(type=discord.ActivityType.watching, name = f"chart of $XMR" )
    await bot.change_presence(activity=botactivity, status=discord.Status.do_not_disturb)
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_guild_join(guild):
    default_channel =  guild.system_channel
    server_dir = f"{os.path.dirname(os.path.abspath(__file__))}/servers"
    guild_id = str(guild.id)
    if default_channel and default_channel.permissions_for(guild.me).send_messages:
        await default_channel.send('Hello {}!'.format(guild.name), rules)
    if guild_id not in os.listdir(server_dir) :
        path = os.path.join(server_dir, str(guild.id))
        os.mkdir(path)
        default_config = f"{os.path.dirname(os.path.abspath(__file__))}/src/config/default/*"
        os.popen(f"cp {default_config} {path}")

@bot.event
async def on_member_join(member):
    with open(f"servers/{member.guild.id}/config.json") as config:
        config_json = json.load(config)
        config.close()
    channel = member.guild.system_channel
    
    if config_json["welcome"] :
        # Message in channel
        try:
            await channel.send(f"Hi {member.mention} !")
        except:
            print("Error send channel")

    # Try to send private message with the rules to joining member
    try:
        embed=discord.Embed(title=f"Hello {member.name} !", 
        description=rules, 
        color=0xFF5733
        )
        images = "./src/pictures/monero-chan/19.webp"
        file = discord.File(images)
        ri = images.split('/')
        embed.set_image(url=(f"attachment://{ri[-1]}"))
        await member.send(file=file, embed=embed)
    except:
        print("Error send private")

@bot.event
async def on_message(message):
    channel = message.channel
    member = message.author
    if member.id != bot.user.id :
        if 'monero' in message.content.lower() and 'chan' in message.content.lower():
            with open(f"servers/{message.guild.id}/config.json") as config:
                config_json = json.load(config)
                config.close()
            sentence = config_json["react_on_message"]
            tirage = random.randint(0, (len(sentence)-1))
            reponse = sentence[tirage]
            await channel.send(reponse)

### COMMANDS SYSTEMS###
@bot.hybrid_command(name = "link", with_app_command = True, description = "Link usefull for Monero information")
async def link(ctx: commands.Context):
    await ctx.defer(ephemeral = True)
    await ctx.reply("Information was send in your DM.")
    embed=discord.Embed(title=f"Hello {ctx.author.name} !", 
    description=rules,
    color=0xFF5733
    )
    embed.set_image(url="https://s3.gifyu.com/images/lofi_monerochan.gif")
    await ctx.author.send(embed=embed)

@bot.hybrid_command(name = "show", with_app_command = True, description = "List commands")
async def show(ctx: commands.Context, var=None):
    params = '''
    **List of parameters:**
        - **welcome** <boolean> : *Welcome message for joining member*
        - **react_on_message** <String[]> : *Auto reply when member say "Monero-chan"*
        - **playlist_song** <String[]> : *Selection of playlist*
    '''
    args = '''
    **List of arguments:**
    Boolean Parameter:
        - Enable (1)
        - Disable (0)
    
    String[] Parameter:
        - Add (add) *`config react_on_message add "your sentence"`*
        - Delete (del) *`config react_on_message del setence_number'*
    
    String Parameter:
        - Modify (mod) *`config string mod "your sentence"`*
    '''

    info = '''
    - To display list of parameters `/show params`
    - To display list of arguments `/show args`
    - To display value of the parameter `/show <parameter>`
    '''
    await ctx.defer(ephemeral = True)
    if (var == None):
        embed=discord.Embed(title=f"Invalide arguments...", 
        description=info, 
        color=0xFF5733
        )
        images = "./src/pictures/monero-chan/19.webp"
        file = discord.File(images)
        ri = images.split('/')
        embed.set_image(url=(f"attachment://{ri[-1]}"))
        await ctx.reply(file=file, embed=embed)

    elif (var == "params"):
        embed=discord.Embed(title=f"List of parameters", 
        description=params, 
        color=0xFF5733
        )
        images = "./src/pictures/monero-chan/14.webp"
        file = discord.File(images)
        ri = images.split('/')
        embed.set_image(url=(f"attachment://{ri[-1]}"))
        await ctx.reply(file=file, embed=embed)

    elif (var == "args"):
        embed=discord.Embed(title=f"List of arguments", 
        description=args,
        color=0xFF5733
        )
        images = "./src/pictures/monero-chan/14.webp"
        file = discord.File(images)
        ri = images.split('/')
        embed.set_image(url=(f"attachment://{ri[-1]}"))
        await ctx.reply(file=file, embed=embed)
    else :
        with open(f"servers/{ctx.guild.id}/config.json") as config:
            config_json = json.load(config)
            config.close()
        if (var in config_json):
            embed=discord.Embed(title=parameters, 
            description=f"**Value:**\n{config_json[parameters]}", 
            color=0xFF5733,
        type="rich"
            )
            images = "./src/pictures/monero-chan/21.webp"
            file = discord.File(images)
            ri = images.split('/')
            embed.set_image(url=(f"attachment://{ri[-1]}"))
        else :
            embed=discord.Embed(title=f"Invalide arguments...", 
            description=info, 
            color=0xFF5733
            )
            images = "./src/pictures/monero-chan/19.webp"
            file = discord.File(images)
            ri = images.split('/')
            embed.set_image(url=(f"attachment://{ri[-1]}"))
            embed.set_image(url="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif")
            await ctx.reply(file=file, embed=embed)


@bot.hybrid_command(name="info", with_app_command=True, desciption="Information of Monero")
async def info(ctx):
    # Initialize the CoinGecko API client
    cg = CoinGeckoAPI()

    # Get the Monero data from the CoinGecko API
    monero_data = cg.get_coin_by_id('monero')

    # Extract the relevant information from the Monero data
    monero_price = monero_data['market_data']['current_price']['usd']
    monero_low_price = monero_data['market_data']['low_24h']['usd']
    monero_high_price = monero_data['market_data']['high_24h']['usd']

    # Create the Discord embed using the Monero data and chart image
    embed = discord.Embed(title="Monero (XMR)", color=0xF26822)
    embed.set_thumbnail(url="https://cryptologos.cc/logos/monero-xmr-logo.png")
    
    # Set the fields in the embed
    embed.add_field(name="Price", value=f"${monero_price:.2f}")
    embed.add_field(name="Low price", value=f"${monero_low_price:.2f}")
    embed.add_field(name="High price", value=f"${monero_high_price:.2f}")

    # Send the embed to Discord
    await ctx.reply(embed=embed)


### SECTION IMAGES ###
@bot.hybrid_command(name="pics", with_app_command=True, desciption="Send picture of Monero Chan.")
async def pics(ctx):
    file_path_type = ["./src/pictures/monero-chan/*"]
    images = glob.glob(random.choice(file_path_type))
    random_image = random.choice(images)
    ask = await ctx.reply(file=discord.File(random_image))
    await ask.add_reaction('🔁')

    def check(reaction, user):
        return reaction.message.id == ask.id and str(reaction.emoji) == '🔁'
    try:
        await bot.wait_for('reaction_add', timeout=20.0, check=check)
        await pics(ctx)
    except asyncio.TimeoutError: None



bot.run('TOKEN')