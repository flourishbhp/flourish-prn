from faker import Faker
from model_mommy.recipe import Recipe
from .models import CaregiverOffStudy, TbReferalAdol

fake = Faker()

caregiveroffstudy = Recipe(
    CaregiverOffStudy, )

tbadolreferral = Recipe(
    TbReferalAdol)
