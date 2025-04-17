import os
import uuid
import pandas as pd
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from .utils.data_processing import run_pipeline_for_sheet, extract_section_name, clean_dataframe_for_json
from django.db import models

def user_quarter_upload_path(instance, filename):
    instance.section_name = extract_section_name(filename)
    return os.path.join("uploads", str(instance.uuid), filename)

class Quarter(models.Model):
    number = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['-number']

    def __str__(self):
        return f"Q{self.number}"
    

class ExcelFile(models.Model):
    quarter = models.ForeignKey("Quarter", on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=user_quarter_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_processed = models.BooleanField(default=False, editable=True) # TODO: Flip this to true
    section_name = models.CharField(max_length=255, editable=False, blank=True)
    
    def __str__(self):
        return f"{self.file.name} ({self.quarter})"

    def process_and_store_csv(self):
        # Do not "save" itself, instead update just this field. Calling .save() causes a recursion
        ExcelFile.objects.filter(pk=self.pk).update(is_processed=False)

        xlsx_path = self.file.path
        output_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', str(self.uuid))
        os.makedirs(output_dir, exist_ok=True)

        try:
            xls = pd.ExcelFile(xlsx_path)

            for sheet_name in xls.sheet_names:
                df_raw = xls.parse(sheet_name, header=None)
                if df_raw.empty:
                    continue

                processed_data_frame, clean_sheet_name, sheet_title  = run_pipeline_for_sheet(xls, sheet_name, output_dir)
                print(processed_data_frame)
                data_json = clean_dataframe_for_json(processed_data_frame)
                print(data_json)
                # Check for other CSV's and mark them as not active
                CSVData.objects.filter(
                    quarter_file__quarter=self.quarter,
                    sheet_name_slug=clean_sheet_name,
                    is_current=True
                ).update(is_current=False)

                CSVData.objects.create(
                    quarter_file=self,
                    sheet_name_pretty=sheet_title,
                    sheet_name_slug=clean_sheet_name,
                    quarter_uuid=self.quarter.uuid,
                    data=data_json,
                    is_current=True
                )
        
            # Do not "save" itself, instead update just this field. Calling .save() causes a recursion
            ExcelFile.objects.filter(pk=self.pk).update(is_processed=True)

        except Exception as e:
            print(f"Erro a processar {xlsx_path}: {e}")

class CSVData(models.Model):
    quarter_file = models.ForeignKey("ExcelFile", on_delete=models.CASCADE, related_name="csvs")
    sheet_name_pretty = models.CharField(max_length=255)
    sheet_name_slug = models.CharField(max_length=255)
    quarter_uuid = models.UUIDField(null=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=list)

    def __str__(self):
        return f"{self.sheet_name_pretty} ({self.uuid})"
