from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
import random
from project.models import Task, Category, Priority, SubTask, Note

fake = Faker()


class Command(BaseCommand):
    help = "Populate initial data with faker"

    def handle(self, *args, **kwargs):
        # Add Categories
        categories = ["Work", "School", "Personal", "Finance", "Projects"]
        for cat in categories:
            Category.objects.get_or_create(name=cat)

        # Add Priorities
        priorities = ["High", "Medium", "Low", "Critical", "Optional"]
        for pri in priorities:
            Priority.objects.get_or_create(name=pri)

        # Create Fake Tasks
        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                priority=random.choice(Priority.objects.all()),
                category=random.choice(Category.objects.all()),
            )

            # Create subtasks
            for _ in range(random.randint(1, 3)):
                SubTask.objects.create(
                    title=fake.sentence(nb_words=3),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                    parent_task=task,
                )

            # Create notes
            for _ in range(random.randint(1, 2)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

        self.stdout.write(self.style.SUCCESS("Fake data created successfully!"))