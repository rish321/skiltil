from django.contrib import admin

# Register your models here.

class BaseAdmin(admin.ModelAdmin):
	actions = ['download_csv']

	def download_csv(self, request, queryset):
		return self.create_download_csv(queryset)

	download_csv.short_description = "Download CSV file for selected stats."

	def create_download_csv(self, queryset):
		import csv
		from django.http import HttpResponse
		import StringIO
		f = StringIO.StringIO()
		writer = csv.writer(f)
		fields = [fi.name for fi in queryset.model._meta.fields
				  + queryset.model._meta.many_to_many]
		writer.writerow([fi for fi in fields])
		for s in queryset:
			row = []
			for fieldname in fields:
				value = getattr(s, fieldname)
				row.append(str(value))
			writer.writerow(row)
		# writer.writerow([fi for fi in fields])
		f.seek(0)
		response = HttpResponse(f, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=' + queryset.model._meta.verbose_name_plural.lower().replace(" ", "_") + ".csv"
		return response
