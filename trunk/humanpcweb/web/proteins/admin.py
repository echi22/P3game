# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Eze"
__date__ ="$08/09/2011 17:24:52$"

if __name__ == "__main__":
    print "Hello World"

from web.proteins.models import ComparisonProtein
from web.proteins.models import Protein
from web.proteins.models import Comparison
from web.proteins.models import Classification
from web.proteins.models import UserProfile
from web.proteins.models import Score
from web.proteins.models import GameInstance
from django.contrib import admin
admin.site.register(Protein)
admin.site.register(Comparison)
admin.site.register(Classification)
admin.site.register(ComparisonProtein)
admin.site.register(UserProfile)
admin.site.register(Score)
admin.site.register(GameInstance)