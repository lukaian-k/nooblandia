import discord


async def ready(client):
    activity = discord.Game(name='Minecraft', type=3)

    await client.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    print(f'Init: {client.user.name}')
    print(f'Bot ID: {client.user.id}')
    print(f'Ping: {round (client.latency*1000)}')
