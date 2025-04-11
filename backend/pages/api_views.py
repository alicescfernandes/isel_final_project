import os
import pandas as pd
from pages.models import Quarter
import os
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Quarter, CSVFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CSVFile
from django.shortcuts import get_object_or_404
import pandas as pd
from .chart_classification import CHART_CLASSIFICATION
class QuarterListAPIView(APIView):
    def get(self, request):
        # Preparar a lista de quarters
        quarters = Quarter.objects.all()
        last_quarter = quarters[0]
        if not quarters:
            return Response({"error": "No quarters found"}, status=404)

        first_quarter = quarters[::-1][0]     # mais antigo

        # Obter o número do quarter pedido (ou usar o último por defeito)
        query_quarter = request.query_params.get("q", last_quarter.number)

        try:
            quarter = Quarter.objects.get(number=int(query_quarter))
        except Quarter.DoesNotExist:
            return Response({"error": "Quarter not found"}, status=404)

        # Resposta JSON personalizada
        return Response({
            "number": quarter.number,
            "uuid": str(quarter.uuid),
            "isFirst": quarter.number == first_quarter.number,
            "isLast": quarter.number == last_quarter.number,
        })

def get_quarter_navigation_object(quarter_number, slug):
    # Obter todos os quarter_uuids associados ao slug
    quarter_uuids = (
        CSVFile.objects
        .filter(is_current=True) 
        .filter(sheet_name_slug=slug)
        .values_list('quarter_uuid', flat=True)
        .distinct()
    )
    
    # Obter os objetos Quarter correspondentes, ordenados por número
    all_quarters = list(
        Quarter.objects
        .filter(uuid__in=quarter_uuids)
        .order_by('number')
    )

    curr_q = get_object_or_404(Quarter, number=quarter_number)

    try:
        current_index = next(i for i, q in enumerate(all_quarters) if q.pk == curr_q.pk)
    except StopIteration:
        return None  # current quarter não está na lista filtrada

    prev_q = all_quarters[current_index - 1] if current_index > 0 else None
    next_q = all_quarters[current_index + 1] if current_index < len(all_quarters) - 1 else None

    return {
        'current': curr_q.number,
        'prev': prev_q.number if prev_q else None,
        'next': next_q.number if next_q else None,
    }

# http://localhost:8000/api/chart/?slug=customer-needs-and-wants&q=1
# http://localhost:8000/api/chart/?slug=competitors-prices-apac&q=1

class ChartDataAPIView(APIView):
    def get(self, request, format=None):
        quarters = Quarter.objects.all()
        last_quarter = quarters[0]            # mais recente

        slug = request.query_params.get('slug')
        quarter_number = request.query_params.get('q', last_quarter.number)
        filter = request.query_params.get('opt')  # opcional

        if not slug:
            return Response(
                {"error": "Both 'slug' query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        curr_q = get_object_or_404(Quarter, number=quarter_number)
        
        csv_file = get_object_or_404(
            CSVFile,
            sheet_name_slug=slug,
            quarter_uuid=curr_q.uuid,
            is_current=True
        )

        file_path = csv_file.csv_path
                
        try:
            df = pd.read_csv(file_path)

            application_col = df.columns[0]
            filter_cols = df.columns[1:]

            df[filter_cols] = df[filter_cols].apply(pd.to_numeric, errors='coerce')

            available_filters = filter_cols.tolist()
            selected_filter = filter if filter in available_filters else available_filters[0]

            applications = df[application_col].fillna("").tolist()
            values = df[selected_filter].fillna(0).tolist()
            
            
            return Response({
                'quarter':get_quarter_navigation_object(quarter_number, slug),
                'chart_config':{
                    "traces":[
                        {
                            "type": "bar", #TODO: Mapping for slugs to chart types
                            "x": applications,
                            "y": values
                        }
                    ],
                    "layout":{}
                },
                'title': csv_file.sheet_name,
                "options": available_filters,
                'selected_option': selected_filter
            })

        except Exception as e:
            return Response({
                'quarter':get_quarter_navigation_object(quarter_number, slug),
                "error": f"Error reading file: {str(e)}",
                'chart_config':{
                    "traces":[],
                    "layout":{}
                },
                'title': csv_file.sheet_name,
                "options": available_filters,
                'selected_option': selected_filter
            })
        
        
def format_chart_trace(x,y, type):
    if(type == "pie"):        
        return {
            "values": y,
            "labels": x,
            "type": 'pie'
        }
        
    return {
            "type": type,
            "x": x,
            "y": y
        }
    
class ChartDataAPIViewV2(APIView):
    def get(self, request, format=None):
        quarters = Quarter.objects.all()
        last_quarter = quarters[0]            # mais recente

        slug = request.query_params.get('slug')
        quarter_number = request.query_params.get('q', last_quarter.number)
        filter = request.query_params.get('opt')  # opcional

        if not slug:
            return Response(
                {"error": "Missing required 'slug' query parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        chart_meta = CHART_CLASSIFICATION.get(slug)
        if not chart_meta:
            return Response(
                {"error": f"No chart classification found for slug '{slug}'."},
                status=status.HTTP_404_NOT_FOUND
            )

        type = chart_meta["type"]
        chart_type = chart_meta["chart_type"]

        curr_q = get_object_or_404(Quarter, number=quarter_number)
        csv_file = get_object_or_404(
            CSVFile,
            sheet_name_slug=slug,
            quarter_uuid=curr_q.uuid,
            is_current=True
        )
        

        try:
            df = pd.read_csv(csv_file.csv_path)
                        
            if(type == "simple"):

                application_col = df.columns[0]
                filter_cols = df.columns[1:]

                df[filter_cols] = df[filter_cols].apply(pd.to_numeric, errors='coerce')

                available_filters = filter_cols.tolist()
                selected_filter = filter if filter in available_filters else available_filters[0]

                applications = df[application_col].fillna("").tolist()
                values = df[selected_filter].fillna(0).tolist()
                
                
                trace = format_chart_trace(applications,values, chart_type)
                
                return Response({
                    'quarter':get_quarter_navigation_object(quarter_number, slug),
                    'chart_config':{
                        "traces":[trace],
                        "layout":{}
                    },
                    'title': csv_file.sheet_name,
                    "options": available_filters,
                    'selected_option': selected_filter
                })
        
            if(type=="double"):
                
                column_filter_name = chart_meta["column_name"]
                                
                available_column_filters = df[column_filter_name].unique()
                selected_column_filter = filter if filter in available_column_filters else available_column_filters[0]

            
                # Filtrar as linhas onde a coluna 'Company' == 'SWITCH'
                filtered_df = df[df[column_filter_name] == selected_column_filter]

                # Remover a coluna 'Company'
                filtered_df = filtered_df.drop(columns=[column_filter_name])

                traces = []
                x = filtered_df.columns[1:].to_list()
                for _, row in filtered_df.iterrows():
                    trace = {
                        "x": x,
                        "y": [row[col] for col in x],
                        "name": row[0],
                        "type": "bar"
                    }
                    traces.append(trace)
            
                response_data = {
                    'quarter': get_quarter_navigation_object(quarter_number, slug),
                    'title': csv_file.sheet_name,
                    'type': chart_type,
                    'chart_config':{
                        "traces":traces,
                        "layout":{
                            "barmode": "stack",
                            "showlegend":True,
                            "legend": {
                                "title": { "text": '' },     
                                "traceorder": 'normal'
                            }
                        }
                    },
                    "options": available_column_filters,
                    'selected_option': selected_column_filter,
                    'columns_filter':{
                        'available': available_column_filters,
                        'selected': selected_column_filter
                    }
                }
                

                return Response(response_data)

        except Exception as e:
            return Response({
                'quarter':get_quarter_navigation_object(quarter_number, slug),
                "error": f"Error reading file: {str(e)}",
                'chart_config':{
                    "traces":[],
                    "layout":{}
                },
                'title': csv_file.sheet_name,
                "options": [],
                'selected_option': None
            })