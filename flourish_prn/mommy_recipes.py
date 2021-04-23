from faker import Faker
from model_mommy.recipe import Recipe
from .models import CaregiverOffStudy


fake = Faker()

caregiveroffstudy = Recipe(
    CaregiverOffStudy,)
