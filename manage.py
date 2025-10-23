"""
Management CLI for the application
"""
import click
import os
from app import create_app
from app.services.supabase import get_supabase_admin_client, get_db_connection
from dotenv import load_dotenv

load_dotenv()

app = create_app()


@click.group()
def cli():
    """Management commands"""
    pass


@cli.command()
def provision():
    """Provision database with migrations and seed data"""
    click.echo('Provisioning database...')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        migrations_dir = os.path.join(os.path.dirname(__file__), 'supabase', 'migrations')
        
        # Execute migrations in order
        migration_files = [
            '00_schema.sql',
            '01_rls.sql',
            '02_seed.sql',
            '03_storage.sql'
        ]
        
        for migration_file in migration_files:
            file_path = os.path.join(migrations_dir, migration_file)
            
            if os.path.exists(file_path):
                click.echo(f'Executing {migration_file}...')
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    sql = f.read()
                    cursor.execute(sql)
                    conn.commit()
                
                click.echo(f'✓ {migration_file} executed successfully')
            else:
                click.echo(f'⚠ {migration_file} not found, skipping...')
        
        cursor.close()
        conn.close()
        
        click.echo('✓ Database provisioned successfully!')
    
    except Exception as e:
        click.echo(f'✗ Error provisioning database: {str(e)}', err=True)
        raise


@cli.command()
def seed():
    """Load seed data only"""
    click.echo('Loading seed data...')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        seed_file = os.path.join(os.path.dirname(__file__), 'supabase', 'migrations', '02_seed.sql')
        
        if os.path.exists(seed_file):
            with open(seed_file, 'r', encoding='utf-8') as f:
                sql = f.read()
                cursor.execute(sql)
                conn.commit()
            
            click.echo('✓ Seed data loaded successfully!')
        else:
            click.echo('✗ Seed file not found', err=True)
        
        cursor.close()
        conn.close()
    
    except Exception as e:
        click.echo(f'✗ Error loading seed data: {str(e)}', err=True)
        raise


@cli.command()
@click.option('--email', prompt='Admin email', help='Admin email address')
@click.option('--password', prompt='Admin password', hide_input=True, confirmation_prompt=True, help='Admin password')
@click.option('--name', prompt='Full name', help='Admin full name')
def create_admin(email, password, name):
    """Create admin user"""
    click.echo(f'Creating admin user: {email}...')
    
    try:
        from app.services.auth import AuthService
        
        # Sign up user
        result = AuthService.sign_up(email, password, name)
        
        if result['success']:
            # Update role to admin
            supabase = get_supabase_admin_client()
            supabase.table('app_users').update({
                'role': 'admin',
                'email_verified': True
            }).eq('id', result['user'].id).execute()
            
            click.echo(f'✓ Admin user created successfully!')
            click.echo(f'Email: {email}')
            click.echo(f'Please verify the email in Supabase dashboard if needed.')
        else:
            click.echo(f'✗ Error creating admin: {result["error"]}', err=True)
    
    except Exception as e:
        click.echo(f'✗ Error: {str(e)}', err=True)
        raise


@cli.command()
def test_connection():
    """Test Supabase connection"""
    click.echo('Testing Supabase connection...')
    
    try:
        supabase = get_supabase_admin_client()
        
        # Try to query a table
        response = supabase.table('app_roles').select('*').limit(1).execute()
        
        click.echo('✓ Connection successful!')
        click.echo(f'Supabase URL: {os.getenv("SUPABASE_URL")}')
    
    except Exception as e:
        click.echo(f'✗ Connection failed: {str(e)}', err=True)
        raise


@cli.command()
def run():
    """Run the Flask development server"""
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    cli()
