from faker import Faker
from model_mommy.recipe import Recipe
from .models import CaregiverOffStudy, TBAdolOffStudy, ChildOffStudy

fake = Faker()

caregiveroffstudy = Recipe(
    CaregiverOffStudy, )

tbadoloffstudy = Recipe(
    TBAdolOffStudy)

childoffstudy = Recipe(ChildOffStudy)
