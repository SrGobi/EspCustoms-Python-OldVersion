import asyncio, discord, fortnitepy, functools, time, datetime, json, logging, traceback
import sys, os, requests
from discord.ext import commands, tasks
from functools import partial
from PIL import Image
from io import BytesIO
from colorama import init
init(autoreset=True)
from colorama import Fore, Back, Style

from fortnitepy.ext import commands as fortnite_commands
from discord.ext import commands as discord_commands

color_main = discord.Color(0xF5F5F5)
color_done = discord.Color(0x00FFFF)
color_warn = discord.Color(0xFFFF00)
color_errr = discord.Color(0xFF0000)

loop = asyncio.get_event_loop()

filename = 'device_auths.json'

#Functions
def es_numero(str_num: str, convertir: bool):
    try:
        num = float(str_num)
        if convertir:
            return True, num
        return True
    except:
        return False

def getTiempesito() -> str:
    tiempesito = datetime.datetime.now().strftime('%H:%M:%S')
    return tiempesito

def pAdvertencia(msg: str) -> None:
    print(Fore.BLACK + Back.YELLOW + f"[{getTiempesito()}] [WARNING] " + msg + Style.RESET_ALL)

def pError(msg: str) -> None:
    print(Fore.BLACK + Back.RED + f"[{getTiempesito()}] [ERROR] " + msg + Style.RESET_ALL)

try:
    requests.get("http://216.58.192.142")
except Exception as e:
    pError(f"No tienes acceso a internet ({e})")
    exit()

#Settings
def cargarAjustes():
    try:
        with open("ajustes.json", encoding="utf-8") as f:
            print("Cargando 'ajustes.json'...")
            time.sleep(1)
            global config
            config = json.load(f)
            print("¡Configuración cargada correctamente!")
    except Exception as e:
        print(f"Hubo un problema al cargar 'ajustes.json' ({e})")
        exit()

cargarAjustes()

#Platform types
if config['plataforma'].lower() in ["win", "windows"]:
    plataforma = fortnitepy.Platform.WINDOWS
elif config['plataforma'].lower() in ["mac", "macintosh"]:
    plataforma = fortnitepy.Platform.MAC
elif config['plataforma'].lower() in ["psn", "playstation"]:
    plataforma = fortnitepy.Platform.PLAYSTATION
elif config['plataforma'].lower() in ["xb", "xbox"]:
    plataforma = fortnitepy.Platform.XBOX
elif config['plataforma'].lower() in ["ns", "switch"]:
    plataforma = fortnitepy.Platform.SWITCH
elif config['plataforma'].lower() == "ios":
    plataforma = fortnitepy.Platform.IOS
elif config['plataforma'].lower() in ["and", "android"]:
    plataforma = fortnitepy.Platform.ANDROID
else:
    plataforma = fortnitepy.Platform.SWITCH
    pAdvertencia("{config['plataforma']} no es una plataforma válida")
    pAdvertencia("Se ha puesto la plataforma en SWITCH")

#Authentication
def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}


def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)

discord_bot_token = config["token"]
device_auth_details = get_device_auth_details().get(config["email"], {})
fortnite_bot = fortnite_commands.Bot(
    command_prefix=config["prefijo"],
    loop=loop,
    description=config["description"],
    auth=fortnitepy.AdvancedAuth(
        email=config["email"],
        password=config["password"],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    ),
    status=config["estado"],
    platform=plataforma,
    avatar=fortnitepy.Avatar(asset=config["kairos_avatar_id"], background_colors=config["kairos_avatar_fondo"])
)

discord_bot = discord_commands.Bot(
    loop=loop,
    command_prefix=config["prefijo"],
    description=config["description"],
    case_insensitive=True
)

#Reading event device_auths.json
@fortnite_bot.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)


@fortnite_bot.event
async def event_before_close():
    await discord_bot.close()

#Bot Fortnite Main Event
@fortnite_bot.event
async def event_ready():
    print('Fortnite bot ready by ESP CUSTOMS')
    member = fortnite_bot.party.me
    await member.edit_and_keep(
        functools.partial(fortnitepy.ClientPartyMember.set_outfit, asset=config["skin_id"]),
        functools.partial(fortnitepy.ClientPartyMember.set_backpack, asset=config["mochila_id"]),
        functools.partial(fortnitepy.ClientPartyMember.set_banner, icon=config["escudo"], color=config["escudo_color"], season_level=config["nivel_pase"])
    )
    await discord_bot.start(discord_bot_token)

#Bot Discord Main Event
@discord_bot.event
async def on_ready():
    await discord_bot.change_presence(activity=discord.Streaming(name="New Version Bot", url="https://www.twitch.tv/srgobiy"))
    print('ESP CUSTOMS DISCORD')

#COGS
@discord_bot.command()
@commands.has_permissions(administrator = True)
async def loadcog(ctx, cog):
    discord_bot.load_extension(f"cogs.{cog}")
@discord_bot.command()
@commands.has_permissions(administrator = True)
async def unloadcog(ctx, cog):
    discord_bot.unload_extension(f"cogs.{cog}")

################################################

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        discord_bot.load_extension(f"cogs.{filename[:-3]}")

#CONSOLE MESSAGES
@discord_bot.event
async def on_message(message):
    if message.author.bot:
        return
    print('Mensaje de Discord recibido de {0.author.display_name} | Content: "{0.content}"'.format(message))
    await discord_bot.process_commands(message)

@fortnite_bot.event
async def event_message(message):
    print('Recibí un mensaje de Fortnite de {0.author.display_name} | Content: "{0.content}"'.format(message))

#BY JOINING THE FORTNITE BOT
@fortnite_bot.event
async def event_party_member_join(member):
    await fortnite_bot.party.send(config["msg_unirse"])
    if fortnite_bot.user.display_name != member.display_name:
        print(f"[{getTiempesito()}] {member.display_name} has joined the room.")
    # TODO: emojis
    if config["emote"]:
        time.sleep(1)
        await fortnite_bot.party.me.set_emote(asset=config["emote_id"], run_for=config["emote_duración"])

#ACCEPT FRIENDS
@fortnite_bot.event
async def event_friend_request(request):
    if config['aceptaramigos']:
        await request.accept()
        print(Fore.BLUE + f"[{getTiempesito()}] La solicitud de amistad de {request.display_name}")
    else:
        if request.display_name in config["admins"]:
            await request.accept()
            print(Fore.BLUE + f"[{getTiempesito()}] La solicitud de amistad de {request.display_name}")  
        else:
            print(Fore.BLACK + Back.YELLOW + f"[{getTiempesito()}] La solicitud de amistad de {request.display_name} (Motivo: aceptaramigos esta desactivado y no es admin)")

#JOIN INVITATIONS
@fortnite_bot.event
async def event_party_invite(invite):
    if config['unirseinvitaciones']:
        try:
            await invite.accept()
            print(Fore.BLUE + f'[{getTiempesito()}] Se ha aceptado una invitación a la sala {invite.sender.display_name}')
        except Exception as e:
            print(f"Hubo un problema al unirse ({e})")
            pass
    else:
        if invite.sender.display_name in config["admins"]:
            await invite.accept()
            print(Fore.BLUE + f'[{getTiempesito()}] Se ha aceptado una invitación a la sala {invite.sender.display_name}')
        else:
            print(Fore.BLACK + Back.YELLOW + f'[{getTiempesito()}] Se rechazó una invitación a una sala {invite.sender.display_name} (Motivo: unirseinvitaciones está deshabilitado y no es administrador.)')
            await invite.sender.send(f"Este bot no puede aceptar su invitación de salida en este momento porque no es un administrador.")
            await invite.sender.send(f"Si conoces a la persona que controla este bot, puedes pedirle que active la capacidad de aceptar invitaciones o hacerte administrador.")

"""
@discord_bot.command()
@commands.has_permissions(manage_messages = True)
async def on_member_join(ctx, *, member, user: discord.Member = None):
    if user == None:
        user = ctx.author
    on_member_join = Image.open("imagenes/ESP.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((150,150))

    on_member_join.paste(pfp, (205,61))

    on_member_join.save("imagenes/profile.png")

    idchannel = input("The channel is: @")

    await ctx.discord_bot.get_channel(idchannel).send(file = discord.File("imagenes/profile.png") + f" has joined")
"""
#Verification command to link Fortnite account with Discord
@discord_bot.command()
@commands.has_permissions(manage_messages = True)
async def verification(ctx, member: discord.Member = None):
    author = ctx.author
    embed=discord.Embed(title="Epic Account Registration", description="Follow the prompts to verify:", color=color_main)
    embed.add_field(name="Step 1", value="Tienes que poner lo que especifica el autor, al contratar el bot", inline=False)
    embed.add_field(name="Step 2", value="Tienes que poner lo que especifica el autor, al contratar el bot", inline=False)
    embed.add_field(name="Step 3", value="Tienes que poner lo que especifica el autor, al contratar el bot", inline=True)
    embed.add_field(name="Step 3", value="Tienes que poner lo que especifica el autor, al contratar el bot", inline=True)
    embed.set_footer(text=f"Host: {author} | Made by BLD SRGOBI#5100")
    x = await ctx.send(embed=embed)

    embed_1=discord.Embed(title="ESP Verification", description="Follow the prompts to verify:", color=color_main)
    embed_1.add_field(name="Step 1", value="1 | Add to bot ``ESP CUSTOMS``", inline=False)
    embed_1.add_field(name="Step 2", value="2 | Whisper your Discord id: ``360881334647914506``", inline=False)
    embed_1.add_field(name="Step 3", value="3 | Reactions to the message you received by MD", inline=True)
    embed_1.add_field(name="Step 3", value="4 | Once you have reacted to the DM, you are ready to play!", inline=True)
    embed_1.set_footer(text=f"Host: {author} | Made by BLD SRGOBI#5100")
    await x.add_reaction("✋")
    reaction, user = await discord_bot.wait_for("reaction_add")
    def check(reaction, user):
        return user != discord_bot.user and str(reaction.emoji) in ["✋"]
    while True:
        reaction, user = await discord_bot.wait_for("reaction_add")
        try:
            if str(reaction.emoji) == "✋":
                await x.remove_reaction(reaction, user) 
                channel = await user.create_dm()
                await channel.send(embed=embed_1)
        except:
            await channel.send(f"¡Se ha producido un error!")
    def check_1(m):
        return (m).author.id == ctx.author.id
    
    message = await discord_bot.wait_for('message', check=check_1)
    await ctx.send(f"Enviar mensaje a {member}")

    await member.send(f"{message.content}")

#DISCORD MESSAGE COMMAND FOR FORTNITE CUSTOMS GAMES
@discord_bot.command()
@commands.has_permissions(manage_messages = True)
async def code(ctx, *, words):
    author = ctx.author
    icon = ctx.guild.icon_url
    embed_2=discord.Embed(title="Custom Key", description="Key distribution", color=color_main)
    embed_2.add_field(name="Step 1", value="Add ESP CUSTOMS bot in game", inline=False)
    embed_2.add_field(name="Step 2", value="React to the hand", inline=False)
    embed_2.add_field(name="Step 3", value="Join the bot and play the game", inline=True)
    embed_2.set_footer(text=f"Host: {author} | Made by BLD SRGOBI#5100 and yanuu ;k#4594")
    x = await ctx.send(embed=embed_2)
    await x.add_reaction("✋")
    while True:
        try:
            await fortnite_bot.party.set_playlist(playlist="Playlist_ShowdownAlt_Duos")
            await fortnite_bot.party.set_custom_key(f"{words}" .format(words))
        except:
            await ctx.author.send(f"¡I can't change the mode if I'm not a leader!")
    await fortnite_bot.party.me.leave()
    message = await ctx.send(embed=embed_2)
    while True:
        await asyncio.sleep(5)
        embed_3=discord.Embed(title="ESP CUSTOMS", description=f"", color=color_main)
        embed_3.add_field(name="Verification FN", value="Working.", inline=True)
        embed_3.add_field(name="Customs FN", value="Working.", inline=True)
        embed_3.add_field(name="Custom Commands", value="Working.", inline=True)
        embed_3.add_field(name="Premium", value="Working.", inline=True)
        embed_3.add_field(name="Dashboard", value="Working.", inline=True)
        embed_3.add_field(name="Torunaments", value="Working.", inline=True)
        embed_3.set_thumbnail(url=icon)
        embed_3.set_footer(text=f"Host: {author} | Made by BLD SRGOBI#5100")
        await message.edit(embed=embed_3)

#BASIC COMMANDS FOR GOBI
@discord_bot.command()
async def mydiscordcommand(ctx):
    await ctx.send('Hola a todos discord!')


@fortnite_bot.command()
async def myfortnitecommand(ctx):
    await ctx.send('Hola a todos fortnite!')

#Fortnite Commands
## not ready-ready
## no-participate-participate
## friends
## Privacy
## skin
## backpack
## emote
## Leave
## playlist-info
## Leader
## mode
@fortnite_bot.event
async def event_friend_message(message):
    args = message.content.split()
    split = args[1:]
    joinedArguments = " ".join(split)
    print(f"[{getTiempesito()}] " + "{0.author.display_name}: {0.content}".format(message))
    pre = config["prefijo"]
    
    # TODO: comandos no admin, piedra papel tijera...
    # TODO: skin, mochila, emote... para gente que no sabe las IDs
    # TODO: poder configurar que comandos son admin
    if message.author.display_name in config["admins"] or config["todos_admins"]:

        if pre + "notready" in args[0] or pre + "ready" in args[0]:
            await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
            await message.reply("El estado de la habitación cambió a: no listo")

        elif pre + "ready" in args[0]:
            await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.READY)
            await message.reply("El estado de la habitación cambió a: listo")

        elif pre + "notparticipate" in args[0]:
            await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
            await message.reply("El estado de la habitación cambió a: no participa")

        elif pre + "userid" in args[0]:
            usuario = await fortnite_bot.fetch_profile(joinedArguments)
            miembro = fortnite_bot.party.members.get(usuario.id)
            if miembro == None:
                await message.reply("Error: este usuario no existe o no está en su habitación")
            else:
                await message.reply(f"ID: {miembro}")
                print(miembro)

        elif pre + "add" in args[0].lower():
            user = await fortnite_bot.fetch_profile(joinedArguments)
            friends = fortnite_bot.friends
            if user is None:
                await message.reply(f"No hay ningún jugador nombrado {joinedArguments} en Fortnite.")
                print(Fore.BLACK + Back.RED + f"[{getTiempesito()}] [ERROR] No hay ningún jugador nombrado {joinedArguments}")
            else:
                try:
                    if (user.id in friends):
                        await message.reply(f"Ya he agregado a {user.display_name}")
                        print(Fore.BLACK + Back.RED + f"[{getTiempesito()}] [ERROR] El bot ya se ha agregado a {user.display_name} ")
                    else: 
                        await fortnite_bot.add_friend(user.id)
                        await message.reply(f"He enviado una solicitud a {user.display_name}")
                        print(Fore.GREEN + f"[{getTiempesito()}] {fortnite_bot.user.display_name} te ha enviado una solicitud {user.display_name}")
                except Exception as e:
                    pass
                    print(Fore.BLACK + Back.RED + f"[{getTiempesito()}] [ERROR] Se produjo un error al agregar a {joinedArguments}") 

        elif pre + "remove" in args[0].lower():
            user = await fortnite_bot.fetch_profile(joinedArguments)
            friends = fortnite_bot.friends
            if user is None:
                await message.reply(f"No tengo amigo llamado {joinedArguments}.")
                print(Fore.BLACK + Back.RED + f"[{getTiempesito()}] [ERROR] No hay amigo llamado {joinedArguments} en la lista de amigos del bot")
            else:
                try:
                    if (user.id in friends):
                        await fortnite_bot.remove_or_decline_friend(user.id)
                        await message.reply(f"Yo he eliminado {user.display_name} de la lista de amigos.")
                        print(Fore.GREEN + f"[{getTiempesito()}] {fortnite_bot.user.display_name} se ha llevado {user.display_name} como amigo.")
                    else: 
                        await message.reply(f"No he agregado a {user.display_name}.")
                        print(Fore.BLACK + Back.RED + f"[{getTiempesito()}] [ERROR] {fortnite_bot.user.display_name} traté de eliminar {user.display_name} de la lista de amigos del bot, pero este usuario no está agregado.")
                except Exception as e:
                    pass
                    print(Fore.BLACK + Back.RED + f"[{getTiempesito()}] [ERROR] Hubo un problema al eliminar {joinedArguments} de la lista de amigos del bot.")

        elif pre + "friends" in args[0].lower():
            friends = fortnite_bot.friends
            onlineFriends = []
            offlineFriends = []
            try:
                for friend in friends:
                    if friend.is_online():
                        onlineFriends.append(friend.display_name)
                    else:
                        offlineFriends.append(friend.display_name)
                print(f"[{getTiempesito()}] " + Fore.WHITE + "Friends list: " + Fore.GREEN + f"{len(onlineFriends)} Online " + Fore.WHITE + "/" + Fore.LIGHTBLACK_EX + f" {len(offlineFriends)} Disconnected " + Fore.WHITE + "/" + Fore.LIGHTWHITE_EX + f" {len(onlineFriends) + len(offlineFriends)} In total")
                for x in onlineFriends:
                    if x is not None:
                        print(Fore.GREEN + " " + x + Fore.WHITE)
                for x in offlineFriends:
                    if x is not None:
                        print(Fore.LIGHTBLACK_EX + " " + x + Fore.WHITE)
            except Exception as e:
                print(f"Hubo un problema al buscar a tus amigos ({e})")
                pass
            await message.reply("Revisa la consola para ver la lista de amigos.")

        elif pre + "privacy" in args[0].lower():
            if len(args) != 2:
                await message.reply(f"Sintaxis de comando incorrecta")
                return
            else:
                if fortnite_bot.party.me.leader == True:
                    if args[1].lower() == "public":
                        await fortnite_bot.party.me.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                    elif args[1].lower() == "private":
                        await fortnite_bot.party.me.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
                    elif args[1].lower() == "friends":
                        await fortnite_bot.party.me.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS)
                    elif args[1].lower() == "friendsoffriends":
                        await fortnite_bot.party.me.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS_ALLOW_FRIENDS_OF_FRIENDS)
                    else:
                        await message.reply(f"{args[1]} privacidad de la habitación no válida")
                        return
                    await message.reply(f"He cambiado la privacidad de esta habitación a {args[1]}")
                else:
                    await message.reply("Necesito un líder para cambiar la privacidad de la habitación..")

        elif pre + "skin" in args[0].lower():
            if len(args) != 2:
                await message.reply(f"Sintaxis de comando incorrecta")
                return
            else:
                await fortnite_bot.party.me.set_outfit(asset=args[1])

        elif pre + "backpack" in args[0].lower():
            if len(args) != 2:
                await message.reply(f"Sintaxis de comando incorrecta")
                return
            else:
                await fortnite_bot.party.me.set_backpack(asset=args[1])

        elif pre + "emote" in args[0].lower():
            if len(args) == 1:
                await fortnite_bot.party.me.clear_emote()
                await message.reply("Gesto borrado")
                return
            elif len(args) == 2:
                await fortnite_bot.party.me.set_emote(asset=args[1])
                await message.reply(f"Jugando {args[1]}")
            elif len(args) == 3:
                emote_dur_num = es_numero(args[2], True)
                if emote_dur_num:
                    await fortnite_bot.party.me.set_emote(asset=args[1], run_for=emote_dur_num[1])
                    await message.reply(f"Jugando {args[1]} durante {args[2]} segundos")
                else:
                    await message.reply(f"Uso: {config['prefijo']}emote <EID (opcional)> <seconds (opcional)>")
            else:
                await message.reply(f"Uso: {config['prefijo']}emote <EID (opcional)> <seconds (opcional)>")


        elif pre + "leave" in args[0].lower():
            if config["emote_abandonar"]:
                await fortnite_bot.party.me.set_emote(config["emote_abandonar_id"])
                time.sleep(1.5)
            await fortnite_bot.party.send(config["msg_abandonar"])
            await fortnite_bot.party.me.leave()          

        elif pre + "leader" in args[0].lower():
            if len(args) != 1:
                user = await fortnite_bot.fetch_profile(joinedArguments)
                member = fortnite_bot.party.members.get(user.id)
            if len(args) == 1:
                user = await fortnite_bot.fetch_profile(message.author.display_name)
                member = fortnite_bot.party.members.get(user.id)
            if member is None:
                await message.reply("Este usuario no está en la sala. ¿Escribiste el nombre correctamente?")
            else:
                try:
                    await member.promote()
                    await message.reply(f"He hecho un líder {member.display_name}.")
                except Exception as e:
                    pass
                    await message.reply(f"No puedo dar un líder a {member.display_name}, porque no tengo un líder.")

        elif pre + "playlist-info" in args[0]:
            await message.reply(f"PlaylistName: {fortnite_bot.party.playlist_info[0]}")
            await message.reply(f"TournamentId: {fortnite_bot.party.playlist_info[1]}")
            await message.reply(f"EventWindowId: {fortnite_bot.party.playlist_info[2]}")
            await message.reply(f"RegionId: {fortnite_bot.party.playlist_info[3]}")
            print(Fore.BLUE + f"PlaylistName: {fortnite_bot.party.playlist_info[0]}")
            print(Fore.BLUE + f"TournamentId: {fortnite_bot.party.playlist_info[1]}")
            print(Fore.BLUE + f"EventWindowId: {fortnite_bot.party.playlist_info[2]}")
            print(Fore.BLUE + f"RegionId: {fortnite_bot.party.playlist_info[3]}")

        elif pre + "mode" in args[0].lower():
            if len(args) == 1:
                await message.reply(f"Entrar en un modo de juego")
                return

            if "Playlist_" in args[1]:
                await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
                try:
                    await fortnite_bot.party.set_playlist(playlist="Estás en este modo de juego")
                except:
                    await message.reply(f"¡No puedes usar este comando si no soy un líder!")
                    return
                await message.reply(f"Cambiar el modo de juego...")
                try:
                    await fortnite_bot.party.set_playlist(playlist=args[1], tournament="epicgames_Arena_S13_Trios", event_window="Arena_S13_Division1_Trios")
                    await fortnite_bot.party.me.leave()
                except:
                    pass
                    await message.reply(f"¡No puedes usar este comando si no soy un líder!")
                    pAdvertencia("El modo no se pudo cambiar porque el bot no es un líder.")
            else:
                await message.reply(f"Comando incorrecto")

fortnite_bot.run()