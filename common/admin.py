from django.contrib import admin
from common.models import *

admin.site.register(MsCountry)
admin.site.register(MsRegion)

admin.site.register(MsInputDef)
admin.site.register(MsInputColumnDef)
admin.site.register(MsInputType)
admin.site.register(MsRegisterPolicy)

admin.site.register(RunResultRecord)
admin.site.register(IssueRecord)
admin.site.register(IssueContextRecord)

admin.site.register(TestNameList)
