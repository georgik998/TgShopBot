from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text
from tg_bot.infra.database.config import postgresql_settings
from tg_bot.infra.database.models import Base

# Извлекаем параметры подключения из настроек
user = postgresql_settings.POSTGRES_USER
password = postgresql_settings.POSTGRES_PASSWORD
host = postgresql_settings.POSTGRES_HOST
port = postgresql_settings.POSTGRES_PORT
dbname = postgresql_settings.POSTGRES_DB
timezone = postgresql_settings.POSTGRES_TIMEZONE
init_sql_file_path = postgresql_settings.DATABASE_INIT_SQL_FILE_PATH

DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=50,
    max_overflow=5,
)

async_session = async_sessionmaker(
    engine, expire_on_commit=False,
)


async def reset_database():
    async with async_session() as session:
        await session.execute(text("""CREATE OR REPLACE FUNCTION generate_short_id_for_ref_links() RETURNS TEXT AS $$
DECLARE
    chars TEXT := 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    new_id TEXT;
	exists_flag INT;
BEGIN
    LOOP
        new_id := '';
        FOR i IN 1..8 LOOP
            new_id := new_id || substr(chars, (floor(random() * length(chars)) + 1)::INT, 1);
        END LOOP;

        -- Проверка уникальности
        EXECUTE 'SELECT 1 FROM ref_links WHERE id = $1 LIMIT 1' INTO exists_flag USING new_id;
		IF exists_flag IS NULL THEN
		    RETURN new_id;
		END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;"""))
        await session.execute(text("""CREATE OR REPLACE FUNCTION generate_short_id_for_user_purchases() RETURNS TEXT AS $$
DECLARE
    chars TEXT := 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    new_id TEXT;
    exists_flag INT;
BEGIN
    LOOP
        new_id := '';
        FOR i IN 1..12 LOOP
            new_id := new_id || substr(chars, (floor(random() * length(chars)) + 1)::INT, 1);
        END LOOP;

        -- Проверка уникальности
        EXECUTE 'SELECT 1 FROM user_purchases WHERE id = $1 LIMIT 1' INTO exists_flag USING new_id;
        IF exists_flag IS NULL THEN
            RETURN new_id;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;"""))
        await session.commit()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        """
        Настройка конфига посгре блять его sql, часовой пояс, базовые данные
        """
        await session.execute(text(f"SET TIMEZONE TO '{timezone}'"))

        await session.execute(text("INSERT INTO texts (start) VALUES('/start');"))
        await session.execute(text("INSERT INTO contacts (owner) VALUES ('https://t.me/fagerewaader')"))
        await session.execute(text("INSERT INTO banners (id) VALUES(1)"))
        await session.execute(
            text(
                'INSERT INTO users (tg_id,father_id, is_admin, balance) VALUES(1190261959,1190261959, TRUE,77777);'))
        await session.execute(text('INSERT INTO notify_channels (id) VALUES(1);'))
        await session.commit()
