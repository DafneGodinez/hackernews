import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

#1
class CreateKit(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    #posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    #3
    def mutate(self, info, name, description):
        user = info.context.user or None

        link = Link(
            name=name, 
            description=description,
            #posted_by=user, 
            )
        link.save()

        return CreateKit(
            id=link.id,
            name=link.name,
            description=link.description,
            #posted_by=link.posted_by,
        )

#4
class Mutation(graphene.ObjectType):
    create_kit = CreateKit.Field()