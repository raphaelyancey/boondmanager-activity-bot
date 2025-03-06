# BoondManager Activity Bot

Working boilerplate to automatically fill activity on BoondManager. Tweak to your liking.

## Install

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then create these two files

`~/.config/systemd/user/boondmanager-activity-bot.timer`
```ini
[Unit]
Description=Run boondmanager-activity-bot.service

[Timer]
OnCalendar=Fri *-*-1..7 11:30:00
Persistent=true

[Install]
WantedBy=timers.target
```

`~/.config/systemd/user/boondmanager-activity-bot.service`
```ini
[Unit]
Description=BoondManager Activity Bot
After=network.target

[Service]
ExecStart=bash -c "zenity --question --text=\"Time to fill the BoondManager activity 🔫\" && /path/to/boondmanager-activity-bot/venv/bin/python /path/to/boondmanager-activity-bot/main.py"
Environment="BOOND_PASSWORD=password"
Environment="BOOND_LOGIN=your@email.com"
Restart=no
```

Replace
- `/path/to/boondmanager-activity-bot` with the actual path of the cloned repo
- `password` with your BoondManager password
- `your@email.com` with your BoondManager login
- `Fri *-*-1..7 11:30:00` with another systemd interval if needed (defaults to first Friday of the month at 11.30am)

And load the service & timer
```bash
systemctl --user daemon-reload
systemctl --user enable boondmanager-activity-bot.timer
systemctl --user start boondmanager-activity-bot.timer
```

Check that it has successfully been scheduled with
```bash
systemctl --user list-timers
```

# TODO

- Target the correct activity with XPath (+ text) rather than CSS
