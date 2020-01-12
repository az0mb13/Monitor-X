crontab -l | { cat; echo "0 */12 * * * /home/z0mb13/Desktop/projects/Monitor-X/cron.py"; } | crontab -
