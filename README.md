# Notes

*Disclaimer*: 

* All code is experimental and there's no guarantee it cannot fail. Plus, script has only been tested with a personal gmail account. No idea how to make it work for others - maybe add instructions here if you want to contribute.

*Steps to make it work*
1. If using gmail (only tested), create an app password with 2FA enabled. Instructions [here](https://support.google.com/mail/answer/185833?hl=en-GB) - takes only 1 min to create. 
1. Modify the `alert_config.json`
2. Modify `email_alert.py` alert frequency (via `time_sleep`) and `threshold_kb`
3. Run `email_alert.py` in the background
```python
python email_alert.py &
```
4. Wait until you receive an annoying email reminding you to clean up your directory (specidied in `alert_config.json`)
