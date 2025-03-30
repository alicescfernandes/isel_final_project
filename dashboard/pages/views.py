import os
import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

# Create your views here.

@login_required
def home(request):
    # Get the path to the xlsx directory
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    xlsx_dir = os.path.join(current_dir, 'xlsx')
    
    if not os.path.exists(xlsx_dir):
        return render(request, 'pages/home.html', {'charts': [], 'error': f'Directory not found: {xlsx_dir}'})
    
    charts = []
    
    # Process each XLSX file in the directory
    files = os.listdir(xlsx_dir)
    
    for filename in files:
        if filename.endswith('.xlsx'):
            file_path = os.path.join(xlsx_dir, filename)
            try:
                # Read the Excel file
                df = pd.read_excel(file_path)
                
                # Get the title from the first row
                title = df.columns[0]
                
                # Convert all columns except the first one to numeric
                for col in df.columns[1:]:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Set the first column as index and transpose
                df = df.set_index(df.columns[0]).transpose()
                
                # Create a line chart
                fig = px.line(df,title=title,
                                labels={"index": "Product Category", "value": "Score", "variable": "Customer Need"})
                
                # Update layout for better appearance
                fig.update_layout(
                    height=600,  # Taller graph
                    width=1200,  # Wider graph
                    showlegend=False,
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="right",
                        x=0.99,
                        traceorder="normal"
                    ),
                    xaxis=dict(
                        tickangle=45,  # Rotate labels 45 degrees
                    ),
                    template="plotly_dark",
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    modebar={
                        'orientation': 'h',
                        'bgcolor': 'rgba(0,0,0,0)',
                        'color': 'white',
                        'activecolor': 'lightgray'
                    }
                )
                
                # Add gridlines
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
                
                # Convert the plot to HTML with proper modebar configuration
                chart_html = fig.to_html(
                    full_html=False,
                    config={
                        'displayModeBar': True,
                        'displaylogo': False,
                        'modeBarButtonsToRemove': [
                            'lasso2d',
                            'select2d',
                            'autoScale2d',
                            'toggleSpikelines',
                            'hoverClosestCartesian',
                            'hoverCompareCartesian'
                        ],
                        'toImageButtonOptions': {'height': None, 'width': None}
                    }
                )
       
                charts.append({
                    'title': title,
                    'html': chart_html,
                    'filename': filename
                })
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                import traceback
                print(traceback.format_exc())
    
    if not charts:
        return render(request, 'pages/home.html', {'charts': [], 'error': 'No valid XLSX files were processed'})
    
    return render(request, 'pages/home.html', {'charts': charts})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    # Add styling to form fields
    for field in form.fields.values():
        field.widget.attrs.update({
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
        })
    
    return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'login'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
