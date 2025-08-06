```markdown
# 🎵 Discord Voice Channel Selfbot

*Stay connected to your favorite Discord voice channels 24/7*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Android%20(Termux)-green.svg)](https://termux.com)
[![License](https://img.shields.io/badge/License-Educational-red.svg)](#disclaimer)

⚠️ **WARNING: This project violates Discord's Terms of Service. Use at your own risk. Educational purposes only.**

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔄 **24/7 Operation** | Maintains constant voice channel presence |
| 🚀 **Auto-Restart** | Boots automatically and recovers from crashes |
| 🛡️ **Anti-Detection** | Smart delays and rate limiting to avoid Discord detection |
| 📊 **Health Monitoring** | Built-in logging and status checking |
| 📱 **Mobile Optimized** | Designed specifically for Android devices |

---

## 🚀 Quick Setup

### 📋 Prerequisites
- Android device with **Termux** installed
- Discord account and user token
- Stable internet connection (WiFi recommended)

### ⚡ Installation

```
# Install dependencies
pkg update && pkg upgrade -y
pkg install python git clang make pkg-config libffi libsodium -y
pip install discord.py-self
SODIUM_INSTALL=system pip install pynacl
```

### 🔧 Configuration

```
# Create bot file
nano vc_selfbot.py
```

Edit these values in the code:
```
# 🎯 CONFIGURATION
USER_TOKEN = "YOUR_USER_TOKEN_HERE"    # 🔑 Your Discord token
GUILD_ID = 123456789012345678           # 🏠 Server ID  
CHANNEL_ID = 123456789012345678         # 🎤 Voice channel ID
```

---

## 🔑 Getting Required Information

<details>
<summary>🎯 Discord User Token</summary>

1. Open Discord in **browser** (not desktop app)
2. Press **F12** → Console tab
3. Paste and run:
   ```
   window.webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]);m.find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
   ```
4. Copy the returned token

</details>

<details>
<summary>🏠 Server & Channel IDs</summary>

1. Enable **Developer Mode** in Discord Settings → Advanced
2. Right-click server name → **"Copy Server ID"**
3. Right-click voice channel → **"Copy Channel ID"**

</details>

---

## 🏃‍♂️ Running the Bot

### 🧪 Test Run
```
python vc_selfbot.py
```

### 🌙 Background Operation
```
nohup python vc_selfbot.py > selfbot.log 2>&1 &
```

### 📊 Check Status
```
ps aux | grep vc_selfbot    # Check if running
tail -f selfbot.log         # View live logs
```

---

## 🔄 24/7 Auto-Start Setup

### 📱 Install Termux:Boot
Download **Termux:Boot** from F-Droid or Google Play and grant permissions.

### 🚀 Create Boot Script
```
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start_selfbot.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home
if pgrep -f vc_selfbot.py >/dev/null; then exit 0; fi
nohup python vc_selfbot.py >> selfbot.log 2>&1 &
echo "🚀 Selfbot started $(date)" >> selfbot.log
EOF
chmod +x ~/.termux/boot/start_selfbot.sh
```

### ⚙️ Android Optimization
- **Disable battery optimization** for Termux in Android settings
- Use **stable WiFi** connection
- Keep device **plugged in** when possible

---

## 🔍 Monitoring

### 🩺 Quick Health Check
```
cat > check.sh << 'EOF'
echo "🔍 Selfbot Status Check"
if pgrep -f vc_selfbot.py >/dev/null; then
    echo "✅ Status: RUNNING"
    echo "⏱️  Uptime: $(ps -o etime= -p $(pgrep -f vc_selfbot) 2>/dev/null)"
else
    echo "❌ Status: NOT RUNNING"
    echo "🔄 Restarting..."
    ~/.termux/boot/start_selfbot.sh
fi
EOF
chmod +x check.sh && ./check.sh
```

### 📈 Monitor Commands
```
tail -f selfbot.log                           # 📺 Live logs
grep "Joined voice channel" selfbot.log      # ✅ Successful joins
grep "ERROR\|4006" selfbot.log | tail -5     # ⚠️  Recent errors
> selfbot.log                                # 🗑️  Clear logs
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| 🚫 `IndentationError` | Use consistent 4-space indentation |
| 🔧 `PyNaCl failed` | Run: `pkg install clang make libsodium` |
| ⚡ `4006 errors` | Bot handles automatically with backoff |
| 🔄 `Keeps disconnecting` | Check WiFi stability |
| 🚀 `Won't start on boot` | Install Termux:Boot app |

### 📊 Healthy vs Warning Signs

**✅ Healthy Operation:**
```
✅ Logged in as YourUser
🔄 Starting keep-alive loop...
🎵 Joined voice channel: General
```

**⚠️ Warning Signs:**
```
❌ Multiple 4006 errors
❌ Login failures  
❌ Guild/channel not found
```

---

## 🛡️ Security & Safety

- 🔐 **Never share your Discord token** - treat it like a password
- 👤 **Use a dedicated account** if possible
- 👁️ **Monitor for unusual activity** - Discord may detect selfbot usage
- 🤐 **Keep it private** - don't advertise automation usage

---

## ⚖️ Legal Disclaimer

<div align="center">

⚠️ **IMPORTANT NOTICE** ⚠️

This project **violates Discord's Terms of Service**  
Your account **may be suspended or banned**  
Use **at your own risk** for **educational purposes only**

**The authors are not responsible for any consequences**

</div>

---

<div align="center">

### 🌟 Educational Project • Use Responsibly • Respect Platform Rules 🌟

Made with ❤️ by Gem for learning automation concepts

</div>
```

This README includes:
- 🎨 Beautiful visual design with badges and emojis
- 📱 Mobile-friendly formatting
- 🔧 Complete setup instructions
- 🚀 One-line installation commands
- 📊 Monitoring and troubleshooting sections
- ⚖️ Clear legal disclaimers
- 🎯 Organized with collapsible sections

Copy and paste this directly into your GitHub repository!

