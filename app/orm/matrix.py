"""Matrix ORM functions."""

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.matrix import Matrix
from app.schemas.matrix import CreateMatrix


async def create_matrix(matrix_data: CreateMatrix, db: AsyncSession):
    """Create a new matrix."""
    query = (
        insert(Matrix)
        .values(coordinates=matrix_data.coordinates, user_id=matrix_data.user_id)
        .returning(Matrix)
    )
    result = await db.execute(query)
    created_matrix = result.scalar()
    await db.commit()
    return created_matrix
