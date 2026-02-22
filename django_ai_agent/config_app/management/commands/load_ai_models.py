import os
import yaml
from django.core.management.base import BaseCommand
from django.conf import settings
from django_ai_agent.config_app.models import AIModel

class Command(BaseCommand):
    help = 'Load AI models from config.yaml into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--config',
            type=str,
            default='config.yaml',
            help='Path to the config.yaml file'
        )

    def handle(self, *args, **options):
        config_path = options['config']
        
        # If relative path, make it relative to the Django project
        if not os.path.isabs(config_path):
            config_path = os.path.join(settings.BASE_DIR, '..', config_path)
        
        if not os.path.exists(config_path):
            self.stdout.write(
                self.style.ERROR(f'Config file not found: {config_path}')
            )
            return

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            ai_models_config = config.get('ai_models', {})
            
            created_count = 0
            updated_count = 0
            
            for provider, provider_config in ai_models_config.items():
                models = provider_config.get('models', [])
                api_key = provider_config.get('api_key', '')
                base_url = provider_config.get('base_url', '')
                
                for model_config in models:
                    model_name = model_config.get('name')
                    is_active = model_config.get('enabled', False)
                    
                    # Create a friendly name for the model
                    display_name = f"{provider.title()} {model_name}"
                    
                    # Update or create the model
                    ai_model, created = AIModel.objects.update_or_create(
                        provider=provider,
                        model_name=model_name,
                        defaults={
                            'name': display_name,
                            'api_key': api_key,
                            'base_url': base_url,
                            'is_active': is_active
                        }
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Created AI model: {display_name}')
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'Updated AI model: {display_name}')
                        )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully loaded AI models: {created_count} created, {updated_count} updated'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading AI models: {str(e)}')
            )
