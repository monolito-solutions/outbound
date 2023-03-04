from uuid import UUID
from modules.despachos.domain.entities import Despacho
from .dtos import DespachoDTO


class DespachosRepositorySQLAlchemy:

    def __init__(self, db) -> None:
        self.db = db

    def get_by_id(self, id: UUID) -> Despacho:
        despachos_dto = self.db.session.query(DespachoDTO).filter_by(id=str(id)).one()
        return Despacho(**despachos_dto.to_dict())

    def create(self, Despacho: Despacho):
        despacho_dto = DespachoDTO(**Despacho.to_dict())
        self.db.add(despacho_dto)
        self.db.commit()
        self.db.refresh(despacho_dto)
        return despacho_dto

    def delete(self, id: UUID):
        # TODO
        raise NotImplementedError
