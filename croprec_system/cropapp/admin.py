from django.contrib import admin
from .models import UserProfile, CropRecord, Feedback


'''admin.site.register(UserProfile)
admin.site.register(CropRecord)
admin.site.register(Feedback)'''

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

@admin.register(CropRecord)
class CropRecordAdmin(admin.ModelAdmin):
    list_display = ['predicted_crop', 'farmer_name', 'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'recommended_on']
    list_filter = ['predicted_crop', 'recommended_on']
    search_fields = ['farmer__username', 'predicted_crop']
    date_hierarchy = 'recommended_on'
    def farmer_name(self, obj):
        name = obj.farmer.get_full_name()
        return name if name else obj.farmer.username
    farmer_name.short_description = 'Farmer'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'rating', 'created_at']
