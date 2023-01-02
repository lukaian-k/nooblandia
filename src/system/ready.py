import discord


async def ready(client):
    activity = {
        "game": discord.Game(
            name='Minecraft',
            type=3
        ),

        "listening": discord.Activity(
            type=discord.ActivityType.listening,
            name="Here Always (SEUNGMIN of Stray Kids)"
        ),

        "streaming": discord.Streaming(
            name='Minecraft com Mod!',
            game='Minecraft',

            platform='Twitch',
            twitch_name='rahnoob',
            url='https://www.twitch.tv/rahnoob',

            assets={
                "large_image": 'assets/img/large_image',
                "large_text": 'Olá! Venha conhecer meu canal na Twitch!',

                "small_image": 'assets/img/small_image',
                "small_text": 'Oii! Como que cê ta?!',
            }
        ),
    }

    await client.change_presence(
        status=discord.Status.online,
        activity=activity["streaming"]
    )

    print(f'Init: {client.user.name}')
    print(f'Bot ID: {client.user.id}')
    print(f'Ping: {round (client.latency*1000)}')
