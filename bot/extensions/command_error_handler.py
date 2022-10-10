from logging import warning
from discord.ext import commands
from discord.ext.commands import Cog, MissingRequiredArgument, CommandNotFound, MissingPermissions
from lib.config_required import MissingRequiredConfig


class CommandErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, command_error):
        warning(f"Error: {command_error}. Issued by {ctx.author}")

        if isinstance(command_error, CommandNotFound):
            await self.send_command_help(ctx)
        elif isinstance(command_error, MissingPermissions):
            await ctx.send("You don't have the authorization to use that command.")
        elif isinstance(command_error, commands.CommandOnCooldown):
            await ctx.send('**You\'re on Cooldown**, wait {:.2f} seconds.'.format(command_error.retry_after))
        elif isinstance(command_error, MissingRequiredConfig):
            await ctx.send("This command is disabled due to missing configs. Look at the logs for more info.")
        elif isinstance(command_error, MissingRequiredArgument):
            await self.send_command_help(ctx)
        else:
            await ctx.send("An error occurred. Contact the administrators")

    @staticmethod
    def send_command_help(ctx):
        if ctx.command:
            return ctx.send_help(ctx.command)

        return ctx.send_help()


async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))
