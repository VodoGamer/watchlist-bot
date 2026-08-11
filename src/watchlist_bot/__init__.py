def main():
    from pathlib import Path

    from watchlist_bot.client import bot
    from watchlist_bot.commands import update_bot_commands

    bot.loop_wrapper.lifespan.add_startup_task(update_bot_commands)
    bot.dispatch.load_from_dir(Path("src", "watchlist_bot", "handlers"))

    bot.run_forever()
