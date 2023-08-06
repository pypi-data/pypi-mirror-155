import aiohttp
from click import command
import asyncio
import json
import os
import time
import datetime
from os import path

os.system('pip install -U fortnitepy')

import fortnitepy

os.system('pip install -U BenBotAsync')

import BenBotAsync

email = input("Email: ")
password = input("Password: ")
owner = input("Owner: ")

hours = 0
filename = "device_auths.json"

banned_users = []

def get_device_auth_details():
        with open(filename, 'r') as fp:
            return json.load(fp)
        return {}


def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)

def to_dict(self):
    data = {'appInstalled': 'init'}
    if self.asset:
        data['avatar'] = self.asset.lower()

class DuplicateFriendship():
    pass

class Forbidden():
    pass

class NotOwner():
    pass


class MyClient(fortnitepy.Client):
    def __init__(self):
        device_auth_details = get_device_auth_details().get(email, {})
        super().__init__(
            auth=fortnitepy.AdvancedAuth(
                email=email,
                password=password,
                prompt_authorization_code=True,
                prompt_code_if_invalid=True,
                delete_existing_device_auths=True,
                **device_auth_details
            )
        )
        self.session_event = asyncio.Event()



    async def event_device_auth_generate(self, details, email):
        store_device_auth_details(email, details)

    async def event_ready(self):
        sp = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name= "Raider's Revenge", backendType="AthenaPickaxe")
        sb =await BenBotAsync.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name="Galactic Disc", backendType="AthenaBackpack")
        print('\033[1;37;49m Client is ready as: ' + '\033[1;34;49m {0.user.display_name}'.format(self))
        self.session = aiohttp.ClientSession()
        self.session_event.set()
        await self.set_presence("Lobbybot coded by Zockerwolf76")
        self.party.update_presence()
        await self.party.me.set_outfit(asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG')
        await self.party.me.set_pickaxe(asset=sp.id)
        await self.party.me.set_backpack(asset=sb.id)
        await self.party.me.set_banner(icon = "OT11Banner", color="defaultcolor22", season_level="9999")
        try:
            for friend in self.friends:
                await self.party.invite(friend.id)
        except fortnitepy.Forbidden:
            pass
        except fortnitepy.PartyError:
            pass
        my_file = "friendlist.txt"
        if path.exists(my_file):
            with open(my_file, 'r') as fp:
                lines = fp.readlines()
            with open(my_file ,"w", encoding="utf-8") as f:
                if lines.strip("\n") == "a":
                    for friend in self.friends:
                        f.write(f"{friend.display_name} + ({friend.id})\n")


    async def event_friend_request(self, IncommingPendingFriend):
            await IncommingPendingFriend.accept()
            d = datetime.datetime.now()
            print("\033[1;37;49m User: " + f"\033[1;34;49m {IncommingPendingFriend.display_name} " + "\033[1;37;49m Action:" + "\033[1;32;49m friend request (accept) " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

    async def event_party_invite(self, ReceivedPartyInvitation):
        if (ReceivedPartyInvitation.sender.display_name) == owner:
            hello = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", matchMethod="full", name= "Wave", asset = "EID_Wave", backendType="AthenaDance")
            sp = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name= "Raider's Revenge", backendType="AthenaPickaxe")
            sb =await BenBotAsync.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name="Galactic Disc", backendType="AthenaBackpack")
            await ReceivedPartyInvitation.accept()
            await self.party.me.set_outfit(asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG')
            await self.party.me.set_pickaxe(asset=sp.id)
            await self.party.me.set_backpack(asset=sb.id)
            await self.party.me.set_emote(asset=hello.id)
            await self.party.me.set_banner(icon = "OT11Banner", color="defaultcolor22", season_level="9999")
            await self.party.send("Hello " + owner + "! Thanks for the invite. :)")


    async def event_party_member_join(self, member):
        try:
            if (member.display_name) == "{0.user.display_name}".format(self):
                return
            else:
                member.add()
        except fortnitepy.DuplicateFriendship:
            return
        except fortnitepy.Forbidden:
            return
            
    async def event_party_member_join(self, member):
        if (member.display_name) == "{0.user.display_name}".format(self):
            return
        
        else:
            d = datetime.datetime.now()
            print("\033[1;37;49m User: " + f"\033[1;34;49m {member.display_name} ({member.id}) " + "\033[1;37;49m Action:" + "\033[1;32;49m joined " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            await self.party.send("Hey " + member.display_name + "! If you need help... please join our discord server: https://dsc.gg/zockerwolf or use my !help command")

        
    async def event_party_member_leave(self, member):
            if (member.display_name) == "{0.user.display_name}".format(self):
                return
            else:
                d = datetime.datetime.now()
                print("\033[1;37;49m User: " + f"\033[1;34;49m {member.display_name} " + "\033[1;37;49m Action:" + "\033[1;31;49m leaved " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  +  "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

         
    async def event_party_message(self, message):
        await self.session_event.wait()
        split = message.content.split()
        command = split[0].lower()
        args = split[1:]
        content = ' '.join(args)

        
        if command == '!skin':
            try: 
                skin = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name=content, backendType="AthenaCharacter")
                await self.party.me.set_outfit(asset=skin.id)
                await message.reply("Set skin to " + skin.name + "!")
                d = datetime.datetime.now()
                print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m {skin.name} ({skin.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f"Failed to find a skin with the name: {content}.")
                d = datetime.datetime.now()
                print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;31;49m {content} " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
    
            
        elif command == '!emote':
            try:
                emote = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name=content, backendType="AthenaDance")
                await self.party.me.set_emote(asset=emote.id)
                await message.reply("Set emote to " + emote.name + "!")
                d = datetime.datetime.now()
                print ("\033[1;37;49m Type: " + "\033[1;36;49m Emote " + "\033[1;37;49m Name: " + f"\033[1;32;49m {emote.name} ({emote.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f"Failed to find a emote with the name: {content}.")
                d = datetime.datetime.now()
                print ("\033[1;37;49m Type: " + "\033[1;36;49m Emote " + "\033[1;37;49m Name: " + f"\033[1;31;49m {content} " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))


        elif command == '!pickaxe':
            try:
                pa = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name=content, backendType="AthenaPickaxe")
                await self.party.me.set_pickaxe(asset = pa.id)
                await message.reply("Set pickaxe to " + pa.name + "!")
                time.sleep(2)
                d = datetime.datetime.now()
                print ("\033[1;37;49m Type: " + "\033[1;36;49m Pickaxe " + "\033[1;37;49m Name: " + f"\033[1;32;49m {pa.name} ({pa.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f"Failed to find a pickaxe with the name: {content}.")
                d = datetime.datetime.now()
                print ("\033[1;37;49m Type: " + "\033[1;36;49m Pickaxe " + "\033[1;37;49m Name: " + f"\033[1;31;49m {content} " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

            
        elif command == '!backpack':
            try:
                bp = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name=content, backendType="AthenaBackpack")
                await self.party.me.set_backpack(asset=bp.id)
                await message.reply("Set backpack to " + bp.name + "!")
                d = datetime.datetime.now()
                print ("\033[1;37;49m Type: " + "\033[1;30;49m Backpack " + "\033[1;37;49m Name: " + f"\033[1;32;49m {bp.name} ({bp.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f"Failed to find a backpack with the name: {content}.")
                d = datetime.datetime.now()
                print ("\033[1;37;49m Type: " + "\033[1;30;49m Backpack " + "\033[1;37;49m Name: " + f"\033[1;31;49m {content} " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

        elif command == '!emoji':
            try:
                emoji = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", matchMethod="contains", name=content, backendType="AthenaEmoji")
                await self.party.me.set_emoji(asset=emoji.id)
                await message.reply("Set emoticon to " + emoji.name + "!")
                d = datetime.datetime.now()
                print ("\033[1;37;49m Type: " + "\033[1;33;49m Emoji " + "\033[1;37;49m Name: " + f"\033[1;32;49m {emoji.name} ({emoji.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f"Failed to find a emoji with the name: {content}.")
                d = datetime.datetime.now()
                print("\033[1;37;49m Type: " + "\033[1;33;49m Emoji " + "\033[1;37;49m Name: " + f"\033[1;31;49m {content} " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

        
        elif command == "!floss":
            floss = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", name = "Floss" , WID = "WID_Floss")
            await self.party.me.set_emote(asset=floss.id)
            await message.reply("Set emote to floss!")
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;36;49m Emote " + "\033[1;37;49m Name: " + f"\033[1;32;49m {floss.name} ({floss.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            
        elif command == "!pinkghoul":
            pg = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", asset='CID_029_Athena_Commando_F_Halloween', name = "Ghoul Trooper")
            pink = self.party.me.create_variants(material=3)
            await self.party.me.set_outfit(asset=pg.id, variants = pink)
            await message.reply('Skin set to Pink Ghoul Trooper!')
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m {pg.name} ({pg.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            
        elif command == "!checkeredrenegade":
            cr = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", asset='CID_028_Athena_Commando_F', name = "Renegade Raider")
            c = self.party.me.create_variants(material=2)
            await self.party.me.set_outfit(asset=cr.id, variants = c)
            await message.reply('Skin set to Checkered Renegade!')
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m {cr.name} ({cr.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

        elif command == "!galaxy":
            g = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", asset='CID_175_Athena_Commando_M_Celestial', name = "Galaxy")
            await self.party.me.set_outfit(asset=g.id)
            await message.reply('Skin set to Galaxy!')
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m {g.name} ({g.id}) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            
        elif command == "!purpleskull":
            skin_variants = self.party.me.create_variants(clothing_color=1)
            await self.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=skin_variants)
            await message.reply('Skin set to Purple Skull Trooper!')
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m Skull Trooper (CID_030_Athena_Commando_M_Halloween) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

        elif command == "!hologram":
            await self.party.me.set_outfit(asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG')
            await message.reply('Skin set to Star Wars Hologram!')
            d = datetime.datetime.now()
            print ("\033[1;37;49m Type: " + "\033[1;35;49m Skin " + "\033[1;37;49m Name: " + f"\033[1;32;49m Star Wars Hologram (CID_VIP_Athena_Commando_M_GalileoGondola_SG) " + " \033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        
        elif command == "!leave":
            if (message.author.display_name) == owner:  
                bye = await BenBotAsync.get_cosmetic(lang="en", searchLang="en", name = "salute") 
                await self.party.me.set_emote(asset=bye.id)
                await message.reply("Bye!")
                time.sleep(3)
                await self.party.me.leave()
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)")
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m TRIED Owner command:" + f"\033[1;31;49m !leave " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            

        elif command == "!promote":
            if (message.author.display_name) == owner:
                    user = await self.fetch_user(message.author.display_name)
                    member = self.party.get_member(user.id)
                    await member.promote()
                    await message.reply("Promoted Member: " + message.author.display_name)
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)")  
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m TRIED Owner command:" + f"\033[1;31;49m !promote " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            

        elif command == "!cban":
            if (message.author.display_name) == owner:
                user = await self.fetch_user(content)
                member = self.party.get_member(user.id)
                await self.party.chatban_member(user.id)
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)") 
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;31;49m TRIED Owner command:" + f"\033[1;32;49m !cban " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        
        
        elif command == "!sitout":
            if (message.author.display_name) == owner:
                await self.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)") 
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;31;49m TRIED Owner command:" + f"\033[1;32;49m !sitout " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            

        elif command == "!sitin":
            if (message.author.display_name) == owner:
                await self.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)") 
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;31;49m TRIED Owner command:" + f"\033[1;32;49m !sitin " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
             

        elif command == "!unready":
            if (message.author.display_name) == owner:
                await self.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)") 
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;31;49m TRIED Owner command:" + f"\033[1;32;49m !unready " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
             

        elif command == "!ready":
            if (message.author.display_name) == owner:
                await self.party.me.set_ready(fortnitepy.ReadyState.READY)
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)") 
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;31;49m TRIED Owner command:" + f"\033[1;32;49m !ready " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
            

        elif command == "!match":
            if (message.author.display_name) == owner:
                d = datetime.datetime.now()
                await self.party.me.set_in_match(players_left=1, started_at=None)
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)") 
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;31;49m TRIED Owner command: " + f"\033[1;32;49m !match " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
             

        elif command == "!lobby":
            if (message.author.display_name) == owner:
                d = datetime.datetime.now()
                await self.party.me.clear_in_match()
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)") 
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;31;49m TRIED Owner command: " + f"\033[1;32;49m !lobby " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

        elif command == "!banner":
            if (message.author.display_name) == owner:
                d = datetime.datetime.now()
                await self.party.me.set_banner(icon=content)
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)") 
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;31;49m TRIED Owner command: " + f"\033[1;32;49m !banner " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))


        elif command == "!level":
            if (message.author.display_name) == owner:
                d = datetime.datetime.now()
                await self.party.me.set_banner(season_level=content)
            else:
                d = datetime.datetime.now()
                await message.reply(f"{owner} is my owner, not you! :)") 
                print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;31;49m TRIED Owner command: " + f"\033[1;32;49m !level " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))

        elif command == "!help":
            await message.reply("---------------Commands 1/1---------------\n"+"- !skin (name)  /  equip (name) skin\n"+"- !emote (name)  /  equip (name) emote\n"+"- !backpack (name)  /  equip (name) backpack\n"+"- !pickaxe (name)  /  equip (name) pickaxe\n"+"- !emoji (name)  /  equip (name) emoji\n"+"- !galaxy  /  Galaxy Skin\n"+"- !purpleskull  /  Skull Trooper (purple)\n"+"- !pinkghoul  /  Ghoul Trooper (pink)\n"+"- !checkeredrenegade  /  Renegade Raider (checkered)\n"+"- !floss  /  Floss emote\n"+"- !hologram  /  Star Wars hologram\n"+"- !friends  /  list of my friends\n"+"- !help  /  List of all commands")
            d = datetime.datetime.now()
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m executed command: " + f"\033[1;32;49m !help " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))
        
        
        elif command == "!friends":
            online = 0
            offline = 0
            for friend in self.friends:
                if friend.is_online():
                    online = online + 1
                else:
                    offline =offline + 1 
            await message.reply(f"Online Friends = {online} / Offline Friends = {offline}")
        
            await message.reply("")
            d = datetime.datetime.now()
            print ("\033[1;37;49m User: " + f"\033[1;34;49m {message.author.display_name} " + "\033[1;37;49m executed command: " + f"\033[1;32;49m !friends " + "\033[1;37;49m Bot:" + "\033[1;34;49m {0.user.display_name}".format(self)  + "\033[1;37;49m  Datetime: " +  "\033[1;33;49m %s/%s/%s" % (d.day, d.month, d.year) + "\033[1;33;49m %s:%s:%s" % (d.hour + hours, d.minute, d.second))


        

                

            


c = MyClient()
c.run()