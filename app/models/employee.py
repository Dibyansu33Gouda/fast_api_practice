from sqlalchemy import String , ForeignKey
from sqlalchemy.orm import Mapped , mapped_column , relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.departments import Department00

class Employee(Base):
    __tablename__="employees"
    
    id: Mapped[int] =mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(100))
    email: Mapped[str]=mapped_column(String(100),unique=True)
    department_id:Mapped[int]=mapped_column(ForeignKey("departments.id"))
    
    department:Mapped["Department"]=relationship(back_populates="employees")
    