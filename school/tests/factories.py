import factory
from factory.django import DjangoModelFactory

# import models
from school.models import Subject, StudentClass, ClassLevel, Sections

# create factories


class SubjectFactory(DjangoModelFactory):

    class Meta:
        model = Subject

    name = factory.Sequence(lambda n: f"subject-{n}") 
    code = factory.Sequence(lambda n: f"{n + 1 }{n+2}{n + 3}{n + 4}")
    description = f"this is a subject"
    is_active = True


class ClassLevelFactory(DjangoModelFactory):
    class Meta:
        model = ClassLevel
        skip_postgeneration_save = True

    monthly_fee = "10" 
    name = factory.Sequence(lambda n: str(n + 1))

    # jodi many_to_many fields hoy tahole Post_generation lage, 
    # agge class_level obj save hobe ar pore subject ta add hobe 
    @factory.post_generation
    def subjects(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.subjects.add(*extracted)
        else:
            self.subjects.add(SubjectFactory())


class SectionFactory(DjangoModelFactory):
    class Meta:
        model = Sections
    section = factory.Sequence(lambda n: chr(65 + n))



class StudentClassFactory(DjangoModelFactory):
    class Meta:
        model = StudentClass

    student_class_level = factory.SubFactory(ClassLevelFactory)
    section = factory.SubFactory(SectionFactory)

    