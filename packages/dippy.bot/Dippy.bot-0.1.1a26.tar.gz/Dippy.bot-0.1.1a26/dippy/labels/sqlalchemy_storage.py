from __future__ import annotations
from ast import literal_eval
from dippy.labels.storage import StorageInterface, NOT_SET, Label
from dippy.sqlalchemy_connector import SQLAlchemyConnector
from sqlalchemy import Column, Integer, String, BigInteger
from typing import Any, Optional
import asyncio


class LabelModel(SQLAlchemyConnector.BaseModel):
    __tablename__ = "dippy_labels"

    id = Column(Integer, primary_key=True)
    object_id = Column(BigInteger, nullable=False)
    object_type = Column(String(32), nullable=False)
    key = Column(String(256), nullable=False)
    value = Column(String(2048), nullable=False)


class SQLAlchemyStorage(StorageInterface):
    db: SQLAlchemyConnector

    async def delete(self, object_type: str, object_id: int, key: str):
        await asyncio.get_running_loop().run_in_executor(
            None, self._delete, object_type, object_id, key
        )

    def _delete(self, object_type, object_id, key):
        with self.db.session() as session:
            session.query(LabelModel).filter(
                (LabelModel.object_id == object_id)
                & (LabelModel.object_type == object_type)
                & (LabelModel.key == key)
            ).delete()
            session.commit()

    async def find(
        self,
        object_type: Optional[str] = None,
        object_id: Optional[int] = None,
        *,
        key: Optional[str] = None,
        value: Any = NOT_SET,
    ) -> list[Label]:
        return await asyncio.get_running_loop().run_in_executor(
            None, self._find, object_type, object_id, key, value
        )

    def _find(self, object_type, object_id, key, value):
        with self.db.session() as session:
            query = session.query(LabelModel)
            if object_type:
                query = query.filter(LabelModel.object_type == object_type)
            if object_id:
                query = query.filter(LabelModel.object_id == object_id)
            if key:
                query = query.filter(LabelModel.key == key)

            session.expunge_all()
            return [
                Label(row.object_type, row.object_id, row.key, literal_eval(row.value))
                for row in query.all()
                if value is NOT_SET or literal_eval(row.value) == value
            ]

    async def get(
        self, object_type: str, object_id: int, key: str, default: Any = None
    ) -> Any:
        return await asyncio.get_running_loop().run_in_executor(
            None, self._get, object_type, object_id, key, default
        )

    def _get(self, object_type, object_id, key, default):
        result = self._get_from_db(object_type, object_id, key)
        return literal_eval(result.value) if result else default

    async def has(self, object_type: str, object_id: int, key: str) -> bool:
        return await asyncio.get_running_loop().run_in_executor(
            None, self._has, object_type, object_id, key
        )

    def _has(self, object_type, object_id, key):
        with self.db.session() as session:
            count = (
                session.query(LabelModel)
                .filter(
                    (LabelModel.object_type == object_type)
                    & (LabelModel.object_id == object_id)
                    & (LabelModel.key == key)
                )
                .count()
            )
            return count > 0

    async def set(self, object_type: str, object_id: int, key: str, value: Any):
        await asyncio.get_running_loop().run_in_executor(
            None, self._set, object_type, object_id, key, value
        )

    def _set(self, object_type, object_id, key, value):
        label = self._get_from_db(object_type, object_id, key)
        with self.db.session() as session:
            if label:
                label.value = repr(value)
                session.add(label)
            else:
                label = LabelModel(
                    object_type=object_type,
                    object_id=object_id,
                    key=key,
                    value=repr(value),
                )
            session.add(label)
            session.commit()

    async def setup(self):
        return

    def _get_from_db(self, object_type: str, object_id: int, key: str) -> LabelModel:
        with self.db.session() as session:
            result: LabelModel = (
                session.query(LabelModel)
                .filter(
                    (LabelModel.object_type == object_type)
                    & (LabelModel.object_id == object_id)
                    & (LabelModel.key == key)
                )
                .first()
            )
            session.expunge_all()
            return result
