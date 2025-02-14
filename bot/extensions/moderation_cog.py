from bot import app
from logging import info
from discord import Member
from discord.ext.commands import Cog, has_permissions, hybrid_command, Context
from bot.helpers.log_helper import danger
from datetime import datetime


class ModerationCog(Cog, name="Moderation", description="Collection of administrative commands."):
    def __init__(self, bot):
        self.bot = bot

    @property
    def moderation_channel(self):
        return self.bot.get_channel_by_name("moderation_logs")

    @hybrid_command(name='kick', help="Allows a staff member to kick a user based on their behaviour.")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, reason="No reason given"):
        log = danger("KICK", f"{member.mention} has been kicked.")
        log.add_field("Issuer: ", ctx.author)
        log.add_field("Reason: ", reason)

        await ctx.guild.kick(user=member, reason=reason)
        await log.send(self.moderation_channel)

    @hybrid_command(name='ban', help="Allows a staff member to ban a user based on their behaviour.")
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, reason="No reason"):
        log = danger("BAN", f"{member.mention} has been banned.")
        log.add_field("Issuer: ", ctx.author.mention)
        log.add_field("Reason: ", reason)

        await ctx.guild.ban(user=member, reason=reason)
        await log.send(self.moderation_channel)

    @hybrid_command(name='unban', help="Allows a staff member to unban a user.")
    @has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        log = danger("UNBAN", f"{user.name} has been unbanned.")

        await ctx.guild.unban(user)
        await log.send(self.moderation_channel)

    @hybrid_command(name='purge', help="Deletes n amount of messages.")
    @has_permissions(manage_messages=True)
    async def purge(self, ctx: Context, limit):
        await ctx.channel.purge(limit=limit+1)
        await danger(
            "PURGE",
            f"{limit} message(s) purged by {ctx.author.mention} in {ctx.channel.mention}"
        ).send(ctx.channel)

    @Cog.listener()
    async def on_member_join(self, member):
        minimum_account_age = app.config.get("moderation", "minimum_account_age")
        account_age_in_days = (datetime.now().replace(tzinfo=None) - member.created_at.replace(tzinfo=None)).days

        if account_age_in_days <= minimum_account_age:
            info(f"{member} kicked due to account age restriction!")

            log = danger("KICK", f"{member} has been kicked.")
            log.add_field("Reason: ", "Automatically kicked due to account age restriction")

            await member.send(f"Your account needs to be {minimum_account_age} days old or more to join the server.")
            await member.guild.kick(user=member, reason="Account age restriction")
            await log.send(self.moderation_channel)


async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
