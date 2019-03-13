from django.contrib import admin

# Register your models here.
from .models import Contest, UserLeaderboard, Submission

#admin.site.register(Contest)

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
	list_display = ('owner','title','text','org','creation_time','reg_deadline','status')

@admin.register(UserLeaderboard)
class LBAdmin(admin.ModelAdmin):
	list_display = ('user', 'contest', 'lb_time', 'lb_score', 'lb_sub_count', 'lb_sub_count_period', 'lb_rank')
	list_filter = ('user', 'contest', 'lb_rank')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'contest', 'sub_time', 'sub_text', 'sub_score', 'sub_status', 'filename', 'filepath')
	list_filter = ('user', 'contest')