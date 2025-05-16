# tags = {
#     'bold': {
#         'open': '<b>',
#         'close': '</b>'
#     },
#     'italic': {
#         'open': '<i>',
#         'close': '</i>'
#     },
#     'underline': {
#         'open': '<u>',
#         'close': '</u>'
#     },
#     'strikethrough': {
#         'open': '<del>',
#         'close': '</del>'
#     },
#     'blockquote': {
#         'open': '<blockquote>',
#         'close': '</blockquote>'
#     },
#     'pre': {
#         'open': '<code>',
#         'close': '</code>'
#     },
#     'spoiler': {
#         'open': '<span class="tg-spoiler">',
#         'close': '</span>'
#     }
# }
# shift = 0
# # text = message.text
# # entities = message.entities
# if entities:
#     for entity in entities:
#         offset = entity.offset
#         length = entity.length
#         type = entity.type
#         if type == 'text_link':
#             open_tag, close_tag = f'<a href="{entity.url}">', '</a>'
#         else:
#             open_tag, close_tag = tags[type]['open'], tags[type]['close']
#         text = text[:offset + shift] + open_tag + text[offset + shift:offset + shift + length] + close_tag + text[
#                                                                                                              offset + shift + length:]
#         shift += len(open_tag) + len(close_tag)


from aiogram.types import Message
from html import escape


def parse_text(message: Message) -> str:
    """
    Корректно возвращает текст с HTML-тегами, учитывая UTF-16 смещения Telegram (для emoji)
    """
    if not message.text or not message.entities:
        return message.text or ""

    raw_text = message.text
    utf16_text = raw_text.encode("utf-16-le")
    result = ""
    last_offset = 0

    def utf16_index_to_str_index(utf16_bytes: bytes, utf16_index: int) -> int:
        """Переводит индекс в UTF-16 кодовых единицах в индекс Python строки"""
        return len(utf16_bytes[:utf16_index * 2].decode("utf-16-le"))

    for entity in message.entities:
        start = utf16_index_to_str_index(utf16_text, entity.offset)
        end = utf16_index_to_str_index(utf16_text, entity.offset + entity.length)

        result += escape(raw_text[last_offset:start])

        content = escape(raw_text[start:end])
        if entity.type == "bold":
            result += f"<b>{content}</b>"
        elif entity.type == "italic":
            result += f"<i>{content}</i>"
        elif entity.type == "underline":
            result += f"<u>{content}</u>"
        elif entity.type == "strikethrough":
            result += f"<s>{content}</s>"
        elif entity.type == "code":
            result += f"<code>{content}</code>"
        elif entity.type == "pre":
            result += f"<pre>{content}</pre>"
        elif entity.type == "text_link" and entity.url:
            result += f'<a href="{escape(entity.url)}">{content}</a>'
        else:
            result += content

        last_offset = end

    result += escape(raw_text[last_offset:])
    return result
