import factory

from .models import Activity, Process


class ProcessFactory(factory.DjangoModelFactory):
    process_key = factory.Faker("uuid4")

    class Meta:
        model = Process


class ActivityFactory(factory.DjangoModelFactory):
    activity_id = factory.Sequence(lambda x: "42%d" % x)
    process = factory.SubFactory(ProcessFactory)

    class Meta:
        model = Activity
