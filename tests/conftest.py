import pytest
from sqlalchemy import create_engine, text

def pytest_runtest_makereport(item, call):
    """Hook to detect test failures"""
    if call.excinfo is not None:
        item.module.pytest_failed = True

def pytest_addoption(parser):
    parser.addoption(
        "--cleanup-test-dbs",
        action="store_true",
        default=False,
        help="Clean up all test databases (test_db_*)"
    )

def pytest_sessionstart(session):
    if session.config.getoption("cleanup_test_dbs"):
        engine = create_engine(
            "postgresql://postgres:demopassword@localhost:5433/postgres",
            isolation_level="AUTOCOMMIT"
        )
        with engine.connect() as conn:
            # Get list of test databases
            result = conn.execute(text("""
                SELECT datname FROM pg_database 
                WHERE datname LIKE 'test_db_%'
            """))
            test_dbs = [row[0] for row in result]
            
            # Terminate connections and drop each test database
            for db_name in test_dbs:
                print(f"Cleaning up database: {db_name}")
                conn.execute(text(f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{db_name}'
                    AND pid <> pg_backend_pid()
                """))
                conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
            
            if test_dbs:
                print(f"\nCleaned up {len(test_dbs)} test database(s)")
            else:
                print("\nNo test databases found to clean up")
        
        # Exit after cleanup
        pytest.exit("Cleanup complete")
