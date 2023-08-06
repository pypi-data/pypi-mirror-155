from bevy import Context, Factory, Injectable
from dippy.config import Config
from dippy.sqlalchemy_connector import SQLAlchemyConnector
from dippy.labels.memory_storage import MemoryStorage
from dippy.labels.sqlalchemy_storage import SQLAlchemyStorage
from dippy.labels.config_model import LabelConfigModel, DatabaseConfigModel
from dippy.events import EventHub
from dippy.extensions.extension_manager import ExtensionManager
from dippy.logging import Logging
from nextcord import Intents
from nextcord.ext.commands import Bot
from pathlib import Path
import dippy.config.json_loader
import dippy.config.yaml_loader


class Client(Bot, Injectable):
    config: Config
    context: Context
    events: EventHub
    extension_manager: ExtensionManager
    log_factory: Factory[Logging]

    def __init__(self, name: str = "Dippy.bot", *args, **kwargs):
        if "intents" not in kwargs:
            kwargs["intents"] = self._build_intents()
        super().__init__(*args, **kwargs)
        Logging.setup_logger()

        self.log = self.log_factory(name)

    def dispatch(self, event_name, *args, **kwargs):
        super(Client, self).dispatch(event_name, *args, **kwargs)
        self.events.emit(event_name, *args, *kwargs)

    async def on_ready(self):
        self.log.info("Bot is ready")

    def run(self, *args, **kwargs):
        self._setup_labels()
        self.loop.call_soon(self._setup_extensions)
        super().run(*args, **kwargs)

    def _build_intents(self) -> Intents:
        config = self.config.get("intents", default={})
        intents = Intents.default() if config.pop("use_defaults", False) else Intents()
        for intent, value in config.items():
            setattr(intents, intent, value)
        return intents

    def _setup_extensions(self):
        self.extension_manager.load_extensions()
        self.extension_manager.create_extensions()

    def _setup_labels(self):
        label_config = self.config.get("labels", LabelConfigModel, LabelConfigModel())
        storage_type = MemoryStorage
        if label_config.storage == "sqlalchemy":
            self.log.info(
                f"Connecting database: {self._build_db_url(label_config.database, True)}"
            )
            database_url = self._build_db_url(label_config.database)
            db = SQLAlchemyConnector(database_url)
            db.create_tables()
            self.context.add(db)
            storage_type = SQLAlchemyStorage

        self.context.add(self.context.create(storage_type))

    def _build_db_url(self, db: DatabaseConfigModel, obscure_password: bool = False):
        url = f"{db.engine}://"
        if db.username:
            url += db.username
            if db.password:
                url += f":{'******' if obscure_password else db.password}"
            url += "@"
        url += db.host
        if db.database:
            url += f"/{db.database}"
        return url

    @classmethod
    def launch(
        cls, token: str = None, config: tuple[str] = ("bot.json",), *args, **kwargs
    ):
        config_files = []
        for file in config:
            path = Path(file)
            if path.exists():
                print(f">>> Adding {path.resolve()}")
                config_files.append(path.resolve())

        if not config_files:
            raise ValueError(
                f"Unable to find any config files: {config} - {Path().resolve()}"
            )

        context = Context()
        context.add(Config(*config_files))
        client = context.create(cls, *args, **kwargs)
        context.add(client)
        client.run(token)
