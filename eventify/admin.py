from django.contrib import admin
from .models import Post, Service,Comment,ServiceComment,RegisterEvent,RegisterService
from simple_history.admin import SimpleHistoryAdmin


class PostAdmin(SimpleHistoryAdmin,admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'date_posted','isLate','IsCancelled')
    list_display_links = ('id', 'title')
    list_filter = ('author', 'date_posted','isLate','IsCancelled')
    search_fields = ('title', 'content', 'author')
    list_per_page = 20


admin.site.register(Post, PostAdmin)



class ServiceAdmin(SimpleHistoryAdmin,admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'date_posted','currentAtt','isLate','IsCancelled')
    list_display_links = ('id', 'title')
    history_list_display = ["title"]
    list_filter = ('author', 'date_posted','isLate','IsCancelled')
    search_fields = ('title', 'content','author__username')
    list_per_page = 20


admin.site.register(Service, ServiceAdmin)


class CommentAdmin(SimpleHistoryAdmin,admin.ModelAdmin):
    list_display = ('id', 'author', 'post',
                    'approved_comment', 'created_date')
    list_display_links = ('id', 'author', 'post')
    list_filter = ('author', 'created_date')
    list_editable = ('approved_comment', )
    search_fields = ('author', 'post')
    list_per_page = 20


admin.site.register(Comment, CommentAdmin)

class ServiceCommentAdmin(SimpleHistoryAdmin,admin.ModelAdmin):
    list_display = ('id', 'author', 'service',
                    'approved_comment', 'created_date')
    list_display_links = ('id', 'author', 'service')
    list_filter = ('author', 'created_date')
    list_editable = ('approved_comment', )
    search_fields = ('author', 'service')
    list_per_page = 20


admin.site.register(ServiceComment, ServiceCommentAdmin)

class RegisterEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post',
                    'approved_register', 'created_date')
    list_filter = ('author', 'created_date','post__title')
    list_editable = ('approved_register', )
    search_fields = ('post__title',)
    list_per_page = 20


admin.site.register(RegisterEvent, RegisterEventAdmin)

class RegisterServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'service',
                    'approved_register', 'created_date')
    list_filter = ('author', 'created_date','service__title')
    list_editable = ('approved_register', )
    search_fields = ('service__title',)
    list_per_page = 20


admin.site.register(RegisterService, RegisterServiceAdmin)