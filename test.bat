@echo off
call ..\faves-private\env.bat
python faves.py dreikanter -lk %lastfm_key% -vi %vk_id% -vs %vk_secret% -l faves.log -v
