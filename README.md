# Discord Voice Channel Selfbot

Maintains 24/7 connection to a Discord voice channel on Android (Termux).

**Note:** This violates Discord's Terms of Service. Use at your own risk.

## Setup

1. **Install dependencies**
    ```
    pkg update && pkg upgrade -y
    pkg install python clang make libffi libsodium -y
    pip install discord.py-self
    SODIUM_INSTALL=system pip install pynacl
    ```

2. **Configure the bot**
    - Create `vc_selfbot.py` with your selfbot code
    - Edit these variables:
      ```
      USER_TOKEN = "your_discord_token"
      GUILD_ID = 123456789012345678
      CHANNEL_ID = 123456789012345678
      ```

3. **Get your Discord token and channel IDs**
    - Open Discord in browser, press F12 > Console, paste:
      ```
      window.webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]);m.find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
      ```
    - Enable Developer Mode in Discord settings to copy server/channel IDs

## Usage

- Start manually:
    ```
    python vc_selfbot.py
    ```
- Run in background:
    ```
    nohup python vc_selfbot.py > selfbot.log 2>&1 &
    ```
- Check if running:
    ```
    ps aux | grep vc_selfbot
    ```
- View logs:
    ```
    tail -f selfbot.log
    ```

## 24/7 Auto-Start

1. **Install Termux:Boot app** (F-Droid or Google Play)
2. **Create auto-start script**
    ```
    mkdir -p ~/.termux/boot
    cat > ~/.termux/boot/start_selfbot.sh << 'EOF'
    #!/data/data/com.termux/files/usr/bin/bash
    cd /data/data/com.termux/files/home
    if pgrep -f vc_selfbot.py >/dev/null; then exit 0; fi
    nohup python vc_selfbot.py >> selfbot.log 2>&1 &
    EOF
    chmod +x ~/.termux/boot/start_selfbot.sh
    ```

## Tips

- Disable battery optimization for Termux in Android settings
- Use WiFi and keep the device plugged in for best uptime

## Disclaimer

For educational use only. Using selfbots is against Discord's Terms; your account may be banned.

## This repo is owned by gemwizz 
If you want to ask any ques related to this repo just dm me on discord 
