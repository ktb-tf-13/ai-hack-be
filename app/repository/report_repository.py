from sqlalchemy.ext.asyncio import AsyncSession
from app.model.models import WeeklyReport

class ReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_weekly_report(self, user_id: str, year: int, week: int, summary: str, feedback: str):
        report = WeeklyReport(
            user_id=user_id,
            year=year,
            week=week,
            summary=summary,
            feedback=feedback
        )
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        return report

    async def get_weekly_report(self, user_id: str, year: int, week: int) -> WeeklyReport:
        from sqlalchemy import select
        result = await self.db.execute(
            select(WeeklyReport)
            .where(
                WeeklyReport.user_id == user_id,
                WeeklyReport.year == year,
                WeeklyReport.week == week
            )
        )
        return result.scalars().first()
