# Notes

## Disclaimer

* All code is experimental and there's no guarantee it won't fail. Plus, the current implementation has only been tested with Gmail. No idea how to make it work for Outlook. If you want to contribute, you can add instructions for that here.

## Steps to make it work
1. If using Gmail (only tested), create an app password with 2FA enabled. Instructions [here](https://support.google.com/mail/answer/185833?hl=en-GB). It takes only 1 min to create one.
2. Modify the `alert_config.json` parameters.
3. Modify `email_alert.py` alert frequency (via `time_sleep`) and `threshold_kb`
4. Run `email_alert.py` in the background
```python
python email_alert.py &
```
5. Wait until you receive an annoying email reminding you to clean up your directory (specified in `alert_config.json`)

Notes: 
* To disable,just kill the job.
* You can run a quick test to see if it works by executing
```python
python email_alert.py y
```

## Contributions

Totally welcome! Quite a few things can be improved. If you have spare time to improve the implementation  :slightly_smiling_face:, please, go ahead!!
