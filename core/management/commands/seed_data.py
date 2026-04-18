"""
Management command: python manage.py seed_data
Seeds the database with sample students, events, and messages.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student
from events.models import Event
from contact.models import Message
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding database...')

        # ── Admin user ──────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@eduadmin.com', 'admin1234')
            self.stdout.write(self.style.SUCCESS('  ✓ Admin user created  (admin / admin1234)'))
        else:
            self.stdout.write('  · Admin user already exists')

        # ── Students ────────────────────────────────────────────
        students_data = [
            ('Alice Johnson', 'CS', 1, 'alice@college.edu', '+1-555-0101'),
            ('Bob Martinez', 'EE', 2, 'bob@college.edu', '+1-555-0102'),
            ('Clara Smith', 'ME', 3, 'clara@college.edu', '+1-555-0103'),
            ('David Lee', 'CE', 4, 'david@college.edu', '+1-555-0104'),
            ('Emma Wilson', 'BIO', 1, 'emma@college.edu', '+1-555-0105'),
            ('Frank Brown', 'MBA', 2, 'frank@college.edu', '+1-555-0106'),
            ('Grace Kim', 'CS', 3, 'grace@college.edu', '+1-555-0107'),
            ('Henry Davis', 'MATH', 2, 'henry@college.edu', '+1-555-0108'),
            ('Isla Turner', 'ARTS', 1, 'isla@college.edu', '+1-555-0109'),
            ('Jake White', 'EE', 4, 'jake@college.edu', '+1-555-0110'),
            ('Karen Black', 'CS', 2, 'karen@college.edu', '+1-555-0111'),
            ('Liam Hall', 'ME', 1, 'liam@college.edu', '+1-555-0112'),
        ]

        created = 0
        for name, dept, year, email, phone in students_data:
            _, was_created = Student.objects.get_or_create(
                email=email,
                defaults=dict(name=name, department=dept, year=year, phone=phone)
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'  ✓ {created} students created'))

        # ── Events ──────────────────────────────────────────────
        today = date.today()
        events_data = [
            ('Annual Science Fair', 'Students from all departments showcase research projects and innovations.', today + timedelta(days=14)),
            ('Freshers Welcome Party', 'An evening of music, games, and introductions for new students.', today + timedelta(days=3)),
            ('Inter-College Hackathon', '24-hour coding competition open to all CS and EE students.', today + timedelta(days=21)),
            ('Career Fair 2024', 'Top companies recruiting for internships and full-time roles.', today + timedelta(days=30)),
            ('Sports Day', 'Annual athletic competition across departments.', today - timedelta(days=7)),
            ('Cultural Fest', 'Celebrate diversity with performances, food, and art.', today + timedelta(days=45)),
        ]

        ev_created = 0
        for title, desc, dt in events_data:
            _, was_created = Event.objects.get_or_create(
                title=title,
                defaults=dict(description=desc, date=dt)
            )
            if was_created:
                ev_created += 1
        self.stdout.write(self.style.SUCCESS(f'  ✓ {ev_created} events created'))

        # ── Contact Messages ────────────────────────────────────
        messages_data = [
            ('Sarah Connor', 'sarah@example.com', 'Admission Inquiry', 'I would like to know the admission process for the CS department for next year.', False),
            ('Tom Hardy', 'tom@example.com', 'Scholarship Information', 'Could you please share details about scholarships available for second-year students?', False),
            ('Priya Sharma', 'priya@example.com', 'Event Registration', 'How do I register for the upcoming hackathon? Looking forward to participating!', True),
            ('James Bond', 'james@example.com', 'Fee Structure', 'Please send me the fee structure for the MBA program.', True),
            ('Linda Park', 'linda@example.com', 'Library Access', 'I am having trouble accessing the online library portal. Can you help?', False),
        ]

        msg_created = 0
        for name, email, subject, body, is_read in messages_data:
            _, was_created = Message.objects.get_or_create(
                email=email,
                subject=subject,
                defaults=dict(name=name, body=body, is_read=is_read)
            )
            if was_created:
                msg_created += 1
        self.stdout.write(self.style.SUCCESS(f'  ✓ {msg_created} messages created'))

        self.stdout.write(self.style.SUCCESS('\n✅ Seeding complete! Visit http://127.0.0.1:8000/login/'))
        self.stdout.write(self.style.WARNING('   Login: admin / admin1234'))
