import discord
import asyncio
import random
import json
import time
from datetime import datetime
from discord.ext import tasks

# 🔐 SECURITY SETTINGS - EDIT THESE
YOUR_USER_ID = 123456789012345678  # Replace with your Discord user ID
USER_TOKEN = "YOUR_USER_TOKEN_HERE"  # Replace with your token
COMMAND_PREFIX = "++"

class SimpleSecureSelfBot:
    def __init__(self):
        self.client = discord.Client()
        self.owner_id = YOUR_USER_ID
        self.start_time = time.time()
        
        # 📱 Simple Settings (Easy to edit from Discord)
        self.settings = {
            "auto_reply": True,
            "status_changer": True,
            "afk_mode": False,
            "ghost_detection": True,
            "auto_react": False
        }
        
        # 💬 Auto Reply Messages (Edit these easily)
        self.replies = {
            "hello": ["Hey! 👋", "Hello there! 😊", "Hi! 🎉"],
            "how are you": ["I'm good! 😄", "Great! ⭐", "Doing well! 💪"],
            "thanks": ["Welcome! 😊", "No problem! 👍", "Anytime! 💯"]
        }
        
        # 🎭 Status Messages (Rotates every 5 minutes)
        self.statuses = [
            "🤖 Online 24/7",
            "💬 ++menu for options",
            "👀 Watching chat",
            "⚡ Ready to help"
        ]
        
        # 😊 React Emojis
        self.react_emojis = ["👍", "❤️", "😂", "🔥"]
        
        # 💾 Data Storage
        self.deleted_messages = []
        self.afk_message = "I'm AFK right now!"
        
        self.setup_events()

    def is_owner(self, user_id):
        """Check if user is the bot owner"""
        return user_id == self.owner_id

    def setup_events(self):
        @self.client.event
        async def on_ready():
            print(f"✅ Logged in as {self.client.user}")
            print(f"🔐 Only {self.client.get_user(self.owner_id)} can use commands")
            print(f"💬 Type {COMMAND_PREFIX}menu to start")
            
            if self.settings["status_changer"]:
                self.change_status.start()
                
        @self.client.event
        async def on_message(self, message):
            # Only respond to owner's commands
            if message.author.id == self.owner_id and message.content.startswith(COMMAND_PREFIX):
                await self.handle_command(message)
                return
                
            # Don't respond to own messages
            if message.author == self.client.user:
                return
                
            # Auto reply when mentioned
            if (self.settings["auto_reply"] and 
                self.client.user in message.mentions):
                await self.auto_reply(message)
                
            # Auto react (random chance)
            if (self.settings["auto_react"] and 
                random.random() < 0.1):  # 10% chance
                emoji = random.choice(self.react_emojis)
                try:
                    await message.add_reaction(emoji)
                except:
                    pass
                    
        @self.client.event
        async def on_message_delete(self, message):
            if self.settings["ghost_detection"]:
                # Store deleted message info
                if len(self.deleted_messages) >= 50:
                    self.deleted_messages.pop(0)  # Keep only last 50
                    
                self.deleted_messages.append({
                    "author": str(message.author),
                    "content": message.content[:100],
                    "channel": str(message.channel),
                    "time": datetime.now().strftime("%H:%M")
                })

    async def auto_reply(self, message):
        """Send automatic replies"""
        if self.settings["afk_mode"]:
            await asyncio.sleep(2)
            await message.reply(f"{self.afk_message} 😴")
            return
            
        # Check for triggers
        content = message.content.lower()
        for trigger, responses in self.replies.items():
            if trigger in content:
                response = random.choice(responses)
                await asyncio.sleep(random.uniform(1, 3))
                await message.reply(response)
                break

    async def handle_command(self, message):
        """Handle owner commands"""
        content = message.content[len(COMMAND_PREFIX):].strip()
        
        try:
            if content == "menu":
                await self.show_menu(message)
            elif content == "settings":
                await self.show_settings(message)
            elif content.startswith("toggle "):
                await self.toggle_setting(message, content[7:])
            elif content == "replies":
                await self.show_replies(message)
            elif content.startswith("add "):
                await self.add_reply(message, content[4:])
            elif content.startswith("remove "):
                await self.remove_reply(message, content[7:])
            elif content == "statuses":
                await self.show_statuses(message)
            elif content.startswith("newstatus "):
                await self.add_status(message, content[10:])
            elif content.startswith("afk "):
                await self.set_afk(message, content[4:])
            elif content == "afk":
                await self.toggle_afk(message)
            elif content == "ghost":
                await self.show_ghost(message)
            elif content == "stats":
                await self.show_stats(message)
            elif content == "clear":
                await self.clear_chat(message)
            else:
                await self.show_help(message)
                
        except Exception as e:
            await message.edit(content=f"❌ Error: {str(e)}")
            await asyncio.sleep(5)
            await message.delete()

    async def show_menu(self, message):
        """Show main menu"""
        menu = f"""
🤖 **Simple Self-Bot Menu**

**📱 Quick Commands:**
`{COMMAND_PREFIX}settings` - View/change settings
`{COMMAND_PREFIX}replies` - Edit auto-replies
`{COMMAND_PREFIX}statuses` - Edit status messages
`{COMMAND_PREFIX}afk` - Toggle AFK mode
`{COMMAND_PREFIX}ghost` - See deleted messages
`{COMMAND_PREFIX}stats` - Bot statistics
`{COMMAND_PREFIX}clear` - Clear this chat

**💡 Examples:**
• `{COMMAND_PREFIX}toggle auto_reply` - Turn auto-reply on/off
• `{COMMAND_PREFIX}add hello | Hi there!` - Add new reply
• `{COMMAND_PREFIX}newstatus Playing games` - Add status
• `{COMMAND_PREFIX}afk I'm sleeping` - Set AFK message

Type any command to get started! 🚀
        """
        await message.edit(content=menu)

    async def show_settings(self, message):
        """Show current settings"""
        settings_text = "⚙️ **Current Settings:**\n\n"
        
        for setting, enabled in self.settings.items():
            status = "✅ ON" if enabled else "❌ OFF"
            settings_text += f"• `{setting}`: {status}\n"
            
        settings_text += f"\n💡 Use `{COMMAND_PREFIX}toggle <setting>` to change"
        settings_text += f"\n📱 Use `{COMMAND_PREFIX}menu` to go back"
        
        await message.edit(content=settings_text)

    async def toggle_setting(self, message, setting):
        """Toggle a setting on/off"""
        if setting not in self.settings:
            await message.edit(content=f"❌ Setting '{setting}' not found!\nUse `{COMMAND_PREFIX}settings` to see all settings")
            return
            
        self.settings[setting] = not self.settings[setting]
        status = "✅ ON" if self.settings[setting] else "❌ OFF"
        
        # Handle special cases
        if setting == "status_changer":
            if self.settings[setting] and not self.change_status.is_running():
                self.change_status.start()
            elif not self.settings[setting] and self.change_status.is_running():
                self.change_status.cancel()
                
        await message.edit(content=f"⚙️ `{setting}` is now {status}")
        await asyncio.sleep(3)
        await message.delete()

    async def show_replies(self, message):
        """Show current auto-replies"""
        reply_text = "💬 **Auto-Reply Messages:**\n\n"
        
        for trigger, responses in self.replies.items():
            reply_text += f"**{trigger}:**\n"
            for i, response in enumerate(responses, 1):
                reply_text += f"  {i}. {response}\n"
            reply_text += "\n"
            
        reply_text += f"💡 **Add new:** `{COMMAND_PREFIX}add hello | Hi friend!`\n"
        reply_text += f"🗑️ **Remove:** `{COMMAND_PREFIX}remove hello`"
        
        await message.edit(content=reply_text[:2000])

    async def add_reply(self, message, text):
        """Add new auto-reply"""
        if " | " not in text:
            await message.edit(content=f"❌ Format: `{COMMAND_PREFIX}add trigger | response`\nExample: `{COMMAND_PREFIX}add hello | Hi there!`")
            return
            
        parts = text.split(" | ", 1)
        trigger = parts[0].strip().lower()
        response = parts[1].strip()
        
        if trigger not in self.replies:
            self.replies[trigger] = []
            
        self.replies[trigger].append(response)
        
        await message.edit(content=f"✅ Added reply for '{trigger}':\n💬 {response}")
        await asyncio.sleep(5)
        await message.delete()

    async def remove_reply(self, message, trigger):
        """Remove auto-reply trigger"""
        trigger = trigger.lower()
        if trigger in self.replies:
            del self.replies[trigger]
            await message.edit(content=f"🗑️ Removed all replies for '{trigger}'")
        else:
            await message.edit(content=f"❌ No replies found for '{trigger}'")
        await asyncio.sleep(3)
        await message.delete()

    async def show_statuses(self, message):
        """Show current status messages"""
        status_text = "🎭 **Status Messages:**\n\n"
        
        for i, status in enumerate(self.statuses, 1):
            status_text += f"{i}. {status}\n"
            
        status_text += f"\n💡 **Add new:** `{COMMAND_PREFIX}newstatus Your message here`"
        
        await message.edit(content=status_text)

    async def add_status(self, message, status_text):
        """Add new status message"""
        self.statuses.append(status_text)
        await message.edit(content=f"✅ Added new status: {status_text}")
        await asyncio.sleep(3)
        await message.delete()

    async def set_afk(self, message, afk_text):
        """Set AFK message"""
        self.afk_message = afk_text
        self.settings["afk_mode"] = True
        await message.edit(content=f"😴 AFK mode ON\n💬 Message: {afk_text}")
        await asyncio.sleep(3)
        await message.delete()

    async def toggle_afk(self, message):
        """Toggle AFK mode"""
        self.settings["afk_mode"] = not self.settings["afk_mode"]
        if self.settings["afk_mode"]:
            await message.edit(content=f"😴 AFK mode ON\n💬 Message: {self.afk_message}")
        else:
            await message.edit(content="👋 AFK mode OFF - Welcome back!")
        await asyncio.sleep(3)
        await message.delete()

    async def show_ghost(self, message):
        """Show recently deleted messages"""
        if not self.deleted_messages:
            await message.edit(content="👻 No deleted messages recorded yet!")
            return
            
        ghost_text = "👻 **Recently Deleted Messages:**\n\n"
        for msg in self.deleted_messages[-10:]:
            ghost_text += f"**{msg['author']}** at {msg['time']}: {msg['content']}\n"
            
        await message.edit(content=ghost_text[:2000])

    async def show_stats(self, message):
        """Show bot statistics"""
        uptime = time.time() - self.start_time
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        
        stats = f"""
📊 **Bot Statistics**

⏰ **Uptime:** {hours}h {minutes}m
🌐 **Servers:** {len(self.client.guilds)}
💬 **Auto-Replies:** {len(self.replies)}
🎭 **Statuses:** {len(self.statuses)}
🗑️ **Deleted Messages:** {len(self.deleted_messages)}
⚙️ **Active Features:** {sum(self.settings.values())}/{len(self.settings)}
        """
        
        await message.edit(content=stats)

    async def clear_chat(self, message):
        """Clear recent messages in chat"""
        deleted = 0
        async for msg in message.channel.history(limit=50):
            if msg.author == self.client.user:
                try:
                    await msg.delete()
                    deleted += 1
                    await asyncio.sleep(0.5)
                except:
                    pass
                    
        temp = await message.channel.send(f"🧹 Cleared {deleted} messages!")
        await asyncio.sleep(3)
        await temp.delete()

    async def show_help(self, message):
        """Show help for unknown commands"""
        help_text = f"""
❓ **Unknown command!**

Type `{COMMAND_PREFIX}menu` to see all available commands.

**Quick help:**
• `{COMMAND_PREFIX}settings` - Change bot settings
• `{COMMAND_PREFIX}replies` - Edit auto-replies  
• `{COMMAND_PREFIX}afk` - Toggle AFK mode
• `{COMMAND_PREFIX}stats` - View statistics
        """
        await message.edit(content=help_text)

    @tasks.loop(minutes=5)
    async def change_status(self, message=None):
        """Change status every 5 minutes"""
        if not self.settings["status_changer"] or not self.statuses:
            return
            
        status_text = random.choice(self.statuses)
        activity = discord.Game(name=status_text)
        
        try:
            await self.client.change_presence(
                status=discord.Status.online,
                activity=activity
            )
        except:
            pass

    def run(self):
        """Start the bot"""
        print("🤖 Starting Simple Secure Self-Bot...")
        print("⚠️  WARNING: Self-bots violate Discord ToS!")
        print(f"🔐 Only user ID {YOUR_USER_ID} can use commands")
        
        if USER_TOKEN == "YOUR_USER_TOKEN_HERE":
            print("❌ Please set your USER_TOKEN!")
            return
            
        if YOUR_USER_ID == 123456789012345678:
            print("❌ Please set your YOUR_USER_ID!")
            return
            
        try:
            self.client.run(USER_TOKEN, bot=False)
        except Exception as e:
            print(f"❌ Error: {e}")

# 🚀 Run the bot
if __name__ == "__main__":
    bot = SimpleSecureSelfBot()
    bot.run()
                
