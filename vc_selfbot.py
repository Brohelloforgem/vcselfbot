#!/usr/bin/env python3
import discord, asyncio, logging

# ─── CONFIG ──────────────────────────────────────────────────────────────
USER_TOKEN  = "YOUR_USER_TOKEN"
GUILD_ID    = 123456789012345678
CHANNEL_ID  = 123456789012345678

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

class VoiceChannelSelfbot:
    def __init__(self, token: str, guild_id: int, channel_id: int):
        self.token      = token
        self.guild_id   = guild_id
        self.channel_id = channel_id

        # exactly 8 spaces from the margin (inside __init__)
        self.client = discord.Client(
            self_bot=True,
            chunk_guilds_at_startup=False,
            member_cache_flags=discord.MemberCacheFlags.none()
        )

        # still inside __init__
        self.client.event(self.on_ready)
        self.client.event(self.on_voice_state_update)

    # 4 spaces from left margin (class level)
    async def on_ready(self):
        logger.info(f"Logged in as {self.client.user}")
        asyncio.create_task(self.keep_alive_loop())

    async def on_voice_state_update(self, member, before, after):
        if member.id == self.client.user.id and after.channel is None:
            logger.warning("Disconnected, reconnecting…")
            await asyncio.sleep(5)
            await self.join_voice_channel()

    async def join_voice_channel(self):
        # 8 spaces inside method
        try:
            guild = self.client.get_guild(self.guild_id)
            if guild is None:
                logger.error(f"Guild {self.guild_id} not found")
                return False
            channel = guild.get_channel(self.channel_id)
            if channel is None or channel.type != discord.ChannelType.voice:
                logger.error(f"Voice channel {self.channel_id} not found")
                return False

            for vc in self.client.voice_clients:
                if vc.channel.id == self.channel_id:
                    return True          # already connected
                await vc.disconnect()

            await channel.connect(reconnect=True)
            logger.info(f"✅ Joined VC: {channel.name}")
            return True

        except Exception as e:
            logger.error(f"Join error: {e}")
            return False

    async def keep_alive_loop(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            if not any(vc.channel.id == self.channel_id
                       for vc in self.client.voice_clients):
                await self.join_voice_channel()
            await asyncio.sleep(30)

    def run(self):
        self.client.run(self.token)


if __name__ == "__main__":
    if "YOUR_USER_TOKEN" in USER_TOKEN:
        print("❌  Put your real token in USER_TOKEN"); exit(1)
    bot = VoiceChannelSelfbot(USER_TOKEN, GUILD_ID, CHANNEL_ID)
    bot.run()
    
