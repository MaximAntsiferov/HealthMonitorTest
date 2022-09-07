import sqlalchemy as sa
import databases
from source.settings import settings


database = databases.Database(settings.database_url)
metadata = sa.MetaData()

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("email", sa.String(50), unique=True),
    sa.Column("created_at", sa.Date),
    sa.Column("updated_at", sa.Date),
    sa.Column("hashed_password", sa.String),

)

tests = sa.Table(
    "tests",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("user", sa.Integer, sa.ForeignKey('users.id')),
    sa.Column("created_at", sa.Date),
    sa.Column("updated_at", sa.Date),
    sa.Column("acet", sa.Integer),
    sa.Column("keto", sa.Integer),
    sa.Column("rpm", sa.Integer),
)

engine = sa.create_engine(settings.database_url, echo=True)