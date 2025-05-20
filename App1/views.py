from django.shortcuts import render, redirect#, get_object_or_404
from django.http import Http404
from App1.pests import get_pests_diseases
from django import template
# from .models import Farm, Pest, Surveillance
# from .forms import FarmForm, PestForm, SurveillanceForm

def home(request):
    """View for the home/landing page"""
    return render(request, "App1/index.html", {
        "title": "Home - Mango Monitoring",
    })


def project_list(request): 
    """View for the project list page showing all pests/diseases"""
    try:
        pests_diseases = get_pests_diseases()
        return render(request, "App1/projectlist.html", {
            "title": "Pests & Diseases - Mango Monitoring",
            "pests_diseases": pests_diseases
        })
    except Exception as e:
        # Log error in production: logger.error(f"Error fetching pests: {e}")
        return render(request, "App1/error.html", {
            "message": "Could not load pest data. Please try again later."
        })

def project_details(request, project_id):
    """View for the project details page showing specific pest/disease info"""
    try:
        pests_diseases = get_pests_diseases()
        project = next((p for p in pests_diseases if p.id == int(project_id)), None)
        
        if not project:
            raise Http404(f"Pest/Disease with ID {project_id} not found")
            
        # Prepare description if it's not already a dictionary
        if not isinstance(project.description, dict):
            project.description = {
                "general": project.description,
            }
    
        excluded_keys = ['general', 'eggs', 'immatures', 'adults']
        return render(request, "App1/projectdetails.html", {
            "title": f"{project.name} - Mango Monitoring",
            "project": project,
            "excluded_keys": ["excluded_keys"]  # Add this for template filtering
        })

    except ValueError:
        return redirect('App1:projectlist')
    except Exception as e:
        # Log error in production
        return render(request, "App1/error.html", {
            "message": "An error occurred while loading this page."
        })

def about(request):
    """View for the about page with team information"""
    team_members = [
        {"name": "Erri Petalas", "student_id": "S320775"},
        {"name": "Surendra Phuyal", "student_id": "S372088"},
        {"name": "Rekha Khadka", "student_id": "S372366"},
        {"name": "Dylan Tomlinson", "student_id": "S372936"}, 
    ]
    
    return render(request, "App1/about.html", {
        "title": "About - Mango Monitoring",
        "team_members": team_members
    })



# def farm_list(request):
#     farms = Farm.objects.all()
#     return render(request, 'App1/farm_list.html', {'farms': farms})

# def farm_create(request):
#     form = FarmForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('farm_list')
#     return render(request, 'App1/form.html', {'form': form})

# def farm_update(request, pk):
#     farm = get_object_or_404(Farm, pk=pk)
#     form = FarmForm(request.POST or None, instance=farm)
#     if form.is_valid():
#         form.save()
#         return redirect('farm_list')
#     return render(request, 'App1/form.html', {'form': form})

# def farm_delete(request, pk):
#     farm = get_object_or_404(Farm, pk=pk)
#     if request.method == 'POST':
#         farm.delete()
#         return redirect('farm_list')
#     return render(request, 'App1/confirm_delete.html', {'object': farm})

# # PEST VIEWS
# def pest_list(request):
#     pests = Pest.objects.all()
#     return render(request, 'App1/pest_list.html', {'pests': pests})

# def pest_create(request):
#     form = PestForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('pest_list')
#     return render(request, 'App1/form.html', {'form': form})

# def pest_update(request, pk):
#     pest = get_object_or_404(Pest, pk=pk)
#     form = PestForm(request.POST or None, instance=pest)
#     if form.is_valid():
#         form.save()
#         return redirect('pest_list')
#     return render(request, 'App1/form.html', {'form': form})

# def pest_delete(request, pk):
#     pest = get_object_or_404(Pest, pk=pk)
#     if request.method == 'POST':
#         pest.delete()
#         return redirect('pest_list')
#     return render(request, 'App1/confirm_delete.html', {'object': pest})

# # SURVEILLANCE VIEWS
# def surveillance_list(request):
#     records = Surveillance.objects.select_related('farm', 'pest')
#     return render(request, 'App1/surveillance_list.html', {'records': records})

# def surveillance_create(request):
#     form = SurveillanceForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('surveillance_list')
#     return render(request, 'App1/form.html', {'form': form})

# def surveillance_update(request, pk):
#     record = get_object_or_404(Surveillance, pk=pk)
#     form = SurveillanceForm(request.POST or None, instance=record)
#     if form.is_valid():
#         form.save()
#         return redirect('surveillance_list')
#     return render(request, 'App1/form.html', {'form': form})

# def surveillance_delete(request, pk):
#     record = get_object_or_404(Surveillance, pk=pk)
#     if request.method == 'POST':
#         record.delete()
#         return redirect('surveillance_list')
#     return render(request, 'App1/confirm_delete.html', {'object': record})


