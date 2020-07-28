import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Person, Staff, Planet, Movie


class PersonType(DjangoObjectType):
    class Meta:
        model = Person


class StaffType(DjangoObjectType):
    class Meta:
        model = Staff
        convert_choices_to_enum = True


class PlanetType(DjangoObjectType):
    class Meta:
        model = Planet


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class Query(graphene.ObjectType):
    person = graphene.List(PersonType)
    character = graphene.List(StaffType)
    planet = graphene.List(PlanetType)
    movie = graphene.List(MovieType)

    def resolve_person(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')
        persons = Person.objects.all()
        return persons

    def resolve_character(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        characters = Staff.objects.filter(type_staff=Staff.character)
        return characters

    def resolve_planet(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        return Planet.objects.all()

    def resolve_movie(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        return Movie.objects.all()


class CreatePerson(graphene.Mutation):
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        person = Person(name=name)
        person.save()

        return CreatePerson(
            name=person.name,
        )


class CreateStaff(graphene.Mutation):
    staff_type = graphene.String()
    person = graphene.String()

    class Arguments:
        type_staff = graphene.String()
        person = graphene.String()

    def mutate(self, info, type_staff, person):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        person_staff, created = Person.objects.get_or_create(name=person)

        staff = Staff(type_staff=type_staff, person=person_staff)
        staff.save()

        return CreateStaff(
            staff_type=staff.type_staff,
            person=staff.person
        )


class CreatePlanet(graphene.Mutation):
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        planet = Planet(name=name)
        planet.save()
        return CreatePlanet(
            name=planet.name,
        )


class CreateMovie(graphene.Mutation):
    name = graphene.String()
    detail = graphene.String() 
    planets = graphene.List(graphene.String)
    staff_characters = graphene.List(graphene.String)
    staff_directors = graphene.List(graphene.String)
    staff_producers = graphene.List(graphene.String)
    
    class Arguments:
        name = graphene.String()
        detail = graphene.String()
        planets = graphene.List(graphene.String) 
        staff_characters = graphene.List(graphene.String)
        staff_directors = graphene.List(graphene.String)
        staff_producers = graphene.List(graphene.String)

    def mutate(self, info, name, detail, planets, staff_characters, staff_directors, staff_producers):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        movie, created_movie = Movie.objects.get_or_create(name=name, detail=detail)
        movie.save()
        print("hhhh", movie.planet)
        for planet in planets:
            new_planet, created_planet = Planet.objects.get_or_create(name=planet)
            movie.planet.add(new_planet)
        print(movie.planet)
        
        """ person_staff, created = Person.objects.get_or_create(name=person)
        staff = Staff(type_staff=type_staff, person=person_staff)
        staff.save()
         """   
        return CreateMovie(
            name=movie.name,
            detail=movie.detail,
            planet=movie.planet,
            staff=movie.staff
        )


class Mutation(graphene.ObjectType):
    create_character = CreateStaff.Field()
    create_planet = CreatePlanet.Field()
    create_peron = CreatePerson.Field()
    create_movie = CreateMovie.Field()
