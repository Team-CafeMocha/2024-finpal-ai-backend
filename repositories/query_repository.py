from typing import Optional

from entities import QueryEntity
from models.query import (Query, QueryCreate)
from sqlalchemy.orm import Session
from database import SessionLocal


class QueryRepository:
    db: Session = SessionLocal()

    def create_query(self, queryCreate: QueryCreate) ->  Optional[Query]:
        db_chat = QueryEntity(**queryCreate.model_dump())
        self.db.add(db_chat)
        self.db.commit()
        self.db.refresh(db_chat)
        return Query.model_validate(db_chat)

    def read_query(self, query_id: int) ->  Optional[Query]:
        db_query = self.db.query(QueryEntity).filter_by(id=query_id).first()
        query = Query.model_validate(db_query)
        return query

    def update_query(self, query: Query) -> Optional[Query]:
        db_query_query = self.db.query(QueryEntity).filter_by(id=query.id)
        if db_query_query is None: return None
        db_query = db_query_query.first()
        db_query_query.update(query.model_dump())
        self.db.commit()
        self.db.refresh(db_query)
        return Query.model_validate(db_query)

    def delete_query(self, query_id: int) ->  Optional[Query]:
        db_query_query = self.db.query(QueryEntity).filter_by(id=query_id)
        if db_query_query is None: return None
        query = Query.model_validate(db_query_query.first())
        db_query_query.delete()
        self.db.commit()
        return query
