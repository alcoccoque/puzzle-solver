"""This module contains the routes for the puzzle solver."""

from typing import Any

from fastapi import APIRouter, HTTPException
from starlette import status

from app.dependencies.core import DBSessionDep
from app.dependencies.user import CurrentUserDep
from app.orm import matrix as matrix_orm
from app.puzzle_solver import FieldState, PuzzleGenerator, PuzzleSolver
from app.schemas.matrix import CreateMatrix, ShowMatrix, SolveMatrix

router = APIRouter(prefix="/api", tags=["puzzle_solver"])


@router.post(
    "/solve",
    response_model=ShowMatrix,
    status_code=status.HTTP_200_OK,
)
async def solve_matrix(
    solve_matrix_schema: SolveMatrix,
    db: DBSessionDep,
    user: CurrentUserDep,
) -> Any:
    """Solve the matrix and return the solved puzzle."""
    try:
        result = FieldState.from_list_to_state(solve_matrix_schema.rows)
        if state := result.get("state"):
            solver = PuzzleSolver(state)
            result = solver.solve()
            solved_puzzle = result.get("solved_puzzle")
            if solved_puzzle:
                new_matrix = CreateMatrix(coordinates=solved_puzzle, user_id=user.id)
                matrix = await matrix_orm.create_matrix(matrix_data=new_matrix, db=db)
                return matrix
        raise HTTPException(status_code=400, detail=result.get("error"))
    except HTTPException as e:
        await db.rollback()
        raise e
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get(
    "/generate",
    response_model=ShowMatrix,
    status_code=status.HTTP_200_OK,
)
async def generate_matrix(
    size: int,
    filled_percentage: float,
    db: DBSessionDep,
    user: CurrentUserDep,
) -> Any:
    """Generate a new matrix."""
    try:
        generator = PuzzleGenerator(size)
        board = generator.generate_puzzle(filled_percentage)

        new_matrix = CreateMatrix(coordinates=board, user_id=user.id)
        matrix = await matrix_orm.create_matrix(matrix_data=new_matrix, db=db)
        return matrix
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
