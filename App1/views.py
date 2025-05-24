from django.shortcuts import render, redirect
from django.http import Http404
from App1.pests import get_pests_diseases

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
            "excluded_keys": excluded_keys 
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