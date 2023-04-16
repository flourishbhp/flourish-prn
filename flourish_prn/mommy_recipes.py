from faker import Faker
from model_mommy.recipe import Recipe
from .models import CaregiverOffStudy, TbReferalAdol, ChildOffStudy

fake = Faker()

caregiveroffstudy = Recipe(
    CaregiverOffStudy, )

tbadolreferral = Recipe(
    TbReferalAdol)

childoffstudy = Recipe(ChildOffStudy)
