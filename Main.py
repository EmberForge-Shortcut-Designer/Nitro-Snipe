import discord, sys, time, os, colorama, datetime, io, ctypes
import re, json, requests

from discord.ext import (
    commands,
    tasks
)

from colorama import Fore
from win10toast import ToastNotifier
import pyPrivnote as pn
from time import sleep

toaster = ToastNotifier()

with open('config.json') as f:
    config = json.load(f)

token = config.get('token')
onalt = config.get("on-alt")
rtoken = config.get("reedem-token")

edelay = config.get("delay-enabled")
delay = config.get("delay")

giveaway_sniper = config.get('giveaway_sniper')
slotbot_sniper = config.get('slotbot_sniper')
nitro_sniper = config.get('nitro_sniper')
privnote_sniper = config.get('privnote_sniper')
notification = config.get('notification')

def startprint():

    headers = {
        'Authorization': rtoken,
        'Content-Type': 'application/json'
    }

    res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
    res = res.json()
    s_name = res['username']
    s_tag = res['discriminator']


    if onalt == False:
        onaltt = " "
    else:
        onaltt = f"{Fore.LIGHTBLACK_EX}({s_name}#{s_tag})"

    if edelay == True:
        ddelay = f"{Fore.LIGHTBLACK_EX}({delay} seconds)"
    else:
        ddelay = " "

    if giveaway_sniper == True:
        giveaway = "Active" 
    else:
        giveaway = "Disabled"

    if nitro_sniper == True:
        nitro = "Active"
    else:
        nitro = "Disabled"

    if notification == True:
        notify = "Active"
    else:
        notify = "Disabled"    
    if privnote_sniper == True:
        privnote = "Active"
    else:
        privnote = "Disabled"    




    print(f'''{Fore.RESET}


                                             {Fore.GREEN}╔═╗  ╔╗╔  ╦  ╦═╗  ╦═╗  ╦═╗
                                             {Fore.LIGHTBLACK_EX}╚═╗  ║║║  ║  ╠═╝  ╠╣   ╠╦╝
                                             {Fore.WHITE}╚═╝  ╝╚╝  ╩  ╩    ╩═╝  ╩╚═

                                            
                                             {Fore.WHITE}Logged User     -  {Fore.GREEN}{Sniper.user.name}#{Sniper.user.discriminator}

                                             {Fore.WHITE}Nitro Sniper    -  {Fore.GREEN}{nitro} {onaltt}
                                             {Fore.WHITE}Giveaway Sniper -  {Fore.GREEN}{giveaway} {ddelay}
                                             {Fore.WHITE}Privnote Sniper -  {Fore.GREEN}{privnote}
                                             {Fore.WHITE}Notification    -  {Fore.GREEN}{notify}
                                            
    '''+Fore.RESET)


colorama.init()
Sniper = discord.Client()
Sniper = commands.Bot(
    description='Discord Sniper',
    command_prefix="",
    self_bot=True
)

def Clear():
    os.system('cls')
Clear()

def Init():

    if config.get('token') == "token-here":
        
        Clear()
        print(f"{Fore.RED}Error {Fore.WHITE}You didnt put your token in the config.json file"+Fore.RESET)
    else:
        token = config.get('token')
        try:
            Sniper.run(token, bot=False, reconnect=True)
            os.system(f'title Discord Sniper')
        except discord.errors.LoginFailure:
            print(f"""
            
                                             {Fore.GREEN}╔═╗  ╔╗╔  ╦  ╦═╗  ╦═╗  ╦═╗
                                             {Fore.LIGHTBLACK_EX}╚═╗  ║║║  ║  ╠═╝  ╠╣   ╠╦╝
                                             {Fore.WHITE}╚═╝  ╝╚╝  ╩  ╩    ╩═╝  ╩╚═
            
            
            
            
                            {Fore.RED}Error {Fore.WHITE}Token is invalid"""+Fore.RESET)
            os.system('pause >NUL')



@Sniper.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, discord.errors.Forbidden):
        print(f"{Fore.RED}Error: {Fore.WHITE}Discord error: {error}"+Fore.RESET)    
    else:
        print(f"{Fore.RED}Error: {Fore.WHITE}{error_str}"+Fore.RESET)

@Sniper.event
async def on_message(message):
    def GiveawayInfo():
        print(
        f"{Fore.LIGHTBLACK_EX} Server: {Fore.WHITE}{message.guild}"  
        f"\n{Fore.LIGHTBLACK_EX} Channel: {Fore.WHITE}{message.channel}"  
    +Fore.RESET)

    def GiveawayDelayInfo():
        print(
        f"{Fore.LIGHTBLACK_EX} Server: {Fore.WHITE}{message.guild}"  
        f"\n{Fore.LIGHTBLACK_EX} Channel: {Fore.WHITE}{message.channel}"  
        f"\n{Fore.LIGHTBLACK_EX} Delay: {Fore.WHITE}{delay} seconds"  
    +Fore.RESET) 

    def NitroInfo(elapsed, code):
        print(
        f"{Fore.LIGHTBLACK_EX} Server: {Fore.WHITE}{message.guild}"
        f"\n{Fore.LIGHTBLACK_EX} Channel: {Fore.WHITE}{message.channel}" 
        f"\n{Fore.LIGHTBLACK_EX} Author: {Fore.WHITE}{message.author}"
        f"\n{Fore.LIGHTBLACK_EX} Author ID: {Fore.WHITE}{message.author.id}"
        f"\n{Fore.LIGHTBLACK_EX} Elapsed: {Fore.WHITE}{elapsed}s"
        f"\n{Fore.LIGHTBLACK_EX} Code: {Fore.WHITE}{code}"
    +Fore.RESET)

    def PrivnoteInfo(elapsed, code):
        print(
        f"\n{Fore.LIGHTBLACK_EX} Server: {Fore.WHITE}{message.guild}"
        f"\n{Fore.LIGHTBLACK_EX} Channel: {Fore.WHITE}{message.channel}"
        f"\n{Fore.LIGHTBLACK_EX} Elapsed: {Fore.WHITE}{elapsed}s"
        f"\n{Fore.LIGHTBLACK_EX} Content: {Fore.WHITE}Privnote content is saved in Privnote/{code}.txt"
    +Fore.RESET)        

    time = datetime.datetime.now().strftime("%H:%M")
    if 'discord.gift/' in message.content:
        if nitro_sniper == True:
            start = datetime.datetime.now()
            code = re.search("discord.gift/(.*)", message.content).group(1)
            if onalt == True:
                headers = {'Authorization': rtoken}
            else:
                headers = {'Authorization': token}
            r = requests.post(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem', 
                headers=headers,
            ).text
        
            elapsed = datetime.datetime.now() - start
            elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'

            if 'This gift has been redeemed already.' in r:
                print(""
                f"\n{Fore.RED}{time} - Nitro is Already Redeemed"+Fore.RESET)
                NitroInfo(elapsed, code)
            elif 'subscription_plan' in r:
                print(""
                f"\n{Fore.GREEN}{time} - Nitro Successfuly Claimed!"+Fore.RESET)
                NitroInfo(elapsed, code)
                if notification == True:
                    toaster.show_toast("Sniper",
                    "Nitro Claimed! Look into console",
                    icon_path="./drop.ico",
                    duration=7)
            elif 'Unknown Gift Code' in r:
                print(""
                f"\n{Fore.YELLOW}{time} - Unknown Nitro Gift Code"+Fore.RESET)
                NitroInfo(elapsed, code)
        else:
            return

    if 'discord.com/gifts/' in message.content:
        if nitro_sniper == True:
            start = datetime.datetime.now()
            code = re.search("discord.com/gifts/(.*)", message.content).group(1)
            if onalt == True:
                headers = {'Authorization': rtoken}
            else:
                headers = {'Authorization': token}
            r = requests.post(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem', 
                headers=headers,
            ).text
        
            elapsed = datetime.datetime.now() - start
            elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'

            if 'This gift has been redeemed already.' in r:
                print(""
                f"\n{Fore.RED}{time} - Nitro is Already Redeemed"+Fore.RESET)
                NitroInfo(elapsed, code)
            elif 'subscription_plan' in r:
                print(""
                f"\n{Fore.GREEN}{time} - Nitro Successfuly Claimed!"+Fore.RESET)
                NitroInfo(elapsed, code)
                if notification == True:
                    toaster.show_toast("Sniper",
                    "Nitro Claimed! Look into console",
                    icon_path="./drop.ico",
                    duration=7)
            elif 'Unknown Gift Code' in r:
                print(""
                f"\n{Fore.YELLOW}{time} - Unknown Nitro Gift Code"+Fore.RESET)
                NitroInfo(elapsed, code)
        else:
            return

    if 'discordapp.com/gifts/' in message.content:
        if nitro_sniper == True:
            start = datetime.datetime.now()
            code = re.search("discordapp.com/gifts/(.*)", message.content).group(1)
            if onalt == True:
                headers = {'Authorization': rtoken}
            else:
                headers = {'Authorization': token}
            r = requests.post(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem', 
                headers=headers,
            ).text
        
            elapsed = datetime.datetime.now() - start
            elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'

            if 'This gift has been redeemed already.' in r:
                print(""
                f"\n{Fore.RED}{time} - Nitro is Already Redeemed"+Fore.RESET)
                NitroInfo(elapsed, code)
            elif 'subscription_plan' in r:
                print(""
                f"\n{Fore.GREEN}{time} - Nitro Successfuly Claimed!"+Fore.RESET)
                NitroInfo(elapsed, code)
                if notification == True:
                    toaster.show_toast("Sniper",
                    "Nitro Claimed! Look into console",
                    icon_path="./drop.ico",
                    duration=7)
            elif 'Unknown Gift Code' in r:
                print(""
                f"\n{Fore.YELLOW}{time} - Unknown Nitro Gift Code"+Fore.RESET)
                NitroInfo(elapsed, code)
        else:
            return




    if 'GIVEAWAY' in message.content:
        if giveaway_sniper == True:
            if message.author.id == 294882584201003009:
                try:
                    if edelay == False:
                        await message.add_reaction("🎉")
                except discord.errors.Forbidden:
                    print(""
                    f"\n{Fore.RED}{time} - Couldnt React to Giveaway"+Fore.RESET)
                    GiveawayInfo()            
                if edelay == True:
                    print(""
                    f"\n{Fore.GREEN}{time} - Giveaway Found!"+Fore.RESET)
                    GiveawayDelayInfo()
                else:
                    print(""
                    f"\n{Fore.GREEN}{time} - Giveaway Sniped"+Fore.RESET)
                    GiveawayInfo()
                if notification == True:
                    if edelay == True:
                        toaster.show_toast("Sniper",
                        f"Sniping Giveaway in {delay}s. Look into console",
                        icon_path="./drop.ico",
                        duration=7)
                    else:
                        toaster.show_toast("Sniper",
                        "Giveaway Sniped! Look into console",
                        icon_path="./drop.ico",
                        duration=7)
                try:
                    if edelay == True:
                        sleep(delay)
                        await message.add_reaction("🎉")
                        print("")
                        print(f"{Fore.GREEN}Giveaway Sniped with delay {delay} seconds!")
                except discord.errors.Forbidden:
                    print(""
                    f"\n{Fore.RED}{time} - Couldnt React to Giveaway"+Fore.RESET)
                    GiveawayInfo()   
        else:
            return

    if f'Congratulations <@{Sniper.user.id}>' in message.content:
        if giveaway_sniper == True:
            if message.author.id == 294882584201003009:    
                print(""
                f"\n{Fore.GREEN}{time} - Giveaway Won"+Fore.RESET)
                GiveawayInfo()
                if notification == True:
                    toaster.show_toast("Sniper",
                    "Giveaway Won! Look into console",
                    icon_path="./drop.ico",
                    duration=7)

        else:
            return

    if 'privnote.com' in message.content:
        if privnote_sniper == True:
            start = datetime.datetime.now()
            code = re.search('privnote.com/(.*)', message.content).group(1)
            link = 'https://privnote.com/'+code
            try:
                note_text = pn.read_note(link)
            except Exception as e:
                print(e)    
            with open(f'Privnote/{code}.txt', 'a+') as f:
                print(f"\n{Fore.GREEN}{time} - Privnote Sniped"+Fore.RESET)
                elapsed = datetime.datetime.now() - start
                elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'
                PrivnoteInfo(elapsed, code)
                f.write(note_text)
                if notification == True:
                    toaster.show_toast("Sniper",
                    "Privnote sniped! Look into console",
                    icon_path="./drop.ico",
                    duration=7)
        else:
            return
    await Sniper.process_commands(message)

@Sniper.event
async def on_connect():
    Clear()

    if onalt == False:
        onaltt = " "
    else:
        onaltt = f"{Fore.LIGHTBLACK_EX}({s_name}#{s_tag})"

    if edelay == True:
        ddelay = f"{Fore.LIGHTBLACK_EX}({delay} seconds)"
    else:
        ddelay = " "

    if giveaway_sniper == True:
        giveaway = "Active" 
    else:
        giveaway = "Disabled"

    if nitro_sniper == True:
        nitro = "Active"
    else:
        nitro = "Disabled"

    if notification == True:
        notify = "Active"
    else:
        notify = "Disabled"    
    if privnote_sniper == True:
        privnote = "Active"
    else:
        privnote = "Disabled"  
    
    startprint()
    ctypes.windll.kernel32.SetConsoleTitleW(f'Discord Sniper - User: {Sniper.user.name} - Made by LnX')


Init()