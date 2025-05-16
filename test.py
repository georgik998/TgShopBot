from aiogram import Bot

from asyncio import run


async def main():
    message = await Bot('8194187894:AAGmqMe6Nw0oZn9f77UpciKR4qf8GatZZ1w').send_message(
        chat_id=1190261959,
        text="""<b>1</b>
<i>2</i>
<u>3</u>
<s>4</s>
<code>5</code> 
<pre>6</pre>
<span class="tg-spoiler">твой скрытый текст</span>
<blockquote>7</blockquote>
""",
        parse_mode='HTML'
    )
    print(message.entities)


run(main())
