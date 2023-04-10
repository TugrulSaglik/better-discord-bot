import discord
import bot_data

def run_discord_bot():
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    
    
    #The following function censors specific embeds and attachments in a message using the outlawed_videos in bot_data.py
    async def censor_function(message):
        for name in bot_data.outlawed_videos:
            if name in message.content or message.content.endswith(name):
                await message.delete()
                await message.channel.send(f"<@{message.author.id}>, bu medyayı Çomartern İmparatorluğunda paylaşmak bir suçtur, ve sözdeki medya silinmiştir. Lütfen bu davranışı tekrarlamayınız.")
    
            # check message attachments for banned words
            for attachment in message.attachments:
                for name in bot_data.outlawed_videos:
                    if attachment.filename.endswith(name) or attachment.url.endswith(name) or attachment.proxy_url.endswith(name) or attachment.url == name or name in attachment.url or name in attachment.proxy_url:
                        await message.delete()
                        await message.channel.send(f"<@{message.author.id}>, bu medyayı Çomartern İmparatorluğunda paylaşmak bir suçtur, ve sözdeki medya silinmiştir. Lütfen bu davranışı tekrarlamayınız.")

            # check message embeds for banned words
            for name in bot_data.outlawed_videos:
                for embed in message.embeds:
                    try:
                        if embed and (name in embed.title or name in str(embed.description)):
                            await message.delete()
                            await message.channel.send(f"<@{message.author.id}>, bu medyayı Çomartern İmparatorluğunda paylaşmak bir suçtur, ve sözdeki medya silinmiştir. Lütfen bu davranışı tekrarlamayınız.")
                    except TypeError:
                        pass
    
    #The following function uses censor_function() to delete an arbitrary amount of messages in channels listed in channel_list in bot_data.py
    async def history_checker():
        
        for chan in bot_data.channel_list:
            channel = client.get_channel(chan)
            message_count = 0
            async for message in channel.history(limit=1000):
                await censor_function(message)
                message_count += 1
            print(f"{message_count} messages checked in {channel.name}")

    #Runs certain things when the bot initializes
    @client.event
    async def on_ready():
        
        print(f'{client.user} is now running!')

        game = discord.Game("İmparator Ozan çok yaşa!")
        
        await client.change_presence(status=discord.Status.online, activity = game)

        await history_checker()

    #Runs certain things when the bot sees a new message
    @client.event
    async def on_message(message):

        
        if message.author.id == 1088115533444026378:
            return            
        
        await censor_function(message)

    #Runs certain things when the bot sees a new edited message
    @client.event
    async def on_message_edit(before, after):
        
        await censor_function(after)


    client.run("MTA4ODExNTUzMzQ0NDAyNjM3OA.GJioRe.P9Q4F9JGXgYW3P4T5uIw0MEcNzJH9s7jVy0pZc")