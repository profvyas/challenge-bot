import discord
import os
import inspect
import asyncio

from help import Help
from constructs import Response
import exceptions

class ChallengeBot(discord.Client):


    def __init__(self):
        super().__init__()
        self.help = Help(self)
        # ToDo: add config, logging and permissions attr


    def run(self):
        self.loop.run_until_complete(self.start(os.environ['TOKEN']))

    async def on_ready(self):
        # ToDo: add log instead of print
        print('we have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        await self.wait_until_ready()

        # check message prefix
        message_content = message.content.strip()
        if not message_content.startswith('bb!'):
            return

        # Ignore commands from self
        if message.author == self.user:
            # ToDo: add warning log
            return

        # Ignore commands from other bots
        if message.author.bot:
            # ToDo: add warning log
            return

        command, *args = message_content.split(' ')
        command = command[len('bb!'):].lower().strip()

        # no args produces [''] above
        if args:
            args = ' '.join(args).lstrip(' ').split(' ')
        else:
            args = []
        
        try:
            # get the cmd_{command} function
            handler = getattr(self, 'cmd_' + command, None)

            # throw error if command not found
            if not handler:
                raise exceptions.CommandNotFoundException(
                    "No such command:{0}".format(command))

            argspec = inspect.signature(handler)
            params = argspec.parameters.copy()
            
            sentmsg = response = None

            # ToDo: move to utils if bloating. Discuss with team.
            # get command arguments by name
            handler_kwargs = {}

            if params.pop('channel', None):
                handler_kwargs['channel'] = message.channel

            if params.pop('guild', None):
                handler_kwargs['guild'] = message.guild

            response = await handler(**handler_kwargs)
            if response and isinstance(response, Response):
                
                # for embedded content
                if not isinstance(response.content, discord.Embed):
                    content = self._gen_embed()
                    content.title = command
                    content.description = response.content
                else:
                    content = response.content
                
                # ToDo: handle if required
                if response.reply:
                    pass
                
                sentmsg = await self.safe_send_message(
                    message.channel, content,
                    expire_in=response.delete_after
                )


        except (exceptions.ChallengeBotException) as e:
            # ToDo: error logging
            print("Error in {0}: {1.__class__.__name__}: {1.message}".format(command, e))

    
    # sends message
    async def safe_send_message(self, dest, content, **kwargs):
        expire_in = kwargs.pop('expire_in', 0)
        msg = None
        try:
            if content is not None:
                msg = await dest.send(embed=content)

        except discord.Forbidden:
            print("Cannot send message to {0}no permission", dest.name)
        
        # ToDo: handle invalid channel, HTTPException

        finally:
            if msg and expire_in:
                # future is needed to make non-blocking
                asyncio.ensure_future(self._wait_delete_msg(msg, expire_in))
    
    async def _wait_delete_msg(self, msg, expire_in):
        """delete message callback"""
        await asyncio.sleep(expire_in)
        return await msg.delete()

    def _gen_embed(self):
        """Provides a basic template for embeds"""
        e = discord.Embed()
        e.colour = 7506394
        e.set_author(name=self.user.name)
        ### ToDo: can set avatar and author link of github
        return e


    # ToDo: remove this. Used for initial testing.
    async def cmd_command(self, channel, guild):
        await channel.send("you just called the challenge-bot from " + str(channel.mention) +  " channel in '" + str(guild.name) + "' server with server id:" + str(guild.id) +"!")

    async def cmd_help(self, channel):
        return self.help.get_help(channel)

        