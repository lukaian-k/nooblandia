import discord


async def ready(client):
    activity = {
        "game": discord.Game(name='Minecraft', type=3),
        "listening": discord.Activity(type=discord.ActivityType.listening, name="Here Always (SEUNGMIN of Stray Kids)"),
    }

    await client.change_presence(
        status=discord.Status.online,
        activity=activity["listening"]
    )

    print(f'Init: {client.user.name}')
    print(f'Bot ID: {client.user.id}')
    print(f'Ping: {round (client.latency*1000)}')
