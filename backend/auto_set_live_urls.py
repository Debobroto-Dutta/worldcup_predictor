"""
Automatically set live streaming URLs for matches that have started
This runs periodically to ensure all started matches have live URLs
"""
from datetime import datetime
from backend.models import db, Match


def auto_set_live_urls(app):
    """
    Automatically set live streaming URLs for matches that have started
    but don't have a URL yet
    """
    with app.app_context():
        try:
            # Find matches that have started but don't have live URLs
            now = datetime.utcnow()
            matches_without_urls = Match.query.filter(
                Match.match_date <= now,
                Match.live_stream_url == None
            ).all()
            
            if not matches_without_urls:
                print("ℹ️  All started matches already have live URLs")
                return 0
            
            updated_count = 0
            for match in matches_without_urls:
                # Set default live stream URL
                match.live_stream_url = f"https://cricboost.pages.dev/?id=h"
                updated_count += 1
                print(f"✅ Set live URL for: {match.team_home} vs {match.team_away}")
            
            db.session.commit()
            
            if updated_count > 0:
                print(f"✅ Auto-set live URLs for {updated_count} match(es)")
            
            return updated_count
            
        except Exception as e:
            print(f"❌ Error auto-setting live URLs: {e}")
            db.session.rollback()
            return 0


def setup_auto_url_scheduler(app):
    """
    Set up scheduler to automatically set live URLs every 30 minutes
    """
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    
    scheduler = BackgroundScheduler()
    
    # Run every 30 minutes
    scheduler.add_job(
        func=lambda: auto_set_live_urls(app),
        trigger=IntervalTrigger(minutes=30),
        id='auto_set_live_urls',
        name='Auto-set live streaming URLs for started matches',
        replace_existing=True
    )
    
    scheduler.start()
    print("✅ Auto live URL setter initialized (runs every 30 minutes)")
    
    # Run once immediately
    auto_set_live_urls(app)
    
    return scheduler


# Made with Bob