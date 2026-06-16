"""
Manually update a live match with scores and streaming URL
Run this script to update a specific match that is currently live
"""
import sys
from backend.app import app
from backend.models import db, Match
from datetime import datetime


def update_live_match(match_id, home_score, away_score, live_url=None):
    """
    Update a match with live scores and streaming URL
    
    Args:
        match_id: ID of the match to update
        home_score: Current home team score
        away_score: Current away team score
        live_url: Live streaming URL (optional, defaults to cricboost)
    """
    with app.app_context():
        try:
            match = Match.query.get(match_id)
            
            if not match:
                print(f"❌ Match with ID {match_id} not found")
                return False
            
            print(f"\n📊 Updating match: {match.team_home} vs {match.team_away}")
            print(f"   Match Date: {match.match_date}")
            print(f"   Current Status: {'Finished' if match.is_finished else 'Live/Upcoming'}")
            
            # Update scores
            match.home_score = home_score
            match.away_score = away_score
            
            # Set as not finished (it's live)
            match.is_finished = False
            
            # Set live streaming URL
            if live_url:
                match.live_stream_url = live_url
            else:
                match.live_stream_url = "https://cricboost.pages.dev/?id=h"
            
            db.session.commit()
            
            print(f"\n✅ Match updated successfully!")
            print(f"   Score: {match.team_home} {home_score} - {away_score} {match.team_away}")
            print(f"   Live URL: {match.live_stream_url}")
            print(f"   Status: LIVE (not finished)")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error updating match: {e}")
            db.session.rollback()
            return False


def finish_match(match_id):
    """
    Mark a match as finished and remove live URL
    
    Args:
        match_id: ID of the match to finish
    """
    with app.app_context():
        try:
            match = Match.query.get(match_id)
            
            if not match:
                print(f"❌ Match with ID {match_id} not found")
                return False
            
            print(f"\n📊 Finishing match: {match.team_home} vs {match.team_away}")
            
            # Mark as finished
            match.is_finished = True
            
            # Remove live URL
            match.live_stream_url = None
            
            # Calculate points for predictions
            for prediction in match.predictions:
                prediction.points_earned = prediction.calculate_points()
            
            db.session.commit()
            
            print(f"✅ Match finished!")
            print(f"   Final Score: {match.team_home} {match.home_score} - {match.away_score} {match.team_away}")
            print(f"   Live URL: Removed")
            print(f"   Points calculated for {len(match.predictions)} prediction(s)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error finishing match: {e}")
            db.session.rollback()
            return False


def list_matches():
    """List all matches with their IDs"""
    with app.app_context():
        matches = Match.query.order_by(Match.match_date).all()
        
        print("\n" + "="*70)
        print("  ALL MATCHES")
        print("="*70)
        
        for match in matches:
            status = "✅ Finished" if match.is_finished else "🔴 Live/Upcoming"
            score = f"{match.home_score}-{match.away_score}" if match.home_score is not None else "Not started"
            live_url = "Yes" if match.live_stream_url else "No"
            
            print(f"\nID: {match.id}")
            print(f"   {match.team_home} vs {match.team_away}")
            print(f"   Date: {match.match_date}")
            print(f"   Score: {score}")
            print(f"   Status: {status}")
            print(f"   Live URL: {live_url}")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  LIVE MATCH UPDATER")
    print("="*70)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  List all matches:")
        print("    python update_live_match.py list")
        print("\n  Update live match:")
        print("    python update_live_match.py <match_id> <home_score> <away_score> [live_url]")
        print("\n  Finish match:")
        print("    python update_live_match.py finish <match_id>")
        print("\nExamples:")
        print("  python update_live_match.py list")
        print("  python update_live_match.py 1 150 145")
        print("  python update_live_match.py 1 150 145 https://cricboost.pages.dev/?id=h")
        print("  python update_live_match.py finish 1")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        list_matches()
    elif command == 'finish':
        if len(sys.argv) < 3:
            print("❌ Error: Match ID required")
            print("Usage: python update_live_match.py finish <match_id>")
            sys.exit(1)
        match_id = int(sys.argv[2])
        finish_match(match_id)
    else:
        # Update live match
        if len(sys.argv) < 4:
            print("❌ Error: Match ID and scores required")
            print("Usage: python update_live_match.py <match_id> <home_score> <away_score> [live_url]")
            sys.exit(1)
        
        match_id = int(sys.argv[1])
        home_score = int(sys.argv[2])
        away_score = int(sys.argv[3])
        live_url = sys.argv[4] if len(sys.argv) > 4 else None
        
        update_live_match(match_id, home_score, away_score, live_url)

# Made with Bob