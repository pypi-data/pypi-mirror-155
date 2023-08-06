import datetime
import logging
import os
from enum import Enum
from typing import List, Optional, Dict

import discord
from discord.ext.commands import Context, Bot, Cog, command
from discord_ext_commands_coghelper import CogHelper
from discord_ext_commands_coghelper.utils import (
    Constant,
    to_utc_naive,
    get_list,
    get_bool,
    get_before_after_fmts,
    get_corrected_before_after_str,
)

logger = logging.getLogger(__name__)


class _SortOrder(Enum):
    ASCENDING = 1
    DESCENDING = 2

    @staticmethod
    def parse(value: str):
        return _SortOrder.DESCENDING if value == "descending" else _SortOrder.ASCENDING

    @staticmethod
    def reverse(value) -> bool:
        return True if value == _SortOrder.DESCENDING else False


class _EmojiCountType(Enum):
    MESSAGE_CONTENT = 1
    MESSAGE_REACTION = 2


class _EmojiCounter:
    def __init__(self, emoji: discord.Emoji):
        self._emoji = emoji
        self._rank = 0
        self._counts = {t: 0 for t in _EmojiCountType}

    def increment(self, count_type: _EmojiCountType):
        self._counts[count_type] += 1

    @property
    def emoji(self) -> discord.Emoji:
        return self._emoji

    @property
    def rank(self) -> int:
        return self._rank

    @rank.setter
    def rank(self, value):
        self._rank = value

    @property
    def content_count(self) -> int:
        return self._counts[_EmojiCountType.MESSAGE_CONTENT]

    @property
    def reaction_count(self) -> int:
        return self._counts[_EmojiCountType.MESSAGE_REACTION]

    @property
    def total_count(self) -> int:
        return sum(self._counts.values())


class _Constant(Constant):
    TIMEZONE_OFFSET = int(os.environ.get("DISCORD_EMOJI_RANKING_TIMEZONE_OFFSET", 0))
    TZ = datetime.timezone(datetime.timedelta(hours=TIMEZONE_OFFSET))
    DATE_FORMAT_SLASH = "%Y/%m/%d"
    DATE_FORMAT_HYPHEN = "%Y-%m-%d"
    DATE_FORMATS = [DATE_FORMAT_SLASH, DATE_FORMAT_HYPHEN]
    DEFAULT_RANK: int = 10


def _get_times_str(count: int) -> str:
    if count == 1:
        return "1 time"
    return f"{count} times"


def _get_rank_str(rank: int) -> str:
    if rank == 1:
        return "1st"
    if rank == 2:
        return "2nd"
    if rank == 3:
        return "3rd"
    return f"{rank}th"


class EmojiRanking(Cog, CogHelper):
    def __init__(self, bot: Bot):
        CogHelper.__init__(self, bot)
        self._channel_ids: List[int]
        self._before: Optional[datetime.datetime] = None
        self._after: Optional[datetime.datetime] = None
        self._order = _SortOrder.ASCENDING
        self._rank = _Constant.DEFAULT_RANK
        self._contains_bot = False

    @command()
    async def emoji_ranking(self, ctx, *args):
        await self.execute(ctx, args)

    def _parse_args(self, ctx: Context, args: Dict[str, str]):
        self._channel_ids = get_list(args, "channel", ",", lambda value: int(value), [])
        self._before, self._after = get_before_after_fmts(
            ctx, args, *_Constant.DATE_FORMATS, tz=_Constant.TZ
        )
        self._order = _SortOrder.parse(args.get("order", ""))
        self._rank = int(args.get("rank", _Constant.DEFAULT_RANK))
        self._contains_bot = get_bool(args, "bot", False)

    async def _execute(self, ctx: Context):
        before = to_utc_naive(self._before)
        after = to_utc_naive(self._after)

        counters = [_EmojiCounter(emoji) for emoji in ctx.guild.emojis]

        channels = (
            [ctx.guild.get_channel(channel_id) for channel_id in self._channel_ids]
            if len(self._channel_ids) > 0
            else ctx.guild.channels
        )
        channels = [
            channel
            for channel in channels
            if channel is not None and isinstance(channel, discord.TextChannel)
        ]
        for channel in channels:
            logger.debug(f"count emoji in {channel.name} channel.")
            try:
                messages = [
                    message
                    async for message in channel.history(
                        limit=None, before=before, after=after
                    )
                ]
            except discord.Forbidden as e:
                # BOTに権限がないケースはログを出力して続行
                logger.warning(f"exception={e}, channel={channel}")
            else:
                counters = await self.count_emojis(counters, messages)

        rank = max(1, min(self._rank, len(ctx.guild.emojis)))
        sorted_counters = self.sort_ranking(counters, rank)

        # Embed生成
        if self._order == _SortOrder.DESCENDING:
            title = f"Emoji Usage Ranking Top {rank}"
        else:
            title = f"Emoji Usage Ranking Top {rank} Worst"
        before_str, after_str = get_corrected_before_after_str(
            self._before, self._after, ctx.guild, _Constant.TZ, *_Constant.DATE_FORMATS
        )
        description = f"{after_str} ~ {before_str}"
        embed = discord.Embed(title=title, description=description)
        for counter in sorted_counters:
            name = f"{_get_rank_str(counter.rank)} {counter.emoji} Total: {_get_times_str(counter.total_count)}"
            value = f"In Messages: {counter.content_count} Reactions: {counter.reaction_count}"
            embed.add_field(name=name, value=value, inline=False)

        # 集計結果を送信
        logger.debug("send result")
        await ctx.send(embed=embed)
        await ctx.send(" ".join([str(counter.emoji) for counter in sorted_counters]))

    async def count_emojis(
        self, counters: List[_EmojiCounter], messages: List[discord.Message]
    ) -> List[_EmojiCounter]:
        for message in messages:
            for counter in counters:
                # メッセージ内に使われているかのカウント
                if counter.emoji.name in message.content:
                    # BOTを弾く
                    if self._contains_bot or not message.author.bot:
                        counter.increment(_EmojiCountType.MESSAGE_CONTENT)
                # リアクションに使われているかのカウント
                for reaction in message.reactions:
                    if not isinstance(reaction.emoji, discord.Emoji):
                        continue
                    if reaction.emoji.id != counter.emoji.id:
                        continue
                    # BOTを弾く
                    if not self._contains_bot and all(
                        [user.bot async for user in reaction.users()]
                    ):
                        continue
                    counter.increment(_EmojiCountType.MESSAGE_REACTION)
        return counters

    def sort_ranking(
        self, counters: List[_EmojiCounter], slice_num: int
    ) -> List[_EmojiCounter]:
        # ソートした上で要求された順位までの要素数に切り取る
        reverse = _SortOrder.reverse(self._order)
        sorted_counters = sorted(
            counters, key=lambda c: c.total_count, reverse=reverse
        )[0:slice_num]

        # 同順位を考慮した順位付け
        for index, counter in enumerate(sorted_counters):
            rank = index + 1
            if index > 0:
                prev = sorted_counters[index - 1]
                if prev.total_count == counter.total_count:
                    rank = prev.rank

            counter.rank = rank

        return sorted_counters


def setup(bot: Bot):
    return bot.add_cog(EmojiRanking(bot))
