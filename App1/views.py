from django.shortcuts import render
from App1.models import get_pests_diseases

def home(request):
    """view for the home/landing page"""
    context = {
        "title": "Home - Mango Monitoring",
        
    }
    return render(request, "App1/index.html", context)

def project_list(request): 
    """View for the project list page showing all pests/diseases"""
    pests_diseases = get_pests_diseases()  # Added parentheses to call the function
    context = {
        "title": "Pests & Diseases - Mango Monitoring",
        "pests_diseases": pests_diseases
    }
    return render(request, "App1/projectlist.html", context)

def project_details(request, project_id):
    """View for the project details page showing specific pest/disease info"""
    pests_diseases = get_pests_diseases()
    
    # Find the pest/disease with the matching ID
    project = None
    for pest_disease in pests_diseases:
        if pest_disease.id == int(project_id):
            project = pest_disease
            break
    
    # If no matching pest/disease is found, redirect to the list page
    if project is None:
        return project_list(request)
    else:
        # Define context only when we have a valid project
        context = {
            "title": f"{project.name} - Mango Monitoring",
            "project": project
        }
        return render(request, "App1/projectdetails.html", context)

def about(request):
    """
    View for the about page with team information
    Update the student ID with your own
    
    """
    team_members = [
        {
            "name": "Erri Petalas",  
            "student_id": "S320775"
        },
        {
            "name": "Surendra Phuyal",
            "student_id": "S123457"
        },
          {
            "name": "Rekha Khadka",
            "student_id": "S372366"
        },
            {
            "name": "Dylan Tomlinson",
            "student_id": "S372936" 
        },
    ]
    
    context = {
        "title": "About - Mango Monitoring",
        "team_members": team_members
    }
    return render(request, "App1/about.html", context)