"""
Database migration script for Render External PostgreSQL
Adds live_stream_url and espn_match_id fields to Match table

This script reads DATABASE_URL from environment variables (Render sets this automatically)
No need to manually enter credentials!
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def migrate_database():
    """Add new columns to Match table in external PostgreSQL database"""
    
    # Get DATABASE_URL from environment (Render sets this automatically)
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable not found!")
        print("\nFor local testing, set it like this:")
        print("export DATABASE_URL='postgresql://user:password@host:port/database'")
        print("\nOn Render, this is set automatically.")
        return False
    
    # Fix Render's postgres:// to postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        print("✓ Fixed DATABASE_URL format (postgres:// → postgresql://)")
    
    print(f"\n🔗 Connecting to database...")
    print(f"   Host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'hidden'}")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("\n✅ Connected to PostgreSQL database successfully!")
            
            # Check if columns already exist
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'match' 
                AND column_name IN ('live_stream_url', 'espn_match_id')
            """)
            
            result = conn.execute(check_query)
            existing_columns = [row[0] for row in result]
            
            if 'live_stream_url' in existing_columns and 'espn_match_id' in existing_columns:
                print("\n✓ Columns already exist! No migration needed.")
                print("  - live_stream_url: EXISTS")
                print("  - espn_match_id: EXISTS")
                return True
            
            # Add columns if they don't exist
            print("\n🔄 Adding new columns to 'match' table...")
            
            if 'live_stream_url' not in existing_columns:
                conn.execute(text("""
                    ALTER TABLE match 
                    ADD COLUMN IF NOT EXISTS live_stream_url VARCHAR(500)
                """))
                conn.commit()
                print("  ✅ Added column: live_stream_url")
            else:
                print("  ✓ Column already exists: live_stream_url")
            
            if 'espn_match_id' not in existing_columns:
                conn.execute(text("""
                    ALTER TABLE match 
                    ADD COLUMN IF NOT EXISTS espn_match_id VARCHAR(100)
                """))
                conn.commit()
                print("  ✅ Added column: espn_match_id")
            else:
                print("  ✓ Column already exists: espn_match_id")
            
            # Verify columns were added
            result = conn.execute(check_query)
            final_columns = [row[0] for row in result]
            
            if 'live_stream_url' in final_columns and 'espn_match_id' in final_columns:
                print("\n✅ Migration completed successfully!")
                print("\n📊 Database is now ready for new features:")
                print("  ✓ Live streaming URLs")
                print("  ✓ ESPN API integration")
                print("  ✓ User predictions view")
                return True
            else:
                print("\n⚠️  Warning: Columns may not have been added correctly")
                return False
                
    except SQLAlchemyError as e:
        print(f"\n❌ Database error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify DATABASE_URL is correct")
        print("2. Check database permissions")
        print("3. Ensure database is accessible")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def show_instructions():
    """Show instructions for running on Render"""
    print("\n" + "="*60)
    print("  RENDER DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    print("\n📋 To run this migration on Render:")
    print("\n1. Go to your Render Dashboard")
    print("2. Open your Web Service")
    print("3. Click on 'Shell' tab")
    print("4. Run this command:")
    print("\n   python migrate_render_postgres.py")
    print("\n5. Wait for success message")
    print("\n" + "="*60)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  DATABASE MIGRATION FOR RENDER POSTGRESQL")
    print("="*60)
    
    # Check if running on Render (has DATABASE_URL)
    if not os.environ.get('DATABASE_URL'):
        print("\n⚠️  DATABASE_URL not found in environment variables")
        show_instructions()
        print("\n💡 TIP: On Render, DATABASE_URL is set automatically.")
        print("   Just run this script from the Render Shell.")
        sys.exit(1)
    
    # Run migration
    success = migrate_database()
    
    if success:
        print("\n🎉 All done! Your database is ready for the new features.")
        print("\n📝 Next steps:")
        print("  1. Restart your Render service (if not auto-restarted)")
        print("  2. Test the new features in admin panel")
        print("  3. Check NEW_FEATURES_GUIDE.md for usage instructions")
        sys.exit(0)
    else:
        print("\n❌ Migration failed. Please check the errors above.")
        sys.exit(1)

# Made with Bob