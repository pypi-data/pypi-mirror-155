import asyncio
import contextlib
import os
import re
from datetime import datetime, timezone
from itertools import zip_longest
from json import dump, load
from logging import getLogger
from shutil import copy
from typing import Dict, List, Optional, Union

from core.config import ConfigManager
from core.models import DMDisabled, SafeFormatter
from core.thread import ThreadManager
from core.utils import (
    create_not_found_embed,
    escape_code_block,
    format_description,
    trigger_typing,
    truncate,
)

from interactions import (
    Channel,
    ChannelType,
    Choice,
    Client,
    CommandContext,
    Embed,
    Extension,
    Guild,
    Member,
    Message,
    Modal,
    Option,
    OptionType,
    Overwrite,
    Permissions,
    TextInput,
    TextStyleType,
    User,
)
from interactions import extension_autocomplete as ext_atc
from interactions import extension_command as ext_cmd
from interactions import extension_listener as ext_lst
from interactions import extension_message_command as ext_mcmd
from interactions import extension_user_command as ext_ucmd
from interactions.ext.get import get
from interactions.ext.paginator import Page, Paginator
from interactions.ext.wait_for import setup as _setup
from interactions.ext.wait_for import wait_for

logger = getLogger("modmail")


class Modmail(Extension):
    """Commands directly related to Modmail functionality."""

    async def is_blocked(
        self,
        author: User,
        *,
        guild: Guild = None,
    ) -> bool:

        member = await guild.get_member(int(author.id))
        if not isinstance(member, Member):
            # try to find in other guilds
            for g in self.bot.guilds:
                member = await g.get_member(int(author.id))
                if isinstance(member, Member):
                    break

        if member is None:
            logger.debug("User not in guild, %s.", author.id)

        if member is not None:
            author: Member = member

        if str(author.id) in self.blocked_whitelisted_users(int(guild.id)):
            for _ in self.blocked_users(int(guild.id)):
                if str(author.id) in _:
                    del _
                    with open("config.json", "r+") as cfg:
                        _cfg: dict = load(cfg)
                        _cfg["blocked"] = self.config["blocked"]
                        dump(_cfg, cfg)
                    break
            return False

        if not self.check_manual_blocked(author, int(guild.id)):
            return True

        if not self.check_manual_blocked_roles(author, guild):
            return True

        return False

    def blocked_users(self, guild_id: int) -> Optional[List[Dict[str, str]]]:
        return self.config["blocked"].get(guild_id, None)

    def blocked_whitelisted_users(self, guild_id: int) -> Optional[List[str]]:
        return self.config["blocked_whitelist"].get(guild_id, None)

    def check_manual_blocked_roles(self, author: Member, guild: Guild) -> bool:
        for r in author.roles:
            if str(r) in self.blocked_roles:
                r = await guild.get_role(r)
                blocked_reason = self.blocked_roles.get(str(r)) or ""
                now = datetime.now(timezone.utc)

                # etc "blah blah blah... until 2019-10-14T21:12:45.559948."
                end_time = re.search(r"until ([^`]+?)\.$", blocked_reason)
                if end_time is None:
                    # backwards compat
                    end_time = re.search(r"%([^%]+?)%", blocked_reason)
                    if end_time is not None:
                        logger.warning(
                            r"Deprecated time message for role %s, block and unblock again to update.",
                            r.name,
                        )

                if end_time is not None:
                    after = (datetime.fromisoformat(end_time[1]) - now).total_seconds()
                    if after <= 0:
                        # No longer blocked
                        self.blocked_roles.pop(str(r.id))
                        with open("config.json", "r+") as cfg:
                            _cfg: dict = load(cfg)
                            _cfg["blocked_roles"] = self.config["blocked_roles"]
                            dump(_cfg, cfg)
                        logger.debug("No longer blocked, role % s.", r.name)
                        return True
                logger.debug("User blocked, role %s.", r.name)
                return False

        return True

    def check_manual_blocked(self, author: Member, guild_id: int) -> bool:
        if all(str(author.id) not in _ for _ in self.blocked_users(guild_id)):
            return True

    @property
    def blocked_roles(self) -> Dict[str, str]:
        return self.config["blocked_roles"]

    @property
    def snippets(self) -> Dict[str, dict]:
        return self.config["snippets"]

    @property
    def main_color(self) -> int:
        return self.config.get("main_color")

    @property
    def error_color(self) -> int:
        return self.config.get("error_color")

    @property
    def mod_color(self) -> int:
        return self.config.get("mod_color")

    def modmail_guild(self, guild_id) -> Optional[Guild]:
        """
        The guild that the bot is operating in
        (where the bot is creating threads)
        """
        if not self.config["modmail_guild_id"]:
            return None

        modmail_guild_id = self.config["modmail_guild_id"]
        if guild_id not in modmail_guild_id:
            return None
        with contextlib.suppress(ValueError):
            guild = next(guild for guild in self.bot.guilds if int(guild.id) == int(guild_id))
            if guild is not None:
                return guild
        return None

    def main_category(self, guild_id) -> Optional[Channel]:
        if self.modmail_guild(guild_id) is not None:
            category_id = self.config["main_category_id"][str(guild_id)]
            if category_id is not None:
                with contextlib.suppress(ValueError):
                    cat = next(
                        channel
                        for channel in self.modmail_guild(guild_id).channels
                        if int(channel.id) == category_id
                        and channel.type == ChannelType.GUILD_CATEGORY
                    )
                    if cat is not None:
                        return cat
                self.config.remove("main_category_id")
                logger.debug("MAIN_CATEGORY_ID was invalid, removed.")
            cat = next(
                channel
                for channel in self.modmail_guild(guild_id).channels
                if channel.name == "Modmail" and channel.type == ChannelType.GUILD_CATEGORY
            )
            if cat is not None:
                self.config["main_category_id"][str(guild_id)] = int(cat.id)
                logger.debug(
                    'No main category set explicitly, setting category "Modmail" as the main category.'
                )
                return cat
        return None

    @property
    def recipient_color(self) -> int:
        return self.config.get("recipient_color")

    @ext_lst
    async def on_guild_create(self, guild: Guild):
        if int(guild.id) not in self.config["modmail_guild_id"]:
            self.config["modmail_guild_id"].append(int(guild.id))
        with open("config.json", "r+") as cfg:
            _cfg: dict = load(cfg)
            _cfg["modmail_guild_id"] = self.config["modmail_guild_id"]
            dump(_cfg, cfg)

    def __init__(self, bot, guild_id: Union[int, List[int]] = None):
        self.me = None
        self.bot: Client = bot
        if "config.json" not in os.listdir():
            copy("core/config.json", "config.json")
            # this is needed to not overwrite new config files on update - at least I hope pip keeps it
        if not hasattr(self.bot, "wait_for_component"):
            _setup(self.bot)
        self.config = ConfigManager(self.bot)
        self.config.populate_cache()
        self.threads = ThreadManager(self.bot, self)
        self.formatter = SafeFormatter()
        if guild_id:
            if isinstance(guild_id, list):
                for _id in guild_id:
                    if _id not in self.config["modmail_guild_id"]:
                        self.config["modmail_guild_id"].append(_id)
            elif guild_id not in self.config["modmail_guild_id"]:
                self.config["modmail_guild_id"].append(guild_id)
            with open("config.json", "r+") as cfg:
                _cfg: dict = load(cfg)
                _cfg["modmail_guild_id"] = self.config["modmail_guild_id"]
                dump(_cfg, cfg)

        logger.info("Modmail is now ready!")

    @ext_cmd(
        name="setup",
        description="Sets up your server for Modmail.",
        default_member_permissions=Permissions.ADMINISTRATOR,
        dm_permission=False,
    )
    @trigger_typing
    async def setup_modmail(self, ctx: CommandContext):
        """
        Sets up a server for Modmail.

        You only need to run this command
        once after configuring Modmail.
        """
        await ctx.defer(ephemeral=True)
        if not self.modmail_guild(int(ctx.guild_id)):
            return await ctx.send(
                "This guild is not registered for modmail. Please register this guild first."
            )

        if self.main_category(int(ctx.guild_id)) is not None:
            logger.debug("Can't re-setup server, main_category is found.")
            return await ctx.send(f"{self.modmail_guild(int(ctx.guild_id))} is already set up.")

        if self.modmail_guild(int(ctx.guild_id)) is None:
            embed = Embed(
                title="Error",
                description="Modmail functioning guild not found.",
                color=self.error_color,
            )
            return await ctx.send(embeds=embed)

        self.me = await ctx.client.get_self()

        overwrites = [
            Overwrite(id=int(ctx.guild_id), type=0, deny=Permissions.VIEW_CHANNEL),
            Overwrite(
                id=self.me["id"],
                type=1,
                allow=Permissions.VIEW_CHANNEL | Permissions.READ_MESSAGE_HISTORY,
            ),
        ]

        category = await self.modmail_guild(int(ctx.guild_id)).create_channel(
            name="MODMAIL",
            permission_overwrites=overwrites,
            type=ChannelType.GUILD_CATEGORY,
        )

        await category.modify(position=0)

        thread_channel = await self.modmail_guild(int(ctx.guild_id)).create_channel(
            parent_id=int(category.id),
            type=ChannelType.GUILD_TEXT,
            name="Modmail-Threads",
            permission_overwrites=overwrites,
        )

        self.config["main_category_id"][str(ctx.guild_id)] = int(category.id)
        self.config["thread_channel_id"][str(category.id)] = int(thread_channel.id)

        with open("config.json", "r+") as cfg:
            _cfg = load(cfg)
            _cfg["thread_channel_id"][str(category.id)] = int(thread_channel.id)
            _cfg["main_category_id"][str(ctx.guild_id)] = int(category.id)
            dump(_cfg, cfg)

        await ctx.send("**Successfully set up server.**\n", ephemeral=True)

    @ext_lst
    async def on_message_create(self, message: Message):
        if message.author.bot:
            return

        ch = await message.get_channel()

        if ch.type == ChannelType.DM:
            return await self.process_dm_modmail(message)

    async def process_dm_modmail(self, message: Message) -> None:
        """Processes messages sent to the bot."""

        blocked_emoji, sent_emoji = self.config["blocked_emoji"], self.config["sent_emoji"]

        channel = await message.get_channel()

        thread = await self.threads.find(recipient=message.author)
        if thread is None:

            if self.config["dm_disabled"].get(int(message.guild_id), DMDisabled.NONE) in (
                DMDisabled.NEW_THREADS,
                DMDisabled.ALL_THREADS,
            ):
                embed = Embed(
                    title=self.config["disabled_new_thread_title"],
                    color=self.error_color,
                    description=self.config["disabled_new_thread_response"],
                )
                embed.set_footer(text=self.config["disabled_new_thread_footer"])
                logger.info(
                    "A new thread was blocked from %s due to disabled Modmail.", message.author
                )
                await channel.send(embeds=embed)
                return await message.create_reaction(blocked_emoji)

            thread = await self.threads.create(message.author, message=message)
        elif (
            self.config["dm_disabled"].get(int(message.guild_id), DMDisabled.NONE)
            == DMDisabled.ALL_THREADS
        ):
            embed = Embed(
                title=self.config["disabled_current_thread_title"],
                color=self.error_color,
                description=self.config["disabled_current_thread_response"],
            )
            embed.set_footer(
                text=self.config["disabled_current_thread_footer"],
            )
            logger.info("A message was blocked from %s due to disabled Modmail.", message.author)
            await channel.send(embeds=embed)
            return await message.create_reaction(blocked_emoji)

        if not thread.cancelled:
            try:
                await thread.send(message, message.content)
            except Exception:
                logger.error("Failed to send message:", exc_info=True)
                await message.create_reaction(blocked_emoji)
            else:
                for user in thread.recipients:
                    # send to all other recipients
                    if user != message.author:
                        try:
                            await thread.send(message, message.content, user)
                        except Exception:
                            # silently ignore
                            logger.error("Failed to send message:", exc_info=True)

                await message.create_reaction(sent_emoji)

    @ext_cmd(
        name="snippets",
        description="Pre-defined response management",
        default_member_permissions=Permissions.MODERATE_MEMBERS | Permissions.ADMINISTRATOR,
        dm_permission=False,
        options=[
            Option(
                name="list",
                description="list all existing snippets",
                type=OptionType.SUB_COMMAND,
            ),
            Option(
                name="raw",
                description="View the raw content of a snippet.",
                type=OptionType.SUB_COMMAND,
                options=[
                    Option(
                        name="snippet_name",
                        description="The name of the snippet",
                        required=True,
                        autocomplete=True,
                        type=OptionType.STRING,
                    ),
                ],
            ),
            Option(
                name="create",
                description="Creates a snippet",
                type=OptionType.SUB_COMMAND,
            ),
            Option(
                name="send",
                description="Send a snippet to the channel",
                type=OptionType.SUB_COMMAND,
                options=[
                    Option(
                        name="snippet_name",
                        description="The name of the snippet",
                        required=True,
                        autocomplete=True,
                        type=OptionType.STRING,
                    ),
                ],
            ),
            Option(
                name="delete",
                description="Delete a snippet",
                type=OptionType.SUB_COMMAND,
                options=[
                    Option(
                        name="snippet_name",
                        description="The name of the snippet",
                        required=True,
                        autocomplete=True,
                        type=OptionType.STRING,
                    ),
                ],
            ),
            Option(
                name="edit",
                description="Edit a snippet",
                type=OptionType.SUB_COMMAND,
                options=[
                    Option(
                        name="snippet_name",
                        description="The name of the snippet",
                        required=True,
                        autocomplete=True,
                        type=OptionType.STRING,
                    ),
                ],
            ),
        ],
    )
    async def _snippets(
        self, ctx: CommandContext, sub_command: str, **kwargs
    ):  # right, we have a property without _
        function = getattr(self, f"snippets_{sub_command}")
        await function(ctx, **kwargs)

    async def snippets_list(self, ctx: CommandContext):

        if not self.snippets[str(ctx.guild_id)]:
            embed = Embed(
                color=self.error_color, description="You dont have any snippets at the moment."
            )
            embed.set_footer(text='Check "/snippets create" to add a snippet.')
            embed.set_author(name="Snippets", icon_url=ctx.guild.icon_url)
            return await ctx.send(embeds=embed, ephemeral=True)

        embeds = []
        await ctx.get_guild()

        for i, names in enumerate(
            zip_longest(*(iter(sorted(self.snippets[str(ctx.guild_id)])),) * 15)
        ):
            description = format_description(i, names)
            embed = Embed(color=self.main_color, description=description)
            embed.set_author(name="Snippets", icon_url=ctx.guild.icon_url)
            embeds.append(embed)

        pages = [Page(embeds=embed) for embed in embeds]
        paginator = Paginator(
            client=self.bot,
            ctx=ctx,
            pages=pages,
            timeout=120,
        )
        await paginator.run()

    @ext_atc(command="snippets", name="snippet_name")
    async def snippets_autocomplete(self, ctx: CommandContext, user_input: str = ""):

        if not (guild_snippets_dict := self.snippets.get(str(ctx.guild_id))):
            choice = Choice(name="No snippets present", value="no_snippets")
            return await ctx.populate(choices=[choice])

        elif not user_input:
            choice = Choice(name="Type something to trigger completion", value="no_input")
            return await ctx.populate(choices=[choice])

        i = 0
        _choices = []
        for name in guild_snippets_dict.keys():
            name: str
            if name.startswith(user_input):
                _choices.append(Choice(name=name, value=name))
            if i == 25:
                break

        return await ctx.populate(choices=_choices)

    async def snippets_raw(self, ctx: CommandContext, *, snippet_name: str):
        if snippet_name == "no_input":
            return await ctx.send("Please enter a valid snippet name", ephemeral=True)

        if (
            not (guild_snippets := self.snippets.get(str(ctx.guild_id)))
            or snippet_name == "no_snippets"
        ):
            embed = Embed(
                color=self.error_color, description="You dont have any snippets at the moment."
            )
            embed.set_footer(text='Check "/snippets create" to add a snippet.')
            await ctx.get_guild()
            embed.set_author(name="Snippets", icon_url=ctx.guild.icon_url)
            return await ctx.send(embeds=embed, ephemeral=True)
        val = guild_snippets.get(snippet_name)
        if val is None:
            embed = create_not_found_embed(snippet_name, guild_snippets, "Snippet")
        else:
            val = truncate(escape_code_block(val), 2048 - 7)
            embed = Embed(
                title=f'Raw snippet - "{snippet_name}":',
                description=f"```\n{val}```",
                color=self.main_color,
            )

        return await ctx.send(embeds=embed, ephemeral=True)

    async def snippets_send(self, ctx: CommandContext, snippet_name: str):
        if snippet_name == "no_input":
            return await ctx.send("Please enter a valid snippet name", ephemeral=True)

        if (
            not (guild_snippets := self.snippets.get(str(ctx.guild_id)))
            or snippet_name == "no_snippets"
        ):
            embed = Embed(
                color=self.error_color, description="You dont have any snippets at the moment."
            )
            embed.set_footer(text='Check "/snippets create" to add a snippet.')
            await ctx.get_guild()
            embed.set_author(name="Snippets", icon_url=ctx.guild.icon_url)
            return await ctx.send(embeds=embed, ephemeral=True)

        val = guild_snippets.get(snippet_name)
        if val is None:
            embed = create_not_found_embed(snippet_name, guild_snippets, "Snippet")
            return await ctx.send(embeds=embed, ephemeral=True)
        else:
            embed = Embed(
                title=f'Snippet - "{snippet_name}":', description=val, color=self.main_color
            )
            await ctx.get_channel()
            await ctx.channel.send(embeds=embed)
        return await ctx.send("Success", ephemeral=True)

    async def snippets_create(self, ctx: CommandContext):

        modal = Modal(
            custom_id="new_snippet",
            title="Create a new Snippet",
            components=[
                TextInput(
                    custom_id="name",
                    style=TextStyleType.SHORT,
                    label="The name of the snippet",
                    required=True,
                    min_length=1,
                    max_langth=120,
                ),
                TextInput(
                    custom_id="value",
                    style=TextStyleType.PARAGRAPH,
                    label="The value of the snippet",
                    required=True,
                    min_length=10,
                    max_length=4000,
                ),
            ],
        )

        await ctx.popup(modal)

        __args = []

        def check(_ctx: CommandContext):
            return _ctx.data.custom_id == "new_snippet"

        _context: CommandContext = await wait_for(self.bot, "on_modal", check=check, timeout=300)
        await _context.defer(ephemeral=True)
        if _context.data._json.get("components"):
            for component in _context.data.components:
                if component.get("components"):
                    __args.append([_value["value"] for _value in component["components"]][0])
                else:
                    __args.append([_value.value for _value in component.components][0])
        name, value = __args
        if name in self.snippets.get(str(ctx.guild_id)):
            embed = Embed(
                title="Error",
                color=self.error_color,
                description=f"Snippet `{name}` already exists.",
            )
            return await _context.send(embeds=embed, ephemeral=True)

        if len(name) > 120:
            embed = Embed(
                title="Error",
                color=self.error_color,
                description="Snippet names cannot be longer than 120 characters.",
            )
            return await _context.send(embeds=embed, ephemeral=True)

        with open("config.json", "r+") as cfg:
            _cfg: dict = load(cfg)
            if not (guild_snippets := self.snippets.get(str(ctx.guild_id))):
                self.snippets.update({str(ctx.guild_id): {name: value}})
            else:
                guild_snippets[name] = value
            _cfg["snippets"] = self.snippets
            dump(_cfg, cfg)

        embed = Embed(
            title="Added snippet",
            color=self.main_color,
            description="Successfully created snippet.",
        )
        return await _context.send(embeds=embed, ephemeral=True)

    async def snippets_delete(self, ctx: CommandContext, snippet_name: str):
        """Remove a snippet."""
        await ctx.defer(ephemeral=True)
        if snippet_name == "no_input":
            return await ctx.send("Please enter a valid snippet name", ephemeral=True)

        if (
            not (guild_snippets := self.snippets.get(str(ctx.guild_id)))
            or snippet_name == "no_snippets"
        ):
            embed = Embed(
                color=self.error_color, description="You dont have any snippets at the moment."
            )
            embed.set_footer(text='Check "/snippets create" to add a snippet.')
            await ctx.get_guild()
            embed.set_author(name="Snippets", icon_url=ctx.guild.icon_url)
            return await ctx.send(embeds=embed, ephemeral=True)
        if snippet_name in guild_snippets:
            embed = Embed(
                title="Removed snippet",
                color=self.main_color,
                description=f"Snippet `{snippet_name}` is now deleted.",
            )
            with open("config.json", "r+") as cfg:
                _cfg: dict = load(cfg)
                del guild_snippets[snippet_name]
                _cfg["snippets"] = self.snippets
                dump(_cfg, cfg)

        else:
            embed = create_not_found_embed(snippet_name, guild_snippets, "Snippet")
        await ctx.send(embeds=embed, ephemeral=True)

    async def snippets_edit(self, ctx: CommandContext, snippet_name: str):

        if snippet_name == "no_input":
            return await ctx.send("Please enter a valid snippet name", ephemeral=True)

        if (
            not (guild_snippets := self.snippets.get(str(ctx.guild_id)))
            or snippet_name == "no_snippets"
        ):
            embed = Embed(
                color=self.error_color, description="You dont have any snippets at the moment."
            )
            embed.set_footer(text='Check "/snippets create" to add a snippet.')
            await ctx.get_guild()
            embed.set_author(name="Snippets", icon_url=ctx.guild.icon_url)
            return await ctx.send(embeds=embed, ephemeral=True)

        modal = Modal(
            custom_id="edit_snippet",
            title="Edit a Snippet",
            components=[
                TextInput(
                    custom_id="name",
                    style=TextStyleType.SHORT,
                    label="The name of the snippet",
                    required=True,
                    value=snippet_name,
                    min_length=1,
                    max_langth=120,
                ),
                TextInput(
                    custom_id="value",
                    style=TextStyleType.PARAGRAPH,
                    label="The value of the snippet",
                    value=guild_snippets[snippet_name],
                    required=True,
                    min_length=10,
                    max_length=4000,
                ),
            ],
        )

        await ctx.popup(modal)

        __args = []

        def check(_ctx: CommandContext):
            return _ctx.data.custom_id == "edit_snippet"

        _context: CommandContext = await wait_for(self.bot, "on_modal", check=check, timeout=300)
        await _context.defer(ephemeral=True)
        if _context.data._json.get("components"):
            for component in _context.data.components:
                if component.get("components"):
                    __args.append([_value["value"] for _value in component["components"]][0])
                else:
                    __args.append([_value.value for _value in component.components][0])
        name, value = __args

        if name == snippet_name:
            guild_snippets[snippet_name] = value
        else:
            del guild_snippets[snippet_name]
            guild_snippets[name] = value

        with open("config.json", "r+") as cfg:
            _cfg = load(cfg)
            _cfg["snippets"] = self.snippets
            dump(_cfg, cfg)
        await ctx.send("Snippet updated!", ephemeral=True)

    @ext_cmd(
        default_member_permissions=Permissions.MODERATE_MEMBERS | Permissions.ADMINISTRATOR,
        name="thread",
        description="Do something with or in the thread",
        dm_permission=False,
        options=[
            Option(
                type=OptionType.SUB_COMMAND,
                name="close",
                description="Closes the Thread",
            ),
            Option(
                type=OptionType.SUB_COMMAND,
                name="lock",
                description="Locks the Thread",
            ),
            Option(
                type=OptionType.SUB_COMMAND,
                name="nsfw",
                description="sets the nsfw value of the thread",
                options=[
                    Option(
                        name="_nsfw",
                        type=OptionType.BOOLEAN,
                        description="Boolean state of nsfw",
                        required=True,
                    ),
                ],
            ),
            Option(
                type=OptionType.SUB_COMMAND,
                name="add_user",
                description="Adds a user to the thread",
                options=[
                    Option(
                        name="member",
                        type=OptionType.USER,
                        description="The User to add to the thread",
                        required=True,
                    ),
                ],
            ),
            Option(
                type=OptionType.SUB_COMMAND,
                name="remove_user",
                description="Removed a user of the thread",
                options=[
                    Option(
                        name="member",
                        type=OptionType.USER,
                        description="The User to add to the thread",
                        required=True,
                    ),
                ],
            ),
            Option(
                type=OptionType.SUB_COMMAND,
                name="reply",
                description="Make a reply in the thread",
                options=[
                    Option(
                        name="anonymous",
                        description="whether the response is anonymous or not",
                        required=False,
                        type=OptionType.BOOLEAN,
                    ),
                    Option(
                        name="plain",
                        description="Whether to send a plain message instead of an embed",
                        type=OptionType.BOOLEAN,
                        required=False,
                    ),
                ],
            ),
            Option(
                type=OptionType.SUB_COMMAND,
                name="edit",
                description="Edit a reply of the thread",
                options=[
                    Option(
                        name="message_id",
                        description="The ID of the message to edit",
                        required=True,
                        type=OptionType.STRING,
                    ),
                ],
            ),
        ],
    )
    async def thread(self, ctx: CommandContext, sub_command: str = None, **kwargs):

        await ctx.get_channel()
        if not await self.threads.find(channel=ctx.channel):
            return await ctx.send("not in a thread", ephemeral=True)

        await ctx.defer(ephemeral=True)

        func = getattr(self, sub_command)
        await func(ctx, **kwargs)

    async def close(self, ctx: CommandContext):
        await ctx.channel.modify(
            archived=True,
            locked=False,
            reason="Closing modmail thread!",
        )
        await ctx.send("updated successfully!", ephemeral=True)

    async def lock(self, ctx: CommandContext):
        await ctx.channel.modify(
            archived=True,
            locked=True,
            reason="Closing modmail thread!",
        )
        await ctx.send("updated successfully!", ephemeral=True)

    async def nsfw(self, ctx: CommandContext, _nsfw: bool):
        await ctx.channel.modify(nsfw=_nsfw)
        await ctx.send("updated successfully!", ephemeral=True)

    async def add_user(self, ctx: CommandContext, member: Member):

        curr_thread = await self.threads.find(recipient=member)
        if curr_thread.channel == ctx.channel:
            return

        if curr_thread:
            em = Embed(
                title="Error",
                description=f"{member.mention} is already in a thread: {curr_thread.channel.mention}.",
                color=self.error_color,
            )
            return await ctx.send(embeds=em, ephemeral=True)

        thread = await self.threads.find(channel=ctx.channel)

        if len(thread.recipients) >= 5:
            em = Embed(
                title="Error",
                description="Only 5 users are allowed in a group conversation",
                color=self.error_color,
            )
            return await ctx.send(embeds=em, ephemeral=True)

        description = self.formatter.format(
            self.config["private_added_to_group_response"], moderator=ctx.author
        )
        em = Embed(
            title=self.config["private_added_to_group_title"],
            description=description,
            color=self.main_color,
        )
        if self.config["show_timestamp"]:
            em.timestamp = datetime.utcnow()
        em.set_footer(text=str(ctx.author), icon_url=ctx.author.user.avatar_url)
        await member.send(embeds=em)

        description = self.formatter.format(
            self.config["public_added_to_group_response"],
            moderator=ctx.author,
            users=member.name,
        )
        em = Embed(
            title=self.config["public_added_to_group_title"],
            description=description,
            color=self.main_color,
        )
        if self.config["show_timestamp"]:
            em.timestamp = datetime.utcnow()
        em.set_footer(text=f"{member}", icon_url=member.user.avatar_url)

        for i in thread.recipients:
            if i != member:
                await i.send(embeds=em)

        await thread.add_users([member])
        await ctx.send("Done", ephemeral=True)

    async def remove_user(self, ctx: CommandContext, member: Member):
        """Removes a user from a modmail thread

        `options` can be `silent` or `silently`.
        """
        curr_thread = await self.threads.find(recipient=member)
        if await ctx.get_channel() != curr_thread.channel:
            em = Embed(
                title="Error",
                description=f"{member.mention} is not in this thread.",
                color=self.error_color,
            )
            await ctx.send(embeds=em, ephemeral=True)
            return
        thread = await self.threads.find(channel=ctx.channel)
        if thread.recipient == member:
            em = Embed(
                title="Error",
                description=f"{member.mention} is the main recipient of the thread and cannot be removed.",
                color=self.error_color,
            )
            await ctx.send(embeds=em, ephemeral=True)
            return

        description = self.formatter.format(
            self.config["private_removed_from_group_response"], moderator=ctx.author
        )
        em = Embed(
            title=self.config["private_removed_from_group_title"],
            description=description,
            color=self.main_color,
        )
        if self.config["show_timestamp"]:
            em.timestamp = datetime.utcnow()
        em.set_footer(text=str(ctx.author), icon_url=ctx.author.user.avatar_url)
        await member.send(embeds=em)

        description = self.formatter.format(
            self.config["public_removed_from_group_response"],
            moderator=ctx.author,
            users=member.name,
        )
        em = Embed(
            title=self.config["public_removed_from_group_title"],
            description=description,
            color=self.main_color,
        )
        if self.config["show_timestamp"]:
            em.timestamp = datetime.now(timezone.utc)
        em.set_footer(text=f"{member}", icon_url=member.user.avatar_url)

        for i in thread.recipients:
            if i != member:
                await i.send(embeds=em)

        await thread.remove_users([member])
        await ctx.send("Done!", ephemeral=True)

    async def reply(self, ctx: CommandContext, *, anonymous: bool = False, plain: bool = False):
        """
        Reply to a Modmail thread.

        Supports attachments and images as well as
        automatically embedding image URLs.
        """

        modal = Modal(
            custom_id="reply",
            title="Reply",
            components=[
                TextInput(
                    custom_id="message",
                    style=TextStyleType.PARAGRAPH,
                    label="The message to send as reply",
                    required=True,
                ),
            ],
        )

        await ctx.popup(modal)

        __args = []

        def check(_ctx: CommandContext):
            return _ctx.data.custom_id == "reply"

        _context: CommandContext = await wait_for(self.bot, "on_modal", check=check, timeout=300)
        await _context.defer(ephemeral=True)
        if _context.data._json.get("components"):
            for component in _context.data.components:
                if component.get("components"):
                    __args.append([_value["value"] for _value in component["components"]][0])
                else:
                    __args.append([_value.value for _value in component.components][0])

        message = __args[0]

        thread = await self.threads.find(channel=ctx.channel)

        async with ctx.client.trigger_typing(int(ctx.channel_id)):
            await thread.reply(ctx, message=message, anonymous=anonymous, plain=plain)

        await _context.send("Done", ephemeral=True)

    async def edit(self, ctx: CommandContext, message_id):

        thread = await self.threads.find(channel=ctx.channel)

        message1: Message
        try:
            message1, *_ = await thread.find_linked_messages(message_id)
        except ValueError:
            return await ctx.send(
                embeds=Embed(
                    title="Failed",
                    description="Cannot find a message to edit. Plain messages are not supported.",
                    color=self.error_color,
                ),
                ephemeral=True,
            )

        if not message1.embeds:
            return await ctx.send(
                embeds=Embed(
                    title="Failed",
                    description="Cannot find a message to edit. Plain messages are not supported.",
                    color=self.error_color,
                ),
                ephemeral=True,
            )

        modal = Modal(
            custom_id="edit",
            title="Edit a message",
            components=[
                TextInput(
                    custom_id="content",
                    value=message1.embeds[0].description,
                    style=TextStyleType.PARAGRAPH,
                    label="The new content",
                    required=True,
                ),
            ],
        )

        await ctx.popup(modal)

        __args = []

        def check(_ctx: CommandContext):
            return _ctx.data.custom_id == "edit"

        _context: CommandContext = await wait_for(self.bot, "on_modal", check=check, timeout=300)
        await _context.defer(ephemeral=True)
        if _context.data._json.get("components"):
            for component in _context.data.components:
                if component.get("components"):
                    __args.append([_value["value"] for _value in component["components"]][0])
                else:
                    __args.append([_value.value for _value in component.components][0])

        message = __args[0]

        try:
            await thread.edit_message(message_id, message)
        except ValueError:
            return await ctx.send(
                embeds=Embed(
                    title="Failed",
                    description="Cannot find a message to edit. Plain messages are not supported.",
                    color=self.error_color,
                ),
                ephemeral=True,
            )

        await _context.send("Done!", ephemeral=True)

    @ext_ucmd(
        name="contact",
        dm_permission=False,
        default_member_permissions=Permissions.MODERATE_MEMBERS | Permissions.ADMINISTRATOR,
    )
    async def contact(
        self,
        ctx: CommandContext,
    ):
        silent = False

        errors = []

        await ctx.get_guild()
        if isinstance(ctx.target, User):
            ctx.target = await ctx.guild.get_member(int(ctx.target.id))

        exists = await self.threads.find(recipient=ctx.target)
        if exists:
            errors.append(f"A thread for {ctx.target.mention} already exists.")
            if exists.channel:
                errors[-1] += f" in {exists.channel.mention}"
            errors[-1] += "."
        elif ctx.target.user.bot:
            errors.append(f"{ctx.target} is a bot, cannot add to thread.")
        elif await self.is_blocked(ctx.target.user, guild=ctx.guild):
            ref = (
                f"{ctx.target.mention} is"
                if int(ctx.author.id) != int(ctx.target.id)
                else "You are"
            )
            errors.append(f"{ref} currently blocked from contacting {self.bot.me.name}.")

        if errors:
            embed = Embed(title="Error", color=self.error_color, description="\n".join(errors))
            msg = await ctx.send(embeds=embed, ephemeral=True)
            await asyncio.sleep(30)
            await msg.delete()

        creator = ctx.author

        thread = await self.threads.create(
            recipient=ctx.target,
            creator=creator,
        )

        if thread.cancelled:
            return

        if self.config["dm_disabled"].get(int(ctx.guild_id), DMDisabled.NONE) in (
            DMDisabled.NEW_THREADS,
            DMDisabled.ALL_THREADS,
        ):
            logger.info("Contacting user %s when Modmail DM is disabled.", ctx.target)

        if not silent and not self.config.get("thread_contact_silently"):
            if creator.id == ctx.target.id:
                description = self.config["thread_creation_self_contact_response"]
            else:
                description = self.formatter.format(
                    self.config["thread_creation_contact_response"], creator=creator
                )

            em = Embed(
                title=self.config["thread_creation_contact_title"],
                description=description,
                color=self.main_color,
            )
            if self.config["show_timestamp"]:
                em.timestamp = datetime.utcnow()
            em.set_footer(text=f"{creator}", icon_url=creator.user.avatar_url)

            await ctx.target.send(embeds=em)

        embed = Embed(
            title="Created Thread",
            description=f"Thread started by {creator.mention} for {ctx.target}.",
            color=self.main_color,
        )
        await thread.wait_until_ready()

        await thread.channel.send(embeds=embed)

    @ext_cmd(
        name="list_blocked_users",
        description="Lists all blocked users of the guild",
        default_member_permissions=Permissions.ADMINISTRATOR | Permissions.MODERATE_MEMBERS,
        dm_permission=False,
    )
    @trigger_typing
    async def blocked(self, ctx: CommandContext):
        """Retrieve a list of blocked users."""
        await ctx.defer()
        embeds = [Embed(title="Blocked Users", color=self.main_color, description="")]

        roles = []
        users = []
        now = datetime.utcnow()

        blocked_users = self.blocked_users(int(ctx.guild_id))
        for item in blocked_users:
            for id_, reason in item:
                # parse "reason" and check if block is expired
                # etc "blah blah blah... until 2019-10-14T21:12:45.559948."
                end_time = re.search(r"until ([^`]+?)\.$", reason)
                if end_time is None:
                    # backwards compat
                    end_time = re.search(r"%([^%]+?)%", reason)
                    if end_time is not None:
                        logger.warning(
                            r"Deprecated time message for user %s, block and unblock again to update.",
                            id_,
                        )

                if end_time is not None:
                    after = (datetime.fromisoformat(end_time.group(1)) - now).total_seconds()
                    if after <= 0:
                        # No longer blocked
                        del item
                        logger.debug("No longer blocked, user %s.", id_)
                        continue

                user = await get(self.bot, User, user_id=int(id_))
                users.append((user.mention, reason))

        blocked_roles = list(self.blocked_roles.items())
        for id_, reason in blocked_roles:
            # parse "reason" and check if block is expired
            # etc "blah blah blah... until 2019-10-14T21:12:45.559948."
            end_time = re.search(r"until ([^`]+?)\.$", reason)
            if end_time is None:
                # backwards compat
                end_time = re.search(r"%([^%]+?)%", reason)
                if end_time is not None:
                    logger.warning(
                        r"Deprecated time message for role %s, block and unblock again to update.",
                        id_,
                    )

            if end_time is not None:
                after = (datetime.fromisoformat(end_time.group(1)) - now).total_seconds()
                if after <= 0:
                    # No longer blocked
                    self.blocked_roles.pop(str(id_))
                    logger.debug("No longer blocked, role %s.", id_)
                    continue
            await ctx.get_guild()
            role = await ctx.guild.get_role(int(id_))
            if role:
                roles.append((role.mention, reason))

        if users:
            embed = embeds[0]

            for mention, reason in users:
                line = f"{mention} - {reason or 'No Reason Provided'}\n"
                if len(embed.description) + len(line) > 2048:
                    embed = Embed(
                        title="Blocked Users (Continued)",
                        color=self.main_color,
                        description=line,
                    )
                    embeds.append(embed)
                else:
                    embed.description += line
        else:
            embeds[0].description = "Currently there are no blocked users."

        embeds.append(Embed(title="Blocked Roles", color=self.main_color, description=""))

        if roles:
            embed = embeds[-1]

            for mention, reason in roles:
                line = f"{mention} - {reason or 'No Reason Provided'}\n"
                if len(embed.description) + len(line) > 2048:
                    embed = Embed(
                        title="Blocked Roles (Continued)",
                        color=self.main_color,
                        description=line,
                    )
                    embeds.append(embed)
                else:
                    embed.description += line
        else:
            embeds[-1].description = "Currently there are no blocked roles."

        with open("config.json", "r+") as cfg:
            _cfg: dict = load(cfg)
            _cfg["blocked"] = self.config["blocked"]
            _cfg["blocked_roles"] = self.config["blocked_roles"]

        pages = [Page(embeds=embed) for embed in embeds]

        session = Paginator(
            client=self.bot,
            ctx=ctx,
            pages=pages,
            timeout=300,
        )

        dump(_cfg, cfg)

        await session.run()

    @ext_cmd(
        name="whitelist",
        description="Add or remove a user from your guilds whitelist",
        default_member_permissions=Permissions.ADMINISTRATOR | Permissions.MODERATE_MEMBERS,
        dm_permission=False,
        options=[
            Option(
                name="user",
                description="The user to whitelist",
                type=OptionType.USER,
                required=True,
            )
        ],
    )
    @trigger_typing
    async def blocked_whitelist(self, ctx: CommandContext, *, user: Member):

        await ctx.defer(ephemeral=True)

        mention = user.mention
        msg = ""

        if str(user.id) in self.blocked_whitelisted_users(int(ctx.guild_id)):
            embed = Embed(
                title="Success",
                description=f"{mention} is no longer whitelisted.",
                color=self.main_color,
            )
            self.blocked_whitelisted_users(int(ctx.guild_id)).remove(str(user.id))
            with open("config.json", "r+") as cfg:
                _cfg: dict = load(cfg)
                _cfg["blocked_whitelist"] = self.config["blocked_whitelist"]
                dump(_cfg, cfg)
            return await ctx.send(embeds=embed, ephemeral=True)

        if guild_whitelist := self.blocked_whitelisted_users(int(ctx.guild_id)):
            guild_whitelist.append(str(user.id))
        else:
            self.config["blocked_whitelist"][int(ctx.guild_id)] = [str(user.id)]

        for _ in self.blocked_users(int(ctx.guild_id)):
            if str(user.id) in _:
                msg = _.get(str(user.id)) or ""
                del _

            with open("config.json", "r+") as cfg:
                _cfg: dict = load(cfg)
                _cfg["blocked_whitelist"] = self.config["blocked_whitelist"]
                _cfg["blocked"] = self.config["blocked"]
                dump(_cfg, cfg)

        if msg.startswith("System Message: "):
            # If the user is blocked internally (for example: below minimum account age)
            # Show an extended message stating the original internal message
            reason = msg[16:].strip().rstrip(".")
            embed = Embed(
                title="Success",
                description=f"{mention} was previously blocked internally for "
                f'"{reason}". {mention} is now whitelisted.',
                color=self.main_color,
            )
        else:
            embed = Embed(
                title="Success",
                color=self.main_color,
                description=f"{mention} is now whitelisted.",
            )

        return await ctx.send(embeds=embed, ephemeral=True)

    @ext_ucmd(
        name="block",
        default_member_permissions=Permissions.ADMINISTRATOR | Permissions.MODERATE_MEMBERS,
        dm_permission=False,
    )
    @trigger_typing
    async def block(
        self,
        ctx: CommandContext,
    ):
        """
        Block a user or role from using Modmail.

        You may choose to set a time as to when the user will automatically be unblocked.

        Leave `user` blank when this command is used within a
        thread channel to block the current recipient.
        `user` may be a user ID, mention, or name.
        `duration` may be a simple "human-readable" time text. See `{prefix}help close` for examples.
        """

        modal = Modal(
            custom_id="block_modal",
            title="Block a user",
            components=[
                TextInput(
                    custom_id="duration",
                    style=TextStyleType.SHORT,
                    label="The time until the user should be muted",
                    placeholder="'HH:MM DD/MM/YYYY'(i.e 04:20 4/2/2023)",
                    required=True,
                    min_length=16,
                    max_length=16,
                ),
            ],
        )

        await ctx.popup(modal)

        __args = []

        def check(_ctx: CommandContext):
            return _ctx.data.custom_id == "block_modal"

        _context: CommandContext = await wait_for(self.bot, "on_modal", check=check, timeout=300)
        await _context.defer(ephemeral=True)
        if _context.data._json.get("components"):
            for component in _context.data.components:
                if component.get("components"):
                    __args.append([_value["value"] for _value in component["components"]][0])
                else:
                    __args.append([_value.value for _value in component.components][0])

        duration: str
        duration = __args[0]

        rest: str
        hours, rest = duration.split(":")
        minutes, rest = rest.split(" ")
        day, month, year = rest.split("/")

        after = datetime(hour=hours, minute=minutes, day=day, month=month, year=year)

        mention = ctx.target.mention

        if str(ctx.target.id) in self.blocked_whitelisted_users(int(ctx.guild_id)):
            embed = Embed(
                title="Error",
                description=f"Cannot block {mention}, user is whitelisted.",
                color=self.error_color,
            )
            return await _context.send(embeds=embed, ephemeral=True)

        reason = f"by {ctx.author.name}#{ctx.author.user.discriminator}"

        if after is not None:
            if "%" in reason:
                raise ValueError('The reason contains illegal character "%".')
            reason += f" until {after.isoformat()}"

        reason += "."

        msg = None

        if msg is None:
            msg = ""

        if msg:
            old_reason = msg.strip().rstrip(".")
            embed = Embed(
                title="Success",
                description=f"{mention} was previously blocked {old_reason}.\n"
                f"{mention} is now blocked {reason}",
                color=self.main_color,
            )
        else:
            embed = Embed(
                title="Success",
                color=self.bot.main_color,
                description=f"{mention} is now blocked {reason}",
            )

        if guild := self.blocked_users(int(ctx.guild_id)):
            guild.append({str(ctx.target.id): reason})
        else:
            self.config["blocked"][int(ctx.guild_id)] = {str(ctx.target.id): reason}

        with open("config.json", "r+") as cfg:
            _cfg: dict = load(cfg)
            _cfg["blocked"] = self.config["blocked"]
            dump(_cfg, cfg)

        return await _context.send(embeds=embed, ephemeral=True)

    @ext_ucmd(
        name="unblock",
        dm_permission=False,
        default_member_permissions=Permissions.MODERATE_MEMBERS | Permissions.ADMINISTRATOR,
    )
    @trigger_typing
    async def unblock(self, ctx: CommandContext):
        """
        Unblock a user from using Modmail.

        Leave `user` blank when this command is used within a
        thread channel to unblock the current recipient.
        `user` may be a user ID, mention, or name.
        """

        await ctx.get_guild()
        await ctx.defer(ephemeral=True)
        if isinstance(ctx.target, User):
            ctx.target = await ctx.guild.get_member(int(ctx.target.id))

        mention = ctx.target.mention
        name = ctx.target.name
        msg = ""
        if guild := self.blocked_users(int(ctx.guild_id)):
            for item in guild.copy():
                if msg := item.get(str(ctx.target.id)):
                    guild.remove(item)
            if msg == "":
                embed = Embed(
                    title="Error", description=f"{mention} is not blocked.", color=self.error_color
                )

                return await ctx.send(embeds=embed, ephemeral=True)
            if msg.startswith("System Message: "):
                # If the user is blocked internally (for example: below minimum account age)
                # Show an extended message stating the original internal message
                reason = msg[16:].strip().rstrip(".") or "no reason"
                embed = Embed(
                    title="Success",
                    description=f"{mention} was previously blocked internally {reason}.\n"
                    f"{mention} is no longer blocked.",
                    color=self.main_color,
                )
                embed.set_footer(
                    text="However, if the original system block reason still applies, "
                    f"{name} will be automatically blocked again. "
                    f'Use "/whitelist" to whitelist the user.'
                )
            else:
                embed = Embed(
                    title="Success",
                    color=self.main_color,
                    description=f"{mention} is no longer blocked.",
                )
            with open("config.json", "r+") as cfg:
                _cfg: dict = load(cfg)
                _cfg["blocked"] = self.config["blocked"]
                dump(_cfg, cfg)
        else:
            embed = Embed(
                title="Error", description=f"{mention} is not blocked.", color=self.error_color
            )
        return await ctx.send(embeds=embed, ephemeral=True)

    @ext_mcmd(
        name="Delete",
        default_member_permissions=Permissions.ADMINISTRATOR | Permissions.MODERATE_MEMBERS,
        dm_permission=False,
    )
    async def delete(self, ctx: CommandContext):
        """
        Delete a message that was sent using the reply command or a note.

        Deletes the previous message, unless a message ID is provided,
        which in that case, deletes the message with that message ID.

        Notes can only be deleted when a note ID is provided.
        """
        thread = await self.threads.find(channel=await ctx.get_channel())
        message_id = ctx.target.id
        try:
            await thread.delete_message(message_id, note=True)
        except ValueError as e:
            logger.warning("Failed to delete message: %s.", e)
            return await ctx.send(
                embeds=Embed(
                    title="Failed",
                    description="Cannot find a message to delete. Plain messages are not supported.",
                    color=self.error_color,
                ),
                ephemeral=True,
            )

    # I don't think we need a repair command - prove it otherwise if you want so

    @ext_cmd(
        name="enable",
        description="Re-enables DM functionalities of Modmail.",
        default_member_permissions=Permissions.ADMINISTRATOR,
        dm_permission=False,
    )
    async def enable(self, ctx: CommandContext):
        embed = Embed(
            title="Success",
            description="Modmail will now accept all DM messages.",
            color=self.main_color,
        )
        await ctx.defer(ephemeral=True)
        if self.config["dm_disabled"].get(int(ctx.guild_id), DMDisabled.NONE) != DMDisabled.NONE:
            self.config["dm_disabled"][int(ctx.guild_id)] = DMDisabled.NONE

        with open("config.json", "r+") as cfg:
            _cfg: dict = load(cfg)
            _cfg["dm_disabled"] = self.config["dm_disabled"]
            dump(_cfg, cfg)

        return await ctx.send(embeds=embed, ephemeral=True)

    @ext_cmd(
        name="disable",
        description="Disable partial or full Modmail thread functions.",
        default_member_permissions=Permissions.ADMINISTRATOR,
        dm_permission=False,
        options=[
            Option(
                name="choice",
                description="What functions you exactly want to disable",
                required=True,
                type=OptionType.STRING,
                choices=[
                    Choice(name="Stop accepting new Modmail threads.", value="new"),
                    Choice(
                        name="Disables all DM functionalities of Modmail.",
                        value="all",
                    ),
                ],
            )
        ],
    )
    async def disable(self, ctx: CommandContext, choice: str):
        await ctx.defer(ephemeral=True)

        if choice == "new":
            embed = Embed(
                title="Success",
                description="Modmail will not create any new threads.",
                color=self.main_color,
            )
            if (
                self.config["dm_disabled"].get(int(ctx.guild_id), DMDisabled.NONE)
                < DMDisabled.NEW_THREADS
            ):
                self.config["dm_disabled"][int(ctx.guild_id)] = DMDisabled.NEW_THREADS

            with open("config.json", "r+") as cfg:
                _cfg: dict = load(cfg)
                _cfg["dm_disabled"] = self.config["dm_disabled"]
                dump(_cfg, cfg)

            return await ctx.send(embeds=embed, ephemeral=True)
        elif choice == "all":
            embed = Embed(
                title="Success",
                description="Modmail will not accept any DM messages.",
                color=self.main_color,
            )

            if (
                self.config["dm_disabled"].get(int(ctx.guild_id), DMDisabled.NONE)
                != DMDisabled.ALL_THREADS
            ):
                self.config["dm_disabled"][int(ctx.guild_id)] = DMDisabled.ALL_THREADS

            with open("config.json", "r+") as cfg:
                _cfg: dict = load(cfg)
                _cfg["dm_disabled"] = self.config["dm_disabled"]
                dump(_cfg, cfg)

            return await ctx.send(embeds=embed, ephemeral=True)

    @ext_cmd(
        name="check_enable",
        description="Check if the DM functionalities of Modmail is enabled.",
        default_member_permissions=Permissions.ADMINISTRATOR,
        dm_permission=False,
    )
    async def isenable(self, ctx: CommandContext):

        if (
            self.config["dm_disabled"].get(int(ctx.guild_id), DMDisabled.NONE)
            == DMDisabled.NEW_THREADS
        ):
            embed = Embed(
                title="New Threads Disabled",
                description="Modmail is not creating new threads.",
                color=self.error_color,
            )
        elif (
            self.config["dm_disabled"].get(int(ctx.guild_id), DMDisabled.NONE)
            == DMDisabled.ALL_THREADS
        ):
            embed = Embed(
                title="All DM Disabled",
                description="Modmail is not accepting any DM messages for new and existing threads.",
                color=self.error_color,
            )
        else:
            embed = Embed(
                title="Enabled",
                description="Modmail now is accepting all DM messages.",
                color=self.main_color,
            )

        return await ctx.send(embeds=embed, ephemeral=True)

        # TODO : add all key configurable


def setup(bot: Client, guild_id: Optional[Union[int, List[int]]] = None):
    Modmail(bot, guild_id)
