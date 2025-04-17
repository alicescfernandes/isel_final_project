import os
import uuid
import pandas as pd
from django.db import models
from django.conf import settings
from .utils.data_processing import run_pipeline_for_sheet, extract_section_name, convert_df_to_json

def user_quarter_upload_path(instance, filename):
    instance.section_name = extract_section_name(filename)
    return os.path.join("uploads", str(instance.uuid), filename)

class Quarter(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    number = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-number']

    def __str__(self):
        return f"Q{self.number}"
    

class ExcelFile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    quarter = models.ForeignKey("Quarter", on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=user_quarter_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
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

                processed_data_frame, sheet_slug, sheet_title  = run_pipeline_for_sheet(xls, sheet_name)

                # Get the column order first, this will be saved in a specific field
                columns = processed_data_frame.columns.tolist()
                data_json = convert_df_to_json(processed_data_frame)
                
                # Check for other CSV's and mark them as not active
                CSVData.objects.filter(
                    quarter_file__quarter=self.quarter,
                    sheet_name_slug=sheet_slug,
                    is_current=True
                ).update(is_current=False)

                CSVData.objects.create(
                    quarter_file=self,
                    sheet_name_pretty=sheet_title,
                    sheet_name_slug=sheet_slug,
                    quarter_uuid=self.quarter.uuid,
                    data=data_json,
                    is_current=True,
                    column_order=columns,  # novo campo no modelo (JSONField ou ArrayField)
                )
        
            # Do not "save" itself, instead update just this field. Calling .save() causes a recursion
            ExcelFile.objects.filter(pk=self.pk).update(is_processed=True)

        except Exception as e:
            print(f"Erro a processar {xlsx_path}: {e}")

class CSVData(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    quarter_file = models.ForeignKey("ExcelFile", on_delete=models.CASCADE, related_name="csvs")
    
    # Sheet name (derived from she actual sheet title) is a more human-like string, that removes some text.
    sheet_name_pretty = models.CharField(max_length=255)
    # Sheet slug is a slug-like string derived from the sheet title, keeping in mind that the user won't change the sheet title, it groups the data into common identifiers
    sheet_name_slug = models.CharField(max_length=255)
    quarter_uuid = models.UUIDField(null=True, editable=False)
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=list)
    column_order = models.JSONField(default=list) # saves the column order. this is crucial for the read from the API

    def __str__(self):
        return f"{self.sheet_name_pretty} ({self.uuid})"
