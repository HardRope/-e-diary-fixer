from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Teacher
from datacenter.models import Subject
from datacenter.models import Lesson
from datacenter.models import Commendation

def get_child_record(name):
    try:
        child_record = Schoolkid.objects.filter(full_name__contains=name).get()
    except:
        print('''
Несуществующее имя, либо больше одного ученика с таким именем,\
уточните имя (введите ФИО)
''')
        return
    return child_record


def choice_praise():
    from random import choice

    with open('praises.txt' , 'r', encoding = 'utf-8') as file:
        praises = [line.rstrip() for line in file]

    return choice(praises)


def fix_marks(name):
    child = get_child_record(name)
    marks = Mark.objects.filter(schoolkid = child, points__lte = 3)

    for entry in marks:
        entry.points = 5
        entry.save()


def remove_chastisements(name):
    child = get_child_record(name)
    comments = Chastisement.objects.filter(schoolkid = child)
    comments.delete()


def create_commendation(name, lesson_name):
    child = get_child_record(name)
    
    
    lessons = Lesson.objects.filter(
            year_of_study = child.year_of_study, 
            group_letter = child.group_letter, 
            subject__title = lesson_name
            )

    lessons = lessons.order_by('date').reverse()

    last_lesson = lessons.first()

    try:
        lesson_subject = last_lesson.subject
    except AttributeError:
        print('\nНеправильное название предмета\nДоступные предметы:')

        subjects_title = set()
        for subject in Subject.objects.all():
            subjects_title.add(subject.title)
        print(*subjects_title, sep = ', ')
        return

    commendation = Commendation.objects.filter(
            schoolkid = child, 
            subject = lesson_subject, 
            teacher = last_lesson.teacher
            ) 

    commendation.create(
            text=choice_praise(), 
            created = last_lesson.date, 
            schoolkid = child, 
            subject = last_lesson.subject, 
            teacher = last_lesson.teacher
            )
