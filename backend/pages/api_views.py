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
            return Response({"error": f"Error reading file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ChartDataAPIViewV2(APIView):
    def get(self, request, format=None):
        quarters = Quarter.objects.all()
        last_quarter = quarters[0]  # Most recent

        slug = request.query_params.get('slug')
        quarter_number = request.query_params.get('q', last_quarter.number)

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
        
        print("type:" + type)

        try:
            df = pd.read_csv(csv_file.csv_path)

            

            # Always take the first column as x-axis labels (e.g., application names, brands, etc.)
            x = df.iloc[:, 0].fillna("").tolist()
            
            
            y = []
            if(type == "simple"):
                filter_cols = df.columns[1:]

                df[filter_cols] = df[filter_cols].apply(pd.to_numeric, errors='coerce')

                available_filters = filter_cols.tolist()
                selected_filter = filter if filter in available_filters else available_filters[0]

                y = df[selected_filter].fillna(0).tolist()
            
                response_data = {
                    'quarter': get_quarter_navigation_object(quarter_number, slug),
                    'title': csv_file.sheet_name,
                    'type': chart_type,
                    'data': {
                        'x': x,
                        'y': y,
                    },
                    "options": available_filters,
                    'selected_option': selected_filter
                }

                return Response(response_data)
        
            if(type=="double"):
                filter_cols = df.columns[1:]

                available_filters_2 = df['Company'].unique()
                selected_filter_2 = available_filters_2[0]

                # Filtrar as linhas onde 'Company' == 'SWITCH'
                filtered_df = df[df['Company'] == 'SWITCH']

                # Remover a coluna 'Company'
                filtered_df = filtered_df.drop(columns=['Company'])

                
                traces = []
                for _, row in filtered_df.iterrows():
                    trace = {
                        "x": ["Price", "Rebate"],
                        "y": [row["Price"], row["Rebate"]],
                        "name": row["Brand"].strip('.').title(),
                        "type": "bar"
                    }
                    traces.append(trace)

                # Estrutura de resposta da API
                api_response = {
                    "data": traces,
                    "layout": {
                        "barmode": "group"
                    }
                }
                
                print(api_response)
                y = []
            
                response_data = {
                    'quarter': get_quarter_navigation_object(quarter_number, slug),
                    'title': csv_file.sheet_name,
                    'type': chart_type,
                    'data': {
                        'x': x,
                        'y': y,
                    },
                    "traces":traces,
                    "options": available_filters_2,
                    'selected_option': selected_filter_2
                }
                

                return Response(response_data)

        except Exception as e:
            return Response(
                {"error": f"Error reading file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
