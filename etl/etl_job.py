import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Story
from app.utils import fetch_top_story_ids, fetch_story_details, log_error
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

# PostgreSQL connection settings
DB_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Ensure tables exist
Base.metadata.create_all(engine)

def upsert_story(data):
    try:
        existing_story = session.query(Story).filter_by(id=data["id"]).first()
        if existing_story:
            if existing_story.score != data["score"] or existing_story.descendants != data["descendants"]:
                print(f"Updated story {data['id']}, score: {existing_story.score} → {data['score']}, descendants: {existing_story.descendants} → {data['descendants']}")
                existing_story.score = data["score"]
                existing_story.descendants = data["descendants"]
                session.commit()
        else:
            story = Story(**data)
            session.add(story)
            session.commit()
    except Exception as e:
        log_error(session, data.get("id"), f"Error inserting/updating story: {e}")
        session.rollback()

def run_etl():
    print("🚀 Starting ETL job")
    try:
        story_ids = fetch_top_story_ids(session)
        for story_id in story_ids[:100]:
            data = fetch_story_details(session, story_id)
            if data:
                upsert_story(data)
        print("✅ ETL job completed")
    finally:
        session.close()

if __name__ == "__main__":
    run_etl()
