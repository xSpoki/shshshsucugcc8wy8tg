"""
“Commons Clause” License Condition v1.0
Copyright xSpoki 2020

Software: frtbot

License: Apache 2.0
"""

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

try:
    import fortnitepy
    from fortnitepy.errors import *
    import BenBotAsync
    import asyncio
    import time as delay
    import datetime
    import json
    import aiohttp
    import time
    import logging
    import functools
    import sys
    import os
    import random
    from colorama import init
    init(autoreset=True)
    from colorama import Fore, Back, Style
except ModuleNotFoundError:
    print(Fore.RED + f'[Youssef_b0t] [N/A] [ERROR] Failed to import 1 or more modules, run "INSTALL PACKAGES.bat".')
    exit()

print(Fore.GREEN + f' Version: 1.1.7')

print(color.CYAN + f' [Youssef_b0t] Youssef b0t made by xSpoki @yusuf_jr_ > enjoy your time!')

def debugOn():
    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

def getTime():
    time = datetime.datetime.now().strftime('%H:%M:%S')
    return time

with open('config.json') as f:
    print(f' [Youssef_b0t] [{getTime()}] Connect To Spoki Service....')
    data = json.load(f)
    print(f' [Youssef_b0t] [{getTime()}] Connected To Spoki Service.')
    
debug = 'False'
if debug == 'True':
    print(f' [Youssef_b0t] [{getTime()}] Waiting access from Spoki Service > checking MAC ADDRESS .....')
    debugOn()
else:
    print(f' [Youssef_b0t] [{getTime()}] Waiting access from Spoki Service > checking MAC ADDRESS .....')

def get_device_auth_details():
    if os.path.isfile('auths.json'):
        with open('auths.json', 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open('auths.json', 'w') as fp:
        json.dump(existing, fp)

device_auth_details = get_device_auth_details().get(data['email'], {})
client = fortnitepy.Client(
    auth=fortnitepy.AdvancedAuth(
        email=data['email'],
        password=data['password'],
        prompt_exchange_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    ),
    status=data['status'],
    platform=fortnitepy.Platform(data['platform']),
    default_party_member_config=[
        functools.partial(fortnitepy.ClientPartyMember.set_outfit, asset=data['cid']),
        functools.partial(fortnitepy.ClientPartyMember.set_backpack, data['bid']),
        functools.partial(fortnitepy.ClientPartyMember.set_banner, icon=data['banner'], color=data['banner_colour'], season_level=data['level']),
        functools.partial(fortnitepy.ClientPartyMember.set_emote, data['eid']),
        functools.partial(fortnitepy.ClientPartyMember.set_pickaxe, data['pid']),
        functools.partial(fortnitepy.ClientPartyMember.set_battlepass_info, has_purchased=True, level=data['bp_tier'], self_boost_xp='0', friend_boost_xp='0')
    ]
)

@client.event
async def event_ready():
    print(Fore.GREEN + ' [Youssef_b0t] [' + getTime() + '] Client ready as {0.user.display_name}.'.format(client))

@client.event
async def event_party_invite(invite):
    if data['joinoninvite'].lower() == 'true':
        if invite.sender.display_name not in data['BlockList']:
            try:
                await invite.accept()
                print(Fore.GREEN + f' [Youssef_b0t] [{getTime()}] Accepted party invite from {invite.sender.display_name}')
            except Exception as e:
                pass
        elif invite.sender.display_name in data['BlockList']:
            print(Fore.GREEN + f' [Youssef_b0t] [{getTime()}] Never accepted party invite from' + Fore.RED + f' {invite.sender.display_name}')
    if data['joinoninvite'].lower() == 'false':
        if invite.sender.display_name in data['FullAccess']:
            await invite.accept()
            print(Fore.GREEN + f' [Youssef_b0t] [{getTime()}] Accepted party invite from {invite.sender.display_name}')
        else:
            print(Fore.GREEN + f' [Youssef_b0t] [{getTime()}] Never accepted party invite from {invite.sender.display_name}')
@client.event
async def event_friend_request(request):
    if data['friendaccept'].lower() == 'true':
        if request.display_name not in data['BlockList']:
            try:
                await request.accept()
                print(f" [Youssef_b0t] [{getTime()}] Accepted friend request from: {request.display_name}")
            except Exception as e:
                pass
        elif request.display_name in data['BlockList']:
            print(f" [Youssef_b0t] [{getTime()}] Never Accepted friend reqest from: " + Fore.RED + f"{request.display_name}")
    if data['friendaccept'].lower() == 'false':
        if request.display_name in data['FullAccess']:
            try:
                await request.accept()
                print(f" [Youssef_b0t] [{getTime()}] Accepted friend request from: {request.display_name}")
            except Exception as e:
                pass
        else:
            print(f" [Youssef_b0t] [{getTime()}] Never accepted friend request from: {request.display_name}")

@client.event
async def event_party_member_join(member):
    if client.user.display_name != member.display_name:
        print(f" [Youssef_b0t] [{getTime()}] {member.display_name} has joined the lobby.")

@client.event
async def event_friend_message(message):
    args = message.content.split()
    split = args[1:]
    joinedArguments = " ".join(split)
    print(' [Youssef_b0t] [' + getTime() + '] {0.author.display_name}: {0.content}'.format(message))

    if "!skin" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)        
        else:
            id = await BenBotAsync.getSkinId(joinedArguments)
            if id == None:
                await message.reply(f"المعذرة منك بس ما لقيت اي سكن باسم: {joinedArguments}")
            else:
                await client.user.party.me.set_outfit(asset=id)
                await message.reply('تم. حطيت السكن: ' + id)
                print(f" [Youssef_b0t] [{getTime()}] Set Skin to: " + id)
        
    if "!backpack" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            if len(args) == 1:
                await client.user.party.me.set_backpack(asset='none')
                await message.reply('Backpack set to None')
                print(f" [Youssef_b0t] [{getTime()}] Set Backpack to None")
            else:
                id = await BenBotAsync.getBackpackId(joinedArguments)
                if id == None:
                    await message.reply(f"اعتذر منك بس ما لقيت اي شنطة باسم: {joinedArguments}")
                else:
                    await client.user.party.me.set_backpack(asset=id)
                    await message.reply('حطيت الشنطة: ' + id)
                    print(f" [Youssef_b0t] [{getTime()}] Set Backpack to: " + id)

    if "!emote" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.clear_emote()
            id = await BenBotAsync.getEmoteId(joinedArguments)
            if id == None:
                await message.reply(f"اسف والله ، بس ما لقيت رقصة باسم: {joinedArguments}")
            else:
                await client.user.party.me.set_emote(asset=id)
                await message.reply('حطيت الرقصة ل: ' + id)
                print(f" [Youssef_b0t] [{getTime()}] Set Emote to: " + id)
    
    if "!pickaxe" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            id = await BenBotAsync.getPickaxeId(joinedArguments)
            if id == None:
                await message.reply(f"اعتذر ، ما لقيت اي بيكاكس بالاسم ذا: {joinedArguments}")
            else:
                await client.user.party.me.set_pickaxe(asset=id)
                await message.reply('Pickaxe set to ' + id)
                print(f" [Youssef_b0t] [{getTime()}] Set Pickaxe to: " + id)

    if "!point" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.clear_emote()
            if len(args) == 1:
                await client.user.party.me.set_emote(asset="/Game/Athena/Items/Cosmetics/Dances/EID_IceKing.EID_IceKing")
                await message.reply('حطيت رقصة: Point It Out')
            else:
                id = await BenBotAsync.getPickaxeId(joinedArguments)
                if id == None:
                    await message.reply(f"اسف ، ما لقيت اي بيكاكس باسم: {joinedArguments}")
                else:
                    await client.user.party.me.set_pickaxe(asset=id)
                    await client.user.party.me.set_emote(asset="/Game/Athena/Items/Cosmetics/Dances/EID_IceKing.EID_IceKing")
                    await message.reply('حطيت رقصة البيكاكس مع بيكاكس: ' + id)
                    print(f" [Youssef_b0t] [{getTime()}] Pointing a pickaxe with: " + id)

    if "!pet" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            id = await BenBotAsync.getPetId(joinedArguments)
            await client.user.party.me.set_backpack(
                    asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + id + "." + id
            )

            await message.reply('Pet set to ' + id)
            print(f" [Youssef_b0t] [{getTime()}] Client's PetCarrier set to: " + id)

    if "!emoji" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            id = await fetch_cosmetic_id(' '.join(split), 'AthenaDance')
            await client.user.party.me.clear_emote()
            await client.user.party.me.set_emote(
                    asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + id + "." + id
            )

            await message.reply('Emoji set to ' + id)
            print(f" [Youssef_b0t] [{getTime()}] Client's Emoji set to " + id)

    if "!prs" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            try:
                variants = client.user.party.me.create_variants(
                   clothing_color=1
                )

                await client.user.party.me.set_outfit(
                    asset='CID_030_Athena_Commando_M_Halloween',
                    variants=variants
                )

                await message.reply('Skin set to Purple Skull Trooper!')
                print(f" [Youssef_b0t] [{getTime()}] Client's Skin set to Purple Skull Trooper")
            except Exception as e:
                pass

    if "!pig" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            try:
                variants = client.user.party.me.create_variants(
                   material=3
                )

                await client.user.party.me.set_outfit(
                    asset='CID_029_Athena_Commando_F_Halloween',
                    variants=variants
                )

                await message.reply('حطيت سكن بنت الزومبي الوردية!')
                print(f" [Youssef_b0t] [{getTime()}] Client's Skin set to Pink Ghoul Trooper")
            except Exception as e:
                pass
                
    if "!re" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            try:
                variants = client.user.party.me.create_variants(
                   material=3
                )

                await client.user.party.me.set_outfit(
                    asset='CID_022_Athena_Commando_F',
                    variants=variants
                )

                await message.reply('حطيت سكن انجولاء السوداء ههههههههههههههههه امزح!')
                print(f" [Youssef_b0t] [{getTime()}] Client's Skin set to Recon Expert")
            except Exception as e:
                pass

    if "!brainiacghoulo" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            try:
                variants = client.user.party.me.create_variants(
                   material=2
                )

                await client.user.party.me.set_outfit(
                    asset='CID_029_Athena_Commando_F_Halloween',
                    variants=variants
                )

                await message.reply('حطيت سكن بنت الزومبي الاصلية!')
                print(f" [Youssef_b0t] [{getTime()}] Client's Skin set to Brainiac Ghoul Trooper")
            except Exception as e:
                pass

    if "!purpleportalo" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            variants = client.user.party.me.create_variants(
                item='AthenaBackpack',
                particle_config='Particle',
                particle=1
            )

            await client.user.party.me.set_backpack(
                asset='BID_105_GhostPortal',
                variants=variants
            )

            await message.reply('Backpack set to Purple Ghost Portal!')
            print(f" [Youssef_b0t] [{getTime()}] Client's Backpack set to Purple Ghost Portal")

    if "!banner" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            if len(args) == 1:
                await message.reply('You need to specify which banner, color & level you want to set the banner as.')
            if len(args) == 2:
                await client.user.party.me.set_banner(icon=args[1], color=data['banner_colour'], season_level=data['level'])
            if len(args) == 3:
                await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=data['level'])
            if len(args) == 4:
                await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])

            await message.reply(f'Banner set to; {args[1]} {args[2]} {args[3]}')
            print(f" [Youssef_b0t] [{getTime()}] Banner set to; {args[1]} {args[2]} {args[3]}")

    if "CID_" in args[0]:
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.set_outfit(
                asset=args[0]
            )
            await message.reply(f'تم وضع السكن: {args[0]}')
            print(f' [Youssef_b0t] [{getTime()}] Skin set to ' + args[0])

    if "!variants" in args[0]:
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            args3 = int(args[3])

            if 'CID' in args[1]:
                variants = client.user.party.me.create_variants(**{args[2]: args3})
                await client.user.party.me.set_outfit(
                    asset=args[1],
                    variants=variants
                )
            elif 'BID' in args[1]:
                variants = client.user.party.me.create_variants(item='AthenaBackpack', **{args[2]: args3})
                await client.user.party.me.set_backpack(
                    asset=args[1],
                    variants=variants
                )
            elif 'PICKAXE_ID' in args[1]:
                variants = client.user.party.me.create_variants(item='AthenaPickaxe', **{args[2]: args3})
                await client.user.party.me.set_pickaxe(
                    asset=args[1],
                    variants=variants
                )

            await message.reply(f'Set variants of {args[1]} to {args[2]} {args[3]}.')
            print(f' [Youssef_b0t] [{getTime()}] Set variants of {args[1]} to {args[2]} {args[3]}.')

    if "!rr" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            variants = client.user.party.me.create_variants(
               material=2
            )

            await client.user.party.me.set_outfit(
                asset='CID_028_Athena_Commando_F',
                variants=variants
            )

            await message.reply('حطيت سكن بنت الطرارة هههههه!')
            print(f" [Youssef_b0t] [{getTime()}] Client's Skin set to Checkered Renegade")

    if "!mintyelf" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            variants = client.user.party.me.create_variants(
                   material=2
                )

            await client.user.party.me.set_outfit(
                asset='CID_051_Athena_Commando_M_HolidayElf',
                variants=variants
                )

            await message.reply('Skin set to Minty Elf!')
            print(f" [Youssef_b0t] [{getTime()}] Client's Skin set to Minty Elf")

    if "EID_" in args[0]:
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.clear_emote()
            await client.user.party.me.set_emote(
                asset=args[0]
            )
            await message.reply('تم ، حطيت الرقصة: ' + args[0] + '!')
        
    if "!stop" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.clear_emote()
            await message.reply('تمام. وقفت الرقصة!')

    if "BID_" in args[0]:
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
            await client.user.party.me.set_backpack(
                asset=args[0]
            )

            await message.reply('Backbling set to ' + message.content + '!')

    if "help" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await message.reply('Commands: !cosmetics - Lists Cosmetic Commands  |  !party - Lists Party Commands | You can view a more detailed commands list in my Instagram Account: @yusuf_jr_!')

    if "!cosmetics" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await message.reply('Cosmetic Commands: !skin (skin name), !backpack (backpack name), !emote (emote name) | !stop-to stop the emote, !pickaxe (pickaxe name), !point (pickaxe name), !pet (pet name), !emoji (emoji name), !variants (CID) (style type) (integer), !purpleskull, !pinkghoul, !brainiacghoul, !purpleportal, !checkeredrenegade, !banner (icon) (colour) (level), CID_, BID_, PICKAXE_ID_, EID_')

    if "!party" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await message.reply('Party Commands: !ready, !unready, !sitout, !sitin, !bp (tier), !level (level), !echo (message), !leave, !kick (username), Playlist_')

    if "Pickaxe_" in args[0]:
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.set_pickaxe(
                    asset=args[0]
            )

            await message.reply('Pickaxe set to ' + args[0] + '!')

    if "PetCarrier_" in args[0]:
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.set_backpack(
                    asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + args[0] + "." + args[0]
            )

    if "Emoji_" in args[0]:
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.set_emote(asset='EID_ClearEmote')
            await client.user.party.me.set_emote(
                    asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + args[0] + "." + args[0]
            )

    if "!ready" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.set_ready(fortnitepy.ReadyState.READY)
            await message.reply('ريدي!')

    if ("!unready" in args[0].lower()) or ("!sitin" in args[0].lower()):
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
            await message.reply('مو ريدي!')

    if "!sitout" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
            await message.reply('مو ريدي!')

    if "!bp" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.set_battlepass_info(has_purchased=True, level=args[1], self_boost_xp='0', friend_boost_xp='0')

    if "!level" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.set_banner(icon=client.user.party.me.banner[0], color=client.user.party.me.banner[1], season_level=args[1])
    
    if "!reset" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            variants = client.user.party.me.create_variants(**{data['variants-type']: data['variants']})
            await client.user.party.me.set_outfit(asset=data['cid'], variants=variants)
            await client.user.party.me.set_backpack(asset=data['bid'])
            await client.user.party.me.set_banner(icon=data['banner'], color=data['banner_colour'], season_level=data['level'])
            await client.user.party.me.set_pickaxe(asset=data['pid'])
            await client.user.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp='0', friend_boost_xp='0')
            await message.reply(f"Reset to default cosmetic loadout.")

    if "!admin" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            if len(args) == 1:
                await message.reply('يرجى تحديد ما إذا كنت تريد إضافة مستخدم أو إزالته من قائمة المشرفين')
                print(f' [Youssef_b0t] [{getTime()}] Please specify if you want to add or remove a user from the admin list, using ' + color.GREEN + '!admin add ' + color.END + 'or ' + color.GREEN + '!admin remove' + color.END)
            if len(args) == 2:
                if args[1].lower() == 'add' or args[1].lower() == 'remove':
                    await message.reply('Please specify the name of the user you want to add/remove from the admin list')
                    print(f' [Youssef_b0t] [{getTime()}] Please specify the name of the user you want to add/remove from the admin list')
                else:
                    await message.reply('استخدام غير صالح')
                    print(f' [Youssef_b0t] [{getTime()}] Invalid usage, try ' + color.GREEN + '!admin add <username> ' + color.END + 'or ' + color.GREEN + '!admin remove <username>' + color.END)
            if len(args) >= 3:
                joinedArgumentsAdmin = " ".join(args[2:])
                user = await client.fetch_profile(joinedArgumentsAdmin)
                try:
                    if args[1].lower() == 'add':
                        if user.display_name not in data['FullAccess']:
                            data['FullAccess'].append(f"{user.display_name}")
                            with open('config.json', 'w') as f:
                                json.dump(data, f, indent=4)
                                print(f" [Youssef_b0t] [{getTime()}] Added " + color.GREEN + f"{user.display_name}" + color.END + " as an admin")
                        elif user.display_name in data['FullAccess']:               
                            print(f" [Youssef_b0t] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is already an admin")
                    elif args[1].lower() == 'remove':
                        if user.display_name in data['FullAccess']:
                            data['FullAccess'].remove(user.display_name)
                            with open('config.json', 'w') as f:
                                json.dump(data, f, indent=4)
                                print(f" [Youssef_b0t] [{getTime()}] Removed " + color.GREEN + f"{user.display_name}" + color.END + " as an admin")
                        elif user.display_name not in data['FullAccess']:
                            print(f" [Youssef_b0t] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is not an admin")
                except AttributeError:
                    pass
                    print(f" [Youssef_b0t] [{getTime()}] Can't find user: " + color.GREEN + f"{joinedArgumentsAdmin}" + color.END)
                    await message.reply(f"I couldn't find an Epic account with the name: {joinedArgumentsAdmin}.")
        if message.author.display_name not in data['FullAccess']:
            if len(args) >= 3 and args[1].lower() == 'add':
                await message.reply(f"Password?")
                res = await client.wait_for('friend_message')
                content = res.content.lower()
                joinedArgumentsAdmin = " ".join(args[2:])
                user = await client.fetch_profile(joinedArgumentsAdmin)
                if content in data['AdminPassword']:
                    if user.display_name not in data['FullAccess']:
                        data['FullAccess'].append(f"{user.display_name}")
                        with open('config.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            await message.reply(f"Correct. Added {user.display_name} as an admin.")
                            print(f" [Youssef_b0t] [{getTime()}] Added " + color.GREEN + f"{user.display_name}" + color.END + " as an admin")
                    elif user.display_name in data['FullAccess']:
                        print(f" [Youssef_b0t] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is already an admin")
                        await message.reply(f"{user.display_name} is already an admin.")

    if "!blocklist" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            if len(args) == 1:
                await message.reply('Please specify if you want to add or remove a user from the block list')
                print(f' [Youssef_b0t] [{getTime()}] Please specify if you want to add or remove a user from the admin list, using ' + color.GREEN + '!admin add ' + color.END + 'or ' + color.GREEN + '!admin remove' + color.END)
            if len(args) == 2:
                if args[1].lower() == 'add' or args[1].lower() == 'remove':
                    await message.reply('Please specify the name of the user you want to add/remove from the block list')
                    print(f' [Youssef_b0t] [{getTime()}] Please specify the name of the user you want to add/remove from the block list')
                else:
                    await message.reply('Invalid usage, try !blocklist add <username> or !blocklist remove <username>')
                    print(f' [Youssef_b0t] [{getTime()}] Invalid usage, try ' + color.GREEN + '!BlockList add <username> ' + color.END + 'or ' + color.GREEN + '!BlockList remove <username>' + color.END)
            if len(args) >= 3:
                joinedArgumentsAdmin = " ".join(args[2:])
                user = await client.fetch_profile(joinedArgumentsAdmin)
                if args[1].lower() == 'add':
                    if user.display_name not in data['FullAccess'] and user.display_name not in data['BlockList']:
                        data['BlockList'].append(f"{user.display_name}")
                        with open('config.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            await message.reply(f"Added {user.display_name} to the blocked list.")
                            print(f" [Youssef_b0t] [{getTime()}] Added " + color.GREEN + f"{user.display_name}" + color.END + " to the blocked list.")
                    elif user.display_name in data['FullAccess']:
                        await message.reply(f"{user.display_name} can not be added to the blocked list.")
                        print(f" [Youssef_b0t] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " cannot be added to the blocked list.")
                    elif user.display_name in data['BlockList']:               
                        await message.reply(f"{user.display_name} is already on the blocked list.")
                        print(f" [Youssef_b0t] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is already on the blocked list.")
                elif args[1].lower() == 'remove':
                    if user.display_name in data['BlockList']:
                        data['BlockList'].remove(user.display_name)
                        with open('config.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            print(f" [Youssef_b0t] [{getTime()}] Removed " + color.GREEN + f"{user.display_name}" + color.END + " from the blocked list.")
                    elif user.display_name not in data['BlockList']:
                        print(f" [Youssef_b0t] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is not on the blocked list.")
        if message.author.display_name not in data['FullAccess']:
            if len(args) >= 3 and args[1].lower() == 'add':
                await message.reply(f"Password?")
                res = await client.wait_for('friend_message')
                content = res.content.lower()
                joinedArgumentsAdmin = " ".join(args[2:])
                user = await client.fetch_profile(joinedArgumentsAdmin)
                if content in data['AdminPassword']:
                    if user.display_name not in data['BlockList']:
                        data['BlockList'].append(f"{user.display_name}")
                        with open('config.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            await message.reply(f"Correct. Added {user.display_name} to the blocked list.")
                            print(f" [Youssef_b0t] [{getTime()}] Added " + color.GREEN + f"{user.display_name}" + color.END + " to the blocked list.")
                    elif user.display_name in data['BlockList']:
                        print(f" [Youssef_b0t] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is already on the blocked list.")
                        await message.reply(f"{user.display_name} is already on the blocked list.")
                elif args[1].lower() == 'remove':
                    await message.reply(f"Password?")
                    res = await client.wait_for('friend_message')
                    content = res.content.lower()
                    joinedArgumentsAdmin = " ".join(args[2:])
                    user = await client.fetch_profile(joinedArgumentsAdmin)
                    if content in data['AdminPassword']:
                        if user.display_name in data['BlockList']:
                            data['BlockList'].remove(user.display_name)
                            with open('config.json', 'w') as f:
                                json.dump(data, f, indent=4)
                                print(f" [Youssef_b0t] [{getTime()}] Removed " + color.GREEN + f"{user.display_name}" + color.END + " from the blocked list.")
                        elif user.display_name not in data['BlockList']:
                            print(f" [Youssef_b0t] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is not on the blocked list.")

            
    if "!leave" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            await client.user.party.me.set_emote('EID_Snap')
            delay.sleep(2)
            await client.user.party.me.leave()
            await message.reply('Bye!')
            print(Fore.GREEN + f' [Youssef_b0t] [{getTime()}] Left the party as I was requested.')
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)

    if "!kick" in args[0].lower() and message.author.display_name in data['FullAccess']:
        user = await client.fetch_profile(joinedArguments)
        member = client.user.party.members.get(user.id)
        if member is None:
            await message.reply("Couldn't find that user, are you sure they're in the party?")
        else:
            try:
                await member.kick()
                await message.reply(f"Kicked user: {member.display_name}.")
                print(Fore.GREEN + f" [Youssef_b0t] [{getTime()}] Kicked user: {member.display_name}")
            except Exception as e:
                pass
                await message.reply(f"Couldn't kick {member.display_name}, as I'm not party leader.")
                print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] Failed to kick member as I don't have the required permissions." + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)

    if "!join" in args[0] and message.author.display_name in data['FullAccess']:
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            friend = client.get_friend(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.id, cache=False, raw=False)
            friend = client.get_friend(user.id)
        if friend is None:
            await message.reply(f"ما قدرت اجون على اليوزر ذا والله ، انت متأكد اني صديق معه عالايبك؟")
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] Unable to join user: {joinedArguments}, are you sure the bot has them added?" + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            try:
                await friend.join_party()
                await message.reply(f"جاري التجوين على {friend.display_name}")
            except Exception as e:
                await message.reply(f"اعتذر بس مني قادر اجون ، جرب ترسل مرة ثانية وشيك اذا البارتي عام")

    if "!invite" in args[0].lower():
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            friend = client.get_friend(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.id, cache=False, raw=False)
            friend = client.get_friend(user.id)
        if friend is None:
            await message.reply(f"اسف ، ما قدرت ارسل لليوزر ذا ، انت متأكد اني صديق معه عالايبك؟")
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] Unable to invite user: {joinedArguments}, are you sure the bot has them added?" + Fore.WHITE)
        else:
            try:
                await friend.invite()
                await message.reply(f"رسلت ل: {friend.display_name}.")
                print(Fore.GREEN + f" [Youssef_b0t] [{getTime()}] Invited user: {friend.display_name}")
            except Exception as e:
                pass
                await message.reply(f"في شي غلط لما حاولت اجون على {friend.display_name}")
                print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] Something went wrong while trying to invite {friend.display_name}" + Fore.WHITE)           

    if "!add" in args[0].lower() and message.author.display_name in data['FullAccess']:
        user = await client.fetch_profile(joinedArguments)
        friends = client.friends
        if user is None:
            await message.reply(f"اعتذر منك بس ما لقيت اي شخص بالاسم ذا: {joinedArguments}.")
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] Unable to find a player with the name {joinedArguments}")
        else:
            try:
                if (user.id in friends):
                    await message.reply(f"انا بالاساس عندي {user.display_name} كصديق بالحساب")
                    print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] You already have {user.display_name} added as a friend.")
                else: 
                    await client.add_friend(user.id)
                    await message.reply(f"رسلت طلب صداقة ل: {user.display_name}")
                    print(Fore.GREEN + f" [Youssef_b0t] [{getTime()}] {client.user.display_name} sent a friend request to {user.display_name}" + Fore.WHITE)
            except Exception as e:
                pass
                print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] Something went wrong adding {joinedArguments}" + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)

    if "!echo" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            await client.user.party.send(joinedArguments)
            print(f' [Youssef_b0t] [{getTime()}] ' + color.GREEN + 'Sent Message:' + color.END + f' {joinedArguments}')
        else:
            if message.author.display_name not in data['FullAccess']:
                await message.reply(f"You don't have access to this command!")


    if "!reset" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            await message.reply("You don't have access to this command!")
        else:
            variants = client.user.party.me.create_variants(**{data['variants-type']: data['variants']})
            await client.user.party.me.set_outfit(asset=data['cid'], variants=variants)
            await client.user.party.me.set_backpack(asset=data['bid'])
            await client.user.party.me.set_banner(icon=data['banner'], color=data['banner_colour'], season_level=data['level'])
            await client.user.party.me.set_pickaxe(asset=data['pid'])
            await client.user.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp='0', friend_boost_xp='0')
            await message.reply(f"Reset to default cosmetic loadout.")

    if "!remove" in args[0].lower() and message.author.display_name in data['FullAccess']:
        user = await client.fetch_profile(joinedArguments)
        friends = client.friends
        if user is None:
            await message.reply(f"اعتذر منك بس ما لقيت اي لاعب بالاسم ذا: {joinedArguments}.")
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] Unable to find a player with the name {joinedArguments}")
        else:
            try:
                if (user.id in friends):
                    await client.remove_or_decline_friend(user.id)
                    await message.reply(f"تمام ، تم بنجاح حذف {user.display_name} من الاصدقاء.")
                    print(Fore.GREEN + f" [Youssef_b0t] [{getTime()}] {client.user.display_name} removed {user.display_name} as a friend.")
                else: 
                    await message.reply(f"I don't have {user.display_name} as a friend.")
                    print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] {client.user.display_name} tried removing {user.display_name} as a friend, but the client doesn't have the friend added." + Fore.WHITE)
            except Exception as e:
                pass
                print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] Something went wrong removing {joinedArguments} as a friend." + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)

    if "!showfriends" in args[0].lower() and message.author.display_name in data['FullAccess']:
        friends = client.friends
        onlineFriends = []
        offlineFriends = []
        try:
            for f in friends:
                friend = client.get_friend(f)
                if friend.is_online():
                    onlineFriends.append(friend.display_name)
                else:
                    offlineFriends.append(friend.display_name)
            print(f" [Youssef_b0t] [{getTime()}] " + Fore.WHITE + "Friends List: " + Fore.GREEN + f"{len(onlineFriends)} Online " + Fore.WHITE + "/" + Fore.LIGHTBLACK_EX + f" {len(offlineFriends)} Offline " + Fore.WHITE + "/" + Fore.LIGHTWHITE_EX + f" {len(onlineFriends) + len(offlineFriends)} Total")
            for x in onlineFriends:
                if x is not None:
                    print(Fore.GREEN + " " + x + Fore.WHITE)
            for x in offlineFriends:
                if x is not None:
                    print(Fore.LIGHTBLACK_EX + " " + x + Fore.WHITE)
        except Exception as e:
            pass
        await message.reply("ابيك تشيك على النافذة حقت الاوامر ياوحش.")   
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)

    if "!members" in args[0].lower() and message.author.display_name in data['FullAccess']:
            members = client.user.party.members
            partyMembers = []
            for m in members:
                member = client.get_user(m)
                partyMembers.append(member.display_name)
            print(f" [Youssef_b0t] [{getTime()}] " + Fore.WHITE + "There are " + Fore.LIGHTWHITE_EX + f"{len(partyMembers)} members in client's party:")
            await message.reply(f"There are {len(partyMembers)} members in {client.user.display_name}'s party:")
            for x in partyMembers:
                if x is not None:
                    print(Fore.GREEN + " " + x + Fore.WHITE)
                    await message.reply(x)

    if "!promote" in args[0].lower() and message.author.display_name in data['FullAccess']:
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            member = client.user.party.members.get(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.display_name)
            member = client.user.party.members.get(user.id)
        if member is None:
            await message.reply("اعتذر منك ما لقيت شخص بالاسم ذا ، متأكد انه معنا بالبارتي؟")
        else:
            try:
                await member.promote()
                await message.reply(f"عطيت الليدر ل: {member.display_name}.")
                print(Fore.GREEN + f" [Youssef_b0t] [{getTime()}] Promoted user: {member.display_name}")
            except Exception as e:
                pass
                await message.reply(f"ما قدرت اعطي الليدر {member.display_name}, لاني مني ماسكه.")
                print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] المعذرة ما قدرت اعطيه الليدر ، ما عندي الصلاحيات اللازمة." + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)


    if args[0] == "!id":
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            user = await client.fetch_profile(joinedArguments, cache=False, raw=False)
            try:
                await message.reply(f"{joinedArguments}'s Epic ID is: {user.id}")
                print(Fore.GREEN + f" [Youssef_b0t] [{getTime()}] {joinedArguments}'s Epic ID is: {user.id}")
            except AttributeError:
                await message.reply(f"I couldn't find an Epic account with the name: {joinedArguments}.")
                print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] اعتذر منك ، ما لقيت ايبك بهاذا الاسم: {joinedArguments}.")


    elif "!cpy" in args[0].lower() and message.author.display_name in data['FullAccess']:
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            member = client.user.party.members.get(user.id)
        else:
            user = await client.fetch_profile(content)
            member = client.user.party.members.get(user.id)

        await client.user.party.me.edit(
            functools.partial(fortnitepy.ClientPartyMember.set_outfit, asset=member.outfit, variants=member.outfit_variants),
            functools.partial(fortnitepy.ClientPartyMember.set_backpack, asset=member.backpack, variants=member.backpack_variants),
            functools.partial(fortnitepy.ClientPartyMember.set_pickaxe, asset=member.pickaxe, variants=member.pickaxe_variants),
        )

        await client.user.party.me.set_emote(asset=member.emote)
        print(Fore.GREEN + f" [Youssef_b0t] [{getTime()}] Skin set to: {member.outfit} and backpack set to {member.backpack} and pickaxe set to: {member.pickaxe}")
    
    if "!pri" in args[0].lower() and message.author.display_name in data['FullAccess']:
        if 'pp' in args[1].lower():
             await client.user.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
        if 'pr' in args[1].lower():
            await client.user.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
            await message.reply(f"حطيت لك البارتي برايفت عشان لا يدخلو نشبات.")

    elif "!gift" in args[0].lower() and message.author.display_name in data['FullAccess']:
        await client.user.party.me.clear_emote()

        await client.user.party.me.set_emote(
            asset='EID_NeverGonna'
        )

        await message.reply('What did you think would happen?')

    if "!fre" in args[0].lower():
        if message.author.display_name not in data['FullAccess']:
            print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [Attention] someone is trying to play with the b0t, if you don't know him ban it immediately, or contact with @yusuf_jr_." + Fore.WHITE)
        else:
            await client.user.party.me.clear_emote()
            if len(args) == 1:
                await client.user.party.me.set_emote(asset="/Game/Athena/Items/Cosmetics/Dances/EID_HIPHOP01.EID_HIPHOP01")
                await message.reply('حطيت رقصة التويتش')


try:
    client.run()
except fortnitepy.AuthException:
    print(Fore.RED + f" [Youssef_b0t] [{getTime()}] [ERROR] Couldn't log into the account, are the account credentials correct?")
