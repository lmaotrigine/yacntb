# YACNTB

<p align="left">
<a href="https://github.com/darthshittious/yacntb/issues"><img src="https://img.shields.io/github/issues/darthshittious/yacntb" alt="Open Issues"></a> 
<a href="https://github.com/darthshittious/yacntb/network/members"><img src="https://img.shields.io/github/forks/darthshittious/yacntb" alt="Repo Forks"></a> 
<a href="https://github.com/darthshittious/yacntb/stargazers"><img src="https://img.shields.io/github/stars/darthshittious/yacntb" alt="Repo Stargazers"></a>
<a href="https://github.com/darthshittious/yacntb/blob/main/LICENSE"><img src="https://img.shields.io/github/license/darthshittious/yacntb" alt="Repo License"></a>
</p>

Yet another CoWIN notification Twitter bot.

## Features

- Find any open slots in any district and tweet important info
- Updates every 4 hours

## Running

1. Run these or equivalents in your terminal

```zsh
git clone https://github.com/darthshittious/yacntb.git
cd yacntb
###
# Optional
python3.9 -m venv venv
source venv/bin/activate
###
pip install -U -r requirements.txt
cp config.example.py config.py
```

2. Update `config.py` with your Twitter API credentials
3. Start the script with `./main.py` or `python3 main.py` or equivalent.

## Deploying

CoWIN APIs are geo-fenced, so you can't deploy on servers outside the country without implementing some kind of proxy.

## Contributing

PRs are welcome. For major changes start a discussion or open an issue first to discuss changes.

## License

[AGPL v3 © Varun J](https://github.com/darthshittious/yacntb/blob/main/LICENSE)

## Support 

Please star to show support, and share this project with your friends 💙

<a href="https://www.buymeacoffee.com/darthshittious" target="_blank">
<img src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png" alt="Buy me a coffee" data-canonical-src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png" width="270" />
</a>

---
Made with ❤️ and [![](https://api.iconify.design/simple-icons:python.svg?color=%234cacfc&height=16)](https://python.org/)
