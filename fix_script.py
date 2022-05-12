from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Teacher
from datacenter.models import Subject
from datacenter.models import Lesson
from datacenter.models import Commendation

from random import choice

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def get_child(name):
    try:
        child_record = Schoolkid.objects.get(full_name__contains=name)
        return child_record
    except ObjectDoesNotExist:
        print('\nНесуществующее имя, введите ФИО\n')
    except MultipleObjectsReturned:
        print('\nНайдено больше одного ученика, уточните ФИО\n')


def get_lessons():
    subjects_title = set()
    for subject in Subject.objects.all():
        subjects_title.add(subject.title)
    return list(subjects_title).sort()


def choice_praise():
    with open('praises.txt', 'r', encoding='utf-8') as file:
        praises = [line.rstrip() for line in file]

    return choice(praises)


def fix_marks(name):
    child = get_child(name)
    marks = Mark.objects.filter(schoolkid=child, points__lte=3)

    for entry in marks:
        entry.points = 5
        entry.save()


def remove_chastisements(name):
    child = get_child(name)
    comments = Chastisement.objects.filter(schoolkid=child)
    comments.delete()


def create_commendation(name, lesson_name):
    child = get_child(name)

    schoolchild_lessons = Lesson.objects.filter(
            year_of_study=child.year_of_study,
            group_letter=child.group_letter,
            subject__title=lesson_name
            )

    if not schoolchild_lessons:
        print('\nНеправильное название предмета.\n')
        return

    last_lesson = schoolchild_lessons.order_by('-date').first()

    commendation = Commendation.objects.filter(
            schoolkid=child,
            subject=last_lesson.subject,
            teacher=last_lesson.teacher
            )

    commendation.create(
            text=choice_praise(),
            created=last_lesson.date,
            schoolkid=child,
            subject=last_lesson.subject,
            teacher=last_lesson.teacher
            )
