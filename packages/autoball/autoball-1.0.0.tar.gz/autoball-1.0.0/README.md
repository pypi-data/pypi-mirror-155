# Autoball

This module simply just automatically generates random 8ball choices.

## Installation

`pip install autoball`

## Usage/Example

```py
from autoball import Auto

# Ver is the version of the 8ball choices, will be listed below.
print(Auto.randoball(ver))
```

### Custom Usage

You can also create custom responses.
```py
from autoball import Custom

print(Custom.customball(["Hello World", "Testing, Testing!"])) 
# Will only work if you put it in an array though.
```

### Discord.py Usage/Example

```py
# I'm not writing an entire 8ball command, but here is how to send it.
from discord.ext import commands
from autoball import Auto

bot = commands.Bot("all your stuff here.")

@bot.command()
async def _8ball(ctx):
  await ctx.send(Auto.randoball("normal")) # Normal Ver

bot.run("token here.")
```

## Versions

- `normal` | More normal responses.
- `uwu` | Normal but uwu translated responses.
- `caesar` | Default responses but caesar encrypted.

## Authors|Credits

`Fruitsy - Main Programmer & Founder - (Fruitsy#3809, https://github.com/ItzBlueBerries/)`

## License

Copyright (c) 2022 Fruitsy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.