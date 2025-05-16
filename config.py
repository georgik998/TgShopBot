from pydantic_settings import BaseSettings

back_button_style = '‹ Назад'
cancel_button_style = '⛌ Отменить'
pagination_next_page_style = '›'
pagination_last_page_style = '»'
pagination_previous_page_style = '‹'
pagination_first_page_style = '«'
element_on_page_in_profile_purchases = 10

caption_len_limit = 1024

base_photo_id = 'AgACAgIAAxkBAAIjoWgkqoKaUEA8aBO6FN4XdlXQ7JjnAAKx7TEbEP8pScLUgTktsdrLAQADAgADeAADNgQ'

dotenv_path = 'tg_bot/.env'

is_reset_database = False


class BotSettings(BaseSettings):
    BOT_API_TOKEN: str
    BOT_URL: str

    class Config:
        env_file = dotenv_path
        extra = "allow"


bot_settings = BotSettings()
