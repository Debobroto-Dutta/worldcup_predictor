"""
Automatically set live streaming URLs for matches that have started
This runs periodically to ensure all started matches have live URLs
"""
from datetime import datetime
from backend.models import db, Match


def auto_set_live_urls(app):
    """
    Automatically set live streaming URLs ONLY for matches that are currently LIVE
    (started but not finished). Remove URLs from finished matches.
    """
    with app.app_context():
        try:
            now = datetime.utcnow()
            
            # Find LIVE matches (started but not finished)
            live_matches = Match.query.filter(
                Match.match_date <= now,
                Match.is_finished == False
            ).all()
            
            # Find finished matches that still have URLs
            finished_matches = Match.query.filter(
                Match.is_finished == True,
                Match.live_stream_url != None
            ).all()
            
            updated_count = 0
            
            # Set URLs for live matches
            for match in live_matches:
                if not match.live_stream_url:
                    match.live_stream_url = f"https://cricboost.pages.dev/?id=h"
                    updated_count += 1
                    print(f"✅ Set live URL for LIVE match: {match.team_home} vs {match.team_away}")
            
            # Remove URLs from finished matches
            for match in finished_matches:
                match.live_stream_url = None
                updated_count += 1
                print(f"🔴 Removed URL from finished match: {match.team_home} vs {match.team_away}")
            
            db.session.commit()
            
            if updated_count > 0:
                print(f"✅ Updated {updated_count} match(es) - Live: {len(live_matches)}, Finished: {len(finished_matches)}")
            else:
                print("ℹ️  No URL updates needed")
            
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