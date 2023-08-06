# discord-emoji-ranking
![Downloads](https://img.shields.io/pypi/dm/discord-emoji-ranking)
![PyPI](https://img.shields.io/pypi/v/discord-emoji-ranking.svg)
![Licence](https://img.shields.io/pypi/l/discord-emoji-ranking.svg)

Discord BOT to provide usage ranking of custom emoji.

## Features
![images](https://github.com/jukey17/discord-emoji-ranking/blob/images/images/features_001.png?raw=true)

## Installation

```
pip isntall discord-emoji-ranking
```

## How to use

### commands
```
/emoji_ranking channel={CHANNEL_ID...} before={YYYY/mm/dd} after={YYYY/mm/dd} order={ascending|descending} rank={1-25} bot={True|False}`
```
### arguments

| param   | description                                                             | default             | required |
|---------|-------------------------------------------------------------------------|---------------------|----------|
| channel | Filter channels. (multiple channels can be specified by separating `,`) | None(all channels)  | optional |
| before  | Retrieve messages before this date.                                     | None(server opened) | optional |
| after   | Retrieve messages after this date.                                      | None(now)           | optional |
| order   | Sort order of ranking. (ascending or descending)                        | ascending           | optional |
| rank    | Number of rankings displayed. (1-25)                                    | 10                  | optional |
| bot     | Includes BOT messages/reactions.                                        | False               | optional |

### examples

#### `/emoji_ranking`
for all channels and all times.

#### `/emoji_ranking channel=000000000000000000 before=2022/01/31 after=2022/01/01`
in channel(id=000000000000000000), 2022/01/01 to 2022/01/31

#### `/emoji_ranking order=5 order=descending`
for all channels and all times.
sort order is descending.
number of ranking displayed is 5.
